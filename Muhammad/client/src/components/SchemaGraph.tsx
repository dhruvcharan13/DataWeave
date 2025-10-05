"use client";

import React, { useCallback, useEffect } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  Handle,
  Position,
  useNodesState,
  useEdgesState,
  MarkerType,
  type Node,
  type Edge,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";

/* ---------- FULL HARDCODED SCHEMA (from bank1.json & bank2.json) ---------- */
const sampleSchemas: any = {
  Bank1: {
    database: "Bank1",
    tables: [
      {
        name: "Bank1_Mock_Customer",
        primaryKey: "customerId",
        foreignKeys: [],
        columns: [
          "phoneNumber","smsNumber","email","street","addressCity","country",
          "legalId","legalDocumentName","legalIssueAuthorised","legalIssueCountry",
          "legalIssueDate","legalExpiredDate","language","dateOfBirth",
          "customerStatus","accountOfficerId","gender","state","postCode",
          "contactDate","lastName","givenName","customerType","customerId"
        ],
      },
      {
        name: "Bank1_Mock_CurSav_Accounts",
        primaryKey: "accountId",
        foreignKeys: [
          { column: "customerId", references: "Bank1_Mock_Customer.customerId" }
        ],
        columns: [
          "accountId","displayName","customerId","customerRole","productId","status",
          "currency","branch","accountOpeningDate","arrangementStartDate",
          "availableBalance","onlineActualBalance","lockedAmount","availableLimit",
          "productDescription","category"
        ],
      },
      {
        name: "Bank1_Mock_CurSav_Transactions",
        primaryKey: "transactionReference",
        foreignKeys: [
          { column: "accountId", references: "Bank1_Mock_CurSav_Accounts.accountId" }
        ],
        columns: [
          "transactionReference","activity","transactionAmount","currency",
          "effectiveDate","transactionDate","bookingDate","narrative",
          "externalEventStatus","userRole","branch","accountId",
          "chargesPaymentTypeName","chargesPropertyName","chargesChargeAmount",
          "taxRate","availableBalance","lockedAmount","approvedOverdraftLimit",
          "accrualAmount","effectiveRate","availableOverdraftLimit","channel"
        ],
      },
      {
        name: "Bank1_Mock_FixedTerm_Accounts",
        primaryKey: "accountId",
        foreignKeys: [
          { column: "customerId", references: "Bank1_Mock_Customer.customerId" },
          { column: "agentCustomerId", references: "Bank1_Mock_Customer.customerId" }
        ],
        columns: [
          "accountId","accountTitles","productId","currency","customerId",
          "customerRole","branch","reason","maturityDate","arrangementEffectiveDate",
          "expiryDate","agentCustomerId","expectedBalance","currentBalance",
          "accruedInterest","jointCustomerName","category","interestRate",
          "interestStatement","status"
        ],
      },
      {
        name: "Bank1_Mock_FixedTerm_Transactions",
        primaryKey: "transactionReference",
        foreignKeys: [
          { column: "accountId", references: "Bank1_Mock_FixedTerm_Accounts.accountId" }
        ],
        columns: [
          "transactionReference","activity","transactionAmount","currency",
          "effectiveDate","transactionDate","reason","externalEventStatus","userRole",
          "branch","chargesChargeAmount","interestAmount","taxRate","currentBalance",
          "interestRate","channel","accountId"
        ],
      },
      {
        name: "Bank1_Mock_Loan_Accounts",
        primaryKey: "accountId",
        foreignKeys: [
          { column: "customerId", references: "Bank1_Mock_Customer.customerId" },
          { column: "agentCustomerIds", references: "Bank1_Mock_Customer.customerId" }
        ],
        columns: [
          "accountId","accountName","productId","currency","customerId","customerRole",
          "branch","reason","maturityDate","arrangementEffectiveDate","expiryDate",
          "agentCustomerIds","loanBalance","availableBalance","loanInterestRate",
          "loanInterestType","compoundType","effectiveRate","gracePeriod",
          "periodicPayment","numberPayments","paymentFrequency","fixedDaysOfMonth",
          "amortisationTerm","principalAmount","principalBalance","interestAmount",
          "chargeAmount","interestBalance","interestFromArrearsBalance","accountType"
        ],
      },
      {
        name: "Bank1_Mock_Loan_Transactions",
        primaryKey: "transactionReference",
        foreignKeys: [
          { column: "accountId", references: "Bank1_Mock_Loan_Accounts.accountId" }
        ],
        columns: [
          "transactionReference","activity","transactionAmount","currency",
          "effectiveDate","reason","externalEventStatus","userRole","branch",
          "principalAmount","interestAmount","chargeAmount","balanceAmount",
          "interestRate","channelName","accountId"
        ],
      },
    ],
  },

  Bank2: {
    database: "Bank2",
    tables: [
      {
        name: "Bank2_Mock_Customer",
        primaryKey: "encodedKey",
        foreignKeys: [],
        columns: [
          "lastName","migrationEventKey","preferredLanguage","notes","gender",
          "emailAddress","encodedKey","id","state","assignedUserKey","homePhone",
          "creationDate","birthDate","firstName","mobilePhone","clientType"
        ],
      },
      {
        name: "Bank2_Mock_Addresses",
        primaryKey: "encodedKey",
        foreignKeys: [
          { column: "parentKey", references: "Bank2_Mock_Customer.encodedKey" }
        ],
        columns: [
          "city","country","encodedKey","line1","parentKey","postcode","region"
        ],
      },
      {
        name: "Bank2_Mock_Deposit_Accounts",
        primaryKey: "encodedKey",
        foreignKeys: [
          { column: "accountHolderKey", references: "Bank2_Mock_Customer.encodedKey" }
        ],
        columns: [
          "encodedKey","id","name","productTypeKey","currencyCode","accountHolderKey",
          "accountHolderType","assignedBranchKey","notes","maturityDate","creationDate",
          "closedDate","assignedUserKey","totalBalance","availableBalance",
          "interestAccrued","ownershipHistory","accountType","interestRate",
          "interestPaymentPoint","status","accountState","lockedBalance","overdraftAmount",
          "productDescription"
        ],
      },
      {
        name: "Bank2_Mock_Deposit_Transactions",
        primaryKey: "id",
        foreignKeys: [
          { column: "parentAccountKey", references: "Bank2_Mock_Deposit_Accounts.encodedKey" }
        ],
        columns: [
          "id","encodedKey","type","amount","currencyCode","creationDate","valueDate",
          "notes","externalId","userKey","branchKey","interestRate","transactionChannel",
          "parentAccountKey","feesAmount","interestAmount","taxRate","totalBalance",
          "bookingDate","feesPredefinedFee","feesName","availableBalance","lockedBalance",
          "overdraftAmount","interestBalance","overdraftLimit"
        ],
      },
      {
        name: "Bank2_Mock_Identifications",
        primaryKey: "encodedKey",
        foreignKeys: [
          { column: "clientKey", references: "Bank2_Mock_Customer.encodedKey" }
        ],
        columns: [
          "clientKey","documentId","documentType","encodedKey","issuingAuthority",
          "issuingCountry","issuingDate","validUntil"
        ],
      },
      {
        name: "Bank2_Mock_Loan_Accounts",
        primaryKey: "id",
        foreignKeys: [
          { column: "accountHolderKey", references: "Bank2_Mock_Customer.encodedKey" }
        ],
        columns: [
          "id","loanName","productTypeKey","currencyCode","accountHolderKey",
          "accountHolderType","assignedBranchKey","notes","maturityDate","creationDate",
          "closedDate","assignedUserKey","totalBalance","availableBalance","interestRate",
          "interestType","interestApplicationMethod","effectiveInterestRate","gracePeriod",
          "periodicPayment","repaymentInstallments","repaymentPeriodUnit","fixedDaysOfMonth",
          "repaymentPeriodCount","amortizationPeriod","principalDue","principalBalance",
          "interestDue","feesDue","interestBalance","interestFromArrearsBalance",
          "interestAccrued","accountType"
        ],
      },
      {
        name: "Bank2_Mock_Loan_Transactions",
        primaryKey: "id",
        foreignKeys: [
          { column: "parentAccountKey", references: "Bank2_Mock_Loan_Accounts.id" }
        ],
        columns: [
          "encodedKey","id","type","amount","originalCurrencyCode","valueDate","notes",
          "externalId","userKey","branchKey","principalAmount","interestAmount",
          "feesAmount","totalBalance","principalBalance","interestRate",
          "transactionChannel","parentAccountKey"
        ],
      },
    ],
  },
};

/* ---------- Node Component ---------- */
function TableNode({ data }: any) {
    const { table } = data;
    const foreignKeyColumns = table.foreignKeys.map((fk: any) => fk.column);
  
    return (
      <Paper
        elevation={3}
        sx={{
          minWidth: 280,
          border: "1.5px solid",
          borderColor: "divider",
          p: 1.5,
          position: "relative",
          bgcolor: "background.paper",
          maxHeight: 320,
          overflow: "hidden",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* Table Header */}
        <Typography
          variant="subtitle2"
          fontFamily="monospace"
          fontWeight={700}
          gutterBottom
          sx={{ color: "text.primary" }}
        >
          {table.name}
        </Typography>
  
        {/* Primary Key */}
        <Box mb={1}>
          <Typography variant="caption" color="primary" fontWeight={600}>
            Primary Key
          </Typography>
          <Typography variant="caption" display="block" fontFamily="monospace">
            {table.primaryKey}
          </Typography>
          <Handle
            type="target"
            position={Position.Left}
            className="!h-3 !w-3 !bg-blue-500 !border-2 !border-white"
          />
        </Box>
  
        <Divider sx={{ my: 0.5 }} />
  
        {/* Foreign Keys */}
        {table.foreignKeys.length > 0 && (
          <Box mb={1}>
            <Typography variant="caption" color="warning.main" fontWeight={600}>
              Foreign Keys
            </Typography>
            {table.foreignKeys.map((fk: any, i: number) => (
              <Box
                key={i}
                display="flex"
                justifyContent="space-between"
                alignItems="center"
                sx={{ gap: 0.5 }}
              >
                <Typography
                  variant="caption"
                  fontFamily="monospace"
                  color="text.secondary"
                  sx={{ fontSize: "0.7rem" }}
                >
                  {fk.column}
                </Typography>
                <Typography
                  variant="caption"
                  sx={{ fontSize: "0.65rem", color: "text.disabled" }}
                >
                  → {fk.references.split(".")[0]}
                </Typography>
                <Handle
                  type="source"
                  position={Position.Right}
                  id={fk.column}
                  className="!h-2 !w-2 !bg-orange-400 !border-2 !border-white"
                  style={{
                    top: `${((i + 1) * 100) / (table.foreignKeys.length + 1)}%`,
                  }}
                />
              </Box>
            ))}
          </Box>
        )}
  
        <Divider sx={{ my: 0.5 }} />
  
        {/* All Attributes / Columns */}
        <Box sx={{ overflowY: "auto", flexGrow: 1, pr: 0.5 }}>
          <Typography
            variant="caption"
            sx={{
              color: "text.secondary",
              fontWeight: 600,
              fontSize: "0.7rem",
              mb: 0.5,
              display: "block",
            }}
          >
            Columns ({table.columns.length})
          </Typography>
  
          {table.columns.map((col: string, i: number) => (
            <Typography
              key={i}
              variant="caption"
              sx={{
                display: "block",
                fontFamily: "monospace",
                fontSize: "0.7rem",
                color: foreignKeyColumns.includes(col)
                  ? "warning.main"
                  : col === table.primaryKey
                  ? "primary.main"
                  : "text.disabled",
                pl: 0.5,
              }}
            >
              {col}
            </Typography>
          ))}
        </Box>
      </Paper>
    );
  }
  

const nodeTypes = { table: TableNode };

/* ---------- Main Graph ---------- */
interface Props {
  selectedDataset: string;
}

export default function SchemaGraph({ selectedDataset }: Props) {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  const generateNodesAndEdges = useCallback((schemaData: any) => {
    const newNodes: Node[] = [];
    const newEdges: Edge[] = [];
    const cols = Math.ceil(Math.sqrt(schemaData.tables.length));
    const spacing = 420;

    schemaData.tables.forEach((table: any, index: number) => {
      const row = Math.floor(index / cols);
      const col = index % cols;

      newNodes.push({
        id: table.name,
        type: "table",
        position: { x: col * spacing + 150, y: row * spacing + 150 },
        data: { table },
      });

      table.foreignKeys.forEach((fk: any) => {
        const [targetTable] = fk.references.split(".");
        newEdges.push({
          id: `${table.name}-${fk.column}-${targetTable}`,
          source: table.name,
          target: targetTable,
          label: fk.column,
          type: "smoothstep",
          animated: true,
          style: { stroke: "orange", strokeWidth: 2 },
          markerEnd: { type: MarkerType.ArrowClosed, color: "orange" },
          labelStyle: { fill: "#111", fontSize: 11, fontWeight: 600 },
          labelBgStyle: {
            fill: "#fff",
            fillOpacity: 1,
            stroke: "orange",
            strokeWidth: 0.5,
          },
          labelBgPadding: [4, 2],
          labelBgBorderRadius: 4,
        });
      });
    });

    setNodes(newNodes);
    setEdges(newEdges);
  }, []);

  useEffect(() => {
    generateNodesAndEdges(sampleSchemas[selectedDataset]);
  }, [selectedDataset, generateNodesAndEdges]);

  return (
    <Box sx={{ width: "100%", height: "100%" }}>
      <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} fitView nodeTypes={nodeTypes}>
        <Background color="#555" gap={16} size={1} />
        <Controls />
        <MiniMap nodeColor={() => "#1e88e5"} maskColor="rgba(0,0,0,0.7)" style={{ borderRadius: 8 }} />
      </ReactFlow>
      <Paper
        elevation={2}
        sx={{
          position: "absolute",
          bottom: 16,
          left: 16,
          px: 2,
          py: 1,
          bgcolor: "background.paper",
          fontSize: 12,
        }}
      >
        Viewing dataset: <b>{selectedDataset}</b>
      </Paper>
    </Box>
  );
}
