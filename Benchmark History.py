# ==== Long benchmark history for the GFC window only ====
# ISF.L data on Yahoo starts in 2009, so the 2007-09 crisis uses the FTSE 100 price index (^FTSE).
# Separate variable names so the backtest's `px` and the canonical `bench_ret` are never overwritten.
_raw = yf.download(GFC_BENCH_TICKER, start="2005-01-01", auto_adjust=True, progress=False)["Close"]
bench_long = _raw.squeeze().pct_change().dropna()
bench_long.index = pd.to_datetime(bench_long.index).tz_localize(None)
print(GFC_BENCH_TICKER, "from", bench_long.index.min().date(), "to", bench_long.index.max().date())
