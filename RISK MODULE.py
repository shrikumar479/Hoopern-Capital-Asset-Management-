total, detail = rate_shock_impact(weights, SECTOR_MAP)
print(f"Portfolio impact from +200bp: {total:.2%}")
print(detail.to_string(index=False))
