# Complete Application Flow Documentation

## 📋 Complete User Journey (After Package Selection)

### Flow Overview:
1. **Package Selection** → 2. **Non-Covered Page** → 3. **User Data Form** → 4. **Application Submission** → 5. **Payment/Processing** → 6. **Completion**

---

## Step-by-Step Flow

### 1. Package Selection (`/insurance-programs/`)
**What happens:**
- User selects Silver, Gold, or Platinum program
- Clicks on program card
- **Redirects to:** `/non-covered/` with program parameter

### 2. Non-Covered Conditions Page (`/non-covered/`)
**What happens:**
- Shows what the insurance doesn't cover
- Displays selected program
- User must declare if pet has pre-existing conditions

**User Options:**
- **"Έχει προϋπάρχουσες παθήσεις"** (Has conditions)
  - **Redirects to:** `/dog-health-conditions/` or `/cat-health-conditions/`
  - User selects specific conditions
  - **Then redirects to:** `/user-data/` with conditions data

- **"Δεν έχει προϋπάρχουσες παθήσεις"** (No conditions)
  - **Redirects to:** `/user-data/` directly with `health_status=healthy`

### 3. User Data & Pricing Page (`/user-data/`)
**What happens:**
- User fills in personal information:
  - Full name, AFM, phone, address, postal code, email, microchip
- Pricing is calculated and displayed
- User can:
  - Add second pet (with 5% discount)
  - Apply ambassador/partner code for discount
  - See final pricing with all discounts applied
- User submits form

**Features:**
- ✅ Ambassador/Partner code validation
- ✅ Discount application
- ✅ Second pet support (5% discount)
- ✅ Real-time pricing calculation

### 4. Application Submission (`handle_application_submission`)
**What happens:**
- Creates `InsuranceApplication` record in database
- Generates application number (HPI10001, HPI10002, etc.)
- Applies ambassador code discounts if used
- Determines next step based on pet health

**Two Possible Outcomes:**

#### A. Pet Has Health Problems:
- **Redirects to:** `/application-processing/?application_id={id}`
- Shows processing page with:
  - Application number (e.g., HPI10001)
  - Message: "Η αίτησή σας βρίσκεται σε επεξεργασία"
  - Underwriting message: "Η αίτηση ελέγχεται από το τμήμα Underwriting"
  - Contact promise: "Θα επικοινωνήσουμε άμεσα μαζί σας"

#### B. Pet is Healthy:
- **Redirects to:** `/payments/select/{application_id}/`
- User proceeds to payment selection

### 5. Payment Selection (`/payments/select/{application_id}/`)
**What happens:**
- User selects payment plan:
  - Annual payment (recommended)
  - 6-month payment
  - 3-month payment
- User clicks "Προχωρήστε στην Πληρωμή"
- **Redirects to:** Viva Wallet checkout page
- User completes payment on Viva Wallet

### 6. Payment Completion

#### Success Path:
- Viva Wallet redirects to: `/payments/success/?s={order_code}`
- Payment is verified with Viva Wallet API
- `PaymentTransaction` status updated to `completed`
- `InsuranceApplication` status updated to `paid`
- **Shows:** Payment success page with confirmation

#### Failure Path:
- Viva Wallet redirects to: `/payments/failure/`
- Payment status marked as `failed`
- Application status marked as `payment_failed`
- **Shows:** Payment failure page with retry option

### 7. Webhook Processing (Background)
**What happens:**
- Viva Wallet sends webhook to: `/payments/webhook/viva/`
- Payment status verified
- Application and payment records updated
- Email notifications sent (if configured)

---

## Complete Flow Diagram

```
Homepage
  ↓
Select Pet Type
  ↓
Pet Gender
  ↓
Pet Birthdate
  ↓
Pet Breed
  ↓
Pet Name
  ↓
Pet Documents (REQUIRED) ← NEW
  ↓
Health Status
  ↓
  ├─ Healthy → Insurance Choice
  └─ Problems → Health Conditions → Insurance Choice
  ↓
Insurance Programs (Package Selection)
  ↓
Non-Covered Page
  ↓
  ├─ Has Conditions → Health Conditions → User Data
  └─ No Conditions → User Data
  ↓
User Data Form (with pricing, ambassador codes, second pet)
  ↓
Application Submission
  ↓
  ├─ Health Problems → Processing Page (with application number)
  └─ Healthy → Payment Selection
  ↓
Payment Selection (Annual/6-month/3-month)
  ↓
Viva Wallet Checkout
  ↓
  ├─ Success → Payment Success Page
  └─ Failure → Payment Failure Page
```

---

## Key Features in Flow

### ✅ Guest User Support
- No authentication required at any step
- All features work for anonymous users

### ✅ Ambassador/Partner Codes
- Validated via `/api/validate-affiliate-code/`
- Discounts applied to premium
- Usage tracked automatically

### ✅ Second Pet Support
- 5% discount applied
- Separate health questionnaire
- Combined pricing display

### ✅ Document Upload
- Required before proceeding
- Drag & drop support
- File validation

### ✅ Health Issues Handling
- Separate questionnaire for each pet
- Processing page with application number
- Underwriting review message

### ✅ Payment Integration
- Viva Wallet integration
- Multiple payment plans
- Webhook verification
- Status tracking

---

## Application States

### InsuranceApplication Status Flow:
1. `submitted` - Initial submission
2. `payment_pending` - Waiting for payment
3. `paid` - Payment completed
4. `approved` - Application approved
5. `active` - Contract active
6. `payment_failed` - Payment failed
7. `rejected` - Application rejected

### PaymentTransaction Status Flow:
1. `pending` - Payment initiated
2. `completed` - Payment successful
3. `failed` - Payment failed
4. `cancelled` - Payment cancelled
5. `refunded` - Payment refunded

---

## URLs Reference

### Main Flow URLs:
- `/` - Homepage
- `/select-pet/` - Pet type selection
- `/pet-gender/` - Gender selection
- `/pet-birthdate/` - Birthdate input
- `/pet-breed/` or `/cat-breed/` - Breed selection
- `/pet-name/` - Name input
- `/pet-documents/` - Document upload (NEW)
- `/health-status/` - Health status selection
- `/dog-health-conditions/` or `/cat-health-conditions/` - Health conditions
- `/insurance-choice/` - Insurance choice
- `/insurance-programs/` - Package selection
- `/non-covered/` - Non-covered conditions
- `/user-data/` - User data and pricing
- `/application-processing/` - Processing page (health issues)
- `/contact-info/` - Contact info (legacy, not used in main flow)

### Payment URLs:
- `/payments/select/{application_id}/` - Payment selection
- `/payments/success/` - Payment success
- `/payments/failure/` - Payment failure
- `/payments/webhook/viva/` - Webhook endpoint

### API URLs:
- `/api/validate-affiliate-code/` - Ambassador code validation

---

## Summary

**After Package Selection:**
1. User sees non-covered conditions
2. Declares pre-existing conditions (or not)
3. Fills user data form with pricing
4. Submits application
5. **If healthy:** Goes to payment selection → Viva Wallet → Success/Failure
6. **If health issues:** Goes to processing page with application number

**The process ends at:**
- ✅ **Payment Success Page** (for healthy pets with successful payment)
- ✅ **Processing Page** (for pets with health issues - shows application number)
- ✅ **Payment Failure Page** (if payment fails - can retry)

All flows work for **guest users** without any authentication required!

