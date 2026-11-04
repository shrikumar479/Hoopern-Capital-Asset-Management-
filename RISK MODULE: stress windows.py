# ==== RISK MODULE: four required stress windows ====
STRESS_WINDOWS = {
    "Global Financial Crisis": ("2007-10-01", "2009-03-31"),
    "COVID crash": ("2020-02-19", "2020-03-23"),
    "2022 rate shock": ("2022-01-01", "2022-10-31"),
    "Mini-budget gilt crisis": ("2022-09-01", "2022-10-31"),
}

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
