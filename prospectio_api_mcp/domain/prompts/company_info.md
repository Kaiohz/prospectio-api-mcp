# STRUCTURED EXTRACTION INSTRUCTIONS

You are an expert at extracting structured company information.

Given ONLY the following company description, output a JSON object with these fields:

## Required Fields

- **industry**: list of strings (industry sectors, e.g. ['Software', 'Healthcare'])
- **compatibility**: integer (score from 0-100, estimate if not provided)
- **location**: list of strings (city, country, etc.)
- **size**: integer (number of employees, estimate if not provided)
- **revenue**: integer (annual revenue in USD, estimate if not provided)

## Rules

- If you cannot determine a field, use a reasonable default (e.g. empty list, 0, or 'N/A').
- **DO NOT** add any explanation, commentary, or extra text.

---

## Input Data

**COMPANY DESCRIPTION:**

{web_content}
