# Replication Code: Institutional Agency in Asymmetric Rivalries

This repository contains the replication scripts for the Supplementary Materials accompanying "Institutional Agency in Asymmetric Rivalries: A Trilateral Mechanism Framework and Falsification Design for Nepal".

## Contents

- **`Replication_Code_Institutional_Agency_SM3.py`** — Reconstructs Table 1 (Nepal Worldwide Governance Indicators, 2002–2024) and runs ADF/KPSS stationarity tests on all six WGI dimensions under a common, capped lag-selection rule (Section 3.1 of the main text).
- **`Replication_Code_Institutional_Agency_SM4.py`** — Sensitivity analysis for the state-capacity attenuation threshold GE* discussed in Section 6 / SM.4, sweeping the illustrative (tau, kappa) parameter grid stated in the main text.

Both scripts are self-contained and run independently of one another (SM.4 does not import from SM.3; it uses an independently hardcoded copy of the same Government Effectiveness series for verification purposes).

## Requirements

- Python 3.8+
- `numpy`
- `pandas` (SM.3 only)

Install with:

```bash
pip install -r requirements.txt
```

## Running the scripts

```bash
python3 Replication_Code_Institutional_Agency_SM3.py
python3 Replication_Code_Institutional_Agency_SM4.py
```

Each script prints its full output to the console; no files are written or read.

## Data source

World Bank Worldwide Governance Indicators, Nepal percentile ranks, 2002–2024.  
https://www.worldbank.org/en/publication/worldwide-governance-indicators

## Citation

If you use this code, please cite it as archived on Zenodo (DOI to be added after first release — see badge below).

## License

Code is released under the MIT License (see LICENSE).
