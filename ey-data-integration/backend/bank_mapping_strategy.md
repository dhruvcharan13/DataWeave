# Bank Data Integration Strategy

## Schema Analysis Results

### Bank 1 Data Structure
- **Customer Table**: 10,000 rows, 24 columns
  - Primary Key: `customerId`
  - Key Fields: `legalId`, `accountOfficerId`
  - Personal Info: `givenName`, `lastName`, `email`, `phoneNumber`, `dateOfBirth`, `gender`
  - Business Info: `customerType`, `customerStatus`

- **Accounts Table**: 15,071 rows, 16 columns
  - Primary Key: `accountId`
  - Foreign Key: `customerId` → Bank1_Customer
  - Financial: `availableBalance`, `currency`, `status`

- **Transactions Table**: 74,604 rows, 23 columns
  - Primary Key: `transactionReference`
  - Foreign Key: `accountId` → Bank1_Accounts
  - Transaction Details: `activity`, `transactionAmount`, `effectiveDate`

### Bank 2 Data Structure
- **Customer Table**: 10,000 rows, 16 columns
  - Primary Key: `encodedKey`
  - Key Fields: `id`, `assignedUserKey`
  - Personal Info: `firstName`, `lastName`, `emailAddress`, `homePhone`, `birthDate`, `gender`
  - Business Info: `clientType`, `state`

- **Accounts Table**: 19,756 rows, 25 columns
  - Primary Key: `encodedKey`
  - Foreign Key: `accountHolderKey` → Bank2_Customer
  - Financial: `availableBalance`, `currencyCode`, `status`

## Cross-Bank Mapping Strategy

### High Confidence Mappings (90%+)
1. **Customer Identifiers**
   - Bank1: `customerId` ↔ Bank2: `encodedKey`
   - Purpose: Primary key mapping for customer records

2. **Personal Information**
   - Bank1: `givenName` ↔ Bank2: `firstName`
   - Bank1: `lastName` ↔ Bank2: `lastName`
   - Bank1: `email` ↔ Bank2: `emailAddress`
   - Bank1: `dateOfBirth` ↔ Bank2: `birthDate`
   - Bank1: `gender` ↔ Bank2: `gender`

3. **Account Information**
   - Bank1: `accountId` ↔ Bank2: `encodedKey`
   - Bank1: `customerId` ↔ Bank2: `accountHolderKey`
   - Bank1: `availableBalance` ↔ Bank2: `availableBalance`
   - Bank1: `currency` ↔ Bank2: `currencyCode`

### Medium Confidence Mappings (80-90%)
1. **Contact Information**
   - Bank1: `phoneNumber` ↔ Bank2: `homePhone`
   - Bank1: `customerType` ↔ Bank2: `clientType`

## Data Integration Workflow

### Phase 1: Schema Mapping
1. Map customer records using high-confidence fields
2. Identify potential duplicates using email, phone, name combinations
3. Create unified customer schema

### Phase 2: Account Consolidation
1. Map accounts to unified customer records
2. Handle multiple accounts per customer
3. Preserve account history and relationships

### Phase 3: Transaction Integration
1. Map transactions to unified account structure
2. Standardize transaction categories and types
3. Create unified transaction schema

## Implementation Strategy

### Backend API Endpoints
- `POST /analyze-schemas` - Analyze uploaded bank data
- `POST /detect-relationships` - Find internal relationships
- `POST /suggest-mappings` - AI-powered cross-bank mappings
- `POST /validate-mappings` - Validate mapping accuracy
- `POST /merge-data` - Execute data integration

### AI-Powered Features
1. **Duplicate Detection**: Use fuzzy matching on names, emails, phones
2. **Relationship Inference**: Analyze transaction patterns
3. **Data Quality**: Identify inconsistencies and missing data
4. **Mapping Validation**: Cross-validate mapping suggestions

## Expected Outcomes

### Unified Customer Schema
```json
{
  "customerId": "unified_id",
  "firstName": "mapped_from_bank1_givenName_or_bank2_firstName",
  "lastName": "mapped_from_both_banks",
  "email": "mapped_from_bank1_email_or_bank2_emailAddress",
  "phone": "mapped_from_bank1_phoneNumber_or_bank2_homePhone",
  "dateOfBirth": "mapped_from_bank1_dateOfBirth_or_bank2_birthDate",
  "gender": "mapped_from_both_banks",
  "customerType": "mapped_from_bank1_customerType_or_bank2_clientType",
  "sourceBanks": ["bank1", "bank2"],
  "confidence": 0.95
}
```

### Unified Account Schema
```json
{
  "accountId": "unified_id",
  "customerId": "unified_customer_id",
  "accountType": "mapped_from_both_banks",
  "balance": "mapped_from_bank1_availableBalance_or_bank2_availableBalance",
  "currency": "mapped_from_bank1_currency_or_bank2_currencyCode",
  "status": "mapped_from_both_banks",
  "sourceBanks": ["bank1", "bank2"],
  "confidence": 0.9
}
```

This strategy provides a comprehensive approach to integrating the two bank datasets while maintaining data integrity and providing confidence scores for each mapping.
