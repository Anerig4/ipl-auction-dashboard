# 🏏 AuctionIQ — IPL 2023 Player Valuation Engine

> **Live Demo → [auctioniq-ipl-2023-player-valuation.streamlit.app](https://auctioniq-ipl-2023-player-valuation-hn5j3pu65kbgrcujxaulxq.streamlit.app/)**

A complete data analytics dashboard for the IPL 2023 Mega Auction — built with Python and Streamlit. Analyzes player ROI, team spending strategy, uncapped gems, and statistical insights across all franchises.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📸 Dashboard Sections

| Section | Description |
|---|---|
| 🏠 **Overview** | KPI metrics, team-wise spend, role distribution, points table |
| 📈 **Player ROI** | Filter by team/role, top-N ROI chart, player spotlight |
| 💰 **Team Strategy** | Budget breakdown by role, price histogram, full player table |
| 💎 **Uncapped Gems** | High-ROI uncapped players above 75th percentile |
| 🔥 **Bench Warmers** | High-cost, low-ROI players — wasted budget by team |
| 🧪 **Statistical Tests** | Chi-Square (Role vs Capped) + Welch's T-Test (ROI by cap status) |
| 📊 **Visual Analysis** | KDE histogram, box plots, scatter plots, correlation heatmap |

---

## 📁 Project Structure

```
ipl-auction-dashboard/
├── app.py                  ← Streamlit entry point + global CSS + routing
├── data_loader.py          ← Data loading, cleaning, merging & ROI engine
├── plot_utils.py           ← Shared dark-theme matplotlib/seaborn helpers
├── requirements.txt
├── README.md
├── data/                   ← Place your 3 CSV files here
│   ├── ipl_auction_2023.csv
│   ├── ipl_player_lifetime.csv
│   └── ipl_points_table.csv
└── sections/
    ├── overview.py
    ├── player_roi.py
    ├── team_strategy.py
    ├── uncapped_gems.py
    ├── bench_warmers.py
    ├── stat_tests.py
    └── visual_analysis.py
```

---

## ⚙️ Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ipl-auction-dashboard.git
cd ipl-auction-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your CSV files to `data/`

| File | Kaggle Source |
|---|---|
| `ipl_auction_2023.csv` | [IPL Auction 2023](https://www.kaggle.com/datasets/shahmirkiani/ipl-auction-2023) |
| `ipl_player_lifetime.csv` | [IPL 2024 Player Lifetime Dataset](https://www.kaggle.com/datasets/aryanverma99/ipl-2024-player-lifetime-dataset) |
| `ipl_points_table.csv` | [IPL Points Table 2008-2024](https://www.kaggle.com/datasets/shivamkumar121215/ipl-points-table-2008-2024) |

The app **auto-loads** all three files on startup — no manual upload needed.

### 4. Run
```bash
streamlit run app.py
```

---

## 📐 ROI Formula

```
Runs_per_match    = Runs / Matches
Wickets_per_match = Wickets / Matches

Performance_Score = Runs_per_match + (Wickets_per_match × 20)
ROI               = Performance_Score / Price_in_Crores
```

Capped status is derived from Nationality — Indian players are treated as **Capped**, all overseas players as **Uncapped**.

---

## 🛠 Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=flat&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8+-11557c?style=flat)
![SciPy](https://img.shields.io/badge/SciPy-1.12+-8CAAE6?style=flat&logo=scipy&logoColor=white)

- **Streamlit** — UI, routing & interactivity
- **Pandas / NumPy** — data cleaning, merging, transformation
- **Matplotlib / Seaborn** — custom dark-theme visualisations
- **SciPy** — Chi-Square and Welch's T-Test statistical analysis

---

## 📄 License

MIT License — free to use, modify and distribute.

