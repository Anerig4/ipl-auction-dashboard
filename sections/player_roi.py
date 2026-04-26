import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from plot_utils import dark_fig, PALETTE, section_header


def render(df):
    section_header("PLAYER ROI ANALYSIS", "Return on investment per player — who delivered the most for their price tag")

    # ── filters ────────────────────────────────────────────────────
    col_f1, col_f2, col_f3 = st.columns(3)
    teams   = ["All"] + sorted(df["Team"].dropna().unique())
    roles   = ["All"] + sorted(df["Role"].dropna().unique())
    sel_team = col_f1.selectbox("Filter by Team", teams)
    sel_role = col_f2.selectbox("Filter by Role", roles)

    filtered = df.copy()
    if sel_team != "All": filtered = filtered[filtered["Team"] == sel_team]
    if sel_role != "All": filtered = filtered[filtered["Role"] == sel_role]

    players = ["All"] + sorted(filtered["Player"].dropna().unique())
    sel_player = col_f3.selectbox("Spotlight Player", players)

    # ── player spotlight ───────────────────────────────────────────
    if sel_player != "All":
        st.markdown("---")
        row = filtered[filtered["Player"] == sel_player].iloc[0]
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Team",          row["Team"])
        m2.metric("Role",          row["Role"])
        m3.metric("Price",         f"₹{row['Price']/1e5:.0f}L")
        m4.metric("ROI",           f"{row['ROI']:.4f}")
        m5.metric("Perf Score",    f"{row['Performance_Score']:.2f}")

        col_s1, col_s2 = st.columns(2)
        col_s1.metric("Runs / Match",    f"{row['Runs_per_match']:.2f}")
        col_s2.metric("Wickets / Match", f"{row['Wickets_per_match']:.3f}")

    st.markdown("---")

    # ── top-N bar chart ────────────────────────────────────────────
    n_top = st.slider("Show top N players by ROI", 5, 25, 10)
    top_n = filtered.nlargest(n_top, "ROI")[
        ["Player","Team","Role","Price","ROI","Performance_Score"]
    ].reset_index(drop=True)

    st.markdown(f"### 🏅 Top {n_top} Players by ROI")
    fig, ax = dark_fig(12, max(4, n_top * 0.45))
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(top_n))]
    bars = ax.barh(top_n["Player"], top_n["ROI"], color=colors,
                   edgecolor="#0d1117", height=0.72)
    for bar, val in zip(bars, top_n["ROI"]):
        ax.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height()/2,
                f"{val:.3f}", va="center", fontsize=8.5, color="#e6edf3")
    ax.set_xlabel("ROI  (Performance per ₹Cr)")
    ax.set_title(f"Top {n_top} Players by ROI", pad=10)
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig); plt.close()

    st.dataframe(
        top_n.style
             .background_gradient(subset=["ROI"], cmap="YlOrRd")
             .format({"Price": "₹{:.0f}", "ROI": "{:.4f}",
                      "Performance_Score": "{:.2f}"}),
        use_container_width=True, hide_index=True
    )

    st.markdown("---")

    # ── best ROI per team ──────────────────────────────────────────
    st.markdown("### 🥇 Best ROI Player per Team")
    best = (filtered.sort_values("ROI", ascending=False)
                    .groupby("Team").first()[["Player","Role","Price","ROI"]]
                    .reset_index()
                    .sort_values("ROI", ascending=False))
    st.dataframe(
        best.style.background_gradient(subset=["ROI"], cmap="YlGn")
                  .format({"Price": "₹{:.0f}", "ROI": "{:.4f}"}),
        use_container_width=True, hide_index=True
    )
