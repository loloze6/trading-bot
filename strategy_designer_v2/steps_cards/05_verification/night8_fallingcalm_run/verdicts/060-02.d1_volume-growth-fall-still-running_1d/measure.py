import numpy as np
import pandas as pd
from scipy import stats

H = 5
FC_COL = "debug_info.components.vol_growth.post_pipeline_value"
RAW_COL = "debug_info.components.vol_growth.last_history_value"


def _col(df, name):
    if name in df.columns:
        return pd.to_numeric(df[name], errors="coerce")
    return pd.Series(np.nan, index=df.index)


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            raw = _col(df, RAW_COL)
            ret20 = close / close.shift(20) - 1.0
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            # 20-day return below 0: recomputed from prices; on the window's first 20 bars
            # (no in-window history) the detector's own decision stands in
            in_sit = np.where(ret20.notna(), ret20 < 0, regime == "mean_reversion")
            active = fc != 0
            # expected side: long on volume growth (raw log ratio > 0), short on shrinkage
            side_ok = np.sign(fc) == np.sign(raw)
            n_active += int(active.sum())
            n_agree += int((active & pd.Series(in_sit, index=df.index) & side_ok.fillna(False)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    threshold_txt = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 100 cases"
    main_name = "OLS slope of 5-day excess forward return on vol_growth post_pipeline_value"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast have a negative 20-day return with the forecast's sign equal to the sign of the volume log ratio (long on growth, short on shrinkage).",
            "reading": "The situation is taken as the 20-day close-to-close return below 0 (the regime rule), the falling profile being enforced by the detector; the side is the sign of the raw volume log ratio.",
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_all = {}
    for coin, wins in bars.items():
        allret = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            pp = _col(df, FC_COL).values
            n = len(df)
            for i in range(0, n - H, H):
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H])) or close[i] == 0:
                    continue
                r = close[i + H] / close[i] - 1.0
                allret.append(r)
                if fc[i] != 0 and np.isfinite(pp[i]):
                    rows.append((coin, r, pp[i]))
        coin_all[coin] = float(np.mean(allret)) if allret else np.nan

    x = []
    y = []
    for coin, r, p in rows:
        m = coin_all.get(coin, np.nan)
        if np.isfinite(m):
            x.append(p)
            y.append(r - m)
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    ncase = int(len(x))

    slope = None
    tval = None
    if ncase >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    if ncase < 100:
        status = "not observable"
        decided = f"Only {ncase} cases, below the plan's minimum of 100."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 over at least 100 cases."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 over at least 100 cases."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 over at least 100 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
            "threshold": threshold_txt,
        },
        "supporting_check": None,
        "counts": {"cases": ncase},
        "decided_by": decided,
        "reading": "The grid is positions 0,5,10,... of each window keeping only cells with a full 5-bar forward return inside the window, the coin's mean 5-day return is taken over all those grid cells of all its windows, and the 20-day-return situation is recomputed from closes with the recorded regime standing in on each window's first 20 bars.",
    }
