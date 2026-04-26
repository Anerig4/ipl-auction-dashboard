import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from plot_utils import dark_fig, PALETTE, section_header, interp_box


def render(df):
    section_header("UNCAPPED GEMS", "High-ROI players who haven't yet earned an international cap — the best value buys")

    uncapped = df[df["Capped"] == 0].copy()

    if uncapped.empty:
        st.warning("No uncapped players found. Ensure your auction CSV has a 'Nationality' column — Indian players are treated as capped.")
        return

    q75 = uncapped["ROI"].quantile(0.75)
    gems = uncapped[uncapped["ROI"] >= q75].sort_values("ROI", ascending=False).reset_index(drop=True)

    # ── KPIs ───────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Uncapped",     len(uncapped))
    c2.metric("ROI 75th Percentile", f"{q75:.4f}")
    c3.metric("Gems Identified",    len(gems))
    c4.metric("Avg Gem Price",      f"₹{gems['Price'].mean()/1e5:.0f}L" if not gems.empty else "—")

    interp_box(
        f"These {len(gems)} uncapped players all have an ROI at or above the 75th percentile "
        f"({q75:.3f}) among overseas/uncapped players — strong performance for a relatively low price.",
        kind="good"
    )

    st.markdown("---")

    # ── bar chart ──────────────────────────────────────────────────
    st.markdown("### 💎 Uncapped Gems — ROI Chart")
    fig, ax = dark_fig(max(10, len(gems) * 0.7 + 2), 5)
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(gems))]
    ax.bar(gems["Player"], gems["ROI"], color=colors, edgecolor="#0d1117", zorder=3)
    ax.axhline(q75, color="#38bdf8", linestyle="--", lw=1.5,
               label=f"Q75 threshold = {q75:.3f}")
    ax.set_xticklabels(gems["Player"], rotation=45, ha="right", fontsize=8.5)
    ax.set_ylabel("ROI")
    ax.set_title("Uncapped Gems — ROI ≥ 75th Percentile", pad=10)
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    st.markdown("---")

    # ── scatter: price vs ROI ──────────────────────────────────────
    st.markdown("### 🔍 Price vs ROI — Uncapped Players")
    fig, ax = dark_fig(9, 5)
    scatter = ax.scatter(
        uncapped["Price"] / 1e5, uncapped["ROI"],
        c=[PALETTE[0] if r >= q75 else PALETTE[3] for r in uncapped["ROI"]],
        s=80, alpha=0.8, edgecolors="#0d1117", linewidths=0.5, zorder=3
    )
    ax.axhline(q75, color="#38bdf8", linestyle="--", lw=1.2, label=f"Q75 = {q75:.3f}")
    for _, row in gems.iterrows():
        ax.annotate(row["Player"], (row["Price"]/1e5, row["ROI"]),
                    fontsize=6.5, color="#e6edf3", alpha=0.85,
                    xytext=(4, 4), textcoords="offset points")
    ax.set_xlabel("Price (₹ Lakhs)")
    ax.set_ylabel("ROI")
    ax.set_title("Price vs ROI — Uncapped Players", pad=10)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.25)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    st.markdown("---")

    # ── table ──────────────────────────────────────────────────────
    st.markdown("### 📋 Gems Table")
    show = [c for c in ["Player","Team","Role","Price","ROI","Performance_Score",
                         "Runs_per_match","Wickets_per_match"] if c in gems.columns]
    st.dataframe(
        gems[show].style
                  .background_gradient(subset=["ROI"], cmap="YlGn")
                  .format({"Price":"₹{:.0f}","ROI":"{:.4f}",
                           "Performance_Score":"{:.2f}",
                           "Runs_per_match":"{:.2f}","Wickets_per_match":"{:.3f}"}),
        use_container_width=True, hide_index=True
    )
