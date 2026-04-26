import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from plot_utils import dark_fig, PALETTE, section_header


def render(df):
    section_header("TEAM STRATEGY BREAKDOWN", "How each franchise distributed their budget across player roles")

    sel_team = st.selectbox("Select Team", sorted(df["Team"].dropna().unique()))
    tdf = df[df["Team"] == sel_team]

    # ── team KPIs ──────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Spend",    f"₹{tdf['Price'].sum()/1e7:.1f} Cr")
    c2.metric("Players Bought", len(tdf))
    c3.metric("Avg ROI",        f"{tdf['ROI'].mean():.3f}")
    c4.metric("Top ROI Player", tdf.loc[tdf["ROI"].idxmax(), "Player"]
                                   if not tdf.empty else "—")

    st.markdown("---")

    # ── pie + histogram ────────────────────────────────────────────
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("### 🥧 Budget Split by Role")
        role_budget = tdf.groupby("Role")["Price"].sum() / 1e7
        if role_budget.empty:
            st.info("No role data available.")
        else:
            fig, ax = dark_fig(6, 5)
            wedges, texts, autotexts = ax.pie(
                role_budget.values, labels=role_budget.index,
                autopct="%1.1f%%", colors=PALETTE[:len(role_budget)],
                startangle=90, pctdistance=0.75,
                wedgeprops={"edgecolor":"#0d1117","linewidth":1.5}
            )
            for t in texts:    t.set_color("#e6edf3"); t.set_fontsize(9)
            for at in autotexts: at.set_color("#0d1117"); at.set_fontsize(8)
            ax.set_title(f"{sel_team} — Role Spend", pad=12)
            plt.tight_layout()
            st.pyplot(fig); plt.close()

    with col_r:
        st.markdown("### 📊 Price Histogram by Role")
        fig, ax = dark_fig(6, 5)
        for i, role in enumerate(tdf["Role"].dropna().unique()):
            vals = tdf[tdf["Role"] == role]["Price"] / 1e5
            ax.hist(vals, bins=8, alpha=0.75, label=role,
                    color=PALETTE[i % len(PALETTE)], edgecolor="#0d1117")
        ax.set_xlabel("Price (₹ Lakhs)")
        ax.set_ylabel("Players")
        ax.set_title("Price Distribution by Role", pad=12)
        ax.legend(fontsize=9)
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    st.markdown("---")

    # ── player ROI bar ─────────────────────────────────────────────
    st.markdown("### 📈 Player ROI — Team View")
    sorted_t = tdf.sort_values("ROI", ascending=False)
    med_roi  = tdf["ROI"].median()
    bar_colors = [PALETTE[0] if r >= med_roi else PALETTE[1] for r in sorted_t["ROI"]]

    fig, ax = dark_fig(12, 4)
    ax.bar(sorted_t["Player"], sorted_t["ROI"], color=bar_colors, edgecolor="#0d1117")
    ax.axhline(med_roi, color="#38bdf8", linestyle="--", lw=1.5,
               label=f"Median ROI = {med_roi:.3f}")
    ax.set_xticklabels(sorted_t["Player"], rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("ROI")
    ax.set_title(f"{sel_team} · Player ROI", pad=10)
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    st.markdown("---")

    # ── full player table ──────────────────────────────────────────
    st.markdown("### 🗃️ Full Player Table")
    show = [c for c in ["Player","Role","Price","Runs_per_match",
                         "Wickets_per_match","Performance_Score","ROI","Capped"]
            if c in tdf.columns]
    st.dataframe(
        tdf[show].sort_values("ROI", ascending=False)
                 .reset_index(drop=True)
                 .style.background_gradient(subset=["ROI"], cmap="RdYlGn")
                 .format({"Price":"₹{:.0f}","ROI":"{:.4f}",
                          "Runs_per_match":"{:.2f}","Wickets_per_match":"{:.3f}",
                          "Performance_Score":"{:.2f}"}),
        use_container_width=True, hide_index=True
    )
