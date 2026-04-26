import matplotlib.pyplot as plt
import numpy as np

PALETTE = [
    "#f5a623","#e84393","#38bdf8","#22c55e",
    "#a78bfa","#fb923c","#34d399","#f87171",
    "#fbbf24","#60a5fa","#4ade80","#f472b6",
]

BG      = "#0d1117"
CARD    = "#161b22"
BORDER  = "#30363d"
MUTED   = "#8b949e"
TEXT    = "#e6edf3"


def apply_theme():
    plt.rcParams.update({
        "figure.facecolor":  BG,
        "axes.facecolor":    CARD,
        "axes.edgecolor":    BORDER,
        "axes.labelcolor":   MUTED,
        "axes.titlecolor":   TEXT,
        "axes.titlesize":    13,
        "axes.labelsize":    10,
        "xtick.color":       MUTED,
        "ytick.color":       MUTED,
        "grid.color":        BORDER,
        "grid.linestyle":    "--",
        "grid.linewidth":    0.5,
        "text.color":        TEXT,
        "font.family":       "DejaVu Sans",
        "axes.spines.top":   False,
        "axes.spines.right": False,
        "figure.dpi":        110,
        "legend.facecolor":  CARD,
        "legend.edgecolor":  BORDER,
        "legend.labelcolor": TEXT,
    })


def dark_fig(w=10, h=5):
    apply_theme()
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(CARD)
    return fig, ax


def dark_figs(rows, cols, w=14, h=6):
    apply_theme()
    fig, axes = plt.subplots(rows, cols, figsize=(w, h))
    fig.patch.set_facecolor(BG)
    for ax in np.array(axes).ravel():
        ax.set_facecolor(CARD)
    return fig, axes


def section_header(title, subtitle=""):
    import streamlit as st
    st.markdown(f"# {title}")
    if subtitle:
        st.markdown(f"<p style='color:#8b949e; margin-top:-10px; font-size:.95rem'>{subtitle}</p>",
                    unsafe_allow_html=True)
    st.markdown("---")


def interp_box(text, kind="neutral"):
    """kind: neutral | good | bad"""
    css = {
        "neutral": ("interp-box", ""),
        "good":    ("sig-box",    ""),
        "bad":     ("nosig-box",  ""),
    }
    cls, _ = css.get(kind, css["neutral"])
    import streamlit as st
    st.markdown(f'<div class="{cls}">{text}</div>', unsafe_allow_html=True)
