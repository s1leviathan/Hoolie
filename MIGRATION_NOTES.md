# Migration Notes - Guest User Support & Null Safety

## Changes Made

### 1. Model Updates for Null Safety

#### InsuranceApplication
- ✅ `application_number` - Already nullable (blank=True, null=True)
- ✅ All optional fields properly nullable

#### PaymentTransaction
- ✅ `order_code` - Changed to nullable (null=True, blank=True) to prevent null issues
- ✅ `amount` - Changed to nullable (null=True, blank=True) for flexibility
- ✅ `payment_method` - Added blank=True for optional field

### 2. Guest User Support

**Current Status: ✅ Already Supported**

The application flow is already designed for guest users:
- No `@login_required` decorators found
- No authentication middleware blocking access
- All views accessible without login
- Ambassador/Partner codes work for guests
- Payment flow works for guests

### 3. Features Available to Guests

✅ All features work for guest users:
- Pet information collection
- Health status questionnaire
- Insurance program selection
- Ambassador/Partner code validation and application
- Document upload
- Payment processing
- Application submission
- Contract generation

## Migration Commands

Run these commands to apply the database changes:

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

## Migration Details

The migration will:
1. Add `application_number` field to `InsuranceApplication` (if not exists)
2. Make `order_code` nullable in `PaymentTransaction`
3. Make `amount` nullable in `PaymentTransaction`
4. Add `blank=True` to `payment_method` in `PaymentTransaction`

## Testing Guest Flow

To test the guest user flow:

1. **Start without logging in** - All pages should be accessible
2. **Complete pet information** - Should work without authentication
3. **Apply ambassador code** - `/api/validate-affiliate-code/` should work
4. **Submit application** - Should create `InsuranceApplication` without user account
5. **Process payment** - Should work for guest users
6. **View processing page** - Should show application number for health issues

## Notes

- All models are now null-safe
- Guest users can complete the entire flow
- Ambassador codes work for guests
- No authentication required for any step
- Application numbers auto-generate (HPI10001, HPI10002, etc.)

