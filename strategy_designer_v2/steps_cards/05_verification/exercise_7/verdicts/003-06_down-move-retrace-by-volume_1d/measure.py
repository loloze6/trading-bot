import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    VOL_WIN = 20
    HEAVY_COL = "debug_info.components.heavy_drop.last_history_value"
    THIN_COL = "debug_info.components.thin_drop.last_history_value"

    rows = []
    for coin in sorted(bars.keys()):
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")

            # raw one-bar move from the config's components, falling back to prices
            move = pd.Series(np.nan, index=df.index)
            for col in (HEAVY_COL, THIN_COL):
                if col in df.columns:
                    move = move.fillna(pd.to_numeric(df[col], errors="coerce"))
            ret_prev = close / close.shift(1) - 1.0  # within the window only
            move = move.fillna(ret_prev)

            # 20-bar mean of volume, including the current bar, within the window
            vmean = vol.rolling(VOL_WIN, min_periods=VOL_WIN).mean()
            thin = vol < vmean
            heavy = vol >= vmean
            vol_known = vmean.notna() & vol.notna()

            next_ret = close.shift(-1) / close - 1.0  # within the window only

            for i in range(len(df)):
                rows.append({
                    "coin": coin,
                    "window": window,
                    "move": move.iloc[i],
                    "drop": ret_prev.iloc[i],
                    "vol_known": bool(vol_known.iloc[i]),
                    "thin": bool(thin.iloc[i]) if vol_known.iloc[i] else False,
                    "heavy": bool(heavy.iloc[i]) if vol_known.iloc[i] else False,
                    "forecast": fc.iloc[i],
                    "next_ret": next_ret.iloc[i],
                })

    d = pd.DataFrame(rows)
    reading = ("Volume class uses the 20-bar mean ending at and including the bar, computed inside each window, "
               "so bars without 20 bars of volume history are left out of both the situation check and the groups; "
               "drop size is close[t]/close[t-1]-1 inside the window; terciles are pooled qcut terciles of |drop| and "
               "a tercile 'has the same sign' when its thin-minus-heavy difference shares the sign of the pooled one; "
               "since the Inconclusive rule keeps negative differences with t above -1, a negative difference is "
               "rejected only with t <= -1 (a zero difference is rejected), and a positive difference with t >= 2 but "
               "a thin mean <= 0 is inconclusive.")

    # ---------- situation check ----------
    if len(d) == 0:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": None, "supporting_check": None, "counts": {},
            "decided_by": "The record holds no bars, so the plan's situation cannot be matched.",
            "reading": reading,
        }

    active = d[d["forecast"].notna() & (d["forecast"] != 0) & d["vol_known"] & d["move"].notna()]
    n_active = len(active)
    if n_active == 0:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"active bars": 0},
            "decided_by": "No active bars with a known volume class: the config never takes the plan's down-bar positions.",
            "reading": reading,
        }
    down = active["move"] < 0
    ok = down & ((active["thin"] & (active["forecast"] > 0)) | (active["heavy"] & (active["forecast"] < 0)))
    agreement = float(ok.sum()) / n_active
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are down bars held long when volume is below its 20-bar mean "
                           "and short when at/above it, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    # ---------- main measure ----------
    g = d[d["vol_known"] & d["move"].notna() & (d["move"] < 0)
          & d["drop"].notna() & (d["drop"] < 0) & d["next_ret"].notna()].copy()
    g["share"] = g["next_ret"] / g["drop"].abs()
    g = g[np.isfinite(g["share"])]
    thin_s = g.loc[g["thin"], "share"].to_numpy()
    heavy_s = g.loc[g["heavy"], "share"].to_numpy()
    n_thin, n_heavy = len(thin_s), len(heavy_s)

    thin_mean = float(np.mean(thin_s)) if n_thin else None
    heavy_mean = float(np.mean(heavy_s)) if n_heavy else None
    diff = (thin_mean - heavy_mean) if (thin_mean is not None and heavy_mean is not None) else None
    t = None
    if n_thin >= 2 and n_heavy >= 2:
        tt = stats.ttest_ind(thin_s, heavy_s, equal_var=False)
        t = float(tt.statistic) if np.isfinite(tt.statistic) else None

    # ---------- supporting check ----------
    sup_val, sup_pass = None, None
    if len(g) >= 3 and diff is not None:
        try:
            terc = pd.qcut(g["drop"].abs(), 3, labels=False, duplicates="drop")
        except ValueError:
            terc = None
        if terc is not None:
            g["terc"] = terc
            same = 0
            for k in sorted(g["terc"].dropna().unique()):
                sub = g[g["terc"] == k]
                a = sub.loc[sub["thin"], "share"]
                b = sub.loc[sub["heavy"], "share"]
                if len(a) == 0 or len(b) == 0:
                    continue
                dk = a.mean() - b.mean()
                if np.sign(dk) == np.sign(diff) and dk != 0:
                    same += 1
            sup_val = same
            sup_pass = bool(same >= 2)

    # ---------- decision ----------
    if n_thin < 20 or n_heavy < 20:
        status = "inconclusive"
        decided_by = "Inconclusive: fewer than 20 thin or 20 heavy down bars in total."
    elif diff is None or t is None:
        status = "inconclusive"
        decided_by = "Inconclusive: the difference or its Welch t could not be computed."
    elif diff > 0 and t >= 2 and thin_mean > 0:
        status = "confirmed"
        decided_by = ("Confirm: thin-minus-heavy give-back difference above 0 with Welch t >= 2 "
                      "and a positive thin-group mean give-back share.")
    elif diff == 0 or (diff < 0 and t <= -1):
        status = "rejected"
        decided_by = ("Reject: the difference is at or below 0, with heavy give-back at or above thin "
                      "and Welch t of -1 or lower.")
    elif diff > 0 and t < 2:
        status = "inconclusive"
        decided_by = "Inconclusive: a positive difference with Welch t below 2."
    elif diff < 0 and t > -1:
        status = "inconclusive"
        decided_by = "Inconclusive: a negative difference with Welch t above -1."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: positive difference with t >= 2 but the thin group's mean give-back is not above 0."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "thin minus heavy mean next-bar give-back share of the drop",
            "value": diff,
            "statistic": {"name": "Welch t", "value": t} if t is not None else None,
            "threshold": ("confirm: difference > 0, Welch t >= 2 and thin mean > 0; reject: difference <= 0 "
                          "with t <= -1; otherwise inconclusive; at least 20 thin and 20 heavy down bars"),
        },
        "supporting_check": {
            "name": "terciles of drop size with the same-sign thin-minus-heavy difference (need >= 2 of 3)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"thin down bars": int(n_thin), "heavy down bars": int(n_heavy)},
        "decided_by": decided_by,
        "reading": reading,
    }
