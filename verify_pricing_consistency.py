#!/usr/bin/env python3
"""
Verify pricing table consistency across all files
"""

# Pricing from fillpdf_utils.py (DETAILED - with breakdown)
FILLPDF_DOG_PRICING = {
    'silver': {
        '10': {'net_premium': 100.16, 'management_fee': 30.05, 'auxiliary_fund': 0.80, 'ipt': 19.53, 'final': 166.75},
        '11-20': {'net_premium': 125.20, 'management_fee': 37.56, 'auxiliary_fund': 1.00, 'ipt': 24.41, 'final': 207.20},
        '21-40': {'net_premium': 141.88, 'management_fee': 42.56, 'auxiliary_fund': 1.13, 'ipt': 27.67, 'final': 234.14},
        '>40': {'net_premium': 154.40, 'management_fee': 46.32, 'auxiliary_fund': 1.24, 'ipt': 30.11, 'final': 254.36}
    },
    'gold': {
        '10': {'net_premium': 141.88, 'management_fee': 42.56, 'auxiliary_fund': 1.13, 'ipt': 27.67, 'final': 234.14},
        '11-20': {'net_premium': 158.57, 'management_fee': 47.57, 'auxiliary_fund': 1.27, 'ipt': 30.92, 'final': 261.09},
        '21-40': {'net_premium': 175.27, 'management_fee': 52.58, 'auxiliary_fund': 1.40, 'ipt': 34.18, 'final': 288.05},
        '>40': {'net_premium': 187.78, 'management_fee': 56.33, 'auxiliary_fund': 1.50, 'ipt': 36.62, 'final': 308.26}
    },
    'platinum': {
        '10': {'net_premium': 225.34, 'management_fee': 67.60, 'auxiliary_fund': 1.80, 'ipt': 43.94, 'final': 368.92},
        '11-20': {'net_premium': 237.87, 'management_fee': 71.36, 'auxiliary_fund': 1.90, 'ipt': 46.38, 'final': 389.15},
        '21-40': {'net_premium': 250.38, 'management_fee': 75.11, 'auxiliary_fund': 2.00, 'ipt': 48.82, 'final': 409.36},
        '>40': {'net_premium': 267.07, 'management_fee': 80.12, 'auxiliary_fund': 2.14, 'ipt': 52.08, 'final': 436.32}
    }
}

FILLPDF_CAT_PRICING = {
    'silver': {
        '10': {'net_premium': 67.37, 'management_fee': 20.21, 'auxiliary_fund': 0.54, 'ipt': 13.14, 'final': 113.81},
        '11-20': {'net_premium': 84.22, 'management_fee': 25.27, 'auxiliary_fund': 0.67, 'ipt': 16.42, 'final': 141.02}
    },
    'gold': {
        '10': {'net_premium': 101.07, 'management_fee': 30.32, 'auxiliary_fund': 0.81, 'ipt': 19.71, 'final': 168.22},
        '11-20': {'net_premium': 113.69, 'management_fee': 34.11, 'auxiliary_fund': 0.91, 'ipt': 22.17, 'final': 188.61}
    },
    'platinum': {
        '10': {'net_premium': 168.44, 'management_fee': 50.53, 'auxiliary_fund': 1.35, 'ipt': 32.84, 'final': 277.02},
        '11-20': {'net_premium': 189.49, 'management_fee': 56.85, 'auxiliary_fund': 1.52, 'ipt': 36.95, 'final': 311.02}
    }
}

# Pricing from utils.py (SIMPLIFIED - final only)
UTILS_DOG_PRICING = {
    'silver': {'10': 166.75, '11-20': 207.20, '21-40': 234.14, '>40': 254.36},
    'gold': {'10': 234.14, '11-20': 261.09, '21-40': 288.05, '>40': 308.26},
    'platinum': {'10': 368.92, '11-20': 389.15, '21-40': 409.36, '>40': 436.32}
}

UTILS_CAT_PRICING = {
    'silver': {'10': 113.81, '11-20': 141.02},
    'gold': {'10': 168.22, '11-20': 188.61},
    'platinum': {'10': 277.02, '11-20': 311.02}
}


def verify_price_sums():
    """Verify that price components sum to final price"""
    print("\n" + "="*80)
    print("🔍 VERIFYING PRICE COMPONENT SUMS")
    print("="*80 + "\n")
    
    all_good = True
    
    for pet_type, pricing in [('DOG', FILLPDF_DOG_PRICING), ('CAT', FILLPDF_CAT_PRICING)]:
        for program, weights in pricing.items():
            for weight, components in weights.items():
                calculated = (
                    components['net_premium'] + 
                    components['management_fee'] + 
                    components['auxiliary_fund'] + 
                    components['ipt']
                )
                final = components['final']
                diff = abs(calculated - final)
                
                if diff > 0.02:  # Allow 2 cent rounding difference
                    print(f"❌ {pet_type} {program} {weight}: Sum={calculated:.2f}€ ≠ Final={final:.2f}€ (diff={diff:.2f}€)")
                    all_good = False
    
    if all_good:
        print("✅ ALL PRICE COMPONENTS SUM CORRECTLY TO FINAL PRICES!")
    else:
        print("⚠️  Some price components don't sum correctly!")
    
    return all_good


def verify_consistency():
    """Verify consistency between fillpdf and utils pricing"""
    print("\n" + "="*80)
    print("🔍 VERIFYING CONSISTENCY BETWEEN FILES")
    print("="*80 + "\n")
    
    all_consistent = True
    
    # Check Dogs
    print("📊 DOGS:")
    for program in ['silver', 'gold', 'platinum']:
        for weight in ['10', '11-20', '21-40', '>40']:
            if weight in FILLPDF_DOG_PRICING[program] and weight in UTILS_DOG_PRICING[program]:
                fillpdf_price = FILLPDF_DOG_PRICING[program][weight]['final']
                utils_price = UTILS_DOG_PRICING[program][weight]
                
                if abs(fillpdf_price - utils_price) > 0.01:
                    print(f"  ❌ {program} {weight}: fillpdf={fillpdf_price}€ vs utils={utils_price}€")
                    all_consistent = False
                else:
                    print(f"  ✅ {program} {weight}: {fillpdf_price}€")
    
    # Check Cats
    print("\n📊 CATS:")
    for program in ['silver', 'gold', 'platinum']:
        for weight in ['10', '11-20']:
            if weight in FILLPDF_CAT_PRICING[program] and weight in UTILS_CAT_PRICING[program]:
                fillpdf_price = FILLPDF_CAT_PRICING[program][weight]['final']
                utils_price = UTILS_CAT_PRICING[program][weight]
                
                if abs(fillpdf_price - utils_price) > 0.01:
                    print(f"  ❌ {program} {weight}: fillpdf={fillpdf_price}€ vs utils={utils_price}€")
                    all_consistent = False
                else:
                    print(f"  ✅ {program} {weight}: {fillpdf_price}€")
    
    print()
    if all_consistent:
        print("✅ ALL PRICES ARE CONSISTENT ACROSS FILES!")
    else:
        print("⚠️  Some prices are inconsistent!")
    
    return all_consistent


def show_pricing_summary():
    """Show a summary of all pricing"""
    print("\n" + "="*80)
    print("📊 PRICING SUMMARY")
    print("="*80 + "\n")
    
    print("🐕 DOGS (Annual):")
    print("-" * 80)
    print(f"{'Program':<12} {'≤10kg':<10} {'11-20kg':<10} {'21-40kg':<10} {'>40kg':<10}")
    print("-" * 80)
    for program in ['silver', 'gold', 'platinum']:
        prices = [
            f"{FILLPDF_DOG_PRICING[program]['10']['final']:.2f}€",
            f"{FILLPDF_DOG_PRICING[program]['11-20']['final']:.2f}€",
            f"{FILLPDF_DOG_PRICING[program]['21-40']['final']:.2f}€",
            f"{FILLPDF_DOG_PRICING[program]['>40']['final']:.2f}€"
        ]
        print(f"{program.capitalize():<12} {prices[0]:<10} {prices[1]:<10} {prices[2]:<10} {prices[3]:<10}")
    
    print("\n🐱 CATS (Annual):")
    print("-" * 80)
    print(f"{'Program':<12} {'≤10kg':<10} {'11-20kg':<10}")
    print("-" * 80)
    for program in ['silver', 'gold', 'platinum']:
        prices = [
            f"{FILLPDF_CAT_PRICING[program]['10']['final']:.2f}€",
            f"{FILLPDF_CAT_PRICING[program]['11-20']['final']:.2f}€"
        ]
        print(f"{program.capitalize():<12} {prices[0]:<10} {prices[1]:<10}")
    
    print("\n💰 SURCHARGES & ADD-ONS:")
    print("-" * 80)
    print("Breed Surcharges:")
    print("  5%:  Cane Corso, Dogo Argentino, Rottweiler")
    print("  20%: Pit Bull, French Bulldog, English Bulldog, Chow Chow")
    print("\nAdd-Ons:")
    print("  Poisoning Coverage: +18€ (Silver), +20€ (Gold), +25€ (Platinum)")
    print("  Blood Checkup:      +28€ (All programs)")
    print("\nSecond Pet Discount: -5%")
    print()


if __name__ == '__main__':
    print("\n" + "="*80)
    print("🏥 HOOLIE PET INSURANCE - PRICING VERIFICATION")
    print("="*80)
    
    # Run all checks
    sums_ok = verify_price_sums()
    consistency_ok = verify_consistency()
    show_pricing_summary()
    
    # Final result
    print("\n" + "="*80)
    print("📋 FINAL RESULT")
    print("="*80)
    
    if sums_ok and consistency_ok:
        print("✅ ALL PRICING TABLES ARE CORRECT AND CONSISTENT!")
        exit(0)
    else:
        print("⚠️  PRICING TABLES HAVE ISSUES - PLEASE REVIEW ABOVE")
        exit(1)


