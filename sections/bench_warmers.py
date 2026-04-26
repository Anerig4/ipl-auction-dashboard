import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from plot_utils import dark_fig, PALETTE, section_header, interp_box


def render(df):
    section_header("BENCH WARMERS · MONEY WASTED", "High-cost players who delivered poor ROI — budget inefficiencies by team")

    med_price = df["Price"].median()
    q25_roi   = df["ROI"].quantile(0.25)
    bench     = df[(df["Price"] > med_price) & (df["ROI"] < q25_roi)].copy()

    # ── KPIs ───────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Median Price Threshold", f"₹{med_price/1e5:.0f}L")
    c2.metric("ROI 25th Percentile",    f"{q25_roi:.4f}")
    c3.metric("Bench Warmers Found",    len(bench))
    c4.metric("Total Wasted Budget",    f"₹{bench['Price'].sum()/1e7:.1f} Cr")

    interp_box(
        f"These {len(bench)} players were bought above the median price "
        f"(₹{med_price/1e5:.0f}L) but returned an ROI below the 25th percentile "
        f"({q25_roi:.3f}) — representing poor value for money.",
        kind="bad"
    )

    st.markdown("---")

    # ── team-wise wasted budget bar ────────────────────────────────
    st.markdown("### 💸 Team-wise Wasted Budget")
    wasted = bench.groupby("Team")["Price"].sum().sort_values(ascending=False) / 1e7

    if wasted.empty:
        st.info("No bench warmers found with current thresholds.")
        return

    fig, ax = dark_fig(11, 5)
    bars = ax.bar(wasted.index, wasted.values,
                  color=PALETTE[1], edgecolor="#0d1117", zorder=3)
    for bar, val in zip(bars, wasted.values):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.05,
                f"₹{val:.1f}Cr", ha="center", fontsize=9, color="#e6edf3")
    ax.set_xticklabels(wasted.index, rotation=45, ha="right", fontsize=9)
    ax.set_ylabel("Wasted Budget (₹ Cr)")
    ax.set_title("Budget Waste by Team  (High Price + Low ROI)", pad=10)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    st.markdown("---")

    # ── scatter: price vs ROI with bench highlighted ───────────────
    st.markdown("### 🔍 All Players — Price vs ROI (Bench Warmers Highlighted)")
    fig, ax = dark_fig(11, 5)

    non_bench = df[~df.index.isin(bench.index)]
    ax.scatter(non_bench["Price"]/1e5, non_bench["ROI"],
               color=PALETTE[2], alpha=0.5, s=50,
               edgecolors="#0d1117", linewidths=0.4, label="Others", zorder=2)
    ax.scatter(bench["Price"]/1e5, bench["ROI"],
               color=PALETTE[1], alpha=0.85, s=80,
               edgecolors="#0d1117", linewidths=0.5, label="Bench Warmers", zorder=3)

    ax.axvline(med_price/1e5, color="#f5a623", linestyle="--", lw=1.2,
               label=f"Median Price = ₹{med_price/1e5:.0f}L")
    ax.axhline(q25_roi, color="#38bdf8", linestyle="--", lw=1.2,
               label=f"ROI Q25 = {q25_roi:.3f}")

    ax.set_xlabel("Price (₹ Lakhs)")
    ax.set_ylabel("ROI")
    ax.set_title("Price vs ROI — Bench Warmers in Red", pad=10)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    st.markdown("---")

    # ── table ──────────────────────────────────────────────────────
    st.markdown("### 📋 Bench Warmers Table")
    show = [c for c in ["Player","Team","Role","Price","ROI",
                         "Performance_Score","Runs_per_match","Wickets_per_match"]
            if c in bench.columns]
    st.dataframe(
        bench[show].sort_values("Price", ascending=False)
                   .reset_index(drop=True)
                   .style.background_gradient(subset=["ROI"], cmap="RdYlGn")
                   .format({"Price":"₹{:.0f}","ROI":"{:.4f}",
                            "Performance_Score":"{:.2f}",
                            "Runs_per_match":"{:.2f}","Wickets_per_match":"{:.3f}"}),
        use_container_width=True, hide_index=True
    )
