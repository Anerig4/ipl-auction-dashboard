import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from plot_utils import dark_fig, PALETTE, section_header, interp_box


def render(df):
    section_header("STATISTICAL TESTS", "Rigorous hypothesis testing on auction data — beyond gut feel")

    tab1, tab2 = st.tabs(["🔬 Chi-Square: Role vs Capped", "📐 T-Test: ROI by Cap Status"])

    # ── Chi-Square ─────────────────────────────────────────────────
    with tab1:
        st.markdown("### Chi-Square Test — Role vs Capped Status")
        st.markdown("""
        **Hypothesis:** Is there a statistically significant association between a player's
        role (Batsman / Bowler / All-rounder) and their capped status?
        """)
        try:
            contingency = pd.crosstab(df["Role"], df["Capped"])
            chi2, p_chi, dof, expected = stats.chi2_contingency(contingency)

            c1, c2, c3 = st.columns(3)
            c1.metric("χ² Statistic",       f"{chi2:.4f}")
            c2.metric("p-value",             f"{p_chi:.4f}")
            c3.metric("Degrees of Freedom",  dof)

            if p_chi < 0.05:
                interp_box(
                    f"✅ <b>Statistically significant</b> (p = {p_chi:.4f} &lt; 0.05)<br>"
                    "There IS a meaningful association between a player's Role and their Capped status. "
                    "Teams appear to favour certain roles when bidding for capped vs uncapped talent.",
                    kind="good"
                )
            else:
                interp_box(
                    f"❌ <b>Not statistically significant</b> (p = {p_chi:.4f} ≥ 0.05)<br>"
                    "No strong evidence of an association between Role and Capped status. "
                    "The distribution of roles appears independent of capped/uncapped classification.",
                    kind="bad"
                )

            st.markdown("**Observed Contingency Table:**")
            st.dataframe(contingency, use_container_width=True)

            # heatmap of observed vs expected
            col_l, col_r = st.columns(2)
            with col_l:
                st.markdown("**Observed Frequencies**")
                fig, ax = dark_fig(5, 3.5)
                import seaborn as sns
                sns.heatmap(contingency, annot=True, fmt="d", cmap="YlOrRd",
                            linewidths=0.5, linecolor="#0d1117",
                            annot_kws={"size":10}, ax=ax, cbar=False)
                ax.set_title("Observed", pad=8)
                plt.tight_layout()
                st.pyplot(fig); plt.close()

            with col_r:
                st.markdown("**Expected Frequencies**")
                expected_df = pd.DataFrame(expected,
                                           index=contingency.index,
                                           columns=contingency.columns).round(1)
                fig, ax = dark_fig(5, 3.5)
                sns.heatmap(expected_df, annot=True, fmt=".1f", cmap="Blues",
                            linewidths=0.5, linecolor="#0d1117",
                            annot_kws={"size":10}, ax=ax, cbar=False)
                ax.set_title("Expected (under H₀)", pad=8)
                plt.tight_layout()
                st.pyplot(fig); plt.close()

        except Exception as ex:
            st.error(f"Chi-Square test failed: {ex}")

    # ── T-Test ─────────────────────────────────────────────────────
    with tab2:
        st.markdown("### Welch's T-Test — ROI: Capped vs Uncapped Players")
        st.markdown("""
        **Hypothesis:** Do capped (Indian) players deliver significantly different ROI
        compared to uncapped/overseas players?
        """)
        try:
            roi_capped   = df[df["Capped"] == 1]["ROI"].dropna()
            roi_uncapped = df[df["Capped"] == 0]["ROI"].dropna()

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Capped Players",    len(roi_capped))
            c2.metric("Uncapped Players",  len(roi_uncapped))
            c3.metric("Capped Avg ROI",    f"{roi_capped.mean():.4f}")
            c4.metric("Uncapped Avg ROI",  f"{roi_uncapped.mean():.4f}")

            if len(roi_capped) < 2 or len(roi_uncapped) < 2:
                st.warning("Not enough data in one group to run the t-test.")
            else:
                t_stat, p_t = stats.ttest_ind(roi_capped, roi_uncapped, equal_var=False)

                c5, c6 = st.columns(2)
                c5.metric("T-Statistic", f"{t_stat:.4f}")
                c6.metric("p-value",     f"{p_t:.4f}")

                if p_t < 0.05:
                    direction = "higher" if roi_capped.mean() > roi_uncapped.mean() else "lower"
                    interp_box(
                        f"✅ <b>Statistically significant</b> (p = {p_t:.4f} &lt; 0.05)<br>"
                        f"Capped players deliver <b>{direction}</b> average ROI than uncapped players. "
                        f"The difference (Δ = {abs(roi_capped.mean()-roi_uncapped.mean()):.4f}) "
                        f"is unlikely to be due to chance.",
                        kind="good"
                    )
                else:
                    interp_box(
                        f"❌ <b>Not statistically significant</b> (p = {p_t:.4f} ≥ 0.05)<br>"
                        "No meaningful ROI difference between capped and uncapped players. "
                        "Cap status alone doesn't predict auction value.",
                        kind="bad"
                    )

                # overlapping histogram
                st.markdown("#### ROI Distribution — Capped vs Uncapped")
                fig, ax = dark_fig(11, 4.5)
                ax.hist(roi_capped,   bins=25, alpha=0.72, color=PALETTE[0],
                        label=f"Capped  (n={len(roi_capped)}, μ={roi_capped.mean():.3f})",
                        edgecolor="#0d1117")
                ax.hist(roi_uncapped, bins=25, alpha=0.72, color=PALETTE[1],
                        label=f"Uncapped (n={len(roi_uncapped)}, μ={roi_uncapped.mean():.3f})",
                        edgecolor="#0d1117")
                ax.axvline(roi_capped.mean(),   color=PALETTE[0], lw=2, linestyle="--")
                ax.axvline(roi_uncapped.mean(), color=PALETTE[1], lw=2, linestyle="--")
                ax.set_xlabel("ROI")
                ax.set_title("ROI Distribution: Capped vs Uncapped", pad=10)
                ax.legend(fontsize=9)
                ax.grid(axis="y", alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig); plt.close()

        except Exception as ex:
            st.error(f"T-test failed: {ex}")

import pandas as pd
import seaborn as sns
