from curves.interpolation import interp_rate
from instruments.cashflows import (
    duration_amortising,
    duration_bullet,
    pv_amortising,
    pv_bullet
)

from portfolio.banking_book import (
    INSTRUMENTS,
    DEPOSIT_BETAS,
    SAVINGS_AMT,
    SAVINGS_BEHAVIOURAL,
    BASE_CURVE,
    EQUITY
)

def calc_duration_of_equity(curve):
    """Compute Duration of Equity = (D_A * A - D_L * L) / Equity."""
    a_dur_pv, l_dur_pv = 0.0, 0.0
    total_a,  total_l  = 0.0, 0.0

    for (name, side, amt, coupon, mat, reprice, floating, cf_type) in INSTRUMENTS:
        if amt == 0: continue
        if   cf_type == "zero":
            dur, pv = 0.0, amt
        elif cf_type == "amortising":
            dur = duration_amortising(amt, coupon, mat, curve)
            pv  = pv_amortising(amt, coupon, mat, curve)
        elif cf_type == "floating":
            dur = reprice
            pv  = amt / (1 + interp_rate(curve, max(reprice,1/365))) ** max(reprice,1/365)
        else:
            dur = duration_bullet(amt, coupon, mat, curve)
            pv  = pv_bullet(amt, coupon, mat, curve)

        if side == "asset": a_dur_pv += dur*pv; total_a += pv
        else:               l_dur_pv += dur*pv; total_l += pv

    # Savings deposits — behavioural duration
    beta = DEPOSIT_BETAS["Savings Deposits"]
    for prop, eff_tenor in SAVINGS_BEHAVIOURAL.values():
        tranche  = SAVINGS_AMT * prop
        base_r   = interp_rate(BASE_CURVE, eff_tenor)
        shocked_r = interp_rate(curve, eff_tenor)
        eff_r    = base_r + beta * (shocked_r - base_r)
        pv       = tranche / (1 + eff_r) ** max(eff_tenor, 1/365)
        l_dur_pv += eff_tenor * pv
        total_l  += pv

    d_a = a_dur_pv / total_a if total_a > 0 else 0
    d_l = l_dur_pv / total_l if total_l > 0 else 0
    doe = (d_a * total_a - d_l * total_l) / EQUITY
    return d_a, d_l, doe
