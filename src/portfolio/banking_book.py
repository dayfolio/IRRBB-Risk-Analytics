EQUITY = 12000  # INR Crores

INSTRUMENTS = [
    # name                  side     amt    coupon   mat  reprice  float  cf_type
    ("Home Loans",         "asset", 30000, 0.0880, 20.0,  20.0,  False, "amortising"),
    ("MSME Term Loans",    "asset", 20000, 0.1050,  5.0,   5.0,  False, "amortising"),
    ("Corporate Loans",    "asset", 25000, 0.0950,  5.0,   1.0,  True,  "floating"),
    ("G-Sec Portfolio",    "asset", 15000, 0.0735, 10.0,  10.0,  False, "bullet"),
    ("T-Bills",            "asset",  5000, 0.0690,  0.5,   0.5,  False, "bullet"),
    ("Cash / CRR",         "asset",  5000, 0.0000,  0.0,   0.0,  False, "zero"),
    ("CASA Current",       "liab",  10000, 0.0000,  0.0,   0.0,  False, "zero"),
    ("Fixed Deposits 1Y",  "liab",  25000, 0.0700,  1.0,   1.0,  False, "bullet"),
    ("Fixed Deposits 3Y",  "liab",  15000, 0.0725,  3.0,   3.0,  False, "bullet"),
    ("Infra Bonds 5Y",     "liab",  10000, 0.0750,  5.0,   5.0,  False, "bullet"),
    ("Repo Borrowing",     "liab",   8000, 0.0650,  0.0,   0.0,  True,  "floating"),
]

DEPOSIT_BETAS = {
    "Savings Deposits": 0.40,
    "CASA Current":     0.00,
    "Repo Borrowing":   0.60,
}

SAVINGS_AMT = 20000  # INR Crores

SAVINGS_BEHAVIOURAL = {
    # label: (proportion, effective_reprice_tenor_yrs)
    "transactional": (0.30, 1/365),
    "core_sticky":   (0.40, 2.0),
    "long_sticky":   (0.30, 4.0),
}





