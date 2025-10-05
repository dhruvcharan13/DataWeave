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
    if (!stored) return;
  
    try {
      const parsed = JSON.parse(stored);
      const formatted: any = {};
  
      ["source", "target"].forEach((key) => {
        const db = parsed[key];
        if (!db || !db.tables) return;
  
     //  Always use simple readable names
let dbName = key === "target" ? "Target" : "Source";

        formatted[dbName] = {
          tables: db.tables.map((table: any) => ({
            name: table.name,
            columns: Array.isArray(table.columns)
              ? table.columns
              : Object.keys(table.columns || {}),
          })),
        };
      });
  
      console.log("✅ Loaded schemas:", formatted);
      setSchemas(formatted);
    } catch (err) {
      console.error("Failed to parse schemaAnalysis:", err);
    }
  }, []);
  
  
  console.log("📂 All schemas:", Object.keys(schemas));


  return (
    <Drawer
  variant="permanent"
  anchor="left"
  sx={{
    width: sidebarWidth,
    flexShrink: 0,
    "& .MuiDrawer-paper": {
      width: sidebarWidth,
      boxSizing: "border-box",
      bgcolor: "background.paper",
      borderRight: "1px solid",
      borderColor: "divider",
      position: "fixed",   // ✅ key fix: stick to viewport edge
      left: 0,             // ✅ force it to the very edge
      top: 72,
      height: "90%",     // ✅ ensure full height
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
