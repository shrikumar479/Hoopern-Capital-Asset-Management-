# ==== RISK MODULE: five-year monthly beta for the two DCF stocks ====
DCF_TICKERS = ["RR.L", "ASML.AS"]

def five_year_monthly_beta(stock_ticker, benchmark_ticker=RISK_BENCH_TICKER):
    raw = yf.download(
        [stock_ticker, benchmark_ticker], period="5y",
        interval="1mo", auto_adjust=True, progress=False, actions=False
    )["Close"]
    if isinstance(raw, pd.Series):
        raise ValueError("Yahoo Finance returned unexpected data; check the ticker symbols.")
    if stock_ticker not in raw.columns or benchmark_ticker not in raw.columns:
        raise ValueError("One or both tickers are missing from the downloaded data.")
    monthly_returns = raw[[stock_ticker, benchmark_ticker]].pct_change(fill_method=None).dropna()
    if len(monthly_returns) < 24:
        raise ValueError(f"Only {len(monthly_returns)} matched monthly returns; check data availability.")
    beta = beta_vs_benchmark(monthly_returns[stock_ticker], monthly_returns[benchmark_ticker])
    return beta, len(monthly_returns), monthly_returns

if len(DCF_TICKERS) == 2:
    beta_rows = []
    for ticker in DCF_TICKERS:
        beta, observations, _ = five_year_monthly_beta(ticker)
        beta_rows.append({"DCF stock": ticker, "5-year monthly beta vs ISF.L": beta,
                          "Matched monthly observations": observations})
    dcf_beta_results = pd.DataFrame(beta_rows)
    display(dcf_beta_results)
    dcf_beta_results.to_csv(path("dcf_stock_betas.csv"), index=False)
    print("Saved dcf_stock_betas.csv — send these beta results to the DCF team.")
else:
    print("Waiting for the DCF team to confirm the two stock tickers.")
    print("Enter exactly two Yahoo Finance tickers in DCF_TICKERS, then re-run this cell.")
