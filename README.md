# 🏏 IPL Auction 2023 — Analytics Dashboard

A complete Streamlit analytics dashboard for IPL 2023 auction data — built for GitHub and deployable to Streamlit Cloud in one click.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 Features

| Section | What you get |
|---|---|
| 🏠 Overview | KPI metrics, team spend, role breakdown, points table |
| 📈 Player ROI | Filters by team/role/player, top-N bar chart, spotlight view |
| 💰 Team Strategy | Budget pie, price histogram, per-team player table |
| 💎 Uncapped Gems | High-ROI uncapped players above Q75, scatter plot |
| 🔥 Bench Warmers | High-cost, low-ROI players, team-wise wasted budget |
| 🧪 Statistical Tests | Chi-Square (Role vs Capped) + Welch's T-Test (ROI by cap) |
| 📊 Visual Analysis | KDE histogram, box plots, scatter, team comparison, heatmap |

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ipl-auction-dashboard.git
cd ipl-auction-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Upload your CSV files in the sidebar

| File | Kaggle Source |
|---|---|
| `ipl_auction_2023.csv` | [IPL Auction 2023](https://www.kaggle.com/datasets/shahmirkiani/ipl-auction-2023) |
| `ipl_player_lifetime.csv` | [IPL 2024 Player Lifetime Dataset](https://www.kaggle.com/datasets/aryanverma99/ipl-2024-player-lifetime-dataset) |
| `ipl_points_table.csv` | [IPL Points Table 2008-2024](https://www.kaggle.com/datasets/shivamkumar121215/ipl-points-table-2008-2024) |

---

## ☁️ Deploy to Streamlit Cloud (free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → set **Main file path** to `app.py`
4. Click **Deploy**

> Note: For cloud deployment, place your CSV files in the `data/` folder and update the file uploader to read from there, or keep the upload widget.

---

## 📁 Project Structure

```
ipl-auction-dashboard/
├── app.py                  # Main Streamlit entry point
├── data_loader.py          # Data loading, cleaning, merging & ROI
├── plot_utils.py           # Shared dark-theme plot helpers
├── requirements.txt
├── README.md
├── data/                   # (optional) place CSVs here
└── sections/
    ├── __init__.py
    ├── overview.py
    ├── player_roi.py
    ├── team_strategy.py
    ├── uncapped_gems.py
    ├── bench_warmers.py
    ├── stat_tests.py
    └── visual_analysis.py
```

---

## 📐 ROI Formula

```
Runs_per_match     = Runs / Matches
Wickets_per_match  = Wickets / Matches

Performance_Score  = Runs_per_match + (Wickets_per_match × 20)
ROI                = Performance_Score / Price_in_Crores
```

Capped status is derived from Nationality — Indian players are treated as **Capped (1)**, all others as **Uncapped (0)**.

---

## 🛠 Tech Stack

- **Streamlit** — UI & interactivity
- **Pandas / NumPy** — data processing
- **Matplotlib / Seaborn** — visualisations
- **SciPy** — statistical tests

---

## 📄 License

MIT License — free to use, modify and distribute.
