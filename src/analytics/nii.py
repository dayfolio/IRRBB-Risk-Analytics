from curves.interpolation import interp_rate
from instruments.cashflows import nii_year1_amortising
from portfolio.banking_book import (
    INSTRUMENTS,
    DEPOSIT_BETAS,
    SAVINGS_AMT,
    SAVINGS_BEHAVIOURAL,
    BASE_CURVE
)

def calc_nii(curve, horizon=1.0):
    """Compute 1-year Net Interest Income under a given yield curve."""
    income, cost = 0.0, 0.0

    for (name, side, amt, coupon, mat, reprice, floating, cf_type) in INSTRUMENTS:
        if amt == 0 or cf_type == "zero":
            continue
        if floating and reprice <= horizon:
            beta     = DEPOSIT_BETAS.get(name, 1.0)
            base_r   = interp_rate(BASE_CURVE, max(reprice, 1/365))
            shocked_r = interp_rate(curve,      max(reprice, 1/365))
            rate     = base_r + beta * (shocked_r - base_r)
            annual_cf = amt * rate
        elif cf_type == "amortising":
            annual_cf = nii_year1_amortising(amt, coupon, mat)
        else:
            annual_cf = amt * coupon

        if side == "asset": income += annual_cf
        else:               cost   += annual_cf

    # Savings deposits — beta-adjusted, tranche-specific
    beta     = DEPOSIT_BETAS["Savings Deposits"]
    base_r   = interp_rate(BASE_CURVE, 1/365)
    for prop, eff_tenor in SAVINGS_BEHAVIOURAL.values():
        tranche = SAVINGS_AMT * prop
        if eff_tenor <= horizon:
            shocked_r = interp_rate(curve, max(eff_tenor, 1/365))
            rate      = base_r + beta * (shocked_r - base_r)
        else:
            rate = 0.0300  # unchanged within 1Y horizon
        cost += tranche * rate

    return income - cost
