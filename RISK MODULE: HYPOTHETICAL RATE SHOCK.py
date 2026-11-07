# ==== HYPOTHETICAL RATE SHOCK (+200bp) ====
# Assumption: a +200bp parallel shift in rates. Each sector's price change is
# approximated by a fixed sensitivity, based on duration-like behaviour:
#   - Utilities: bond-proxy, long duration, most sensitive
#   - Technology: long-duration growth, high multiple compression
#   - Consumer Cyclical: rate-sensitive via consumer credit
#   - Financial Services: mixed (banks gain on NIM, insurers lose on bonds)
#   - Industrials: moderate
#   - Energy: least sensitive, real-asset backing
# These are rough, clearly labelled, and not derived from a model.
RATE_SHOCK_SENSITIVITY = {
    "Utilities":          -0.10,
    "Technology":         -0.09,
    "Consumer Cyclical":  -0.06,
    "Financial Services": -0.04,
    "Industrials":        -0.05,
    "Energy":             -0.03,
    "Basic Materials":    -0.05,   # cyclical, moderate (Rio Tinto)
}

def rate_shock_impact(weights, sector_map, sensitivities=RATE_SHOCK_SENSITIVITY):
    """Portfolio-level return from a +200bp rate shock, plus per-sector detail."""
    w_ = pd.Series(weights).dropna()
    sectors = w_.groupby(w_.index.map(sector_map)).sum()
    missing = [s for s in sectors.index if s not in sensitivities]
    assert not missing, f"No rate-shock sensitivity for: {missing}"   # never silently drop a sector

    rows = []
    for sector, weight in sectors.items():
        sens = sensitivities.get(sector, np.nan)
        rows.append({
            "Sector": sector,
            "Weight": weight,
            "Sensitivity": sens,
            "Contribution": weight * sens,
        })

    detail = pd.DataFrame(rows).sort_values("Contribution")
    total = detail["Contribution"].sum()
    return total, detail
