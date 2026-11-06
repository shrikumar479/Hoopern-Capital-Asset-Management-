# ==== RISK MODULE: setup and client limits (single source of truth) ====
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.stats import norm
from IPython.display import display

RISK_BENCH_TICKER = "ISF.L"     # FTSE 100 total-return proxy – used for EVERYTHING (metrics, beta, charts)
GFC_BENCH_TICKER  = "^FTSE"     # only for the 2007-09 GFC window, which ISF.L data on Yahoo doesn't cover
EURO_BENCH_TICKER = "^STOXX50E" # extra beta for ASML (euro stock, euro DCF inputs)
RISK_HISTORY = "15y"
RISK_FREE_ANNUAL = RISK_FREE    # same rate as the backtest (set once in the Night 2 settings cell)
TRADING_DAYS = 252
TRADING_DAYS_MONTH = 21
RISK_ALPHA = 0.05

# ---- Client limits: CONFIRM VOL_LIMIT AGAINST THE BRIEF (earlier versions used both 15% and 20%) ----
VOL_LIMIT = 0.20
DD_LIMIT = -0.30
STOCK_LIMIT = 0.10
SECTOR_LIMIT = 0.25
BETA_RANGE = (0.8, 1.1)

CLIENT_RISK_LIMITS = pd.DataFrame([
    ("Annualised volatility", f"< {VOL_LIMIT:.0%}", "Annualised standard deviation of returns"),
    ("Maximum drawdown", f">= {DD_LIMIT:.0%}", "Worst peak-to-trough portfolio loss"),
    ("Single-stock weight", f"<= {STOCK_LIMIT:.0%}", "Largest individual portfolio holding"),
    ("Single-sector weight", f"<= {SECTOR_LIMIT:.0%}", "Largest aggregate sector weight"),
    ("Beta vs FTSE 100", f"{BETA_RANGE[0]} to {BETA_RANGE[1]}", "Portfolio sensitivity to benchmark returns"),
], columns=["Risk measure", "Client limit", "Test definition"])

display(CLIENT_RISK_LIMITS)
print(f"Risk-free rate: {RISK_FREE_ANNUAL:.2%} | benchmark: {RISK_BENCH_TICKER} | volatility limit: {VOL_LIMIT:.0%}")
