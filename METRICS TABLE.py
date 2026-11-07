# ==== METRICS TABLE: the reported risk numbers, with pass/fail against all five client limits ====
port_summary  = risk_summary(port_ret,  bench_ret, label="Portfolio")
bench_summary = risk_summary(bench_ret, bench_ret, label=RISK_BENCH_TICKER)
metrics = pd.DataFrame({"Portfolio": port_summary, "Benchmark (FTSE 100, ISF.L)": bench_summary})
metrics = metrics.drop(index="Series", errors="ignore")

sector_w = w.groupby("sector")["weight"].sum()
metrics.loc["Largest single-stock weight"] = [w["weight"].max(), np.nan]
metrics.loc["Largest sector weight"] = [sector_w.max(), np.nan]

def check(name, value):
    if name == "Annualised volatility":       return value < VOL_LIMIT
    if name == "Maximum drawdown":            return value >= DD_LIMIT
    if name == "Beta vs benchmark":           return BETA_RANGE[0] <= value <= BETA_RANGE[1]
    if name == "Largest single-stock weight": return value <= STOCK_LIMIT + 1e-9
    if name == "Largest sector weight":       return value <= SECTOR_LIMIT + 1e-9
    return None

LIMITS = {"Annualised volatility": f"< {VOL_LIMIT:.0%}", "Maximum drawdown": f">= {DD_LIMIT:.0%}",
          "Beta vs benchmark": f"{BETA_RANGE[0]} - {BETA_RANGE[1]}",
          "Largest single-stock weight": f"<= {STOCK_LIMIT:.0%}", "Largest sector weight": f"<= {SECTOR_LIMIT:.0%}"}
metrics["Client limit"] = [LIMITS.get(i, "") for i in metrics.index]
metrics["Pass?"] = [("PASS" if check(i, v) else "BREACH") if check(i, v) is not None else ""
                    for i, v in metrics["Portfolio"].items()]
metrics.to_csv(path("risk_metrics.csv"))

breaches = metrics.index[metrics["Pass?"] == "BREACH"].tolist()
print("BREACHES:", breaches if breaches else "none – all five client limits met")
metrics
