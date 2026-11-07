# ==== RISK MODULE: four required stress windows ====
# (STRESS_WINDOWS is defined once, earlier.)

def stress_period_report(returns, windows=STRESS_WINDOWS):
    r = pd.Series(returns).dropna()
    rows = []
    for event, (start, end) in windows.items():
        period = r.loc[pd.Timestamp(start):pd.Timestamp(end)]
        if period.empty:
            rows.append({"Event": event, "Start": start, "End": end,
                         "Trading days": 0, "Period return": np.nan,
                         "Annualised volatility": np.nan, "Maximum drawdown": np.nan})
            continue
        rows.append({
            "Event": event, "Start": start, "End": end,
            "Trading days": len(period),
            "Period return": (1 + period).prod() - 1,
            "Annualised volatility": annualised_volatility(period),
            "Maximum drawdown": maximum_drawdown(period)
        })
    return pd.DataFrame(rows)

benchmark_stress = stress_period_report(risk_benchmark_returns)
display(benchmark_stress.style.format({
    "Period return": "{:.2%}",
    "Annualised volatility": "{:.2%}",
    "Maximum drawdown": "{:.2%}"
}))
