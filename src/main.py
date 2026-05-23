import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import os, json
from analytics.eve import calc_eve
from analytics.nii import calc_nii
from analytics.duration import calc_duration_of_equity
from analytics.repricing import repricing_gap

from curves.curve import BASE_CURVE
from curves.shocks import (
    SCENARIOS,
    apply_shock
)

from portfolio.banking_book import EQUITY

from reporting.charts import plot


OUTPUT_DIR = "./irrbb_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run():
    base_eve = calc_eve(BASE_CURVE)
    base_nii = calc_nii(BASE_CURVE)
    d_a, d_l, doe = calc_duration_of_equity(BASE_CURVE)

rows = []
    for sc_name, shock_bp in SCENARIOS.items():
        sc_curve  = apply_shock(BASE_CURVE, shock_bp)
        eve       = calc_eve(sc_curve)
        nii       = calc_nii(sc_curve)
        _, _, sc_doe = calc_duration_of_equity(sc_curve)
        rows.append({
            "Scenario":           sc_name,
            "EVE (₹ Cr)":         round(eve),
            "ΔEVE (₹ Cr)":        round(eve - base_eve),
            "ΔEVE (% Equity)":    round((eve - base_eve) / EQUITY * 100, 1),
            "NII (₹ Cr)":         round(nii),
            "ΔNII (₹ Cr)":        round(nii - base_nii),
            "ΔNII (% Base NII)":  round((nii - base_nii) / base_nii * 100, 1),
            "Duration of Equity": round(sc_doe, 2),
        })

    results_df = pd.DataFrame(rows)
    gap_df     = repricing_gap()

results_df.to_csv(f"{OUTPUT_DIR}/scenario_results.csv", index=False)
    gap_df.to_csv(f"{OUTPUT_DIR}/repricing_gap.csv", index=False)

    json.dump({
        "base_eve": base_eve, "base_nii": base_nii,
        "d_asset": d_a, "d_liab": d_l, "doe": doe,
        "equity": EQUITY,
    }, open(f"{OUTPUT_DIR}/base_metrics.json", "w"))

plot(results_df, gap_df, base_eve, base_nii, d_a, d_l, doe)
    print(f"\nAll outputs saved to {OUTPUT_DIR}/")

if __name__ == "__main__":
    run()


