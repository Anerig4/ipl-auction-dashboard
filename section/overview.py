import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from plot_utils import dark_fig, PALETTE, section_header


def render(df, points_table):
    section_header("IPL AUCTION 2023", "Complete auction intelligence — budget, roles & performance at a glance")

    # ── KPI row ────────────────────────────────────────────────────
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Players",   f"{len(df)}")
    c2.metric("Teams",           f"{df['Team'].nunique()}")
    c3.metric("Total Budget",    f"₹{df['Price'].sum()/1e7:.1f} Cr")
    c4.metric("Avg Price",       f"₹{df['Price'].mean()/1e7:.2f} Cr")
    c5.metric("Mean ROI",        f"{df['ROI'].mean():.3f}")
    c6.metric("Matched Stats",   f"{(df['Matches']>0).sum()}/{len(df)}")

    st.markdown("---")

    # ── row 1: team spend + role pie ──────────────────────────────
    col_l, col_r = st.columns([1.6, 1])

    with col_l:
        st.markdown("### 💸 Team-wise Auction Spend")
        team_spend = df.groupby("Team")["Price"].sum().sort_values() / 1e7
        fig, ax = dark_fig(9, 5)
        colors = [PALETTE[i % len(PALETTE)] for i in range(len(team_spend))]
        bars = ax.barh(team_spend.index, team_spend.values,
                       color=colors, edgecolor="#0d1117", height=0.65)
        for bar in bars:
            ax.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height()/2,
                    f"₹{bar.get_width():.1f}Cr", va="center", fontsize=8, color="#8b949e")
        ax.set_xlabel("Total Spend (₹ Cr)")
        ax.set_title("Auction Budget by Team", pad=10)
        ax.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    with col_r:
        st.markdown("### 🎭 Role Distribution")
        role_counts = df["Role"].value_counts()
        fig, ax = dark_fig(5, 5)
        wedges, texts, autotexts = ax.pie(
            role_counts.values, labels=role_counts.index,
            autopct="%1.1f%%", colors=PALETTE[:len(role_counts)],
            pctdistance=0.78, startangle=120,
            wedgeprops={"edgecolor":"#0d1117","linewidth":1.5}
        )
        for t in texts:    t.set_color("#8b949e"); t.set_fontsize(9)
        for at in autotexts: at.set_color("#0d1117"); at.set_fontsize(8); at.set_fontweight("bold")
        ax.set_title("Players by Role", pad=12)
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    st.markdown("---")

    # ── row 2: capped vs uncapped + nationality breakdown ──────────
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### 🎖️ Capped vs Uncapped")
        cap_counts = df["Capped"].map({1:"Capped (Indian)", 0:"Uncapped / Overseas"}).value_counts()
        fig, ax = dark_fig(5, 4)
        ax.bar(cap_counts.index, cap_counts.values,
               color=[PALETTE[0], PALETTE[1]], edgecolor="#0d1117", width=0.5)
        for i, v in enumerate(cap_counts.values):
            ax.text(i, v + 0.5, str(v), ha="center", fontsize=11, fontweight="bold", color="#e6edf3")
        ax.set_ylabel("Number of Players")
        ax.set_title("Capped vs Uncapped Players", pad=10)
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    with col_b:
        st.markdown("### 💰 Price Distribution")
        fig, ax = dark_fig(6, 4)
        ax.hist(df["Price"]/1e5, bins=25, color=PALETTE[2], edgecolor="#0d1117", alpha=0.82)
        ax.axvline(df["Price"].median()/1e5, color=PALETTE[0], lw=2, linestyle="--",
                   label=f"Median ₹{df['Price'].median()/1e5:.0f}L")
        ax.set_xlabel("Price (₹ Lakhs)")
        ax.set_ylabel("Players")
        ax.set_title("Price Distribution — All Players", pad=10)
        ax.legend(fontsize=9)
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig); plt.close()

    st.markdown("---")

    # ── points table ───────────────────────────────────────────────
    if not points_table.empty:
        st.markdown("### 🏆 IPL 2023 Points Table")
        st.dataframe(points_table, use_container_width=True, hide_index=True)
        st.markdown("---")

    # ── raw data preview ───────────────────────────────────────────
    st.markdown("### 📋 Dataset Preview")
    preview_cols = [c for c in ["Player","Team","Role","Price","Capped",
                                 "Runs_per_match","Wickets_per_match",
                                 "Performance_Score","ROI"] if c in df.columns]
    st.dataframe(
        df[preview_cols].sort_values("ROI", ascending=False)
                        .reset_index(drop=True)
                        .style.format({
                            "Price": "₹{:.0f}",
                            "ROI": "{:.4f}",
                            "Runs_per_match": "{:.2f}",
                            "Wickets_per_match": "{:.3f}",
                            "Performance_Score": "{:.2f}",
                        }),
        use_container_width=True, hide_index=True
    )
