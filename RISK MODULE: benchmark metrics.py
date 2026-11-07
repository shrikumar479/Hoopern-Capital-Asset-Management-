# ==== RISK MODULE: benchmark metrics, VaR/CVaR and rolling volatility ====
benchmark_summary = pd.DataFrame([risk_summary(
    risk_benchmark_returns, label="FTSE 100 proxy (ISF.L)"
)])
display(benchmark_summary.style.format({
    "Annualised return (CAGR)": "{:.2%}",
    "Annualised volatility": "{:.2%}",
    "Sharpe": "{:.2f}",
    "Sortino": "{:.2f}",
    "Maximum drawdown": "{:.2%}",
}))

var_table = pd.DataFrame({
    "1 trading day": var_cvar(risk_benchmark_returns, horizon_days=1),
    "1 month (21 trading days)": var_cvar(risk_benchmark_returns, horizon_days=TRADING_DAYS_MONTH)
}).T
display(var_table.style.format({
    "Historical VaR": "{:.2%}",
    "Historical CVaR": "{:.2%}",
    "Parametric VaR (normal)": "{:.2%}",
    "Parametric CVaR (normal)": "{:.2%}",
    "Observations": "{:.0f}"
}))

risk_rolling_vol_12m = risk_benchmark_returns.rolling(TRADING_DAYS).std() * np.sqrt(TRADING_DAYS)
fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(risk_rolling_vol_12m.index, risk_rolling_vol_12m, label="Rolling 12-month annualised volatility")
ax.axhline(VOL_LIMIT, linestyle="--", color="black", lw=1, label=f"Client volatility limit ({VOL_LIMIT:.0%})")
ax.set_title("FTSE 100 proxy — rolling 12-month volatility")
ax.set_ylabel("Annualised volatility")
ax.legend()
ax.grid(True, alpha=0.25)
plt.show()
