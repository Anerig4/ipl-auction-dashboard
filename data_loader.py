import pandas as pd
import numpy as np
import streamlit as st

# ── exact column mapping (confirmed from dataset diagnostic) ───────
# AUCTION : name | player style | final price (in lacs) | franchise | nationality
# PLAYER  : Player_Name | Runs_Scored | Matches_Batted | Year
# POINTS  : year | team | pos | points | Won | Lost


@st.cache_data(show_spinner=False)
def load_all_data(auction_file, player_file, points_file):
    warnings = []

    try:
        auction = _load_auction(auction_file)
    except Exception as e:
        warnings.append(f"Auction load error: {e}")
        auction = pd.DataFrame(columns=["Player","Team","Role","Price","Capped"])

    try:
        player_stats = _load_player_stats(player_file)
    except Exception as e:
        warnings.append(f"Player stats load error: {e}")
        player_stats = pd.DataFrame(columns=["Player","Runs","Wickets","Matches",
                                              "Runs_per_match","Wickets_per_match"])

    try:
        points_table = _load_points_table(points_file)
    except Exception as e:
        warnings.append(f"Points table load error: {e}")
        points_table = pd.DataFrame()

    # ── merge ──────────────────────────────────────────────────────
    df = auction.merge(
        player_stats[["Player","Runs","Wickets","Matches",
                      "Runs_per_match","Wickets_per_match"]],
        on="Player", how="left"
    )
    for col in ["Runs","Wickets","Matches","Runs_per_match","Wickets_per_match"]:
        df[col] = pd.to_numeric(df.get(col, 0), errors="coerce").fillna(0)

    df = _compute_roi(df)
    return df, points_table, warnings


def _load_auction(f):
    df = pd.read_csv(f)
    df.columns = df.columns.str.strip()

    rename = {}
    for c in df.columns:
        cl = c.lower().strip()
        if cl == "name":                 rename[c] = "Player"
        elif cl == "franchise":          rename[c] = "Team"
        elif cl == "player style":       rename[c] = "Role"
        elif "final price" in cl:        rename[c] = "Price"
        elif "base price" in cl:         rename[c] = "Base_Price"
        elif cl == "status":             rename[c] = "Sold_Status"
        elif cl == "nationality":        rename[c] = "Nationality"
    df.rename(columns=rename, inplace=True)

    for col in ["Player","Team","Role","Price"]:
        if col not in df.columns:
            df[col] = np.nan

    # price is in lakhs — convert to rupees
    df["Price"]  = pd.to_numeric(df["Price"], errors="coerce").fillna(0) * 1e5
    df["Player"] = df["Player"].astype(str).str.strip()
    df["Team"]   = df["Team"].astype(str).str.strip()
    df["Role"]   = df["Role"].astype(str).str.strip()

    # derive Capped from Nationality (India = capped)
    if "Nationality" in df.columns:
        df["Capped"] = (df["Nationality"].str.strip().str.lower() == "india").astype(int)
    else:
        df["Capped"] = 0

    # keep only sold players
    df = df[df["Price"] > 0].copy().reset_index(drop=True)
    return df


def _load_player_stats(f):
    df = pd.read_csv(f)
    df.columns = df.columns.str.strip()

    rename = {}
    for c in df.columns:
        cl = c.lower().strip()
        if cl == "player_name":                        rename[c] = "Player"
        elif cl == "runs_scored":                      rename[c] = "Runs"
        elif cl == "matches_batted":                   rename[c] = "Matches"
        elif "wicket" in cl and "taken" in cl:         rename[c] = "Wickets"
        elif cl in ("wickets","wkts","wickets_taken"): rename[c] = "Wickets"
        elif cl == "year":                             rename[c] = "Year"
    df.rename(columns=rename, inplace=True)

    # fallback wicket search
    if "Wickets" not in df.columns:
        for c in df.columns:
            if "wicket" in c.lower() or "wkt" in c.lower():
                df.rename(columns={c: "Wickets"}, inplace=True)
                break
    if "Wickets" not in df.columns:
        df["Wickets"] = 0

    if "Player" not in df.columns:
        raise ValueError("Player stats CSV has no recognisable player-name column.")

    df["Player"] = df["Player"].astype(str).str.strip()
    for col in ["Runs","Wickets","Matches"]:
        if col not in df.columns:
            df[col] = 0
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # filter to 2023 if Year column exists
    if "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
        df23 = df[df["Year"] == 2023].copy()
        if not df23.empty:
            df = df23

    # one row per player
    df = df.groupby("Player", as_index=False).agg(
        {"Runs":"sum","Wickets":"sum","Matches":"sum"}
    )
    df["Runs_per_match"]    = np.where(df["Matches"] > 0, df["Runs"]    / df["Matches"], 0)
    df["Wickets_per_match"] = np.where(df["Matches"] > 0, df["Wickets"] / df["Matches"], 0)
    return df


def _load_points_table(f):
    df = pd.read_csv(f)
    df.columns = df.columns.str.strip()

    rename = {}
    for c in df.columns:
        cl = c.lower().strip()
        if cl == "team":     rename[c] = "Team"
        elif cl == "year":   rename[c] = "Year"
        elif cl == "points": rename[c] = "Points"
        elif cl == "won":    rename[c] = "Wins"
        elif cl == "lost":   rename[c] = "Losses"
        elif cl == "pos":    rename[c] = "Position"
    df.rename(columns=rename, inplace=True)

    if "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
        df23 = df[df["Year"] == 2023]
        return df23.reset_index(drop=True) if not df23.empty else df
    return df


def _compute_roi(df):
    df = df.copy()
    df["Performance_Score"] = df["Runs_per_match"] + (df["Wickets_per_match"] * 20)
    price_cr = df["Price"] / 1e7
    df["ROI"] = np.where(price_cr > 0, df["Performance_Score"] / price_cr, 0)
    df["ROI"] = df["ROI"].round(4)
    return df
