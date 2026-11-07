# ==== ROLLING VOLATILITY (63-day) ====
roll = 63
roll_port  = port_ret.rolling(roll).std()  * np.sqrt(TRADING_DAYS)
roll_bench = bench_ret.rolling(roll).std() * np.sqrt(TRADING_DAYS)

fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(roll_port,  label="Portfolio", color=COLOR_PORT, lw=1.2)
ax.plot(roll_bench, label="FTSE 100 (ISF.L)",     color=COLOR_BENCH, lw=1.2, alpha=0.8)
ax.axhline(VOL_LIMIT, color="black", ls="--", lw=1, label=f"Client limit ({VOL_LIMIT:.0%})")
ax.set_title("Rolling 63-day annualised volatility", loc="left", fontweight="bold")
ax.set_ylabel("Annualised volatility")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))
ax.legend(loc="upper left", frameon=False)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(path("charts/rolling_volatility.png"), dpi=300, bbox_inches="tight")
plt.show()
