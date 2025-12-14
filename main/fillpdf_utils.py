"""
Clean fillable PDF contract generation using fillpdf library
(Simple & Stable Version – No PyMuPDF, No Flattening)
"""

import os
from tempfile import TemporaryDirectory
from django.conf import settings
from fillpdf import fillpdfs
from datetime import datetime

try:
    from .qr_utils import generate_contract_verification_qr, generate_terms_qr
except ImportError:
    generate_contract_verification_qr = None
    generate_terms_qr = None


# ----------------------------------------------------
#  PRICING TABLE (TO BE FILLED WITH EXCEL VALUES)
# ----------------------------------------------------
PRICING = {
    "dog": {
        "silver": {
            "10": {
                "annual": {"net": 111.54, "fee": 33.46, "ipt": 21.75, "gross": 166.75},
                "6m":     {"net": 58.56, "fee": 17.57, "ipt": 11.42, "gross": 87.54},
                "3m":     {"net": 30.67, "fee": 9.20, "ipt": 5.98, "gross": 45.86},
                "annual_2nd": {"net": 200.77, "fee": 60.23, "ipt": 39.15, "gross": 300.15},
                "6m_2nd":     {"net": 105.41, "fee": 31.62, "ipt": 20.55, "gross": 157.58},
                "3m_2nd":     {"net": 55.21, "fee": 16.56, "ipt": 10.77, "gross": 82.54},
            },
            "11-20": {
                "annual": {"net": 138.60, "fee": 41.58, "ipt": 27.03, "gross": 207.20},
                "6m":     {"net": 72.76, "fee": 21.83, "ipt": 14.19, "gross": 108.78},
                "3m":     {"net": 38.11, "fee": 11.43, "ipt": 7.43, "gross": 56.98},
                "annual_2nd": {"net": 249.48, "fee": 74.84, "ipt": 48.65, "gross": 372.97},
                "6m_2nd":     {"net": 130.98, "fee": 39.29, "ipt": 25.54, "gross": 195.81},
                "3m_2nd":     {"net": 68.61, "fee": 20.58, "ipt": 13.38, "gross": 102.57},
            },
            "21-40": {
                "annual": {"net": 156.62, "fee": 46.98, "ipt": 30.54, "gross": 234.14},
                "6m":     {"net": 82.22, "fee": 24.67, "ipt": 16.03, "gross": 122.92},
                "3m":     {"net": 43.07, "fee": 12.92, "ipt": 8.40, "gross": 64.39},
                "annual_2nd": {"net": 281.91, "fee": 84.57, "ipt": 54.97, "gross": 421.45},
                "6m_2nd":     {"net": 148.00, "fee": 44.40, "ipt": 28.86, "gross": 221.26},
                "3m_2nd":     {"net": 77.52, "fee": 23.26, "ipt": 15.12, "gross": 115.90},
            },
            ">40": {
                "annual": {"net": 170.14, "fee": 51.04, "ipt": 33.18, "gross": 254.36},
                "6m":     {"net": 89.32, "fee": 26.80, "ipt": 17.42, "gross": 133.54},
                "3m":     {"net": 46.79, "fee": 14.04, "ipt": 9.12, "gross": 69.95},
                "annual_2nd": {"net": 306.25, "fee": 91.88, "ipt": 59.72, "gross": 457.85},
                "6m_2nd":     {"net": 160.78, "fee": 48.23, "ipt": 31.35, "gross": 240.37},
                "3m_2nd":     {"net": 84.22, "fee": 25.27, "ipt": 16.42, "gross": 125.91},
            },
        },

        "gold": {
            "10": {
                "annual": {"net": 156.62, "fee": 46.98, "ipt": 30.54, "gross": 234.14},
                "6m":     {"net": 82.22, "fee": 24.67, "ipt": 16.03, "gross": 122.92},
                "3m":     {"net": 43.07, "fee": 12.92, "ipt": 8.40, "gross": 64.39},
                "annual_2nd": {"net": 281.91, "fee": 84.57, "ipt": 54.97, "gross": 421.45},
                "6m_2nd":     {"net": 148.00, "fee": 44.40, "ipt": 28.86, "gross": 221.26},
                "3m_2nd":     {"net": 77.52, "fee": 23.26, "ipt": 15.12, "gross": 115.90},
            },
            "11-20": {
                "annual": {"net": 174.64, "fee": 52.39, "ipt": 34.05, "gross": 261.09},
                "6m":     {"net": 91.69, "fee": 27.51, "ipt": 17.88, "gross": 137.07},
                "3m":     {"net": 48.03, "fee": 14.41, "ipt": 9.37, "gross": 71.80},
                "annual_2nd": {"net": 314.35, "fee": 94.31, "ipt": 61.30, "gross": 469.96},
                "6m_2nd":     {"net": 165.03, "fee": 49.51, "ipt": 32.18, "gross": 246.73},
                "3m_2nd":     {"net": 86.45, "fee": 25.93, "ipt": 16.86, "gross": 129.24},
            },
            "21-40": {
                "annual": {"net": 192.68, "fee": 57.80, "ipt": 37.57, "gross": 288.05},
                "6m":     {"net": 101.16, "fee": 30.35, "ipt": 19.73, "gross": 151.23},
                "3m":     {"net": 52.99, "fee": 15.90, "ipt": 10.33, "gross": 79.21},
                "annual_2nd": {"net": 346.82, "fee": 104.05, "ipt": 67.63, "gross": 518.50},
                "6m_2nd":     {"net": 182.08, "fee": 54.62, "ipt": 35.51, "gross": 272.21},
                "3m_2nd":     {"net": 95.38, "fee": 28.61, "ipt": 18.60, "gross": 142.59},
            },
            ">40": {
                "annual": {"net": 206.20, "fee": 61.86, "ipt": 40.21, "gross": 308.26},
                "6m":     {"net": 108.25, "fee": 32.48, "ipt": 21.11, "gross": 161.84},
                "3m":     {"net": 56.70, "fee": 17.01, "ipt": 11.06, "gross": 84.77},
                "annual_2nd": {"net": 371.15, "fee": 111.35, "ipt": 72.37, "gross": 554.87},
                "6m_2nd":     {"net": 194.85, "fee": 58.46, "ipt": 38.00, "gross": 291.31},
                "3m_2nd":     {"net": 102.07, "fee": 30.62, "ipt": 19.90, "gross": 152.59},
            },
        },

        "platinum": {
            "10": {
                "annual": {"net": 246.77, "fee": 74.03, "ipt": 48.12, "gross": 368.92},
                "6m":     {"net": 129.55, "fee": 38.87, "ipt": 25.26, "gross": 193.68},
                "3m":     {"net": 67.86, "fee": 20.36, "ipt": 13.23, "gross": 101.45},
                "annual_2nd": {"net": 444.19, "fee": 133.26, "ipt": 86.62, "gross": 664.06},
                "6m_2nd":     {"net": 233.20, "fee": 69.96, "ipt": 45.47, "gross": 348.63},
                "3m_2nd":     {"net": 122.15, "fee": 36.65, "ipt": 23.82, "gross": 182.62},
            },
            "11-20": {
                "annual": {"net": 260.30, "fee": 78.09, "ipt": 50.76, "gross": 389.15},
                "6m":     {"net": 136.66, "fee": 41.00, "ipt": 26.65, "gross": 204.30},
                "3m":     {"net": 71.58, "fee": 21.47, "ipt": 13.96, "gross": 107.02},
                "annual_2nd": {"net": 468.54, "fee": 140.56, "ipt": 91.37, "gross": 700.47},
                "6m_2nd":     {"net": 245.98, "fee": 73.80, "ipt": 47.97, "gross": 367.75},
                "3m_2nd":     {"net": 128.85, "fee": 38.65, "ipt": 25.13, "gross": 192.63},
            },
            "21-40": {
                "annual": {"net": 273.82, "fee": 82.15, "ipt": 53.39, "gross": 409.36},
                "6m":     {"net": 143.76, "fee": 43.13, "ipt": 28.03, "gross": 214.91},
                "3m":     {"net": 75.30, "fee": 22.59, "ipt": 14.68, "gross": 112.57},
                "annual_2nd": {"net": 492.88, "fee": 147.86, "ipt": 96.11, "gross": 736.85},
                "6m_2nd":     {"net": 258.76, "fee": 77.63, "ipt": 50.46, "gross": 386.85},
                "3m_2nd":     {"net": 135.54, "fee": 40.66, "ipt": 26.43, "gross": 202.63},
            },
            ">40": {
                "annual": {"net": 291.85, "fee": 87.56, "ipt": 56.91, "gross": 436.32},
                "6m":     {"net": 153.22, "fee": 45.97, "ipt": 29.88, "gross": 229.07},
                "3m":     {"net": 80.26, "fee": 24.08, "ipt": 15.65, "gross": 119.99},
                "annual_2nd": {"net": 525.33, "fee": 157.60, "ipt": 102.44, "gross": 785.37},
                "6m_2nd":     {"net": 275.80, "fee": 82.74, "ipt": 53.78, "gross": 412.32},
                "3m_2nd":     {"net": 144.47, "fee": 43.34, "ipt": 28.17, "gross": 215.98},
            },
        }
    },

    # ---------------------------
    #            CAT
    # ---------------------------

    "cat": {
        "silver": {
            "10": {
                "annual": {"net": 76.13, "fee": 22.84, "ipt": 14.85, "gross": 113.81},
                "6m":     {"net": 39.97, "fee": 11.99, "ipt": 7.79, "gross": 59.75},
                "3m":     {"net": 20.94, "fee": 6.28, "ipt": 4.08, "gross": 31.30},
                "annual_2nd": {"net": 137.03, "fee": 41.11, "ipt": 26.72, "gross": 204.87},
                "6m_2nd":     {"net": 71.94, "fee": 21.58, "ipt": 14.03, "gross": 107.55},
                "3m_2nd":     {"net": 37.68, "fee": 11.31, "ipt": 7.35, "gross": 56.34},
            },
            "11-20": {
                "annual": {"net": 94.33, "fee": 28.30, "ipt": 18.39, "gross": 141.02},
                "6m":     {"net": 49.52, "fee": 14.86, "ipt": 9.66, "gross": 74.04},
                "3m":     {"net": 25.94, "fee": 7.78, "ipt": 5.06, "gross": 38.78},
                "annual_2nd": {"net": 169.79, "fee": 50.94, "ipt": 33.11, "gross": 253.84},
                "6m_2nd":     {"net": 89.14, "fee": 26.74, "ipt": 17.38, "gross": 133.27},
                "3m_2nd":     {"net": 46.69, "fee": 14.01, "ipt": 9.11, "gross": 69.81},
            },
        },

        "gold": {
            "10": {
                "annual": {"net": 112.52, "fee": 33.76, "ipt": 21.94, "gross": 168.22},
                "6m":     {"net": 59.07, "fee": 17.72, "ipt": 11.52, "gross": 88.31},
                "3m":     {"net": 30.94, "fee": 9.28, "ipt": 6.03, "gross": 46.26},
                "annual_2nd": {"net": 202.54, "fee": 60.76, "ipt": 39.49, "gross": 302.79},
                "6m_2nd":     {"net": 106.33, "fee": 31.90, "ipt": 20.73, "gross": 158.97},
                "3m_2nd":     {"net": 55.70, "fee": 16.71, "ipt": 10.86, "gross": 83.27},
            },
            "11-20": {
                "annual": {"net": 126.16, "fee": 37.85, "ipt": 24.60, "gross": 188.61},
                "6m":     {"net": 66.23, "fee": 19.87, "ipt": 12.92, "gross": 99.02},
                "3m":     {"net": 34.69, "fee": 10.41, "ipt": 6.77, "gross": 51.87},
                "annual_2nd": {"net": 227.09, "fee": 68.13, "ipt": 44.28, "gross": 339.50},
                "6m_2nd":     {"net": 119.22, "fee": 35.77, "ipt": 23.25, "gross": 178.24},
                "3m_2nd":     {"net": 62.45, "fee": 18.73, "ipt": 12.18, "gross": 93.36},
            },
        },

        "platinum": {
            "10": {
                "annual": {"net": 185.30, "fee": 55.59, "ipt": 36.13, "gross": 277.02},
                "6m":     {"net": 97.28, "fee": 29.18, "ipt": 18.97, "gross": 145.44},
                "3m":     {"net": 50.96, "fee": 15.29, "ipt": 9.94, "gross": 76.18},
                "annual_2nd": {"net": 333.54, "fee": 100.06, "ipt": 65.04, "gross": 498.64},
                "6m_2nd":     {"net": 175.11, "fee": 52.53, "ipt": 34.15, "gross": 261.79},
                "3m_2nd":     {"net": 91.72, "fee": 27.52, "ipt": 17.89, "gross": 137.13},
            },
            "11-20": {
                "annual": {"net": 208.04, "fee": 62.41, "ipt": 40.57, "gross": 311.02},
                "6m":     {"net": 109.22, "fee": 32.77, "ipt": 21.30, "gross": 163.29},
                "3m":     {"net": 57.21, "fee": 17.16, "ipt": 11.16, "gross": 85.53},
                "annual_2nd": {"net": 374.47, "fee": 112.34, "ipt": 73.02, "gross": 559.84},
                "6m_2nd":     {"net": 196.60, "fee": 58.98, "ipt": 38.34, "gross": 293.91},
                "3m_2nd":     {"net": 102.98, "fee": 30.89, "ipt": 20.08, "gross": 153.95},
            },
        },
    },
}

# ---------------------------------
# FIX WEIGHT FOR EXCEL PRICING
# ---------------------------------
def normalize_weight(raw_weight):
    raw_weight = str(raw_weight)

    weight_mapping = {
        "up_10": "10",
        "10_25": "11-20",
        "25_40": "21-40",
        "over_40": ">40",

        "10": "10",

        # ✅ FIX: weights below 10
        "1": "10",
        "2": "10",
        "3": "10",
        "4": "10",
        "5": "10",
        "6": "10",
        "7": "10",
        "8": "10",
        "9": "10",

        "11-20": "11-20",
        "21-40": "21-40",
        ">40": ">40",

        "11": "11-20", "12": "11-20", "13": "11-20", "14": "11-20",
        "15": "11-20", "16": "11-20", "17": "11-20", "18": "11-20",
        "19": "11-20", "20": "11-20",

        "21": "21-40", "22": "21-40", "23": "21-40", "24": "21-40",
        "25": "21-40", "26": "21-40", "27": "21-40", "28": "21-40",
        "29": "21-40", "30": "21-40", "31": "21-40", "32": "21-40",
        "33": "21-40", "34": "21-40", "35": "21-40", "36": "21-40",
        "37": "21-40", "38": "21-40", "39": "21-40", "40": "21-40",

        "41": ">40", "42": ">40", "43": ">40", "44": ">40", "45": ">40",
    }

    return weight_mapping.get(raw_weight)


# ----------------------------------------------------
#  PRICING ENGINE (REPLACES OLD WRONG % CALCULATIONS)
# ----------------------------------------------------

def get_pricing_values(application, pet_type, weight_category, program, frequency="annual", is_second_pet=False):
    """
    Returns EXACT Excel pricing.
    frequency must be: 'annual', '6m', '3m'
    """

    program_table = PRICING.get(pet_type, {}).get(program, {})
    row = program_table.get(weight_category, {})

    key = frequency if not is_second_pet else f"{frequency}_2nd"

    if key not in row:
        raise ValueError(f"[PRICING ERROR] Missing Excel price for {pet_type} {program} {weight_category} {key}")

    values = row[key]
    return values["net"], values["fee"], values["ipt"], values["gross"]



# ----------------------------------------------------
#  CONTRACT GENERATION
# ----------------------------------------------------

def generate_contract_with_fillpdf(application, output_path, pet_number=1):
    """Generate contract using fillpdf (simple & stable version)."""

    import logging
    logger = logging.getLogger(__name__)

    # ALWAYS define frequency (safe default)
    frequency_map = {
        "annual": "annual",
        "six_month": "6m",
        "three_month": "3m",
    }

    freq = frequency_map.get(application.get_payment_frequency(), "annual")


    # use freq freely below
    logger.info(f"excel_key={freq}")
    logger.info(f"[PDF] Generating contract (Simple Mode) – Pet {pet_number}, App {application.id}")

    template_path = os.path.join(
        settings.BASE_DIR,
        'ΑΣΦΑΛΙΣΤΗΡΙΟ ΣΥΜΒΟΛΑΙΟ ΤΕΛΙΚΟ PET (1) (2).pdf'
    )

    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Fillable contract template not found: {template_path}")

    # -----------------------------
    # PET SELECTION LOGIC
    # -----------------------------
    if pet_number == 2 and application.has_second_pet:
        pet_name = application.second_pet_name
        pet_type_display = 'Γάτα' if application.second_pet_type == 'cat' else 'Σκύλος'
        pet_breed = application.second_pet_breed
        pet_weight = application.get_weight_display(application.second_pet_weight_category)
        pet_birthdate = application.second_pet_birthdate.strftime('%d/%m/%Y')
        is_second_pet = True
       
        raw_weight = application.second_pet_weight_category if is_second_pet else application.pet_weight_category
        weight = normalize_weight(raw_weight)

        if not weight:
            raise ValueError(f"Invalid weight category for PDF: {raw_weight}")


        pet_type = application.second_pet_type
    else:
        pet_name = application.pet_name
        pet_type_display = application.get_pet_type_display_greek()
        pet_breed = application.pet_breed
        pet_weight = application.get_weight_display(application.pet_weight_category)
        pet_birthdate = application.pet_birthdate.strftime('%d/%m/%Y')
        is_second_pet = False
        raw_weight = application.second_pet_weight_category if is_second_pet else application.pet_weight_category
        weight = normalize_weight(raw_weight)

        if not weight:
            raise ValueError(f"Invalid weight category for PDF: {raw_weight}")
        pet_type = application.pet_type

    logger.info(
    f"[PDF] App #{application.id} | "
    f"payment_frequency={application.get_payment_frequency()} | "
    f"excel_key={freq}"
    )


    # -----------------------------
    # AUTODETECT PAYMENT FREQUENCY
    # -----------------------------
    program = application.program

    # -----------------------------
    # CALCULATE EXACT PRICING
    # -----------------------------
    net, fee, ipt, gross = get_pricing_values(
        application,
        pet_type=pet_type,
        weight_category=weight,
        program=program,
        frequency=freq,
        is_second_pet=is_second_pet
    )

    data = create_contract_field_mapping(
        application, pet_name, pet_type_display, pet_breed,
        pet_weight, pet_birthdate, "",
        net, fee, ipt, gross
    )

    try:
        fillpdfs.write_fillable_pdf(
            input_pdf_path=template_path,
            output_pdf_path=output_path,
            data_dict=data,
            flatten=False
        )
        return output_path

    except Exception as e:
        logger.error(f"[PDF ERROR] {e}")
        raise


# ----------------------------------------------------
#  PDF FIELD MAPPING
# ----------------------------------------------------

def create_contract_field_mapping(application, pet_name, pet_type_display, pet_breed,
                                  pet_weight, pet_birthdate, contract_suffix,
                                  net_premium, fee, ipt, gross):

    import logging
    logger = logging.getLogger(__name__)

    from .models import InsuranceApplication, Questionnaire
    from .utils import get_poisoning_price
    application = InsuranceApplication.objects.select_related("questionnaire").get(pk=application.pk)

    # Get questionnaire and payment frequency
    questionnaire = getattr(application, "questionnaire", None)
    payment_frequency = questionnaire.payment_frequency if questionnaire else "annual"
    
    # Build surcharges text (breed surcharges)
    surcharges_parts = []
    if questionnaire:
        if questionnaire.special_breed_5_percent:
            surcharges_parts.append("Επασφάλιστρο 5%")
        if questionnaire.special_breed_20_percent:
            surcharges_parts.append("Επασφάλιστρο 20%")
    surcharges_text = " | ".join(surcharges_parts) if surcharges_parts else ""
    
    # Calculate add-on prices based on payment frequency
    addon_poisoning = ""
    addon_blood = ""
    addon_poisoning_price = 0
    addon_blood_price = 0
    
    if questionnaire:
        if questionnaire.additional_poisoning_coverage:
            addon_poisoning_price = get_poisoning_price(application.program, payment_frequency)
            addon_poisoning = f"Δηλητηρίαση: {addon_poisoning_price:.2f}€"
        
        if questionnaire.additional_blood_checkup:
            if payment_frequency == "six_month":
                addon_blood_price = round(28.00 * 0.5, 2)  # 50% of annual (add-on scaling)
            elif payment_frequency == "three_month":
                addon_blood_price = round(28.00 * 0.25, 2)  # 25% of annual (add-on scaling)
            else:
                addon_blood_price = 28.00
            addon_blood = f"Αιματολογικό Check Up: {addon_blood_price:.2f}€"
    
    # Use stored premium which includes surcharges and add-ons
    # Get the correct premium based on payment frequency
    if payment_frequency == "six_month":
        stored_gross = float(application.six_month_premium or 0)
    elif payment_frequency == "three_month":
        stored_gross = float(application.three_month_premium or 0)
    else:
        stored_gross = float(application.annual_premium or 0)
    
    # Use stored premium if available (includes add-ons), otherwise calculate from base
    if stored_gross > 0:
        final_gross = stored_gross
        # Scale breakdown components proportionally to match the stored gross
        base_gross = float(gross)
        if base_gross > 0:
            multiplier = final_gross / base_gross
            net_premium = round(float(net_premium) * multiplier, 2)
            fee = round(float(fee) * multiplier, 2)
            ipt = round(float(ipt) * multiplier, 2)
        else:
            # Fallback: use percentage breakdown
            net_premium = round(final_gross * 0.60, 2)
            fee = round(final_gross * 0.18, 2)
            ipt = round(final_gross * 0.215, 2)
    else:
        # Fallback: calculate from base + add-ons
        final_gross = float(gross) + addon_poisoning_price + addon_blood_price
        base_gross = float(gross)
        if base_gross > 0:
            multiplier = final_gross / base_gross
            net_premium = round(float(net_premium) * multiplier, 2)
            fee = round(float(fee) * multiplier, 2)
            ipt = round(float(ipt) * multiplier, 2)
        else:
            final_gross = round(final_gross, 2)
    
    # Prepare PDF mapping
    data = {
        "text_1bwie": application.contract_number or "",
        "text_3ksjz": application.full_name or "",

        "text_5fgpc": application.contract_start_date.strftime("%d/%m/%Y"),
        "text_6zqkn": application.contract_end_date.strftime("%d/%m/%Y"),

        "text_7tbbt": application.get_program_with_frequency_display(),

        "text_8safe": application.full_name,
        "text_9vyoe": application.afm or "",
        "text_10eqtr": application.phone or "",
        "text_11qthp": application.address or "",
        "text_12ul": application.postal_code or "",
        "text_13liqu": application.email or "",

        "text_14rclu": pet_name,
        "text_15vsin": pet_type_display,
        "text_16jfkm": pet_breed,
        "text_17ltlp": pet_weight,
        "text_18yuy": pet_birthdate,
        "text_19nqjo": application.microchip_number or "",

        "text_29bsjj": "",
        "text_30vzyv": surcharges_text,
        "text_31mdpf": addon_poisoning,
        "text_32crsg": addon_blood,

        # PRICING DISPLAY
        "text_33tjdu": f"{net_premium:.2f}€",
        "text_34k": f"{fee:.2f}€",
        "text_35poeh": "–",            # Always dash now
        "text_36sfw": f"{ipt:.2f}€",
        "text_37rpnu": f"{final_gross:.2f}€",
    }

    # Coverage checkboxes
    for cb in [
        "checkbox_20jmec", "checkbox_21jvmm", "checkbox_22cjxd",
        "checkbox_23cdss", "checkbox_24bmgz", "checkbox_25yhjf",
        "checkbox_26wldx", "checkbox_27sj", "checkbox_28okyh"
    ]:
        data[cb] = "Yes_sexk"

    return data
