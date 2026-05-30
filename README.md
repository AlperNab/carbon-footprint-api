# Carbon Footprint Api

This folder has been upgraded into a **standalone real GUI project**.

Run the project GUI:

```bash
./run_gui.sh
```

Windows:

```powershell
.\run_gui_windows.ps1
```

Default local URL: `http://127.0.0.1:9105`

This project includes its own FastAPI backend, browser GUI, provider settings, local/cloud LLM routing, encrypted API-key storage, file uploads, job history, exports, and a project-specific plugin configuration.

See `PROJECT_IMPLEMENTATION.md` and `project_config.json` for the applied project-specific features and customization controls.

---

## Original README

# carbon-footprint-api

> **Company activity data → CO2e footprint with Scope 1/2/3 breakdown.** Reduction opportunities ranked by impact, Science Based Targets alignment, industry benchmark comparison.

[![PyPI](https://img.shields.io/pypi/v/carbon-footprint-api?style=flat)](https://pypi.org/project/carbon-footprint-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Quickstart

```bash
pip install carbon-footprint-api
python -m carbon_footprint_api activity_data.txt --company "Acme Corp" --year 2025 --revenue 50
python -m carbon_footprint_api emissions.csv --json
```

## Activity data format

Plain text or CSV describing: energy consumption (kWh), fuel usage (liters/gallons),
business travel (km by mode), fleet vehicles, purchased goods spend, employee count.

## What's calculated

- **Scope 1** — direct emissions (combustion, process, fugitive)
- **Scope 2** — purchased energy (market-based + location-based)
- **Scope 3** — value chain (15 GHG Protocol categories)
- **Reduction roadmap** — ranked by tCO2e potential vs cost
- **SBT alignment** — 1.5°C pathway vs current trajectory
- **Industry benchmark** — your intensity vs sector median

## License
MIT © [Alper Nabil Gabra Zakher](https://github.com/AlperNab)
