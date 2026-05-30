# Carbon Footprint Api — Standalone Real GUI Implementation

This folder is now its own runnable project app. It does not depend on the root all-project dashboard at runtime.

## Run

```bash
./run_gui.sh
```

Windows:

```powershell
.\run_gui_windows.ps1
```

Default URL: `http://127.0.0.1:9105`

## What is inside this project folder

- `app/` — FastAPI backend for this project.
- `static/` — elegant browser GUI.
- `plugins/carbon-footprint-api.json` — this project’s own feature/customization/input schema.
- `project_config.json` — readable copy of the same project-specific configuration.
- `data/` — local SQLite jobs, uploads, exports.
- `tests/` — verifies this project has a registered real local engine.

## Project-specific scope

- Domain: `ESG / Sustainability`
- Target user: `Domain operator, business owner, analyst, or team member who needs this workflow executed reliably.`
- Core job: Activity data → CO2e scope breakdown
- Suite: `General Automation Suite`

## Deep features applied

- Scope 1/2/3 categorization
- emission factor library
- supplier data import
- reduction scenario planner
- benchmark comparison
- target pathway
- data quality confidence

## Customization controls

- `execution_mode` — Execution mode (select)
- `industry` — industry (text)
- `country` — country (select)
- `reporting_year` — reporting year (text)
- `framework` — framework (select)
- `emission_factors` — emission factors (text)
- `units` — units (text)
- `boundary_rules` — boundary rules (textarea)
- `uncertainty_tolerance` — uncertainty tolerance (slider)
- `output_format` — output format (select)
- `language` — language (select)
- `privacy_mode` — privacy mode (select)
- `confidence_threshold` — Confidence threshold (slider)

## Input fields

- `activity_data` — Activity data (text) required
- `work_brief` — Work brief / source text / URL / instructions (textarea) required

## External data policy

The local deterministic core is real and executable. Live external systems are not simulated. If Shopify, ATS, ERP, OCR/STT, maps, SERP, market data, medical databases, tax/customs databases, or other live systems are required, this project reports the missing connector/API requirement instead of inventing data.

---

## Final UX/UI Layer

This project now uses the **Automation Command Center** pattern.

**UX workflow:** Brief/data intake → structured analysis → action plan → export

**Domain components:**
- Brief analyzer
- KPI cards
- Workflow board
- Decision checklist
- Report builder

**Quick actions:**
- Structure input
- Generate action plan
- Build scorecard
- Prepare final report

**No fake-data policy:** external/live actions require real connectors or API keys. Missing connectors are reported instead of simulated.
