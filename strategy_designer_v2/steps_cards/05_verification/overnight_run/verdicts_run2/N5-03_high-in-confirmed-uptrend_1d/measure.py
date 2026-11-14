import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    COMP = "debug_info.components.near_high.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if not active.any():
                continue
            trending = df["regime"].astype(str) == "trending"
            if COMP in df.columns:
                pos = pd.to_numeric(df[COMP], errors="coerce")
            else:
                pos = pd.Series(np.nan, index=df.index)
            situation = trending & (pos > 0)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "mean excess forward 10-bar return after forecast >= 10",
                "value": None,
                "statistic": None,
                "threshold": "mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects",
            },
            "supporting_check": None,
            "counts": {"non-overlapping cases with forecast >= 10": 0},
            "decided_by": (
                "Fewer than 90% of the bars with a non-zero forecast are long bars of the plan's situation "
                "(regime 'trending' and the 20-bar range position in the upper half)"
                if n_active > 0 else "No bar has a non-zero forecast, so the config never takes the plan's situation."
            ),
            "reading": (
                "The situation is regime == 'trending' (the detector's 200-SMA and 60-bar return rules) with the raw "
                "near_high range position above 0, on the long side."
            ),
        }

    # ---------- 2. Forward returns and coin means ----------
    frames = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            fwd = close.shift(-H) / close - 1.0
            d = pd.DataFrame({
                "coin": coin,
                "window": w,
                "pos": np.arange(len(df)),
                "forecast": pd.to_numeric(df["forecast"], errors="coerce").reset_index(drop=True),
                "regime": df["regime"].astype(str).reset_index(drop=True),
                "fwd": fwd,
            })
            frames.append(d)
    all_df = pd.concat(frames, ignore_index=True)
    all_df = all_df[all_df["fwd"].notna()].copy()
    coin_mean = all_df.groupby("coin")["fwd"].mean()
    all_df["excess"] = all_df["fwd"] - all_df["coin"].map(coin_mean)

    # ---------- 3. Main measure ----------
    strong = all_df[all_df["forecast"].notna() & (all_df["forecast"] >= 10)]
    mean_all_bars = float(strong["excess"].mean()) if len(strong) else None
    grid = strong[strong["pos"] % H == 0]
    n_nonov = int(len(grid))
    x = grid["excess"].to_numpy(dtype=float)
    if n_nonov >= 2 and np.std(x, ddof=1) > 0:
        m = float(np.mean(x))
        t = float(m / (np.std(x, ddof=1) / np.sqrt(n_nonov)))
    else:
        m = float(np.mean(x)) if n_nonov else None
        t = None

    # ---------- 4. Supporting check ----------
    tr = all_df[(all_df["regime"] == "trending") & all_df["forecast"].notna()]
    if len(tr) >= 3 and tr["forecast"].nunique() > 1 and tr["excess"].nunique() > 1:
        rho = float(stats.spearmanr(tr["forecast"], tr["excess"]).correlation)
        sup_pass = bool(rho > 0)
    else:
        rho, sup_pass = None, None

    # ---------- 5. Decision ----------
    if n_nonov < 30:
        status = "not observable"
        decided = (f"Only {n_nonov} non-overlapping cases with forecast >= 10, below the plan's minimum of 30.")
    elif t is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif m > 0 and t >= 2:
        status = "confirmed"
        decided = "Mean excess 10-bar return after forecasts >= 10 is above 0 with t >= 2, on at least 30 non-overlapping cases."
    elif m < 0 and t <= -2:
        status = "rejected"
        decided = "Mean excess 10-bar return after forecasts >= 10 is below 0 with t <= -2, on at least 30 non-overlapping cases."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2 (or its sign disagrees with the mean), so the inconclusive rule applies."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean excess forward 10-bar return after forecast >= 10 (non-overlapping)",
            "value": m,
            "statistic": ({"name": "t of the mean (non-overlapping samples)", "value": t} if t is not None else None),
            "threshold": "mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects; at least 30 non-overlapping cases",
        },
        "supporting_check": {
            "name": "Spearman rank correlation of forecast vs forward 10-bar excess return on trending bars",
            "value": rho,
            "passed": sup_pass,
        },
        "counts": {"non-overlapping cases with forecast >= 10": n_nonov},
        "decided_by": decided,
        "reading": (
            "The situation is regime == 'trending' with the raw near_high range position above 0 on the long side. "
            "The coin mean is taken over all bars with a valid in-window 10-bar return across all its windows. "
            "The mean and t are computed on the non-overlapping grid (positions 0, 10, 20, ... of each window) of "
            f"bars with forecast >= 10; the all-bar mean is {mean_all_bars}. "
            "The supporting check is reported but does not enter the decision, because the confirm and reject rules do not name it."
        ),
    }
