# ==== CONCENTRATION METRICS ====
def concentration_metrics(weights, sector_map=None):
    """weights: {ticker: weight} summing to 1.0. sector_map: {ticker: sector}."""
    w_ = pd.Series(weights).dropna().sort_values(ascending=False)
    out = {
        "Number of holdings": len(w_),
        "Top-5 weight": w_.head(5).sum(),
        "Largest single weight": w_.iloc[0] if len(w_) else np.nan,
        "Herfindahl index": (w_ ** 2).sum(),
    }
    if sector_map is not None:
        sectors = w_.groupby(w_.index.map(sector_map)).sum().sort_values(ascending=False)
        out["Largest sector"] = sectors.index[0]
        out["Largest sector weight"] = sectors.iloc[0]
        out["Sector weights"] = sectors.to_dict()
    return out
