import numpy as np

from curves.interpolation import interp_rate

def pv_bullet(amount, coupon, maturity, discount_curve):
    """PV of an annual coupon bullet instrument (G-Sec, FD, bond)."""
    if maturity <= 0:
        return amount
    years = np.arange(1, int(round(maturity)) + 1, dtype=float)
    pv = sum(
        (amount * coupon + (amount if t == years[-1] else 0))
        / (1 + interp_rate(discount_curve, t)) ** t
        for t in years
    )
    return pv

def duration_bullet(amount, coupon, maturity, discount_curve):
    """Macaulay duration of a bullet instrument."""
    if maturity <= 0 or coupon == 0:
        return 0.0
    years = np.arange(1, int(round(maturity)) + 1, dtype=float)
    weighted, total_pv = 0.0, 0.0
    for t in years:
        cf    = amount * coupon + (amount if t == years[-1] else 0)
        pv_cf = cf / (1 + interp_rate(discount_curve, t)) ** t
        weighted  += t * pv_cf
        total_pv  += pv_cf
    return weighted / total_pv if total_pv > 0 else 0.0

