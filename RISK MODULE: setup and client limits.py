# ==== RISK MODULE: setup and client limits ====
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.stats import norm
from IPython.display import display

RISK_BENCH_TICKER = "ISF.L"     # FTSE 100 total-return proxy used in the group notebook
RISK_HISTORY = "15y"            # task pack: at least 15 years, so 2008 is covered
RISK_FREE_ANNUAL = 0.04          # PLACEHOLDER: replace with Lead-approved UK base rate / short gilt
TRADING_DAYS = 252
TRADING_DAYS_MONTH = 21
RISK_ALPHA = 0.05

CLIENT_RISK_LIMITS = pd.DataFrame([
    ("Annualised volatility", "< 15%", "Annualised standard deviation of returns"),
    ("Maximum drawdown", ">= -30%", "Worst peak-to-trough portfolio loss"),
    ("Single-stock weight", "<= 10%", "Largest individual portfolio holding"),
    ("Single-sector weight", "<= 25%", "Largest aggregate sector weight"),
    ("Beta vs FTSE 100", "0.8 to 1.1", "Portfolio sensitivity to benchmark returns"),
], columns=["Risk measure", "Client limit", "Test definition"])

display(CLIENT_RISK_LIMITS)
print("Risk-free rate currently set to", f"{RISK_FREE_ANNUAL:.2%}",
      "— confirm the correct UK rate with the Lead before final reporting.")
