# ==== RISK MODULE: five-year monthly beta for the two DCF stocks ====
DCF_TICKERS = ["RR.L", "ASML.AS"]

def five_year_monthly_beta(stock_ticker, benchmark_ticker):
    """benchmark_ticker is REQUIRED – no hidden default, so the result never depends on cell order."""
    raw = yf.download([stock_ticker, benchmark_ticker], period="5y",
                      interval="1mo", auto_adjust=True, progress=False, actions=False)["Close"]
    if isinstance(raw, pd.Series):
        raise ValueError("Yahoo Finance returned unexpected data; check the ticker symbols.")
    if stock_ticker not in raw.columns or benchmark_ticker not in raw.columns:
        raise ValueError("One or both tickers are missing from the downloaded data.")
    monthly_returns = raw[[stock_ticker, benchmark_ticker]].pct_change(fill_method=None).dropna()
    if len(monthly_returns) < 24:
        raise ValueError(f"Only {len(monthly_returns)} matched monthly returns; check data availability.")
    bad = monthly_returns[(monthly_returns.abs() > 0.40).any(axis=1)]
    if len(bad):
        print(f"WARNING {stock_ticker}: monthly move over 40% – check for a data error before using this beta:")
        print(bad.round(3))
    beta = beta_vs_benchmark(monthly_returns[stock_ticker], monthly_returns[benchmark_ticker])
    return beta, len(monthly_returns), monthly_returns

beta_rows = []
for ticker in DCF_TICKERS:
    b, n, _ = five_year_monthly_beta(ticker, RISK_BENCH_TICKER)
    beta_rows.append({"DCF stock": ticker, "Benchmark": f"FTSE 100 ({RISK_BENCH_TICKER})",
                      "5-year monthly beta": b, "Matched monthly observations": n})
b, n, _ = five_year_monthly_beta("ASML.AS", EURO_BENCH_TICKER)
beta_rows.append({"DCF stock": "ASML.AS", "Benchmark": f"Euro Stoxx 50 ({EURO_BENCH_TICKER})",
                  "5-year monthly beta": b, "Matched monthly observations": n})
dcf_beta_results = pd.DataFrame(beta_rows)
display(dcf_beta_results)
dcf_beta_results.to_csv(path("dcf_stock_betas.csv"), index=False)
print("Saved dcf_stock_betas.csv – send to the DCF lead (RR uses the FTSE 100 beta; ASML: group to choose).")
