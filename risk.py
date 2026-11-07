print("Saved:", sorted(os.listdir(path("charts"))))
print("CSVs:", [f for f in os.listdir(OUT_DIR) if f.endswith(".csv")])
