def plot(results_df, gap_df, base_eve, base_nii, d_a, d_l, doe):
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.3, "grid.linestyle": "--",
    })
    NAVY = "#1a3a5c"; BLUE = "#1a5276"; RED = "#c0392b"
    AMBER = "#d4ac0d"; GREEN = "#1e8449"

    def bar_cols(vals):
        return [BLUE if v >= 0 else RED for v in vals]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        "IRRBB Sensitivity Analysis — Stylised Indian Bank (RBI Rate Environment, Dec 2024)\n"
        "Amortising CFs  |  Deposit Betas  |  Behavioural Deposit Bucketing",
        fontsize=12, fontweight="bold", y=0.98)

    scenarios = results_df["Scenario"]
    x = np.arange(len(scenarios))

    # ΔEVE
    ax = axes[0, 0]
    vals = results_df["ΔEVE (₹ Cr)"].values
    bars = ax.bar(x, vals, color=bar_cols(vals), edgecolor="white")
    ax.axhline(0, color="black", lw=0.8)
    ax.set_title("Change in Economic Value of Equity (ΔEVE)", fontweight="bold")
    ax.set_ylabel("₹ Crores")
    ax.set_xticks(x); ax.set_xticklabels(scenarios, rotation=30, ha="right", fontsize=8.5)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + (80 if val >= 0 else -280),
                f"₹{val:,.0f}", ha="center", fontsize=7.5, fontweight="bold")

    # ΔNII
    ax = axes[0, 1]
    vals = results_df["ΔNII (₹ Cr)"].values
    bars = ax.bar(x, vals, color=bar_cols(vals), edgecolor="white")
    ax.axhline(0, color="black", lw=0.8)
    ax.set_title("Change in NII — 1Y Horizon, Deposit Betas Applied", fontweight="bold")
    ax.set_ylabel("₹ Crores")
    ax.set_xticks(x); ax.set_xticklabels(scenarios, rotation=30, ha="right", fontsize=8.5)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + (5 if val >= 0 else -25),
                f"₹{val:,.0f}", ha="center", fontsize=7.5, fontweight="bold")

    # Repricing gap
    ax  = axes[1, 0]
    ax2 = ax.twinx()
    bx  = np.arange(len(BUCKETS))
    ax.bar(bx - 0.2, gap_df["Assets (₹ Cr)"].values,      0.35, label="Assets",      color=NAVY,  alpha=0.85, edgecolor="white")
    ax.bar(bx + 0.2, gap_df["Liabilities (₹ Cr)"].values, 0.35, label="Liabilities",  color=AMBER, alpha=0.85, edgecolor="white")
    ax2.plot(bx, gap_df["Cumulative Gap (₹ Cr)"].values, "o--", color=RED, lw=1.8, markersize=5, label="Cumulative Gap")
    ax2.set_ylabel("Cumulative Gap (₹ Cr)", color=RED)
    ax2.tick_params(axis="y", labelcolor=RED)
    ax2.spines["top"].set_visible(False)
    ax.set_title("Repricing Gap — Behavioural Bucketing", fontweight="bold")
    ax.set_ylabel("₹ Crores"); ax.set_xticks(bx); ax.set_xticklabels(BUCKETS)
    ax.legend(loc="upper left", fontsize=8)

    # Duration comparison v1 vs v2
    ax = axes[1, 1]
    labels  = ["Asset Duration", "Liability Duration", "Duration of Equity"]
    v1_vals = [5.87, 1.26, 40.81]
    v2_vals = [d_a, d_l, doe]
    bx = np.arange(3)
    ax.bar(bx - 0.2, v1_vals, 0.35, label="v1 (Bullet)",          color=AMBER, alpha=0.75, edgecolor="white")
    ax.bar(bx + 0.2, v2_vals, 0.35, label="v2 (Amortising+Beta)", color=BLUE,  alpha=0.85, edgecolor="white")
    ax.set_title("Duration Comparison: Bullet vs Amortising", fontweight="bold")
    ax.set_ylabel("Years"); ax.set_xticks(bx); ax.set_xticklabels(labels, fontsize=9)
    ax.legend(fontsize=9)
    for bar, val in zip(ax.patches[:3], v1_vals):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.3, f"{val:.1f}y", ha="center", fontsize=8)
    for bar, val in zip(ax.patches[3:], v2_vals):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.3, f"{val:.1f}y", ha="center", fontsize=8)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/irrbb_charts.png", dpi=160, bbox_inches="tight")
    plt.close()
    print("Charts saved.")
