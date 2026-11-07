# ==== STRESS TESTS (robust) ====
stress = stress_test_table(port_ret, bench_ret, windows=STRESS_WINDOWS)

port_beta = beta_vs_benchmark(port_ret, bench_ret)

# Compute GFC straight from bench_long — no key matching needed
gfc_bench = (1 + bench_long.loc["2007-10-01":"2009-03-31"]).prod() - 1
gfc_est   = port_beta * gfc_bench
print(f"GFC benchmark {gfc_bench:.2%} x beta {port_beta:.3f} = {gfc_est:.2%}")

# Fill the GFC row by NAME (portfolio data starts 2016, so the GFC is estimated)
gfc = stress["Scenario"] == "Global Financial Crisis"
assert gfc.sum() == 1, "GFC row not found – check STRESS_WINDOWS keys"
stress.loc[gfc, "Portfolio"]  = gfc_est
stress.loc[gfc, "Benchmark"]  = gfc_bench
stress.loc[gfc, "Difference"] = gfc_est - gfc_bench
stress["Method"] = np.where(gfc, "Estimated (beta x FTSE 100 price index)", "Historical")
shock, _ = rate_shock_impact(weights, SECTOR_MAP)
stress = pd.concat([stress, pd.DataFrame([{"Scenario": "Hypothetical +200bp rates", "Portfolio": shock,
                    "Benchmark": np.nan, "Difference": np.nan, "Method": "Sector sensitivities (judgement)"}])],
                   ignore_index=True)
stress.to_csv(path("stress_tests.csv"), index=False)
stress
