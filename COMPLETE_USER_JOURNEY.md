# 📋 Complete User Journey - All Pages & Options

## 🏠 **1. HOMEPAGE** (`/`)
**URL:** `/`  
**View:** `index`  
**Template:** `main/index.html`

**Options:**
- ✅ "Ξεκινήστε Τώρα" (Start Now) button → Goes to `/select-pet/`
- ✅ View information about pet insurance
- ✅ View features and benefits

---

## 🐾 **2. SELECT PET TYPE** (`/select-pet/`)
**URL:** `/select-pet/`  
**View:** `select_pet`  
**Template:** `main/select_pet.html`

**Options:**
- ✅ **"Σκύλος" (Dog)** → Goes to `/pet-gender/?type=dog`
- ✅ **"Γάτα" (Cat)** → Goes to `/pet-gender/?type=cat`
- ✅ "Πίσω" (Back) button → Goes to `/` (homepage)

**Parameters Passed:**
- `type` = `dog` or `cat`

---

## ⚥ **3. PET GENDER** (`/pet-gender/`)
**URL:** `/pet-gender/?type={dog|cat}`  
**View:** `pet_gender`  
**Template:** `main/pet_gender.html`

**Options:**
- ✅ **"Αρσενικό" (Male)** → Goes to `/pet-birthdate/?type={type}&gender=male`
- ✅ **"Θηλυκό" (Female)** → Goes to `/pet-birthdate/?type={type}&gender=female`
- ✅ "Πίσω" (Back) button → Goes to `/select-pet/`

**Parameters Passed:**
- `type` = `dog` or `cat`
- `gender` = `male` or `female`

---

## 📅 **4. PET BIRTHDATE** (`/pet-birthdate/`)
**URL:** `/pet-birthdate/?type={type}&gender={gender}`  
**View:** `pet_birthdate`  
**Template:** `main/pet_birthdate.html`

**Options:**
- ✅ Date picker to select pet's birthdate
- ✅ "Επόμενο" (Next) button → Goes to `/pet-breed/` or `/cat-breed/` (based on type)
- ✅ "Πίσω" (Back) button → Goes to `/pet-gender/?type={type}`

**Parameters Passed:**
- `type` = `dog` or `cat`
- `gender` = `male` or `female`
- `birthdate` = `YYYY-MM-DD`

---

## 🐕 **5A. DOG BREED** (`/pet-breed/`)
**URL:** `/pet-breed/?type=dog&gender={gender}&birthdate={date}`  
**View:** `pet_breed`  
**Template:** `main/pet_breed.html`

**Options:**
- ✅ Dropdown with 20 dog breeds:
  - Λαμπραντόρ, Γκόλντεν Ρετρίβερ, Γερμανικός Ποιμενικός, Μπουλντόγκ, Πούντλ, Μπίγκλ, Ρότβαϊλερ, Γιόρκσαϊρ Τέριερ, Ντάξχουντ, Σιμπέριαν Χάσκι, Πομερανιάν, Σιτσού, Μπόξερ, Τσιουάουα, Μαλτέζ, Κοκέρ Σπάνιελ, Μπορντέρ Κόλι, Φρέντς Μπουλντόγκ, Αυστραλιανός Ποιμενικός, Μπασέτ Χάουντ
- ✅ "Επόμενο" (Next) button → Goes to `/pet-name/?type=dog&gender={gender}&birthdate={date}&breed={breed}`
- ✅ "Πίσω" (Back) button → Goes to `/pet-birthdate/?type=dog&gender={gender}`

**Parameters Passed:**
- `type` = `dog`
- `gender` = `male` or `female`
- `birthdate` = `YYYY-MM-DD`
- `breed` = Selected breed name

---

## 🐱 **5B. CAT BREED** (`/cat-breed/`)
**URL:** `/cat-breed/?type=cat&gender={gender}&birthdate={date}`  
**View:** `cat_breed`  
**Template:** `main/cat_breed.html`

**Options:**
- ✅ Dropdown with 20 cat breeds:
  - Περσική, Μέιν Κουν, Σιαμέζα, Ραγκντόλ, Βρετανική Κοντότριχη, Αμπισίνια, Ρωσική Μπλε, Σκωτσέζικη Πτυχωτή, Σφίγκα, Βεγγαλική, Μάνξ, Νορβηγική Δασική, Τούρκικη Αγκυρα, Αμερικανική Κοντότριχη, Εξωτική Κοντότριχη, Ορμιέντλ, Σομαλί, Τονκινέζα, Μπομπέι, Κορνίς Ρεξ
- ✅ "Επόμενο" (Next) button → Goes to `/pet-name/?type=cat&gender={gender}&birthdate={date}&breed={breed}`
- ✅ "Πίσω" (Back) button → Goes to `/pet-birthdate/?type=cat&gender={gender}`

**Parameters Passed:**
- `type` = `cat`
- `gender` = `male` or `female`
- `birthdate` = `YYYY-MM-DD`
- `breed` = Selected breed name

---

## ✏️ **6. PET NAME** (`/pet-name/`)
**URL:** `/pet-name/?type={type}&gender={gender}&birthdate={date}&breed={breed}`  
**View:** `pet_name`  
**Template:** `main/pet_name.html`

**Options:**
- ✅ Text input for pet's name
- ✅ "Επόμενο" (Next) button → Goes to `/pet-documents/?type={type}&gender={gender}&birthdate={date}&breed={breed}&name={name}`
- ✅ "Πίσω" (Back) button → Goes to `/pet-breed/` or `/cat-breed/` (based on type)

**Parameters Passed:**
- `type` = `dog` or `cat`
- `gender` = `male` or `female`
- `birthdate` = `YYYY-MM-DD`
- `breed` = Breed name
- `name` = Pet's name

---

## 📄 **7. PET DOCUMENTS & PHOTOS** (`/pet-documents/`)
**URL:** `/pet-documents/?type={type}&gender={gender}&birthdate={date}&breed={breed}&name={name}`  
**View:** `pet_documents`  
**Template:** `main/pet_documents.html`

**Options:**

### **Document Upload Section:**
- ✅ Drag & drop or click to upload documents
- ✅ Accepts: PDF, JPG, PNG, DOC, DOCX
- ✅ Max size: 10MB per file
- ✅ **REQUIRED:** At least 1 document must be uploaded

### **Photo Upload Section:**
- ✅ Drag & drop or click to upload photos
- ✅ Accepts: JPG, PNG, WEBP (images only)
- ✅ Max size: 10MB per photo
- ✅ **REQUIRED:** At least 5 photos must be uploaded (περιμετρικά - from different angles)
- ✅ Photo counter shows: "X / 5 photos (minimum 5 required)"
- ✅ Grid display of uploaded photos with thumbnails

**API Endpoints:**
- `POST /api/upload-pet-document/` - Upload document
- `POST /api/upload-pet-photo/` - Upload photo

**Options:**
- ✅ "Επόμενο" (Next) button → **Only enabled when:**
  - At least 1 document uploaded ✅
  - At least 5 photos uploaded ✅
  - Goes to `/health-status/?type={type}&gender={gender}&birthdate={date}&breed={breed}&name={name}`
- ✅ "Πίσω" (Back) button → Goes to `/pet-name/?type={type}&gender={gender}&birthdate={date}&breed={breed}`

**Parameters Passed:**
- All previous parameters + `name` = Pet's name

---

## 🏥 **8. HEALTH STATUS** (`/health-status/`)
**URL:** `/health-status/?type={type}&gender={gender}&birthdate={date}&breed={breed}&name={name}`  
**View:** `health_status`  
**Template:** `main/health_status.html`

**Options:**
- ✅ **"Υγιές" (Healthy)** → Goes to `/insurance-programs/?type={type}&gender={gender}&birthdate={date}&breed={breed}&name={name}&health_status=healthy`
- ✅ **"Με προβλήματα" (With problems)** → Goes to `/dog-health-conditions/` or `/cat-health-conditions/` (based on type)
- ✅ "Πίσω" (Back) button → Goes to `/pet-documents/?type={type}&gender={gender}&birthdate={date}&breed={breed}&name={name}`

**Parameters Passed:**
- All previous parameters
- `health_status` = `healthy` or `problems`

---

## 🐕 **9A. DOG HEALTH CONDITIONS** (`/dog-health-conditions/`)
**URL:** `/dog-health-conditions/?type=dog&gender={gender}&birthdate={date}&breed={breed}&name={name}`  
**View:** `dog_health_conditions`  
**Template:** `main/dog_health_conditions.html`

**Options:**
- ✅ Checkboxes for 17 common dog health conditions:
  - Δυσπλασία ισχίου, Δυσπλασία αγκώνα, Καταρράκτης, Γλαύκωμα, Καρδιακές παθήσεις, Επιληψία, Αλλεργίες δέρματος, Οστεοαρθρίτιδα, Διαβήτης, Παχυσαρκία, Προβλήματα θυρεοειδούς, Νεφρικές παθήσεις, Ηπατικές παθήσεις, Αναπνευστικά προβλήματα, Γαστρεντερικές διαταραχές, Όγκοι/Καρκίνος, Τραυματισμοί από ατυχήματα, Χειρουργικές επεμβάσεις
- ✅ Text area for additional conditions/notes
- ✅ "Επόμενο" (Next) button → Goes to `/insurance-programs/?type={type}&gender={gender}&birthdate={date}&breed={breed}&name={name}&health_status=problems&health_conditions={conditions}`
- ✅ "Πίσω" (Back) button → Goes to `/health-status/?type={type}&gender={gender}&birthdate={date}&breed={breed}&name={name}`

**Parameters Passed:**
- All previous parameters
- `health_status` = `problems`
- `health_conditions` = Selected conditions (comma-separated)

---

## 🐱 **9B. CAT HEALTH CONDITIONS** (`/cat-health-conditions/`)
**URL:** `/cat-health-conditions/?type=cat&gender={gender}&birthdate={date}&breed={breed}&name={name}`  
**View:** `cat_health_conditions`  
**Template:** `main/cat_health_conditions.html`

**Options:**
- ✅ Checkboxes for 17 common cat health conditions:
  - Χρόνια νεφρική ανεπάρκεια, Υπερθυρεοειδισμός, Διαβήτης, Καρδιακές παθήσεις, Ουρολιθίαση, Κυστίτιδα, Αλλεργίες δέρματος, Οδοντικά προβλήματα, Αναπνευστικές λοιμώξεις, Γαστρεντερικές διαταραχές, Παχυσαρκία, Οφθαλμικά προβλήματα, Όγκοι/Καρκίνος, Ιογενείς λοιμώξεις (FIV, FeLV), Παρασιτώσεις, Τραυματισμοί από πτώσεις, Χειρουργικές επεμβάσεις
- ✅ Text area for additional conditions/notes
- ✅ "Επόμενο" (Next) button → Goes to `/insurance-programs/?type={type}&gender={gender}&birthdate={date}&breed={breed}&name={name}&health_status=problems&health_conditions={conditions}`
- ✅ "Πίσω" (Back) button → Goes to `/health-status/?type={type}&gender={gender}&birthdate={date}&breed={breed}&name={name}`

**Parameters Passed:**
- All previous parameters
- `health_status` = `problems`
- `health_conditions` = Selected conditions (comma-separated)

---

## 💎 **10. INSURANCE PROGRAMS** (`/insurance-programs/`)
**URL:** `/insurance-programs/?type={type}&gender={gender}&birthdate={date}&breed={breed}&name={name}&health_status={status}&health_conditions={conditions}`  
**View:** `insurance_programs`  
**Template:** `main/insurance_programs.html`

**Options:**
- ✅ **"Silver" (Ασημένιο)** → Goes to `/non-covered/?program=silver&type={type}&gender={gender}&birthdate={date}&breed={breed}&name={name}&health_status={status}&health_conditions={conditions}`
- ✅ **"Gold" (Χρυσό)** → Goes to `/non-covered/?program=gold&type={type}&gender={gender}&birthdate={date}&breed={breed}&name={name}&health_status={status}&health_conditions={conditions}`
- ✅ **"Platinum" (Πλατινένιο)** → Goes to `/non-covered/?program=platinum&type={type}&gender={gender}&birthdate={date}&breed={breed}&name={name}&health_status={status}&health_conditions={conditions}`
- ✅ "Πίσω" (Back) button → Goes to `/health-status/` or health conditions page

**Parameters Passed:**
- All previous parameters
- `program` = `silver`, `gold`, or `platinum`

---

## ⚠️ **11. NON-COVERED CONDITIONS** (`/non-covered/`)
**URL:** `/non-covered/?program={program}&type={type}&gender={gender}&birthdate={date}&breed={breed}&name={name}&health_status={status}&health_conditions={conditions}`  
**View:** `non_covered`  
**Template:** `main/non_covered.html`

**Options:**
- ✅ Displays what the insurance doesn't cover
- ✅ Shows selected program (Silver/Gold/Platinum)
- ✅ **"Έχει προϋπάρχουσες παθήσεις" (Has pre-existing conditions)** → Goes to `/dog-health-conditions/` or `/cat-health-conditions/` (if not already filled)
- ✅ **"Δεν έχει προϋπάρχουσες παθήσεις" (No pre-existing conditions)** → Goes to `/user-data/?program={program}&type={type}&gender={gender}&birthdate={date}&breed={breed}&name={name}&health_status=healthy`
- ✅ "Πίσω" (Back) button → Goes to `/insurance-programs/`

**Parameters Passed:**
- All previous parameters
- `program` = `silver`, `gold`, or `platinum`

---

## 👤 **12. USER DATA & PRICING** (`/user-data/`)
**URL:** `/user-data/?program={program}&type={type}&gender={gender}&birthdate={date}&breed={breed}&name={name}&health_status={status}&health_conditions={conditions}`  
**View:** `user_data`  
**Template:** `main/user_data.html`

**Options:**

### **User Information Fields:**
- ✅ Full Name (required)
- ✅ AFM (Tax ID) (required)
- ✅ Phone (required)
- ✅ Address (required)
- ✅ Postal Code (required)
- ✅ Email (required)
- ✅ Microchip Number (optional)

### **Second Pet Option:**
- ✅ **"Ναι, έχω δεύτερο κατοικίδιο" (Yes, I have a second pet)** checkbox
  - When checked, shows fields for second pet:
    - Second Pet Name
    - Second Pet Type (Dog/Cat)
    - Second Pet Gender (Male/Female)
    - Second Pet Birthdate
    - Second Pet Breed
    - Second Pet Health Status
    - Second Pet Health Conditions (if applicable)
  - **Applies 5% discount** to total premium

### **Ambassador/Partner Code:**
- ✅ Text input for discount code
- ✅ "Εφαρμογή" (Apply) button → Validates code via `/api/validate-affiliate-code/`
- ✅ Shows discount amount if code is valid

### **Pricing Display:**
- ✅ Base premium (calculated from pet type, breed, age, program)
- ✅ Second pet discount (5% if applicable)
- ✅ Ambassador/Partner discount (if code applied)
- ✅ **Final premium** (with all discounts applied)
- ✅ Shows pricing for:
  - Annual payment
  - 6-month payment
  - 3-month payment

**API Endpoints:**
- `POST /api/validate-affiliate-code/` - Validate and apply discount code

**Options:**
- ✅ "Υποβολή Αίτησης" (Submit Application) button → Submits form via AJAX to `/user-data/` (POST)
  - Creates `InsuranceApplication` record
  - Generates application number (HPI10001, HPI10002, etc.)
  - Links uploaded documents and photos to application
  - Generates contract PDF
  - Sends notification emails
  - **Redirects based on health status:**
    - **If healthy:** → `/payments/select/{application_id}/`
    - **If health problems:** → `/application-processing/?application_id={id}`
- ✅ "Πίσω" (Back) button → Goes to `/non-covered/`

**Parameters Passed:**
- All previous parameters
- User data (via POST)

---

## 💳 **13A. PAYMENT SELECTION** (`/payments/select/{application_id}/`)
**URL:** `/payments/select/{application_id}/`  
**View:** `PaymentSelectionView`  
**Template:** `main/payment_selection.html`

**Options:**
- ✅ **"Ετήσια Πληρωμή" (Annual Payment)** - Recommended
- ✅ **"6μηνη Πληρωμή" (6-Month Payment)**
- ✅ **"3μηνη Πληρωμή" (3-Month Payment)**
- ✅ Shows pricing for each option
- ✅ "Προχωρήστε στην Πληρωμή" (Proceed to Payment) button → Redirects to Viva Wallet checkout page
- ✅ "Πίσω" (Back) button → Goes to `/user-data/`

**What Happens:**
- Creates `PaymentTransaction` record
- Generates Viva Wallet checkout URL
- Redirects user to Viva Wallet for payment

---

## ✅ **13B. PAYMENT SUCCESS** (`/payments/success/`)
**URL:** `/payments/success/?s={order_code}`  
**View:** `PaymentSuccessView`  
**Template:** `main/payment_success.html`

**Options:**
- ✅ Displays payment confirmation
- ✅ Shows application number
- ✅ Shows payment amount
- ✅ Shows contract number
- ✅ "Επιστροφή στην Αρχική" (Return to Home) button → Goes to `/`

**What Happens:**
- Verifies payment with Viva Wallet API
- Updates `PaymentTransaction` status to `completed`
- Updates `InsuranceApplication` status to `paid`
- Sends confirmation emails

---

## ❌ **13C. PAYMENT FAILURE** (`/payments/failure/`)
**URL:** `/payments/failure/`  
**View:** `PaymentFailureView`  
**Template:** `main/payment_failure.html`

**Options:**
- ✅ Displays payment failure message
- ✅ "Δοκιμάστε Ξανά" (Try Again) button → Goes back to `/payments/select/{application_id}/`
- ✅ "Επιστροφή στην Αρχική" (Return to Home) button → Goes to `/`

**What Happens:**
- Updates `PaymentTransaction` status to `failed`
- Updates `InsuranceApplication` status to `payment_failed`

---

## ⏳ **14. APPLICATION PROCESSING** (`/application-processing/`)
**URL:** `/application-processing/?application_id={id}`  
**View:** `application_processing`  
**Template:** `main/application_processing.html`

**Options:**
- ✅ Displays application number (e.g., HPI10001)
- ✅ Message: "Η αίτησή σας βρίσκεται σε επεξεργασία"
- ✅ Underwriting message: "Η αίτηση ελέγχεται από το τμήμα Underwriting"
- ✅ Contact promise: "Θα επικοινωνήσουμε άμεσα μαζί σας"
- ✅ "Επιστροφή στην Αρχική" (Return to Home) button → Goes to `/`

**When Shown:**
- User has health problems (pre-existing conditions)
- Application requires manual review

---

## 🙏 **15. THANK YOU PAGE** (`/thank-you/`)
**URL:** `/thank-you/?application_id={id}`  
**View:** `thank_you`  
**Template:** `main/thank_you.html`

**Options:**
- ✅ Displays application number
- ✅ Shows pet name
- ✅ Shows customer email
- ✅ Displays 4-step process explanation:
  1. Email confirmation (within minutes)
  2. Application processing (Underwriting review)
  3. Contact from team (within 48 hours)
  4. Contract issuance
- ✅ "Επιστροφή στην Αρχική" (Return to Home) button → Goes to `/`

**When Shown:**
- After successful application submission
- Shows next steps in the process

---

## 🔍 **QR CODE & VERIFICATION PAGES**

### **16A. CONTRACT VERIFICATION** (`/contract/verify/{contract_number}/`)
**URL:** `/contract/verify/{contract_number}/`  
**View:** `contract_verification`  
**Template:** `qr/contract_verification.html`

**Options:**
- ✅ Displays contract verification status
- ✅ Shows contract details if valid
- ✅ Shows error message if invalid

---

### **16B. TERMS AND CONDITIONS** (`/terms-and-conditions/`)
**URL:** `/terms-and-conditions/`  
**View:** `terms_and_conditions`  
**Template:** `qr/terms_and_conditions.html`

**Options:**
- ✅ Displays terms and conditions
- ✅ Accessible via QR code

---

### **16C. CUSTOMER PORTAL** (`/customer/portal/{contract_number}/`)
**URL:** `/customer/portal/{contract_number}/`  
**View:** `customer_portal`  
**Template:** `qr/customer_portal.html`

**Options:**
- ✅ Displays customer contract information
- ✅ Shows contract details
- ✅ Accessible via QR code

---

## 🔧 **API ENDPOINTS**

### **17A. VALIDATE AFFILIATE CODE** (`/api/validate-affiliate-code/`)
**Method:** `POST`  
**View:** `validate_affiliate_code`

**Parameters:**
- `code` - Ambassador/Partner code

**Returns:**
- `valid` - Boolean
- `discount_amount` - Discount in euros
- `discount_percentage` - Discount percentage
- `message` - Success/error message

---

### **17B. UPLOAD PET DOCUMENT** (`/api/upload-pet-document/`)
**Method:** `POST`  
**View:** `upload_pet_document`

**Parameters:**
- `file` - Document file (PDF, JPG, PNG, DOC, DOCX)
- `pet_name` - Pet's name
- `pet_type` - `dog` or `cat`

**Returns:**
- `success` - Boolean
- `document_id` - Document ID
- `filename` - Original filename
- `file_url` - URL to access file
- `message` - Success/error message

---

### **17C. UPLOAD PET PHOTO** (`/api/upload-pet-photo/`)
**Method:** `POST`  
**View:** `upload_pet_photo`

**Parameters:**
- `file` - Photo file (JPG, PNG, WEBP)
- `pet_name` - Pet's name
- `pet_type` - `dog` or `cat`

**Returns:**
- `success` - Boolean
- `photo_id` - Photo ID
- `filename` - Original filename
- `file_url` - URL to access photo
- `message` - Success/error message

---

## 📊 **COMPLETE FLOW DIAGRAM**

```
1. HOMEPAGE (/)
   ↓
2. SELECT PET TYPE (/select-pet/)
   ├─ Dog → 3. PET GENDER
   └─ Cat → 3. PET GENDER
   ↓
3. PET GENDER (/pet-gender/)
   ├─ Male → 4. PET BIRTHDATE
   └─ Female → 4. PET BIRTHDATE
   ↓
4. PET BIRTHDATE (/pet-birthdate/)
   ↓
5. PET BREED (/pet-breed/ or /cat-breed/)
   ↓
6. PET NAME (/pet-name/)
   ↓
7. PET DOCUMENTS & PHOTOS (/pet-documents/)
   ├─ Upload Documents (min 1 required)
   └─ Upload Photos (min 5 required)
   ↓
8. HEALTH STATUS (/health-status/)
   ├─ Healthy → 10. INSURANCE PROGRAMS
   └─ With Problems → 9. HEALTH CONDITIONS
   ↓
9. HEALTH CONDITIONS (/dog-health-conditions/ or /cat-health-conditions/)
   ↓
10. INSURANCE PROGRAMS (/insurance-programs/)
   ├─ Silver → 11. NON-COVERED
   ├─ Gold → 11. NON-COVERED
   └─ Platinum → 11. NON-COVERED
   ↓
11. NON-COVERED (/non-covered/)
   ├─ Has Conditions → 9. HEALTH CONDITIONS (if not already filled)
   └─ No Conditions → 12. USER DATA
   ↓
12. USER DATA (/user-data/)
   ├─ Fill user information
   ├─ Add second pet (optional, 5% discount)
   ├─ Apply ambassador/partner code (optional)
   └─ Submit Application
   ↓
13. APPLICATION SUBMISSION (handle_application_submission)
   ├─ Creates InsuranceApplication
   ├─ Links documents & photos
   ├─ Generates contract PDF
   ├─ Sends notification emails
   └─ Routes based on health:
      ├─ Healthy → 13A. PAYMENT SELECTION
      └─ Health Problems → 14. APPLICATION PROCESSING
   ↓
13A. PAYMENT SELECTION (/payments/select/{id}/)
   ├─ Annual Payment → Viva Wallet
   ├─ 6-Month Payment → Viva Wallet
   └─ 3-Month Payment → Viva Wallet
   ↓
   Viva Wallet Checkout
   ├─ Success → 13B. PAYMENT SUCCESS
   └─ Failure → 13C. PAYMENT FAILURE
   ↓
13B. PAYMENT SUCCESS (/payments/success/)
   └─ Application completed ✅
   
13C. PAYMENT FAILURE (/payments/failure/)
   └─ Can retry payment
   
14. APPLICATION PROCESSING (/application-processing/)
   └─ Manual review required (health issues)
   
15. THANK YOU (/thank-you/)
   └─ Shows next steps
```

---

## ✅ **REQUIREMENTS SUMMARY**

### **Required at Each Step:**
1. ✅ Pet type selection
2. ✅ Pet gender selection
3. ✅ Pet birthdate
4. ✅ Pet breed selection
5. ✅ Pet name
6. ✅ **At least 1 document** uploaded
7. ✅ **At least 5 photos** uploaded (περιμετρικά)
8. ✅ Health status selection
9. ✅ Health conditions (if applicable)
10. ✅ Insurance program selection
11. ✅ User data form completion
12. ✅ Payment (if healthy) or processing (if health issues)

### **Optional Features:**
- ✅ Second pet (5% discount)
- ✅ Ambassador/Partner code (discount)
- ✅ Microchip number

---

## 🎯 **KEY FEATURES**

- ✅ **No Authentication Required** - All flows work for guest users
- ✅ **Document Upload** - Required before proceeding
- ✅ **Photo Upload** - Minimum 5 photos required (περιμετρικά)
- ✅ **Health Assessment** - Separate flow for pets with health issues
- ✅ **Second Pet Support** - 5% discount applied
- ✅ **Ambassador/Partner Codes** - Discount codes with validation
- ✅ **Multiple Payment Plans** - Annual, 6-month, 3-month
- ✅ **Viva Wallet Integration** - Secure payment processing
- ✅ **Email Notifications** - Company and customer emails
- ✅ **PDF Generation** - Contract PDFs stored in S3
- ✅ **Admin Panel Access** - All documents and photos accessible

---

**Total Pages: 15 main pages + 3 QR pages + 3 API endpoints = 21 endpoints**

