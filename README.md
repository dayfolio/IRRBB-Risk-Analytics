# IRRBB-Risk-Analytics

Python-based balance sheet risk analytics framework for modelling Interest Rate Risk in the Banking Book (IRRBB) under Basel and RBI supervisory standards.

The framework evaluates Economic Value of Equity (EVE), Net Interest Income (NII), Duration of Equity, and behavioural repricing exposure across multiple interest rate stress scenarios using a stylised Indian commercial bank balance sheet.

Built with amortising loan cashflows, floating-rate repricing dynamics, behavioural non-maturity deposit assumptions, and yield curve stress infrastructure aligned with real-world Asset-Liability Management (ALM) practices.

##  Core Analytics

- Economic Value of Equity (EVE) sensitivity under supervisory rate shocks
- Net Interest Income (NII / EaR) exposure modelling
- Duration of Equity decomposition
- Behavioural repricing gap analytics
- Balance sheet sensitivity profiling across the term structure

## Balance Sheet Framework

The banking book includes:


| Assets | Amount (₹ Cr) | Liabilities | Amount (₹ Cr) |
|---|---:|---|---:|
| Home Loans | 30,000 | Savings Deposits | 20,000 |
| MSME Term Loans | 20,000 | CASA Deposits | 10,000 |
| Corporate Loans | 25,000 | Fixed Deposits (1Y) | 25,000 |
| Government Securities | 15,000 | Fixed Deposits (3Y) | 15,000 |
| Treasury Bills | 5,000 | Infra Bonds | 10,000 |
| Cash / CRR | 5,000 | Repo Borrowings | 8,000 |

The framework models:

- amortising retail and MSME loan cashflows
- floating-rate asset and liability repricing
- fixed-income security valuation
- behavioural treatment of non-maturity deposits
- tenor-based repricing exposure across the balance sheet

## Behavioural Assumptions

The analytics framework incorporates:

- deposit beta transmission modelling
- behavioural maturity transformation
- sticky/core deposit segmentation
- repricing asymmetry across liabilities
- behavioural tenor allocation for savings balances

to approximate observed banking book repricing behaviour under changing rate environments.

## Supervisory Stress Framework

Implements Basel IRRBB supervisory shock scenarios across the INR term structure:

- Parallel Up / Down
- Steepener
- Flattener
- Short Rate Up / Down

The framework supports:

- parallel and non-parallel curve shocks
- yield curve interpolation
- shocked discount curve valuation
- balance sheet sensitivity analysis under stressed rate environments

## Supervisory Sensitivity Profile

The balance sheet exhibits a structurally asset-sensitive profile, with asset duration materially exceeding liability duration.

Under the supervisory parallel +250bp shock scenario:

- EVE declines by 55.0% of equity due to long-duration fixed-rate asset exposure
- 1-year NII increases by 15.6% as floating-rate assets reprice faster than liabilities
- Duration of Equity compresses from 25.65 years to 19.26 years under higher-rate conditions

Conversely, under a -250bp parallel shock:

- EVE increases by 74.2% of equity
- NII declines by 15.6% due to reduced floating-rate asset income

The framework also captures non-parallel term structure effects through steepener and flattener scenarios, highlighting sensitivity concentration in the intermediate and long-end asset book.

### Base Balance Sheet Metrics

| Metric | Value |
|---|---:|
| Economic Value of Equity (EVE) | ₹13,580 Cr |
| Net Interest Income (1Y) | ₹2,846 Cr |
| Asset Duration | 4.54 years |
| Liability Duration | 1.67 years |
| Duration of Equity | 25.65 years |

### Scenario Sensitivity

| Scenario | ΔEVE (% Equity) | ΔNII (% Base NII) | Duration of Equity |
|---|---:|---:|---:|
| Parallel Up (+250bp) | -55.0% | 15.6% | 19.26 |
| Parallel Down (-250bp) | 74.2% | -15.6% | 34.55 |
| Steepener | -22.3% | 0.8% | 22.91 |
| Flattener | 25.3% | -0.8% | 28.77 |
| Short Rate Up (+300bp) | -1.3% | 5.6% | 25.62 |
| Short Rate Down (-300bp) | 1.4% | -5.6% | 25.68 |

The behavioural repricing gap profile indicates substantial short-end liability sensitivity driven by deposit funding concentration, partially offset by long-duration retail and fixed-income asset exposure.


## Repository Structure

## Repository Structure

```text
irrbb-risk-analytics/
│
├── README.md
├── requirements.txt
│
├── src/
│   ├── analytics/
│   │   ├── eve.py
│   │   ├── nii.py
│   │   ├── duration.py
│   │   └── repricing.py
│   │
│   ├── curves/
│   │   ├── curve.py
│   │   ├── interpolation.py
│   │   └── shocks.py
│   │
│   ├── instruments/
│   │   ├── cashflows.py
│   │   └── fixed_income.py
│   │
│   ├── portfolio/
│   │   └── banking_book.py
│   │
│   ├── reporting/
│   │   ├── charts.py
│   │   └── tables.py
│   │
│   └── main.py
│
├── outputs/
└── docs/
```





