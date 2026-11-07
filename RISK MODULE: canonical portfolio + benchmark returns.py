# ==== RISK MODULE: canonical portfolio + benchmark returns, VaR/CVaR, stress-period detail ====
# One pair of return series for every risk number: Night 2's backtest (net of costs) vs ISF.L.
port_ret  = pd.read_csv(path("portfolio_daily_returns.csv"), index_col=0, parse_dates=True).squeeze()
bench_ret = pd.read_csv(path("benchmark_daily_returns.csv"), index_col=0, parse_dates=True).squeeze()
assert port_ret.index.equals(bench_ret.index), "portfolio and benchmark dates don't match"
print(port_ret.shape, port_ret.index.min().date(), "to", port_ret.index.max().date())

portfolio_var = pd.DataFrame({
    "1 trading day": var_cvar(port_ret, horizon_days=1),
    "1 month (21 trading days)": var_cvar(port_ret, horizon_days=TRADING_DAYS_MONTH)
}).T
display(portfolio_var)

portfolio_stress = stress_period_report(port_ret)
display(portfolio_stress)
