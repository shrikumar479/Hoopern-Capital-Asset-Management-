# Holdings, weights and sectors all come from `w` (Night 2 weights cell) – nothing hard-coded
SECTOR_MAP = w["sector"].to_dict()
weights    = w["weight"].to_dict()
holdings   = w.index.tolist()
assert len(holdings) == 15 and abs(sum(weights.values()) - 1) < 1e-6
concentration_metrics(weights, SECTOR_MAP)
