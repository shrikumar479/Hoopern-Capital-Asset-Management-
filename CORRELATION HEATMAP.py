# ==== CORRELATION HEATMAP ====
# read the cleaned GBP prices from file, so this works even if Night 1 wasn't run in this session
px_heat = pd.read_csv(path("prices_gbp.csv"), index_col=0, parse_dates=True)[holdings]
stock_rets = px_heat.pct_change(fill_method=None).dropna()
stock_rets = stock_rets[stock_rets.index >= stock_rets.index[-1] - pd.DateOffset(years=3)]   # last 3 years
corr = stock_rets.corr()

fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(corr, cmap="RdYlGn_r", vmin=-1, vmax=1)
fig.colorbar(im, ax=ax, shrink=0.8)
ax.set_xticks(range(len(corr))); ax.set_xticklabels(corr.columns, rotation=90)
ax.set_yticks(range(len(corr))); ax.set_yticklabels(corr.columns)
ax.set_title("Correlation of holdings (3Y daily returns)", loc="left", fontweight="bold")
fig.tight_layout()
fig.savefig(path("charts/correlation_heatmap.png"), dpi=300, bbox_inches="tight")   # save ONCE, before show
plt.show()
