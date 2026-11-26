import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.vol_shift.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if "forecast" not in df.columns or "close" not in df.columns:
                continue
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            vol = df["volume"].astype(float).values if "volume" in df.columns else None
            raw = pd.to_numeric(df[RAW], errors="coerce").values if RAW in df.columns else np.full(len(df), np.nan)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            n = len(df)
            for i in range(n):
                if fc[i] == 0:
                    continue
                n_active += 1
                # 20-day return below 0 (regime rule), from prices when the window holds 20 earlier bars
                if i >= 20 and close[i - 20] > 0:
                    in_sit = (close[i] / close[i - 20] - 1.0) < 0
                else:
                    in_sit = regime[i] == "mean_reversion"
                # expected side: sign of the 30/30-day log volume ratio (long when volume grew)
                r = raw[i]
                if not np.isfinite(r) and vol is not None and i >= 59:
                    a = np.mean(vol[i - 29:i + 1])
                    b = np.mean(vol[i - 59:i - 29])
                    if a > 0 and b > 0:
                        r = np.log(a / b)
                if not np.isfinite(r) or r == 0:
                    side_ok = False
                else:
                    side_ok = np.sign(fc[i]) == np.sign(r)
                if in_sit and side_ok:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The situation is checked as the 20-day close return below 0 (from prices, or the recorded "
               "'mean_reversion' regime where the window holds fewer than 20 earlier bars), the falling profile "
               "being left to the code as the Fidelity says, and the expected side as the sign of the recorded raw "
               "30/30-day log volume ratio; the coin's mean 10-bar return is taken over all its grid cells in all "
               "windows, and the main measure is the mean over day-cases of the per-date summed cell values, with "
               "the ordinary t of that mean.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean of (forecast/10) x excess 10-bar return per day-case",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 confirms (with rank correlation > 0), t <= -2 rejects, on >= 30 day-cases"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Only %.1f%% of active bars are bars with a negative 20-day return where the forecast "
                           "has the sign of the volume log ratio, below the 90%% the plan's Fidelity requires." % (100 * agreement)),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cells = []  # (coin, date, forecast, ret)
    coin_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                r = close[i + H] / close[i] - 1.0
                allr.append(r)
                if np.isfinite(fc[i]) and fc[i] != 0:
                    cells.append((coin, ts.iloc[i].normalize(), float(fc[i]), r))
        coin_rets[coin] = float(np.mean(allr)) if allr else np.nan

    rows = []
    for coin, d, f, r in cells:
        mu = coin_rets.get(coin, np.nan)
        if not np.isfinite(mu):
            continue
        ex = r - mu
        rows.append({"coin": coin, "date": d, "f": f, "ex": ex, "v": f / 10.0 * ex})
    cdf = pd.DataFrame(rows, columns=["coin", "date", "f", "ex", "v"])

    n_cells = int(len(cdf))
    if n_cells > 0:
        day = cdf.groupby("date")["v"].sum().values
    else:
        day = np.array([])
    n_days = int(len(day))

    mean_v = float(np.mean(day)) if n_days > 0 else None
    t = None
    if n_days >= 2:
        sd = np.std(day, ddof=1)
        t = float(mean_v / (sd / np.sqrt(n_days))) if sd > 0 else None

    rho = None
    if n_cells >= 3 and cdf["f"].nunique() > 1 and cdf["ex"].nunique() > 1:
        rr = stats.spearmanr(cdf["f"].values, cdf["ex"].values).correlation
        rho = float(rr) if np.isfinite(rr) else None
    rho_pass = None if rho is None else bool(rho > 0)

    counts = {"day-cases": n_days, "cells": n_cells}

    if n_days < 30:
        status = "not observable"
        decided = "Fewer than 30 day-cases (%d), the plan's minimum count, so the data could not show the idea." % n_days
    elif t is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed (zero spread), so neither the confirm nor the reject rule is met."
    elif t >= 2 and rho_pass:
        status = "confirmed"
        decided = "The main measure's t is 2 or more on at least 30 day-cases and the rank correlation is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The main measure's t is -2 or less on at least 30 day-cases."
    elif t >= 2:
        status = "inconclusive"
        decided = "The t is 2 or more but the rank correlation is 0 or below, so the plan calls it inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 on at least 30 day-cases, so the plan calls it inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean of (forecast/10) x excess 10-bar return per day-case",
                         "value": mean_v,
                         "statistic": {"name": "t of the mean over day-cases", "value": t} if t is not None else None,
                         "threshold": "t >= 2 confirms (with rank correlation > 0), t <= -2 rejects, on >= 30 day-cases"},
        "supporting_check": {"name": "Spearman rank correlation forecast vs excess 10-bar return > 0",
                             "value": rho, "passed": rho_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
