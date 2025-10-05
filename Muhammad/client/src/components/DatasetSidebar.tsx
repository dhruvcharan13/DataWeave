"use client";

import React, { useState, useRef, useEffect } from "react";
import {
  Drawer,
  List,
  ListItemButton,
  ListItemText,
  Collapse,
  Typography,
  Box,
} from "@mui/material";
import {
  ExpandLess,
  ExpandMore,
  Storage,
  TableChartOutlined,
} from "@mui/icons-material";

/* ---------- Full hardcoded schema for Bank1 & Bank2 ---------- */
const sampleSchemas = {
  Bank1: {
    tables: [
      {
        name: "Bank1_Mock_Customer",
        columns: [
          "phoneNumber", "smsNumber", "email", "street", "addressCity", "country",
          "legalId", "legalDocumentName", "legalIssueAuthorised", "legalIssueCountry",
          "legalIssueDate", "legalExpiredDate", "language", "dateOfBirth",
          "customerStatus", "accountOfficerId", "gender", "state", "postCode",
          "contactDate", "lastName", "givenName", "customerType", "customerId"
        ],
      },
      {
        name: "Bank1_Mock_CurSav_Accounts",
        columns: [
          "accountId", "displayName", "customerId", "customerRole", "productId", "status",
          "currency", "branch", "accountOpeningDate", "arrangementStartDate",
          "availableBalance", "onlineActualBalance", "lockedAmount", "availableLimit",
          "productDescription", "category"
        ],
      },
      {
        name: "Bank1_Mock_CurSav_Transactions",
        columns: [
          "transactionReference", "activity", "transactionAmount", "currency",
          "effectiveDate", "transactionDate", "bookingDate", "narrative",
          "externalEventStatus", "userRole", "branch", "accountId",
          "chargesPaymentTypeName", "chargesPropertyName", "chargesChargeAmount",
          "taxRate", "availableBalance", "lockedAmount", "approvedOverdraftLimit",
          "accrualAmount", "effectiveRate", "availableOverdraftLimit", "channel"
        ],
      },
      {
        name: "Bank1_Mock_FixedTerm_Accounts",
        columns: [
          "accountId", "accountTitles", "productId", "currency", "customerId",
          "customerRole", "branch", "reason", "maturityDate",
          "arrangementEffectiveDate", "expiryDate", "agentCustomerId",
          "expectedBalance", "currentBalance", "accruedInterest", "jointCustomerName",
          "category", "interestRate", "interestStatement", "status"
        ],
      },
      {
        name: "Bank1_Mock_FixedTerm_Transactions",
        columns: [
          "transactionReference", "activity", "transactionAmount", "currency",
          "effectiveDate", "transactionDate", "reason", "externalEventStatus",
          "userRole", "branch", "chargesChargeAmount", "interestAmount", "taxRate",
          "currentBalance", "interestRate", "channel", "accountId"
        ],
      },
      {
        name: "Bank1_Mock_Loan_Accounts",
        columns: [
          "accountId", "accountName", "productId", "currency", "customerId",
          "customerRole", "branch", "reason", "maturityDate",
          "arrangementEffectiveDate", "expiryDate", "agentCustomerIds",
          "loanBalance", "availableBalance", "loanInterestRate", "loanInterestType",
          "compoundType", "effectiveRate", "gracePeriod", "periodicPayment",
          "numberPayments", "paymentFrequency", "fixedDaysOfMonth", "amortisationTerm",
          "principalAmount", "principalBalance", "interestAmount", "chargeAmount",
          "interestBalance", "interestFromArrearsBalance", "accountType"
        ],
      },
      {
        name: "Bank1_Mock_Loan_Transactions",
        columns: [
          "transactionReference", "activity", "transactionAmount", "currency",
          "effectiveDate", "reason", "externalEventStatus", "userRole", "branch",
          "principalAmount", "interestAmount", "chargeAmount", "balanceAmount",
          "interestRate", "channelName", "accountId"
        ],
      },
    ],
  },

  Bank2: {
    tables: [
      {
        name: "Bank2_Mock_Customer",
        columns: [
          "lastName", "migrationEventKey", "preferredLanguage", "notes",
          "gender", "emailAddress", "encodedKey", "id", "state",
          "assignedUserKey", "homePhone", "creationDate", "birthDate",
          "firstName", "mobilePhone", "clientType"
        ],
      },
      {
        name: "Bank2_Mock_Addresses",
        columns: [
          "city", "country", "encodedKey", "line1", "parentKey", "postcode", "region"
        ],
      },
      {
        name: "Bank2_Mock_Deposit_Accounts",
        columns: [
          "encodedKey", "id", "name", "productTypeKey", "currencyCode", "accountHolderKey",
          "accountHolderType", "assignedBranchKey", "notes", "maturityDate",
          "creationDate", "closedDate", "assignedUserKey", "totalBalance",
          "availableBalance", "interestAccrued", "ownershipHistory", "accountType",
          "interestRate", "interestPaymentPoint", "status", "accountState",
          "lockedBalance", "overdraftAmount", "productDescription"
        ],
      },
      {
        name: "Bank2_Mock_Deposit_Transactions",
        columns: [
          "id", "encodedKey", "type", "amount", "currencyCode", "creationDate",
          "valueDate", "notes", "externalId", "userKey", "branchKey", "interestRate",
          "transactionChannel", "parentAccountKey", "feesAmount", "interestAmount",
          "taxRate", "totalBalance", "bookingDate", "feesPredefinedFee", "feesName",
          "availableBalance", "lockedBalance", "overdraftAmount", "interestBalance",
          "overdraftLimit"
        ],
      },
      {
        name: "Bank2_Mock_Identifications",
        columns: [
          "clientKey", "documentId", "documentType", "encodedKey", "issuingAuthority",
          "issuingCountry", "issuingDate", "validUntil"
        ],
      },
      {
        name: "Bank2_Mock_Loan_Accounts",
        columns: [
          "id", "loanName", "productTypeKey", "currencyCode", "accountHolderKey",
          "accountHolderType", "assignedBranchKey", "notes", "maturityDate",
          "creationDate", "closedDate", "assignedUserKey", "totalBalance",
          "availableBalance", "interestRate", "interestType", "interestApplicationMethod",
          "effectiveInterestRate", "gracePeriod", "periodicPayment",
          "repaymentInstallments", "repaymentPeriodUnit", "fixedDaysOfMonth",
          "repaymentPeriodCount", "amortizationPeriod", "principalDue",
          "principalBalance", "interestDue", "feesDue", "interestBalance",
          "interestFromArrearsBalance", "interestAccrued", "accountType"
        ],
      },
      {
        name: "Bank2_Mock_Loan_Transactions",
        columns: [
          "encodedKey", "id", "type", "amount", "originalCurrencyCode", "valueDate",
          "notes", "externalId", "userKey", "branchKey", "principalAmount",
          "interestAmount", "feesAmount", "totalBalance", "principalBalance",
          "interestRate", "transactionChannel", "parentAccountKey"
        ],
      },
    ],
  },
};

interface SidebarProps {
  selected: string;
  onSelect: (dataset: string) => void;
}

export default function DatasetSidebar({ selected, onSelect }: SidebarProps) {
  const [expandedBanks, setExpandedBanks] = useState<{ [key: string]: boolean }>({});
  const [expandedTables, setExpandedTables] = useState<{ [key: string]: boolean }>({});
  const [sidebarWidth, setSidebarWidth] = useState(280);
  const [isResizing, setIsResizing] = useState(false);
  const [schemas, setSchemas] = useState<any>({});

  const toggleBankExpand = (bank: string) => {
    setExpandedBanks((prev) => ({ ...prev, [bank]: !prev[bank] }));
  };
  const toggleTableExpand = (table: string) => {
    setExpandedTables((prev) => ({ ...prev, [table]: !prev[table] }));
  };

  const startResize = () => {
    setIsResizing(true);
    document.body.style.cursor = "col-resize";
  };
  const stopResize = () => {
    setIsResizing(false);
    document.body.style.cursor = "default";
  };
  const resize = (e: MouseEvent) => {
    if (!isResizing) return;
    const newWidth = e.clientX;
    if (newWidth > 220 && newWidth < 600) setSidebarWidth(newWidth);
  };

  useEffect(() => {
    window.addEventListener("mousemove", resize);
    window.addEventListener("mouseup", stopResize);
    return () => {
      window.removeEventListener("mousemove", resize);
      window.removeEventListener("mouseup", stopResize);
    };
  });

  useEffect(() => {
    const stored = localStorage.getItem("schemaAnalysis");
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
  
        const formatted: any = {};
        [parsed.source, parsed.target].forEach((db: any) => {
          if (!db?.database || !db?.tables) return;
  
          formatted[db.database] = {
            tables: db.tables.map((table: any) => ({
              name: table.name,
              columns: Array.isArray(table.columns)
                ? table.columns
                : Object.keys(table.columns || {}),
            })),
          };
        });
  
        setSchemas(formatted);
      } catch (err) {
        console.error("Failed to parse schemaAnalysis:", err);
      }
    }
  }, []);
  

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: sidebarWidth,
        flexShrink: 0,
        "& .MuiDrawer-paper": {
          width: sidebarWidth,
          boxSizing: "border-box",
          bgcolor: "background.paper",
          borderRight: "1px solid",
          borderColor: "divider",
          position: "absolute",
        },
      }}
    >
      <Box sx={{ p: 2 }}>
        <Box display="flex" alignItems="center" gap={1} mb={2}>
          <Storage color="primary" />
          <Typography variant="h6" fontWeight={600}>
            Datasets
          </Typography>
        </Box>

        <List dense disablePadding>
          {/* {Object.keys(sampleSchemas).map((bank) => ( */}
          {Object.keys(schemas).map((bank) => (
            <React.Fragment key={bank}>
              <ListItemButton
                selected={selected === bank}
                onClick={() => {
                  onSelect(bank);
                  toggleBankExpand(bank);
                }}
              >
                <ListItemText
                  primary={bank}
                  primaryTypographyProps={{ fontWeight: 600, fontSize: "0.95rem" }}
                />
                {expandedBanks[bank] ? <ExpandLess /> : <ExpandMore />}
              </ListItemButton>

              <Collapse in={expandedBanks[bank]} timeout="auto" unmountOnExit>
                <List component="div" disablePadding sx={{ pl: 2 }}>
                  {/* {sampleSchemas[bank].tables.map((table) => ( */}
                  {schemas[bank]?.tables?.map((table: any) => (  
                    <React.Fragment key={table.name}>
                      <ListItemButton
                        onClick={() => toggleTableExpand(table.name)}
                        sx={{ pl: 2, py: 0.8 }}
                      >
                        <TableChartOutlined
                          fontSize="small"
                          sx={{ mr: 1, color: "text.secondary" }}
                        />
                        <ListItemText
                          primary={table.name}
                          primaryTypographyProps={{
                            fontSize: 13,
                            color: "text.secondary",
                            fontWeight: 500,
                          }}
                        />
                        {expandedTables[table.name] ? (
                          <ExpandLess fontSize="small" />
                        ) : (
                          <ExpandMore fontSize="small" />
                        )}
                      </ListItemButton>

                      <Collapse in={expandedTables[table.name]} timeout="auto" unmountOnExit>
                        <List component="div" disablePadding sx={{ pl: 4 }}>
                          {table.columns.map((col) => (
                            <ListItemButton key={col} disableRipple>
                              <ListItemText
                                primary={col}
                                primaryTypographyProps={{
                                  fontSize: 12,
                                  color: "text.disabled",
                                  fontFamily: "monospace",
                                }}
                              />
                            </ListItemButton>
                          ))}
                        </List>
                      </Collapse>
                    </React.Fragment>
                  ))}
                </List>
              </Collapse>
            </React.Fragment>
          ))}
        </List>
      </Box>

      <Box
        onMouseDown={startResize}
        sx={{
          position: "absolute",
          top: 0,
          right: 0,
          width: "5px",
          height: "100%",
          cursor: "col-resize",
          "&:hover": { bgcolor: "action.hover" },
        }}
      />
    </Drawer>
  );
}
