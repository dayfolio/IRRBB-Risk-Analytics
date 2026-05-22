from curves.interpolation import interp_rate
from instruments.cashflows import pv_amortising, pv_bullet
from portfolio.banking_book import (
    INSTRUMENTS,
    DEPOSIT_BETAS,
    SAVINGS_AMT,
    SAVINGS_BEHAVIOURAL,
    BASE_CURVE
)

def calc_eve(curve):
    """Compute Economic Value of Equity under a given yield curve."""
    asset_pv, liab_pv = 0.0, 0.0

    for (name, side, amt, coupon, mat, reprice, floating, cf_type) in INSTRUMENTS:
        if   cf_type == "zero":        pv = amt
        elif cf_type == "amortising":  pv = pv_amortising(amt, coupon, mat, curve)
        elif cf_type == "floating":
            r  = interp_rate(curve, max(reprice, 1/365))
            pv = amt / (1 + r) ** max(reprice, 1/365)
        else:                          pv = pv_bullet(amt, coupon, mat, curve)

        if side == "asset": asset_pv += pv
        else:               liab_pv  += pv

    # Savings deposits — behavioural tranches with beta-adjusted rate
    beta = DEPOSIT_BETAS["Savings Deposits"]
    for prop, eff_tenor in SAVINGS_BEHAVIOURAL.values():
        tranche  = SAVINGS_AMT * prop
        base_r   = interp_rate(BASE_CURVE, eff_tenor)
        shocked_r = interp_rate(curve, eff_tenor)
        eff_r    = base_r + beta * (shocked_r - base_r)
        liab_pv += tranche / (1 + eff_r) ** max(eff_tenor, 1/365)

    return asset_pv - liab_pv
