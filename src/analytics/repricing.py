import numpy as np
import pandas as pd

from portfolio.banking_book import (
    INSTRUMENTS,
    SAVINGS_AMT,
    SAVINGS_BEHAVIOURAL
)

BUCKETS       = ["<3M", "3–6M", "6M–1Y", "1–3Y", "3–5Y", ">5Y"]
BUCKET_BOUNDS = [(0, 0.25), (0.25, 0.5), (0.5, 1.0), (1.0, 3.0), (3.0, 5.0), (5.0, 100)]

def bucket_index(t):
    for i, (lo, hi) in enumerate(BUCKET_BOUNDS):
        if lo <= t < hi or (i == 5 and t >= 5.0):
            return i
    return 5

def repricing_gap():
    """Build repricing gap table with amortising principal flows and behavioural bucketing."""
    asset_b = np.zeros(6)
    liab_b  = np.zeros(6)

    for (name, side, amt, coupon, mat, reprice, floating, cf_type) in INSTRUMENTS:
        if amt == 0: continue

        if cf_type == "amortising":
            # Distribute principal repayments into buckets month by month
            n  = int(round(mat * 12))
            rm = coupon / 12
            emi     = amt * rm * (1 + rm)**n / ((1 + rm)**n - 1)
            balance = amt
            for m in range(1, n + 1):
                interest_pmt  = balance * rm
                principal_pmt = emi - interest_pmt
                balance      -= principal_pmt
                i = bucket_index(m / 12)
                if side == "asset": asset_b[i] += principal_pmt
                else:               liab_b[i]  += principal_pmt
        else:
            t = reprice if floating else mat
            i = bucket_index(t)
            if side == "asset": asset_b[i] += amt
            else:               liab_b[i]  += amt

    # Savings deposits — behavioural allocation
    for prop, eff_tenor in SAVINGS_BEHAVIOURAL.values():
        liab_b[bucket_index(eff_tenor)] += SAVINGS_AMT * prop

    gap    = asset_b - liab_b
    cumgap = np.cumsum(gap)
    return pd.DataFrame({
        "Bucket":                BUCKETS,
        "Assets (₹ Cr)":         asset_b.round(0),
        "Liabilities (₹ Cr)":    liab_b.round(0),
        "Gap (₹ Cr)":            gap.round(0),
        "Cumulative Gap (₹ Cr)": cumgap.round(0),
    })

