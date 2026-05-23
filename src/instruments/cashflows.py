import numpy as np

from curves.interpolation import interp_rate

def pv_amortising(amount, annual_coupon, maturity_yrs, discount_curve):
    """
    PV of a monthly amortising loan (home loan, auto loan, MSME).
    Computes EMI schedule and discounts each monthly cashflow.
    """
    n  = int(round(maturity_yrs * 12))
    rm = annual_coupon / 12
    if rm == 0 or n == 0:
        return amount
    emi = amount * rm * (1 + rm)**n / ((1 + rm)**n - 1)
    pv  = sum(emi / (1 + interp_rate(discount_curve, m/12)) ** (m/12)
              for m in range(1, n + 1))
    return pv
  

def duration_amortising(amount, annual_coupon, maturity_yrs, discount_curve):
    """Macaulay duration of a monthly amortising loan."""
    n  = int(round(maturity_yrs * 12))
    rm = annual_coupon / 12
    if rm == 0 or n == 0:
        return 0.0
    emi = amount * rm * (1 + rm)**n / ((1 + rm)**n - 1)
    weighted, total_pv = 0.0, 0.0
    for m in range(1, n + 1):
        t   = m / 12
        pv  = emi / (1 + interp_rate(discount_curve, t)) ** t
        weighted  += t * pv
        total_pv  += pv
    return weighted / total_pv if total_pv > 0 else 0.0


def nii_year1_amortising(amount, annual_coupon, maturity_yrs):
    """Interest income in year 1 for an amortising loan."""
    n  = int(round(maturity_yrs * 12))
    rm = annual_coupon / 12
    if rm == 0 or n == 0:
        return 0.0
    emi     = amount * rm * (1 + rm)**n / ((1 + rm)**n - 1)
    balance = amount
    interest_total = 0.0
    for _ in range(12):
        interest_pmt    = balance * rm
        interest_total += interest_pmt
        balance        -= (emi - interest_pmt)
    return interest_total



