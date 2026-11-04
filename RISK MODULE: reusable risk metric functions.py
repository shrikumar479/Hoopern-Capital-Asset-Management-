# ==== RISK MODULE: reusable risk metric functions ====
def annualised_volatility(returns, periods=TRADING_DAYS):
    r = pd.Series(returns).dropna()
    return r.std(ddof=1) * np.sqrt(periods)

def beta_vs_benchmark(asset_returns, benchmark_returns):
    pair = pd.concat([pd.Series(asset_returns, name="asset"),
                      pd.Series(benchmark_returns, name="benchmark")], axis=1).dropna()
    if len(pair) < 2 or pair["benchmark"].var(ddof=1) == 0:
        return np.nan
    return pair["asset"].cov(pair["benchmark"]) / pair["benchmark"].var(ddof=1)

def tracking_error(asset_returns, benchmark_returns, periods=TRADING_DAYS):
    pair = pd.concat([pd.Series(asset_returns, name="asset"),
                      pd.Series(benchmark_returns, name="benchmark")], axis=1).dropna()
    active = pair["asset"] - pair["benchmark"]
    return active.std(ddof=1) * np.sqrt(periods)

def sharpe_ratio(returns, risk_free_annual=RISK_FREE_ANNUAL, periods=TRADING_DAYS):
    r = pd.Series(returns).dropna()
    rf_daily = (1 + risk_free_annual) ** (1 / periods) - 1
    excess = r - rf_daily
    if excess.std(ddof=1) == 0:
        return np.nan
    return (excess.mean() / excess.std(ddof=1)) * np.sqrt(periods)

def sortino_ratio(returns, risk_free_annual=RISK_FREE_ANNUAL, periods=TRADING_DAYS):
    r = pd.Series(returns).dropna()
    rf_daily = (1 + risk_free_annual) ** (1 / periods) - 1
    downside = np.minimum(r - rf_daily, 0)
    downside_deviation = np.sqrt(np.mean(downside ** 2)) * np.sqrt(periods)
    annual_excess = (1 + r).prod() ** (periods / len(r)) - 1 - risk_free_annual
    return annual_excess / downside_deviation if downside_deviation > 0 else np.nan

def drawdown_series(returns):
    r = pd.Series(returns).dropna()
    wealth = (1 + r).cumprod()
    return wealth / wealth.cummax() - 1

def maximum_drawdown(returns):
    dd = drawdown_series(returns)
    return dd.min() if len(dd) else np.nan

def var_cvar(returns, alpha=RISK_ALPHA, horizon_days=1):
    # For a 1-month horizon, compound rolling 21-trading-day returns.
    r = pd.Series(returns).dropna()
    if horizon_days == 1:
        h = r
    else:
        h = (1 + r).rolling(horizon_days).apply(np.prod, raw=True) - 1
        h = h.dropna()
    if len(h) == 0:
        return {}
    q = h.quantile(alpha)
    hist_var = -q
    hist_cvar = -h[h <= q].mean()

    mu = h.mean()
    sigma = h.std(ddof=1)
    z = norm.ppf(alpha)
    param_var = -(mu + sigma * z)
    param_cvar = -(mu - sigma * norm.pdf(z) / alpha) if sigma > 0 else -mu
    return {
        "Historical VaR": hist_var,
        "Historical CVaR": hist_cvar,
        "Parametric VaR (normal)": param_var,
        "Parametric CVaR (normal)": param_cvar,
        "Observations": len(h)
    }

def risk_summary(returns, benchmark_returns=None, label="Returns"):
    r = pd.Series(returns).dropna()
    years = len(r) / TRADING_DAYS
    cagr = (1 + r).prod() ** (1 / years) - 1 if years > 0 else np.nan
    result = {
        "Series": label,
        "Annualised return (CAGR)": cagr,
        "Annualised volatility": annualised_volatility(r),
        "Sharpe": sharpe_ratio(r),
        "Sortino": sortino_ratio(r),
        "Maximum drawdown": maximum_drawdown(r),
        "Beta vs benchmark": beta_vs_benchmark(r, benchmark_returns) if benchmark_returns is not None else np.nan,
        "Tracking error": tracking_error(r, benchmark_returns) if benchmark_returns is not None else np.nan,
    }
    return result

print("Risk calculation functions created.")
