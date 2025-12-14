import os
from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .fillpdf_utils import get_pricing_values, normalize_weight


def recalculate_application_premium(application):
    import logging
    logger = logging.getLogger(__name__)

    try:
        # -------------------------------
        # LOAD QUESTIONNAIRE
        # -------------------------------
        questionnaire = getattr(application, "questionnaire", None)
        if not questionnaire:
            logger.info(
                f"[INFO] No questionnaire yet for application {application.id}, "
                f"continuing premium calculation"
            )

        # -------------------------------
        # WEIGHT NORMALIZATION (FINAL)
        # -------------------------------
        raw_weight = str(application.pet_weight_category)

        logger.info(
            f"[WEIGHT RAW] App={application.id} pet_weight_category={raw_weight}"
        )

        mapped_weight = normalize_weight(raw_weight)

        logger.info(
            f"[WEIGHT MAPPED] App={application.id} mapped_weight={mapped_weight}"
        )

        if not mapped_weight:
            logger.error(f"Invalid weight category: {raw_weight}")
            return

        program = application.program


        logger.info(
            f"[PRICING] App={application.id} "
            f"pet_type={application.pet_type}, "
            f"program={program}, "
            f"mapped_weight={mapped_weight}"
        )

        # -------------------------------
        # EXCEL PRICING (SINGLE SOURCE)
        # -------------------------------
        try:
            _, _, _, annual_price = get_pricing_values(
                application,
                application.pet_type,
                mapped_weight,
                program,
                "annual",
            )

            _, _, _, six_month_price = get_pricing_values(
                application,
                application.pet_type,
                mapped_weight,
                program,
                "6m",
            )

            _, _, _, three_month_price = get_pricing_values(
                application,
                application.pet_type,
                mapped_weight,
                program,
                "3m",
            )



            logger.info(
                f"[EXCEL PRICES] App={application.id} | "
                f"Annual={annual_price}€, "
                f"6M={six_month_price}€, "
                f"3M={three_month_price}€"
            )

        except Exception as e:
            logger.error(f"Excel pricing missing: {e}")
            return

        # -------------------------------
        # SAVE TO DB
        # -------------------------------
        application.annual_premium = Decimal(str(annual_price))
        application.six_month_premium = Decimal(str(six_month_price))
        application.three_month_premium = Decimal(str(three_month_price))

        application.save(
            update_fields=[
                "annual_premium",
                "six_month_premium",
                "three_month_premium",
            ]
        )

        logger.info(
            f"[DB SAVED] App={application.id} "
            f"annual={application.annual_premium}, "
            f"six_month={application.six_month_premium}, "
            f"three_month={application.three_month_premium}"
        )

        # -------------------------------
        # BREAKDOWN (USED BY PDF)
        # -------------------------------
        return

    except Exception as e:
        logger.error(
            f"Premium calculation error for application {application.id}: {e}"
        )


def get_poisoning_price(program, payment_frequency):
    prices = {
        'silver': 18,
        'gold': 20,
        'platinum': 25,
        'dynasty': 25,
    }

    annual_price = prices.get(program, 0)

    if payment_frequency == "six_month":
        return round(annual_price / 2, 2)
    elif payment_frequency == "three_month":
        return round(annual_price / 4, 2)

    return annual_price  # annual


def generate_contract_pdf(application):
    # ALWAYS recalc before PDF
    recalculate_application_premium(application)
    application.refresh_from_db()

    """
    Generate contract PDF with full price breakdown included.
    """
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Generating contract PDF for {application.id}")

    from .models import InsuranceApplication
    application = InsuranceApplication.objects.select_related(
        "questionnaire"
    ).get(pk=application.pk)

    # Ensure premiums exist
    if application.annual_premium is None:
        recalculate_application_premium(application)
        application.refresh_from_db()



    import tempfile
    temp_dir = tempfile.mkdtemp()

    try:
        from .fillpdf_utils import generate_contract_with_fillpdf

        # MULTI PET
        if application.has_second_pet and application.second_pet_name:
            pdf_paths = []

            for pet_number in [1, 2]:
                filename = (
                    f"contract_{application.contract_number}_pet{pet_number}_"
                    f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                )
                temp_path = os.path.join(temp_dir, filename)

                generated = generate_contract_with_fillpdf(
                    application,
                    temp_path,
                    pet_number=pet_number,
                )

                logger.info(
                    f"[PDF INPUT] App={application.id} "
                    f"premium_used={application.get_premium_for_frequency()} "
                    f"frequency={application.questionnaire.payment_frequency}"
                )

                if os.path.exists(generated):
                    s3_key = f"contracts/{filename}"
                    with open(generated, "rb") as f:
                        saved = default_storage.save(
                            s3_key, ContentFile(f.read())
                        )
                        pdf_paths.append(saved)

                        logger.info(
                            f"[PDF GENERATED] App={application.id} path={generated}"
                        )

            return pdf_paths

        # SINGLE PET
        filename = (
            f"contract_{application.contract_number}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        temp_path = os.path.join(temp_dir, filename)

        generated = generate_contract_with_fillpdf(
            application,
            temp_path,
            pet_number=1,
        )

        if os.path.exists(generated):
            s3_key = f"contracts/{filename}"
            with open(generated, "rb") as f:
                saved_path = default_storage.save(
                    s3_key, ContentFile(f.read())
                )
                return [saved_path]

        return []

    finally:
        import shutil
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass

