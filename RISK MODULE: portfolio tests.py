# ==== RISK MODULE: portfolio tests (runs when Night 2 return file exists) ====
# The group's existing Night 2 notebook saves portfolio_daily_returns.csv.
# If it is not present yet, this cell safely explains what is still needed.
portfolio_file = path("portfolio_daily_returns.csv")

if os.path.exists(portfolio_file):
    risk_portfolio = pd.read_csv(portfolio_file, index_col=0, parse_dates=True).iloc[:, 0]
    risk_pair = pd.concat([risk_portfolio.rename("portfolio"),
                           risk_benchmark_returns.rename("benchmark")], axis=1).dropna()

    portfolio_summary = pd.DataFrame([
        risk_summary(risk_pair["portfolio"], risk_pair["benchmark"], "Portfolio"),
        risk_summary(risk_pair["benchmark"], risk_pair["benchmark"], "FTSE 100 proxy (ISF.L)")
    ])
    display(portfolio_summary)

    portfolio_var = pd.DataFrame({
        "1 trading day": var_cvar(risk_pair["portfolio"], horizon_days=1),
        "1 month (21 trading days)": var_cvar(risk_pair["portfolio"], horizon_days=TRADING_DAYS_MONTH)
    }).T
    display(portfolio_var)

    portfolio_stress = stress_period_report(risk_pair["portfolio"])
    display(portfolio_stress)

    # Portfolio drawdown chart
    dd = drawdown_series(risk_pair["portfolio"])
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(dd.index, dd, label="Portfolio drawdown")
    ax.axhline(-0.30, linestyle="--", label="Client maximum drawdown limit (-30%)")
    ax.set_title("Portfolio drawdown")
    ax.set_ylabel("Drawdown")
    ax.legend()
    ax.grid(True, alpha=0.25)
    plt.show()
else:
    print("Portfolio return file not found yet.")
    print("Run the group's Night 2 portfolio backtest first; it should create:")
    print(portfolio_file)
    print("Then re-run this cell to calculate portfolio beta, tracking error, risk ratios, VaR/CVaR and stress results.")
