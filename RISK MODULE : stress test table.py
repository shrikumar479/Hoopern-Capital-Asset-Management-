def stress_test_table_with_shock(portfolio_returns, benchmark_returns,
                                 weights, sector_map, windows=STRESS_WINDOWS):
    table = stress_test_table(portfolio_returns, benchmark_returns, windows)
    shock, _ = rate_shock_impact(weights, sector_map)
    extra = pd.DataFrame([{
        "Scenario": "Hypothetical +200bp rates",
        "Portfolio": shock,
        "Benchmark": np.nan,
        "Difference": np.nan,
    }])
    return pd.concat([table, extra], ignore_index=True)
