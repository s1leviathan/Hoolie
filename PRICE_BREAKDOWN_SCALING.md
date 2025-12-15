# 💰 PRICE BREAKDOWN: ANNUAL → 6-MONTH → 3-MONTH

## 📊 Scaling Factors

| Payment Frequency | Multiplier | Percentage | Formula |
|-------------------|------------|------------|---------|
| **Annual** | 1.0 | 100% | Base price |
| **6-Month** | 0.525 | 52.5% | Annual × 0.525 |
| **3-Month** | 0.275 | 27.5% | Annual × 0.275 |

**Note:** These multipliers apply to:
- Base package prices
- Breed surcharges (5% and 20%)
- Add-ons (Poisoning Coverage, Blood Checkup)

---

## 🐕 DOG PRICING EXAMPLES

### Silver Program

#### ≤10kg (10)
| Frequency | Net | Fee | IPT | **Gross** |
|-----------|-----|-----|-----|-----------|
| Annual | 111.54€ | 33.46€ | 21.75€ | **166.75€** |
| 6-Month | 58.56€ | 17.57€ | 11.42€ | **87.54€** (52.5%) |
| 3-Month | 30.67€ | 9.20€ | 5.98€ | **45.86€** (27.5%) |

**Verification:**
- 6-Month: 166.75 × 0.525 = 87.54€ ✅
- 3-Month: 166.75 × 0.275 = 45.86€ ✅

#### 21-40kg
| Frequency | Net | Fee | IPT | **Gross** |
|-----------|-----|-----|-----|-----------|
| Annual | 156.62€ | 46.98€ | 30.54€ | **234.14€** |
| 6-Month | 82.22€ | 24.67€ | 16.03€ | **122.92€** (52.5%) |
| 3-Month | 43.07€ | 12.92€ | 8.40€ | **64.39€** (27.5%) |

---

### Gold Program

#### 21-40kg (Current Example)
| Frequency | Net | Fee | IPT | **Gross** |
|-----------|-----|-----|-----|-----------|
| Annual | 192.68€ | 57.80€ | 37.57€ | **288.05€** |
| 6-Month | 101.16€ | 30.35€ | 19.73€ | **151.23€** (52.5%) |
| 3-Month | 52.99€ | 15.90€ | 10.33€ | **79.21€** (27.5%) |

**Verification:**
- 6-Month: 288.05 × 0.525 = 151.23€ ✅
- 3-Month: 288.05 × 0.275 = 79.21€ ✅

---

## 🐱 CAT PRICING EXAMPLES

### Silver Program

#### ≤10kg
| Frequency | Net | Fee | IPT | **Gross** |
|-----------|-----|-----|-----|-----------|
| Annual | 76.10€ | 22.83€ | 14.84€ | **113.81€** |
| 6-Month | 39.95€ | 11.99€ | 7.79€ | **59.75€** (52.5%) |
| 3-Month | 20.93€ | 6.28€ | 4.08€ | **31.30€** (27.5%) |

---

## ➕ ADD-ONS PRICING

### Poisoning Coverage

| Program | Annual | 6-Month (52.5%) | 3-Month (27.5%) |
|---------|--------|-----------------|-----------------|
| Silver | 18€ | 9.45€ | 4.95€ |
| Gold | 20€ | **10.50€** | 5.50€ |
| Platinum | 25€ | 13.13€ | 6.88€ |
| Dynasty | 25€ | 13.13€ | 6.88€ |

**Formula:**
- 6-Month: `annual_price × 0.525`
- 3-Month: `annual_price × 0.275`

**Example (Gold):**
- 6-Month: 20€ × 0.525 = 10.50€ ✅
- 3-Month: 20€ × 0.275 = 5.50€ ✅

---

### Blood Checkup

| Frequency | Price |
|-----------|-------|
| Annual | 28.00€ |
| 6-Month | 14.70€ (28 × 0.525) |
| 3-Month | 7.70€ (28 × 0.275) |

---

## 📈 SURCHARGES APPLICATION

### Breed Surcharges (Applied to ALL frequencies)

**5% Surcharge:**
- Applied first: `base_price × 1.05`
- Example: 151.23€ × 1.05 = 158.79€

**20% Surcharge:**
- Applied after 5% (if both): `(base_price × 1.05) × 1.20`
- Or if only 20%: `base_price × 1.20`
- Example: 151.23€ × 1.20 = 181.48€

**Both Surcharges:**
- Example: 151.23€ × 1.05 × 1.20 = 190.55€

**Note:** Surcharges are applied to the base price, then the result is scaled for 6-month/3-month.

---

## 🔢 COMPLETE CALCULATION EXAMPLE

### Scenario: Gold Dog 21-40kg, 6-Month Payment, with Poisoning Coverage

**Step 1: Base Price**
- Annual: 288.05€
- 6-Month: 288.05€ × 0.525 = **151.23€**

**Step 2: Add Poisoning Coverage**
- Annual: 20€
- 6-Month: 20€ × 0.525 = **10.50€**

**Step 3: Final Total**
- 151.23€ + 10.50€ = **161.73€** ✅

---

## 📋 CODE IMPLEMENTATION

### Location: `main/utils.py`

```python
# Base prices from Excel tables
annual_price = get_pricing_values(..., "annual")[3]  # gross
six_month_price = get_pricing_values(..., "6m")[3]    # gross
three_month_price = get_pricing_values(..., "3m")[3]  # gross

# Apply surcharges (if any)
if special_breed_5_percent:
    annual_final *= 1.05
    six_month_final *= 1.05
    three_month_final *= 1.05

if special_breed_20_percent:
    annual_final *= 1.20
    six_month_final *= 1.20
    three_month_final *= 1.20

# Add poisoning coverage
if additional_poisoning_coverage:
    annual_final += get_poisoning_price(program, "annual")      # e.g., 20€
    six_month_final += get_poisoning_price(program, "six_month") # e.g., 10.50€
    three_month_final += get_poisoning_price(program, "three_month") # e.g., 5.50€

# Add blood checkup
if additional_blood_checkup:
    annual_final += 28.00
    six_month_final += round(28.00 * 0.525, 2)  # 14.70€
    three_month_final += round(28.00 * 0.275, 2)  # 7.70€
```

---

## ✅ KEY POINTS

1. **Base prices come from Excel tables** - They are pre-calculated and stored in `PRICING` dictionary
2. **All components scale proportionally** - Net, Fee, IPT all use the same multiplier
3. **Add-ons use the same scaling** - Poisoning and Blood Checkup scale at 52.5% and 27.5%
4. **Surcharges are multiplicative** - Applied to base, then result is scaled
5. **Final premium = Base + Surcharges + Add-ons** (all scaled to selected frequency)

---

## 🧮 VERIFICATION FORMULAS

**6-Month Check:**
```
6_month_total = (annual_base + annual_surcharges + annual_addons) × 0.525
```

**3-Month Check:**
```
3_month_total = (annual_base + annual_surcharges + annual_addons) × 0.275
```

**Example Verification (Gold 21-40kg, 6-Month, Poisoning):**
- Annual base: 288.05€
- Annual poisoning: 20€
- Annual total: 308.05€
- 6-Month: 308.05€ × 0.525 = 161.73€ ✅

