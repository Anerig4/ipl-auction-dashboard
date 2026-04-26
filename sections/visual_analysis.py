import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats
from plot_utils import dark_fig, PALETTE, section_header


def render(df):
    section_header("VISUAL ANALYSIS", "Six in-depth plots — distributions, relationships and team comparisons")

    tabs = st.tabs([
        "📊 ROI Distribution",
        "📦 ROI by Role",
        "🔵 Price vs Performance",
        "🏏 Team ROI",
        "⚡ Top vs Bottom",
        "🌡️ Correlation Heatmap",
    ])

    # ── 1. ROI Histogram + KDE ─────────────────────────────────────
    with tabs[0]:
        st.markdown("### ROI Distribution with KDE")
        st.markdown("Shows how ROI values are spread across all auctioned players.")
        roi_vals = df["ROI"].dropna()
        fig, ax = dark_fig(12, 4.5)
        ax.hist(roi_vals, bins=35, color=PALETTE[0], alpha=0.68,
                edgecolor="#0d1117", density=True, label="Histogram")
        try:
            kde  = stats.gaussian_kde(roi_vals)
            xr   = np.linspace(roi_vals.min(), roi_vals.max(), 400)
            ax.plot(xr, kde(xr), color="#38bdf8", lw=2.5, label="KDE")
        except Exception:
            pass
        ax.axvline(roi_vals.mean(),   color=PALETTE[1], lw=1.8, linestyle="--",
                   label=f"Mean = {roi_vals.mean():.3f}")
        ax.axvline(roi_vals.median(), color=PALETTE[2], lw=1.8, linestyle=":",
                   label=f"Median = {roi_vals.median():.3f}")
        ax.set_xlabel("ROI"); ax.set_ylabel("Density")
        ax.set_title("ROI Distribution — IPL Auction 2023", pad=10)
        ax.legend(fontsize=9); ax.grid(axis="y", alpha=0.3)
        plt.tight_layout(); st.pyplot(fig); plt.close()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Mean",    f"{roi_vals.mean():.4f}")
        col2.metric("Median",  f"{roi_vals.median():.4f}")
        col3.metric("Std Dev", f"{roi_vals.std():.4f}")
        col4.metric("Max ROI", f"{roi_vals.max():.4f}")

    # ── 2. Box plot ROI vs Role ────────────────────────────────────
    with tabs[1]:
        st.markdown("### ROI by Player Role")
        st.markdown("Compares ROI spread across Batsmen, Bowlers, and All-rounders.")
        roles = sorted(df["Role"].dropna().unique())
        data_by_role = [df[df["Role"] == r]["ROI"].dropna() for r in roles]
        fig, ax = dark_fig(10, 5)
        bp = ax.boxplot(data_by_role, labels=roles, patch_artist=True,
                        whiskerprops={"color":"#8b949e","linewidth":1.3},
                        capprops={"color":"#8b949e","linewidth":1.5},
                        medianprops={"color":PALETTE[1],"linewidth":2.5},
                        flierprops={"marker":"o","markerfacecolor":PALETTE[0],
                                    "markersize":5,"alpha":0.6,"markeredgewidth":0})
        for patch, color in zip(bp["boxes"], PALETTE[:len(roles)]):
            patch.set_facecolor(color); patch.set_alpha(0.55)
        ax.set_ylabel("ROI")
        ax.set_title("ROI Distribution by Player Role", pad=10)
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout(); st.pyplot(fig); plt.close()

        st.markdown("**Role-wise ROI Summary**")
        role_summary = df.groupby("Role")["ROI"].agg(["mean","median","std","max","count"])
        role_summary.columns = ["Mean","Median","Std","Max","Players"]
        st.dataframe(role_summary.style.background_gradient(subset=["Mean"], cmap="YlGn")
                                       .format("{:.4f}", subset=["Mean","Median","Std","Max"]),
                     use_container_width=True)

    # ── 3. Scatter Price vs Performance ───────────────────────────
    with tabs[2]:
        st.markdown("### Price vs Performance Score")
        st.markdown("Do expensive players actually perform better?")
        fig, ax = dark_fig(11, 5.5)
        for i, role in enumerate(df["Role"].dropna().unique()):
            sub = df[df["Role"] == role]
            ax.scatter(sub["Price"]/1e5, sub["Performance_Score"],
                       label=role, alpha=0.8, s=70,
                       color=PALETTE[i % len(PALETTE)],
                       edgecolors="#0d1117", linewidths=0.5, zorder=3)
        ax.set_xlabel("Price (₹ Lakhs)")
        ax.set_ylabel("Performance Score  (Runs/M + Wickets/M × 20)")
        ax.set_title("Price vs Performance Score by Role", pad=10)
        ax.legend(fontsize=9, framealpha=0.2)
        ax.grid(alpha=0.25)
        plt.tight_layout(); st.pyplot(fig); plt.close()

        corr_val = df["Price"].corr(df["Performance_Score"])
        st.metric("Price ↔ Performance Correlation", f"{corr_val:.4f}",
                  help="Pearson correlation coefficient. Close to 0 = no relationship.")

    # ── 4. Team ROI box plot ───────────────────────────────────────
    with tabs[3]:
        st.markdown("### Team-wise ROI Distribution")
        st.markdown("Which franchises got the most consistent value from their squad?")
        teams_sorted    = sorted(df["Team"].dropna().unique())
        data_by_team    = [df[df["Team"] == t]["ROI"].dropna() for t in teams_sorted]
        fig, ax = dark_fig(14, 5)
        bp2 = ax.boxplot(data_by_team, labels=teams_sorted, patch_artist=True,
                         whiskerprops={"color":"#8b949e","linewidth":1.2},
                         capprops={"color":"#8b949e","linewidth":1.5},
                         medianprops={"color":PALETTE[1],"linewidth":2.5},
                         flierprops={"marker":"o","markerfacecolor":PALETTE[0],
                                     "markersize":4,"alpha":0.5,"markeredgewidth":0})
        for patch, color in zip(bp2["boxes"], PALETTE * 5):
            patch.set_facecolor(color); patch.set_alpha(0.5)
        ax.set_xticklabels(teams_sorted, rotation=45, ha="right", fontsize=9)
        ax.set_ylabel("ROI")
        ax.set_title("ROI Distribution by Team", pad=10)
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout(); st.pyplot(fig); plt.close()

        st.markdown("**Team-wise ROI Summary**")
        team_summary = df.groupby("Team")["ROI"].agg(["mean","median","max","count"])
        team_summary.columns = ["Mean ROI","Median ROI","Max ROI","Players"]
        st.dataframe(team_summary.sort_values("Mean ROI", ascending=False)
                                  .style.background_gradient(subset=["Mean ROI"], cmap="YlGn")
                                  .format({c:"{:.4f}" for c in ["Mean ROI","Median ROI","Max ROI"]}),
                     use_container_width=True)

    # ── 5. Top vs Bottom ROI ───────────────────────────────────────
    with tabs[4]:
        st.markdown("### Top vs Bottom ROI Players")
        n = max(5, min(15, len(df)//4))
        top_roi    = df.nlargest(n,  "ROI")["ROI"]
        bottom_roi = df.nsmallest(n, "ROI")["ROI"]
        fig, ax = dark_fig(8, 5)
        bp3 = ax.boxplot(
            [top_roi, bottom_roi],
            labels=[f"Top {n} ROI", f"Bottom {n} ROI"],
            patch_artist=True,
            whiskerprops={"color":"#8b949e","linewidth":1.3},
            capprops={"color":"#8b949e","linewidth":1.5},
            medianprops={"color":"#0d1117","linewidth":2.5},
            flierprops={"marker":"o","markersize":6,"alpha":0.6,"markeredgewidth":0}
        )
        bp3["boxes"][0].set_facecolor(PALETTE[2]); bp3["boxes"][0].set_alpha(0.75)
        bp3["boxes"][1].set_facecolor(PALETTE[1]); bp3["boxes"][1].set_alpha(0.75)
        ax.set_ylabel("ROI")
        ax.set_title(f"Top {n} vs Bottom {n} ROI Players", pad=10)
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout(); st.pyplot(fig); plt.close()

        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown(f"**🏅 Top {n} Players**")
            st.dataframe(df.nlargest(n, "ROI")[["Player","Team","ROI"]]
                           .reset_index(drop=True)
                           .style.format({"ROI":"{:.4f}"}),
                         use_container_width=True, hide_index=True)
        with col_r:
            st.markdown(f"**💤 Bottom {n} Players**")
            st.dataframe(df.nsmallest(n, "ROI")[["Player","Team","ROI"]]
                           .reset_index(drop=True)
                           .style.format({"ROI":"{:.4f}"}),
                         use_container_width=True, hide_index=True)

    # ── 6. Correlation Heatmap ─────────────────────────────────────
    with tabs[5]:
        st.markdown("### Feature Correlation Heatmap")
        st.markdown("How do price, performance metrics, and ROI relate to each other?")
        num_cols  = df.select_dtypes(include=np.number).columns.tolist()
        corr_cols = [c for c in ["Price","Runs_per_match","Wickets_per_match",
                                  "Performance_Score","ROI","Capped","Matches"]
                     if c in num_cols]
        corr = df[corr_cols].corr()
        fig, ax = dark_fig(9, 7)
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
                    linewidths=0.6, linecolor="#0d1117",
                    annot_kws={"size":10}, ax=ax,
                    cbar_kws={"shrink":0.8})
        ax.set_title("Feature Correlation Matrix", pad=14)
        plt.tight_layout(); st.pyplot(fig); plt.close()

        st.markdown("**Key Insights:**")
        roi_price_corr = df["ROI"].corr(df["Price"])
        roi_perf_corr  = df["ROI"].corr(df["Performance_Score"])
        c1, c2 = st.columns(2)
        c1.metric("ROI ↔ Price Correlation",       f"{roi_price_corr:.4f}")
        c2.metric("ROI ↔ Performance Correlation", f"{roi_perf_corr:.4f}")
