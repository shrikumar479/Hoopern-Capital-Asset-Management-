# ==== RISK MODULE: download 15+ years of benchmark prices ====
risk_raw = yf.download(
    RISK_BENCH_TICKER, period=RISK_HISTORY, auto_adjust=True,
    progress=False, actions=False
)

if risk_raw.empty:
    raise RuntimeError("No benchmark data downloaded. Check the ticker / internet connection and try again.")

risk_close = risk_raw["Close"]
if isinstance(risk_close, pd.DataFrame):
    risk_close = risk_close.iloc[:, 0]
risk_close.index = pd.to_datetime(risk_close.index).tz_localize(None)
risk_close = risk_close.dropna().sort_index()
risk_benchmark_returns = risk_close.pct_change(fill_method=None).dropna().rename("benchmark_return")

print("Benchmark:", RISK_BENCH_TICKER, "(FTSE 100 ETF total-return proxy)")
print("Price history:", risk_close.index.min().date(), "to", risk_close.index.max().date())
print("Years of data:", round((risk_close.index.max() - risk_close.index.min()).days / 365.25, 1))
display(risk_close.tail())
