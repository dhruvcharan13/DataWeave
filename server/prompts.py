import json
from datetime import datetime

def generate_mapping_prompt(dataset_a, dataset_b):
    """
    Generates a structured prompt to guide an AI model in creating
    a field-level mapping and transformation plan between Dataset A and B.
    
    Args:
        dataset_a (dict or str): Source dataset schema (Bank1)
        dataset_b (dict or str): Target dataset schema (Bank2)
    
    Returns:
        str: A complete prompt string ready for the LLM.
    """

    # Convert JSON strings to dicts if needed
    if isinstance(dataset_a, str):
        dataset_a = json.loads(dataset_a)
    if isinstance(dataset_b, str):
        dataset_b = json.loads(dataset_b)

    # Pretty print JSON for inclusion in the prompt
    dataset_a_json = json.dumps(dataset_a, indent=4, ensure_ascii=False)
    dataset_b_json = json.dumps(dataset_b, indent=4, ensure_ascii=False)

    # Build the full structured prompt
    prompt = f"""
You are an expert data integration assistant named DataWeave AI. Your role is to intelligently merge two banking datasets (Dataset A → Dataset B) into a unified relational model for analytics and reporting. You must generate a valid JSON object describing field-level mappings, joins, transformations, key strategies, and how to handle stray or unmatched fields — following strict no-data-loss principles.

Your response must be a single JSON object, no comments, no additional explanation.  
Follow the structure and rules below exactly.


### NO DATA LOSS POLICY
- **No data should ever be dropped.**
- Unmatched fields must always be retained.
- Use a **hybrid method** for handling extras:
  - If only a few stray fields (1–5) exist for an entity → add them to the main table using `"method": "extend_table"`.
  - If many extra fields exist (10+) or uncertain mappings → move them to a linked `"extras_table"` with a foreign key (e.g. `customerId`, `transactionReference`).
- When a field cannot fit any normalized table, still retain it under the closest logical entity with nulls where unmatched.

---

### TRANSFORMATION POLICY
For each mapping, if data format adjustments are needed, include a `transform` object:
- `"identity"` → keep value as-is  
- `"cast"` → type conversion (e.g. string to float)  
- `"parse_date"` or `"parse_datetime"` → date/time conversions  
- `"string_normalize"` → clean text fields  
- `"currency_normalize"` → handle different currency formats  
- `"custom"` → for any other logic

All applied transformations must also be listed under `"applied_transformations"` at the bottom of the JSON.

---

### OUTPUT FORMAT (RETURN EXACTLY THIS STRUCTURE)
{{
  "version": "mapping-2.0",
  "generated_at": "{datetime.utcnow().isoformat()}Z",
  "model": "gemini-2.5-lite",
  "source_dataset": {{ "name": "DatasetA" }},
  "target_dataset": {{ "name": "DatasetB" }},
  "mappings": [
    {{
      "id": "<stable_id>",
      "domain": "<customers|accounts|transactions|loans|...>",
      "source": {{ "table": "<A_table>", "column": "<A_column>" }},
      "target": {{ "table": "<B_table or merged_table>", "column": "<B_column or unified_column>" }},
      "transform": {{ "type": "<identity|cast|string_normalize|parse_date|parse_datetime|currency_normalize|custom>", "params": {{}} }},
      "confidence": <0..1>,
      "rationale": "<why this mapping was chosen>",
      "status": "suggested",
      "extra_field_handling": {{
        "action": "preserve",
        "method": "extend_table|extras_table",
        "target_table": "<table_name>",
        "link_key": "<foreign_key_name>",
        "reason": "<why this method was chosen>"
      }}
    }}
  ],
}}

---

### CONSTRAINTS
- Return ONLY the JSON object in the format above.
- No natural language explanation or markdown outside the JSON.
- All mappings should include a rationale and confidence value.
- All extra fields must have `action: preserve` and either `extend_table` or `extras_table`.
- Keep consistent table/column naming for clarity in the final merged schema.

---

### DATASET A (Bank1)
{dataset_a_json}

### DATASET B (Bank2)
{dataset_b_json}
"""
    return prompt.strip()


def generate_relationship_prompt(source_info, target_info):
    schema_prompt = """
            Analyze the following database schemas and identify:
            1. Primary keys for each table
            2. Foreign key relationships between tables
            3. Table structures
            4. Sources database: will be source and Target database: will be target
            
            Return only a valid JSON object with this structure:
            {
                "source": {
                    "database": "<name>",
                    "tables": [{
                        "name": "<table_name>",
                        "primaryKey": "<column>",
                        "foreignKeys": [{"column": "<col>", "references": "<table.column>"}],
                        "columns": ["col1": "column_def_from schema", "col2": "column_def_from schema"]
                    }]
                },
                "target": { ... }
            }
            
            Schema Information:
            """ + json.dumps({"source": source_info, "target": target_info}, indent=2)

    return schema_prompt
