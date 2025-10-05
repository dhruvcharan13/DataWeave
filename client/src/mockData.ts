export const mock_suggested_mapping = {
    "version": "mapping-2.0",
    "generated_at": "2025-10-05T07:37:09Z",
    "model": "gemini-2.5-lite",
    "source_dataset": {
      "name": "Dataset A: Core Banking"
    },
    "target_dataset": {
      "name": "Dataset B: Analytics Platform"
    },
    "assumptions": [
      "Dataset A's customerId maps to Dataset B's Customer.id, and Dataset B's Customer.encodedKey must be generated or determined by a lookup table based on A's customerId for foreign key relations.",
      "Multiple source account types (CurSav, Fixed Term) are unified into B's Deposit Accounts.",
      "All account transaction types are unified into a single logical 'Transactions' entity, which will require a full outer join and deduplication."
    ],
    "mappings": [
      {
        "id": "M001_CUSTOMER_ID",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "customerId"
        },
        "target": {
          "table": "Customer",
          "column": "id"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 1.0,
        "rationale": "Direct primary key mapping, ensuring customer record uniqueness.",
        "status": "suggested"
      },
      {
        "id": "M002_CUSTOMER_FIRSTNAME",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "givenName"
        },
        "target": {
          "table": "Customer",
          "column": "firstName"
        },
        "transform": {
          "type": "string_normalize",
          "params": {
            "case": "title"
          }
        },
        "confidence": 0.95,
        "rationale": "Direct semantic mapping. Applying normalization for consistency.",
        "status": "suggested"
      },
      {
        "id": "M003_CUSTOMER_LASTNAME",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "lastName"
        },
        "target": {
          "table": "Customer",
          "column": "lastName"
        },
        "transform": {
          "type": "string_normalize",
          "params": {
            "case": "title"
          }
        },
        "confidence": 0.95,
        "rationale": "Direct semantic mapping. Applying normalization for consistency.",
        "status": "suggested"
      },
      {
        "id": "M004_CUSTOMER_DOB",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "dateOfBirth"
        },
        "target": {
          "table": "Customer",
          "column": "birthDate"
        },
        "transform": {
          "type": "parse_date",
          "params": {
            "format": "YYYY-MM-DD"
          }
        },
        "confidence": 1.0,
        "rationale": "Direct mapping with date parsing for standard format.",
        "status": "suggested"
      },
      {
        "id": "M005_CUSTOMER_EMAIL",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "email"
        },
        "target": {
          "table": "Customer",
          "column": "emailAddress"
        },
        "transform": {
          "type": "string_normalize",
          "params": {
            "case": "lower"
          }
        },
        "confidence": 0.9,
        "rationale": "Semantic mapping. Normalizing email address to lowercase.",
        "status": "suggested"
      },
      {
        "id": "M006_CUSTOMER_PHONE_MOBILE",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "smsNumber"
        },
        "target": {
          "table": "Customer",
          "column": "mobilePhone"
        },
        "transform": {
          "type": "custom",
          "params": {
            "rule": "Cleanse and standardize phone number format"
          }
        },
        "confidence": 0.85,
        "rationale": "Mapping SMS number to mobile phone. Requires cleaning/standardization for international format.",
        "status": "suggested"
      },
      {
        "id": "M007_CUSTOMER_PHONE_HOME_STRAY",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "phoneNumber"
        },
        "target": {
          "table": "Customer",
          "column": "homePhone"
        },
        "transform": {
          "type": "custom",
          "params": {
            "rule": "Cleanse and standardize phone number format"
          }
        },
        "confidence": 0.7,
        "rationale": "Assume 'phoneNumber' is the primary/home number when 'smsNumber' is mapped to 'mobilePhone'.",
        "status": "suggested"
      },
      {
        "id": "M008_CUSTOMER_LANGUAGE",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "language"
        },
        "target": {
          "table": "Customer",
          "column": "preferredLanguage"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 0.9,
        "rationale": "Direct mapping of language preference.",
        "status": "suggested"
      },
      {
        "id": "M009_CUSTOMER_GENDER",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "gender"
        },
        "target": {
          "table": "Customer",
          "column": "gender"
        },
        "transform": {
          "type": "string_normalize",
          "params": {
            "rule": "Map to B's allowed values (e.g., M/F/Other)"
          }
        },
        "confidence": 0.9,
        "rationale": "Direct mapping, ensuring A's values conform to B's enumeration.",
        "status": "suggested"
      },
      {
        "id": "M010_CUSTOMER_TYPE",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "customerType"
        },
        "target": {
          "table": "Customer",
          "column": "clientType"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 0.9,
        "rationale": "Semantic mapping of customer type to client type.",
        "status": "suggested"
      },
      {
        "id": "M011_ADDRESS_STREET",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "street"
        },
        "target": {
          "table": "Addresses",
          "column": "line1"
        },
        "transform": {
          "type": "string_normalize",
          "params": {}
        },
        "confidence": 0.95,
        "rationale": "Mapping street address to address line 1. Requires moving to a new normalized table.",
        "status": "suggested"
      },
      {
        "id": "M012_ADDRESS_CITY",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "addressCity"
        },
        "target": {
          "table": "Addresses",
          "column": "city"
        },
        "transform": {
          "type": "string_normalize",
          "params": {
            "case": "title"
          }
        },
        "confidence": 1.0,
        "rationale": "Direct city mapping to normalized table.",
        "status": "suggested"
      },
      {
        "id": "M013_ADDRESS_STATE",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "state"
        },
        "target": {
          "table": "Addresses",
          "column": "region"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 0.9,
        "rationale": "Mapping state/province to the more generic 'region' field in the normalized table.",
        "status": "suggested"
      },
      {
        "id": "M014_ADDRESS_COUNTRY",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "country"
        },
        "target": {
          "table": "Addresses",
          "column": "country"
        },
        "transform": {
          "type": "string_normalize",
          "params": {
            "rule": "Convert to ISO 3166-1 alpha-3 code"
          }
        },
        "confidence": 0.9,
        "rationale": "Direct country mapping to normalized table. Requires ISO code standardization.",
        "status": "suggested"
      },
      {
        "id": "M015_ADDRESS_POSTCODE",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "postCode"
        },
        "target": {
          "table": "Addresses",
          "column": "postcode"
        },
        "transform": {
          "type": "string_normalize",
          "params": {}
        },
        "confidence": 0.95,
        "rationale": "Direct postal code mapping to normalized table.",
        "status": "suggested"
      },
      {
        "id": "M016_IDENTIFICATION_ID",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "legalId"
        },
        "target": {
          "table": "Identifications",
          "column": "documentId"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 0.95,
        "rationale": "Mapping unique legal ID to documentId. Requires moving to a normalized table.",
        "status": "suggested"
      },
      {
        "id": "M017_IDENTIFICATION_TYPE",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "legalDocumentName"
        },
        "target": {
          "table": "Identifications",
          "column": "documentType"
        },
        "transform": {
          "type": "string_normalize",
          "params": {
            "rule": "Map to B's document types"
          }
        },
        "confidence": 0.9,
        "rationale": "Mapping document name to document type, needs value mapping.",
        "status": "suggested"
      },
      {
        "id": "M018_IDENTIFICATION_AUTHORITY",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "legalIssueAuthorised"
        },
        "target": {
          "table": "Identifications",
          "column": "issuingAuthority"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 0.9,
        "rationale": "Mapping issuing authority.",
        "status": "suggested"
      },
      {
        "id": "M019_IDENTIFICATION_COUNTRY",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "legalIssueCountry"
        },
        "target": {
          "table": "Identifications",
          "column": "issuingCountry"
        },
        "transform": {
          "type": "string_normalize",
          "params": {
            "rule": "Convert to ISO 3166-1 alpha-3 code"
          }
        },
        "confidence": 0.9,
        "rationale": "Mapping issuing country, requires ISO code standardization.",
        "status": "suggested"
      },
      {
        "id": "M020_IDENTIFICATION_ISSUE_DATE",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "legalIssueDate"
        },
        "target": {
          "table": "Identifications",
          "column": "issuingDate"
        },
        "transform": {
          "type": "parse_date",
          "params": {
            "format": "YYYY-MM-DD"
          }
        },
        "confidence": 0.95,
        "rationale": "Mapping issue date with date parsing.",
        "status": "suggested"
      },
      {
        "id": "M021_IDENTIFICATION_EXPIRY_DATE",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "legalExpiredDate"
        },
        "target": {
          "table": "Identifications",
          "column": "validUntil"
        },
        "transform": {
          "type": "parse_date",
          "params": {
            "format": "YYYY-MM-DD"
          }
        },
        "confidence": 0.95,
        "rationale": "Mapping expiry date with date parsing.",
        "status": "suggested"
      },
      {
        "id": "M022_ACCOUNT_CURSAV_ID",
        "domain": "accounts",
        "source": {
          "table": "CurSav Accounts",
          "column": "accountId"
        },
        "target": {
          "table": "Deposit Accounts",
          "column": "id"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 1.0,
        "rationale": "Direct account ID mapping.",
        "status": "suggested"
      },
      {
        "id": "M023_ACCOUNT_FIXEDTERM_ID",
        "domain": "accounts",
        "source": {
          "table": "Fixed Term Accounts",
          "column": "accountId"
        },
        "target": {
          "table": "Deposit Accounts",
          "column": "id"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 1.0,
        "rationale": "Direct account ID mapping for Fixed Term into Deposit Accounts.",
        "status": "suggested"
      },
      {
        "id": "M024_ACCOUNT_CURSAV_NAME",
        "domain": "accounts",
        "source": {
          "table": "CurSav Accounts",
          "column": "displayName"
        },
        "target": {
          "table": "Deposit Accounts",
          "column": "name"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 0.9,
        "rationale": "Mapping account display name to Deposit Accounts name.",
        "status": "suggested"
      },
      {
        "id": "M025_ACCOUNT_FIXEDTERM_NAME",
        "domain": "accounts",
        "source": {
          "table": "Fixed Term Accounts",
          "column": "accountTitles"
        },
        "target": {
          "table": "Deposit Accounts",
          "column": "name"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 0.85,
        "rationale": "Mapping short title to Deposit Accounts name. CurSav takes precedence if both exist for an account.",
        "status": "suggested"
      },
      {
        "id": "M026_ACCOUNT_LOAN_ID",
        "domain": "accounts",
        "source": {
          "table": "Loan Accounts",
          "column": "accountId"
        },
        "target": {
          "table": "Loan Accounts",
          "column": "id"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 1.0,
        "rationale": "Direct account ID mapping for Loan Accounts.",
        "status": "suggested"
      },
      {
        "id": "M027_ACCOUNT_LOAN_NAME",
        "domain": "accounts",
        "source": {
          "table": "Loan Accounts",
          "column": "accountName"
        },
        "target": {
          "table": "Loan Accounts",
          "column": "loanName"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 0.9,
        "rationale": "Direct account name mapping for Loan Accounts.",
        "status": "suggested"
      },
      {
        "id": "M028_ACCOUNT_CURSAV_BALANCE_AVAIL",
        "domain": "accounts",
        "source": {
          "table": "CurSav Accounts",
          "column": "availableBalance"
        },
        "target": {
          "table": "Deposit Accounts",
          "column": "availableBalance"
        },
        "transform": {
          "type": "cast",
          "params": {
            "type": "float"
          }
        },
        "confidence": 1.0,
        "rationale": "Mapping available balance, ensuring data type is float/numeric.",
        "status": "suggested"
      },
      {
        "id": "M029_ACCOUNT_CURSAV_BALANCE_TOTAL",
        "domain": "accounts",
        "source": {
          "table": "CurSav Accounts",
          "column": "onlineActualBalance"
        },
        "target": {
          "table": "Deposit Accounts",
          "column": "totalBalance"
        },
        "transform": {
          "type": "cast",
          "params": {
            "type": "float"
          }
        },
        "confidence": 0.95,
        "rationale": "Mapping online actual balance to total balance, ensuring data type is float/numeric.",
        "status": "suggested"
      },
      {
        "id": "M030_ACCOUNT_FIXEDTERM_BALANCE_TOTAL",
        "domain": "accounts",
        "source": {
          "table": "Fixed Term Accounts",
          "column": "currentBalance"
        },
        "target": {
          "table": "Deposit Accounts",
          "column": "totalBalance"
        },
        "transform": {
          "type": "cast",
          "params": {
            "type": "float"
          }
        },
        "confidence": 0.9,
        "rationale": "Mapping current balance to total balance for Fixed Term, assuming it's the total principal+interest.",
        "status": "suggested"
      },
      {
        "id": "M031_ACCOUNT_LOAN_PRINCIPAL_BALANCE",
        "domain": "accounts",
        "source": {
          "table": "Loan Accounts",
          "column": "principalBalance"
        },
        "target": {
          "table": "Loan Accounts",
          "column": "principalBalance"
        },
        "transform": {
          "type": "cast",
          "params": {
            "type": "float"
          }
        },
        "confidence": 1.0,
        "rationale": "Direct mapping of loan principal balance.",
        "status": "suggested"
      },
      {
        "id": "M032_ACCOUNT_LOAN_TOTAL_BALANCE",
        "domain": "accounts",
        "source": {
          "table": "Loan Accounts",
          "column": "loanBalance"
        },
        "target": {
          "table": "Loan Accounts",
          "column": "totalBalance"
        },
        "transform": {
          "type": "cast",
          "params": {
            "type": "float"
          }
        },
        "confidence": 0.9,
        "rationale": "Mapping outstanding loan balance to total balance (what's owed).",
        "status": "suggested"
      },
      {
        "id": "M033_ACCOUNT_FIXEDTERM_ACCRUED_INTEREST",
        "domain": "accounts",
        "source": {
          "table": "Fixed Term Accounts",
          "column": "accruedInterest"
        },
        "target": {
          "table": "Deposit Accounts",
          "column": "interestAccrued"
        },
        "transform": {
          "type": "cast",
          "params": {
            "type": "float"
          }
        },
        "confidence": 0.95,
        "rationale": "Mapping accrued interest to target's interestAccrued.",
        "status": "suggested"
      },
      {
        "id": "M034_ACCOUNT_LOAN_INTEREST_RATE",
        "domain": "accounts",
        "source": {
          "table": "Loan Accounts",
          "column": "loanInterestRate"
        },
        "target": {
          "table": "Loan Accounts",
          "column": "interestRate"
        },
        "transform": {
          "type": "cast",
          "params": {
            "type": "float"
          }
        },
        "confidence": 0.95,
        "rationale": "Mapping loan interest rate.",
        "status": "suggested"
      },
      {
        "id": "M035_ACCOUNT_LOAN_EFFECTIVE_RATE",
        "domain": "accounts",
        "source": {
          "table": "Loan Accounts",
          "column": "effectiveRate"
        },
        "target": {
          "table": "Loan Accounts",
          "column": "effectiveInterestRate"
        },
        "transform": {
          "type": "cast",
          "params": {
            "type": "float"
          }
        },
        "confidence": 0.95,
        "rationale": "Mapping effective rate to effective interest rate.",
        "status": "suggested"
      },
      {
        "id": "M036_ACCOUNT_LOAN_GRACE_PERIOD",
        "domain": "accounts",
        "source": {
          "table": "Loan Accounts",
          "column": "gracePeriod"
        },
        "target": {
          "table": "Loan Accounts",
          "column": "gracePeriod"
        },
        "transform": {
          "type": "cast",
          "params": {
            "type": "integer"
          }
        },
        "confidence": 1.0,
        "rationale": "Direct mapping of grace period.",
        "status": "suggested"
      },
      {
        "id": "M037_ACCOUNT_LOAN_PAYMENT_PERIODIC",
        "domain": "accounts",
        "source": {
          "table": "Loan Accounts",
          "column": "periodicPayment"
        },
        "target": {
          "table": "Loan Accounts",
          "column": "periodicPayment"
        },
        "transform": {
          "type": "cast",
          "params": {
            "type": "float"
          }
        },
        "confidence": 1.0,
        "rationale": "Direct mapping of periodic payment.",
        "status": "suggested"
      },
      {
        "id": "M038_ACCOUNT_LOAN_FIXED_DAYS_OF_MONTH",
        "domain": "accounts",
        "source": {
          "table": "Loan Accounts",
          "column": "fixedDaysOfMonth"
        },
        "target": {
          "table": "Loan Accounts",
          "column": "fixedDaysOfMonth"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 1.0,
        "rationale": "Direct mapping of fixed days of month for payment.",
        "status": "suggested"
      },
      {
        "id": "M039_TRANSACTION_CURSAV_REF",
        "domain": "transactions",
        "source": {
          "table": "CurSav Account Transactions",
          "column": "transactionReference"
        },
        "target": {
          "table": "Transactions_Unified",
          "column": "transactionReference"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 1.0,
        "rationale": "Unique transaction ID is key for unification.",
        "status": "suggested"
      },
      {
        "id": "M040_TRANSACTION_FIXEDTERM_REF",
        "domain": "transactions",
        "source": {
          "table": "Fixed Term Account Transactions",
          "column": "transactionReference"
        },
        "target": {
          "table": "Transactions_Unified",
          "column": "transactionReference"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 1.0,
        "rationale": "Unique transaction ID is key for unification.",
        "status": "suggested"
      },
      {
        "id": "M041_TRANSACTION_LOAN_REF",
        "domain": "transactions",
        "source": {
          "table": "Loan Account Transactions",
          "column": "transactionReference"
        },
        "target": {
          "table": "Transactions_Unified",
          "column": "transactionReference"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 1.0,
        "rationale": "Unique transaction ID is key for unification.",
        "status": "suggested"
      },
      {
        "id": "M042_TRANSACTION_AMOUNT",
        "domain": "transactions",
        "source": {
          "table": "CurSav Account Transactions",
          "column": "transactionAmount"
        },
        "target": {
          "table": "Transactions_Unified",
          "column": "amount"
        },
        "transform": {
          "type": "cast",
          "params": {
            "type": "float"
          }
        },
        "confidence": 1.0,
        "rationale": "Mapping transaction amount to unified column. Requires type cast.",
        "status": "suggested"
      },
      {
        "id": "M043_TRANSACTION_DATE",
        "domain": "transactions",
        "source": {
          "table": "CurSav Account Transactions",
          "column": "transactionDate"
        },
        "target": {
          "table": "Transactions_Unified",
          "column": "transactionDate"
        },
        "transform": {
          "type": "parse_date",
          "params": {}
        },
        "confidence": 1.0,
        "rationale": "Mapping transaction date to unified column. Requires date parsing.",
        "status": "suggested"
      },
      {
        "id": "M044_TRANSACTION_ACTIVITY",
        "domain": "transactions",
        "source": {
          "table": "CurSav Account Transactions",
          "column": "activity"
        },
        "target": {
          "table": "Transactions_Unified",
          "column": "activityType"
        },
        "transform": {
          "type": "string_normalize",
          "params": {
            "rule": "Map to common activity types (e.g., DEBIT, CREDIT)"
          }
        },
        "confidence": 0.9,
        "rationale": "Mapping activity to unified column, requiring value standardization.",
        "status": "suggested"
      },
      {
        "id": "M045_ACCOUNT_CUSTOMER_STATUS_STRAY",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "customerStatus"
        },
        "target": {
          "table": "Customer",
          "column": "internal_status"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 0.9,
        "rationale": "Internal status is critical but doesn't map directly to a target column. Extend Customer table for no-data-loss.",
        "status": "suggested",
        "extra_field_handling": {
          "action": "preserve",
          "method": "extend_table",
          "target_table": "Customer",
          "link_key": "id",
          "reason": "Only a few stray fields for Customer; retain by extending the main table."
        }
      },
      {
        "id": "M046_ACCOUNT_OFFICER_STRAY",
        "domain": "customers",
        "source": {
          "table": "Customer",
          "column": "accountOfficerId"
        },
        "target": {
          "table": "Customer",
          "column": "account_officer_id"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 0.8,
        "rationale": "Officer ID is likely a key that needs a lookup, but preserved here as a raw ID.",
        "status": "suggested",
        "extra_field_handling": {
          "action": "preserve",
          "method": "extend_table",
          "target_table": "Customer",
          "link_key": "id",
          "reason": "Only a few stray fields for Customer; retain by extending the main table."
        }
      },
      {
        "id": "M047_LOAN_EXTRAS_STRAY",
        "domain": "accounts",
        "source": {
          "table": "Loan Accounts",
          "column": "compoundType"
        },
        "target": {
          "table": "Loan_Extras",
          "column": "compoundType"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 0.8,
        "rationale": "Loan accounts have many specific fields with no target mapping (compoundType, numberPayments, paymentFrequency, amortisationTerm, etc.). Move all to an extras table.",
        "status": "suggested",
        "extra_field_handling": {
          "action": "preserve",
          "method": "extras_table",
          "target_table": "Loan_Extras",
          "link_key": "accountId",
          "reason": "More than 10 unmatched fields for Loan Accounts. Moving to a dedicated extras table to maintain normalized schema in the core Loan Accounts table."
        }
      },
      {
        "id": "M048_LOAN_EXTRAS_STRAY_PAYMENT_FREQUENCY",
        "domain": "accounts",
        "source": {
          "table": "Loan Accounts",
          "column": "paymentFrequency"
        },
        "target": {
          "table": "Loan_Extras",
          "column": "paymentFrequency"
        },
        "transform": {
          "type": "identity",
          "params": {}
        },
        "confidence": 0.8,
        "rationale": "Part of the many Loan extras.",
        "status": "suggested",
        "extra_field_handling": {
          "action": "preserve",
          "method": "extras_table",
          "target_table": "Loan_Extras",
          "link_key": "accountId",
          "reason": "Part of the many Loan extras. Moving to dedicated table."
        }
      }
    ],
    "key_strategies": [
      {
        "domain": "customers",
        "primary_keys": [
          {
            "table": "Customer",
            "columns": [
              "customerId"
            ]
          },
          {
            "table": "Customer",
            "columns": [
              "id"
            ]
          }
        ],
        "join_keys": [
          {
            "source": {
              "table": "Customer",
              "columns": [
                "customerId"
              ]
            },
            "target": {
              "table": "Customer",
              "columns": [
                "id"
              ]
            }
          }
        ],
        "fallback_match": [
          {
            "source": [
              "givenName",
              "lastName",
              "dateOfBirth"
            ],
            "target": [
              "firstName",
              "lastName",
              "birthDate"
            ],
            "strategy": "fuzzy"
          }
        ]
      },
      {
        "domain": "accounts",
        "primary_keys": [
          {
            "table": "CurSav Accounts",
            "columns": [
              "accountId"
            ]
          },
          {
            "table": "Fixed Term Accounts",
            "columns": [
              "accountId"
            ]
          },
          {
            "table": "Loan Accounts",
            "columns": [
              "accountId"
            ]
          }
        ],
        "join_keys": [
          {
            "source": {
              "table": "CurSav Accounts",
              "columns": [
                "accountId"
              ]
            },
            "target": {
              "table": "Deposit Accounts",
              "columns": [
                "id"
              ]
            }
          },
          {
            "source": {
              "table": "Fixed Term Accounts",
              "columns": [
                "accountId"
              ]
            },
            "target": {
              "table": "Deposit Accounts",
              "columns": [
                "id"
              ]
            }
          }
        ],
        "fallback_match": []
      }
    ],
    "output_plans": [
      {
        "output_table": "Customer",
        "join": {
          "type": "full_outer",
          "left": {
            "table": "A.Customer",
            "on": [
              "customerId"
            ]
          },
          "right": {
            "table": "B.Customer",
            "on": [
              "id"
            ]
          },
          "fallback_on": []
        },
        "dedupe": {
          "keys": [
            "id",
            "customerId"
          ],
          "strategy": "prefer_right_non_null",
          "tie_breaker": "creationDate"
        },
        "use_mappings": [
          "M001_CUSTOMER_ID",
          "M002_CUSTOMER_FIRSTNAME",
          "M003_CUSTOMER_LASTNAME",
          "M004_CUSTOMER_DOB",
          "M005_CUSTOMER_EMAIL",
          "M006_CUSTOMER_PHONE_MOBILE",
          "M007_CUSTOMER_PHONE_HOME_STRAY",
          "M008_CUSTOMER_LANGUAGE",
          "M009_CUSTOMER_GENDER",
          "M010_CUSTOMER_TYPE",
          "M045_ACCOUNT_CUSTOMER_STATUS_STRAY",
          "M046_ACCOUNT_OFFICER_STRAY"
        ]
      },
      {
        "output_table": "Deposit Accounts",
        "join": {
          "type": "full_outer",
          "left": {
            "table": "A.CurSav Accounts",
            "on": [
              "accountId"
            ]
          },
          "right": {
            "table": "B.Deposit Accounts",
            "on": [
              "id"
            ]
          },
          "fallback_on": []
        },
        "dedupe": {
          "keys": [
            "id"
          ],
          "strategy": "prefer_right_non_null",
          "tie_breaker": "creationDate"
        },
        "use_mappings": [
          "M022_ACCOUNT_CURSAV_ID",
          "M023_ACCOUNT_FIXEDTERM_ID",
          "M024_ACCOUNT_CURSAV_NAME",
          "M025_ACCOUNT_FIXEDTERM_NAME",
          "M028_ACCOUNT_CURSAV_BALANCE_AVAIL",
          "M029_ACCOUNT_CURSAV_BALANCE_TOTAL",
          "M030_ACCOUNT_FIXEDTERM_BALANCE_TOTAL",
          "M033_ACCOUNT_FIXEDTERM_ACCRUED_INTEREST"
        ]
      },
      {
        "output_table": "Loan Accounts",
        "join": {
          "type": "full_outer",
          "left": {
            "table": "A.Loan Accounts",
            "on": [
              "accountId"
            ]
          },
          "right": {
            "table": "B.Loan Accounts",
            "on": [
              "id"
            ]
          },
          "fallback_on": []
        },
        "dedupe": {
          "keys": [
            "id"
          ],
          "strategy": "prefer_right_non_null",
          "tie_breaker": "creationDate"
        },
        "use_mappings": [
          "M026_ACCOUNT_LOAN_ID",
          "M027_ACCOUNT_LOAN_NAME",
          "M031_ACCOUNT_LOAN_PRINCIPAL_BALANCE",
          "M032_ACCOUNT_LOAN_TOTAL_BALANCE",
          "M034_ACCOUNT_LOAN_INTEREST_RATE",
          "M035_ACCOUNT_LOAN_EFFECTIVE_RATE",
          "M036_ACCOUNT_LOAN_GRACE_PERIOD",
          "M037_ACCOUNT_LOAN_PAYMENT_PERIODIC",
          "M038_ACCOUNT_LOAN_FIXED_DAYS_OF_MONTH"
        ]
      }
    ],
    "applied_transformations": [
      {
        "id": "M002_CUSTOMER_FIRSTNAME",
        "table": "Customer",
        "column": "firstName",
        "transform": "string_normalize",
        "description": "Applies title case normalization to givenName."
      },
      {
        "id": "M003_CUSTOMER_LASTNAME",
        "table": "Customer",
        "column": "lastName",
        "transform": "string_normalize",
        "description": "Applies title case normalization to lastName."
      },
      {
        "id": "M004_CUSTOMER_DOB",
        "table": "Customer",
        "column": "birthDate",
        "transform": "parse_date",
        "description": "Converts dateOfBirth to standard date format."
      },
      {
        "id": "M005_CUSTOMER_EMAIL",
        "table": "Customer",
        "column": "emailAddress",
        "transform": "string_normalize",
        "description": "Converts email to lowercase."
      },
      {
        "id": "M006_CUSTOMER_PHONE_MOBILE",
        "table": "Customer",
        "column": "mobilePhone",
        "transform": "custom",
        "description": "Cleanses and standardizes phone number format for mobilePhone."
      },
      {
        "id": "M007_CUSTOMER_PHONE_HOME_STRAY",
        "table": "Customer",
        "column": "homePhone",
        "transform": "custom",
        "description": "Cleanses and standardizes phone number format for homePhone."
      },
      {
        "id": "M009_CUSTOMER_GENDER",
        "table": "Customer",
        "column": "gender",
        "transform": "string_normalize",
        "description": "Maps gender values to target's allowed enumeration."
      },
      {
        "id": "M014_ADDRESS_COUNTRY",
        "table": "Addresses",
        "column": "country",
        "transform": "string_normalize",
        "description": "Converts country value to ISO 3166-1 alpha-3 code."
      },
      {
        "id": "M019_IDENTIFICATION_COUNTRY",
        "table": "Identifications",
        "column": "issuingCountry",
        "transform": "string_normalize",
        "description": "Converts legal issue country to ISO 3166-1 alpha-3 code."
      },
      {
        "id": "M020_IDENTIFICATION_ISSUE_DATE",
        "table": "Identifications",
        "column": "issuingDate",
        "transform": "parse_date",
        "description": "Converts legal issue date to standard date format."
      },
      {
        "id": "M021_IDENTIFICATION_EXPIRY_DATE",
        "table": "Identifications",
        "column": "validUntil",
        "transform": "parse_date",
        "description": "Converts legal expired date to standard date format."
      },
      {
        "id": "M028_ACCOUNT_CURSAV_BALANCE_AVAIL",
        "table": "Deposit Accounts",
        "column": "availableBalance",
        "transform": "cast",
        "description": "Casts availableBalance to float/numeric type."
      },
      {
        "id": "M029_ACCOUNT_CURSAV_BALANCE_TOTAL",
        "table": "Deposit Accounts",
        "column": "totalBalance",
        "transform": "cast",
        "description": "Casts onlineActualBalance to float/numeric type."
      },
      {
        "id": "M030_ACCOUNT_FIXEDTERM_BALANCE_TOTAL",
        "table": "Deposit Accounts",
        "column": "totalBalance",
        "transform": "cast",
        "description": "Casts currentBalance to float/numeric type."
      },
      {
        "id": "M031_ACCOUNT_LOAN_PRINCIPAL_BALANCE",
        "table": "Loan Accounts",
        "column": "principalBalance",
        "transform": "cast",
        "description": "Casts principalBalance to float/numeric type."
      },
      {
        "id": "M032_ACCOUNT_LOAN_TOTAL_BALANCE",
        "table": "Loan Accounts",
        "column": "totalBalance",
        "transform": "cast",
        "description": "Casts loanBalance to float/numeric type."
      },
      {
        "id": "M033_ACCOUNT_FIXEDTERM_ACCRUED_INTEREST",
        "table": "Deposit Accounts",
        "column": "interestAccrued",
        "transform": "cast",
        "description": "Casts accruedInterest to float/numeric type."
      },
      {
        "id": "M034_ACCOUNT_LOAN_INTEREST_RATE",
        "table": "Loan Accounts",
        "column": "interestRate",
        "transform": "cast",
        "description": "Casts loanInterestRate to float/numeric type."
      },
      {
        "id": "M035_ACCOUNT_LOAN_EFFECTIVE_RATE",
        "table": "Loan Accounts",
        "column": "effectiveInterestRate",
        "transform": "cast",
        "description": "Casts effectiveRate to float/numeric type."
      },
      {
        "id": "M036_ACCOUNT_LOAN_GRACE_PERIOD",
        "table": "Loan Accounts",
        "column": "gracePeriod",
        "transform": "cast",
        "description": "Casts gracePeriod to integer type."
      },
      {
        "id": "M037_ACCOUNT_LOAN_PAYMENT_PERIODIC",
        "table": "Loan Accounts",
        "column": "periodicPayment",
        "transform": "cast",
        "description": "Casts periodicPayment to float/numeric type."
      },
      {
        "id": "M042_TRANSACTION_AMOUNT",
        "table": "Transactions_Unified",
        "column": "amount",
        "transform": "cast",
        "description": "Casts transactionAmount to float/numeric type."
      },
      {
        "id": "M043_TRANSACTION_DATE",
        "table": "Transactions_Unified",
        "column": "transactionDate",
        "transform": "parse_date",
        "description": "Parses transactionDate to standard date format."
      },
      {
        "id": "M044_TRANSACTION_ACTIVITY",
        "table": "Transactions_Unified",
        "column": "activityType",
        "transform": "string_normalize",
        "description": "Standardizes activity values (e.g., CREDIT, DEBIT)."
      }
    ],
    "documentation": {
      "change_log": [
        {
          "mapping_id": "M001_CUSTOMER_ID",
          "description": "Established primary key mapping for Customer entity.",
          "reason": "Required for customer-centric reporting and subsequent joins.",
          "timestamp": "2025-10-05T07:37:09Z"
        },
        {
          "mapping_id": "M047_LOAN_EXTRAS_STRAY",
          "description": "Created Loan_Extras table to preserve all unmapped Loan Account fields.",
          "reason": "Adhering to No Data Loss Policy (Hybrid Method) for entities with high number of stray fields.",
          "timestamp": "2025-10-05T07:37:09Z"
        }
      ],
      "review": {
        "status": "pending",
        "notes": "Confirm logic for generating B.Customer.encodedKey from A.customerId, and confirm business value mapping for gender, customerType, and transaction activity fields. A full_outer join for transactions is necessary to retain all A and B transaction records, requiring a robust deduplication strategy not fully defined here."
      }
    }
  }
