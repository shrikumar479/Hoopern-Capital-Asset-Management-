# ==== STRESS TEST WINDOWS (the ONLY definition – don't redefine later) ====
STRESS_WINDOWS = {
    "Global Financial Crisis": ("2007-10-01", "2009-03-31"),
    "COVID crash":             ("2020-02-19", "2020-03-23"),
    "2022 rate shock":         ("2022-01-01", "2022-10-31"),
    "Mini-budget gilt crisis": ("2022-09-01", "2022-10-31"),
}

def stress_window_returns(returns, windows=STRESS_WINDOWS):
    """Cumulative return in each hard-coded window, for one returns series."""
    r = pd.Series(returns).dropna()
    r.index = pd.to_datetime(r.index)
    out = {}
    for name, (start, end) in windows.items():
        window = r.loc[start:end]
        if len(window) == 0:
            out[name] = np.nan          # no data in this window
        else:
            out[name] = (1 + window).prod() - 1
    return out


def stress_test_table(portfolio_returns, benchmark_returns, windows=STRESS_WINDOWS):
    """Build the Scenario / Portfolio / Benchmark / Difference table."""
    p = stress_window_returns(portfolio_returns, windows)
    b = stress_window_returns(benchmark_returns, windows)
    rows = []
    for name in windows:
        rows.append({
            "Scenario":  name,
            "Portfolio": p[name],
            "Benchmark": b[name],
            "Difference": p[name] - b[name],
        })
    return pd.DataFrame(rows)
