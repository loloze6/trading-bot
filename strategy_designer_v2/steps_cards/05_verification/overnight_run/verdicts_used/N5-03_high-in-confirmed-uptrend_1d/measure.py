import numpy as np
import pandas as pd
from scipy import stats


def _component_raw(df, comp_id, field="last_history_value"):
    """Return the raw component value as a float Series (NaN where missing)."""
    flat = f"debug_info.components.{comp_id}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    if "debug_info.components" in df.columns:
        def get(x):
            try:
                if isinstance(x, dict):
                    v = x.get(comp_id, {})
                    if isinstance(v, dict):
                        return v.get(field, np.nan)
            except Exception:
                pass
            return np.nan
        return pd.to_numeric(df["debug_info.components"].map(get), errors="coerce")
    return pd.Series(np.nan, index=df.index)


def measure(bars):
    H = 10
    THR_F = 10.0
    MIN_CASES = 30

    # ---------- per-coin frames with forward returns ----------
    frames = {}
    for coin in sorted(bars.keys()):
        lst = []
        for w in sorted(bars[coin].keys(), key=lambda s: (len(str(s)), str(s))):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            d = pd.DataFrame(index=range(len(df)))
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            d["forecast"] = pd.to_numeric(df["forecast"], errors="coerce").reset_index(drop=True)
            d["regime"] = df["regime"].astype(str).reset_index(drop=True) if "regime" in df.columns else ""
            d["near_high"] = _component_raw(df, "near_high").reset_index(drop=True)
            d["fwd"] = close.shift(-H) / close - 1.0
            d["pos"] = np.arange(len(df))
            d["grid"] = (d["pos"] % H) == 0
            d["window"] = str(w)
            lst.append(d)
        if lst:
            frames[coin] = pd.concat(lst, ignore_index=True)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, d in frames.items():
        act = d["forecast"].notna() & (d["forecast"] != 0)
        n_active += int(act.sum())
        sit = (d["regime"] == "trending") & (d["near_high"] > 0) & (d["forecast"] > 0)
        n_agree += int((act & sit).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean excess forward 10-bar return on bars with forecast >= 10"
    thr_words = "mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects; at least 30 non-overlapping cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_words},
            "supporting_check": None,
            "counts": {"non-overlapping cases with forecast >= 10": None},
            "decided_by": (f"Only {agreement:.1%} of the {n_active} active bars are trending-regime bars with the close in the "
                           "upper half of its 20-day range and a long forecast, below the 90% required."),
            "reading": "Situation checked on the regime column ('trending') plus near_high raw range position > 0 with a positive forecast.",
        }

    # ---------- main measure ----------
    sel_all = []
    sel_grid = []
    trend_f = []
    trend_x = []
    for coin, d in frames.items():
        valid = d["fwd"].notna()
        coin_mean = d.loc[valid, "fwd"].mean()
        if not np.isfinite(coin_mean):
            continue
        ex = d["fwd"] - coin_mean
        m = valid & d["forecast"].notna() & (d["forecast"] >= THR_F)
        sel_all.append(ex[m].values)
        sel_grid.append(ex[m & d["grid"]].values)
        tm = valid & d["forecast"].notna() & (d["regime"] == "trending")
        trend_f.append(d.loc[tm, "forecast"].values)
        trend_x.append(ex[tm].values)

    all_ex = np.concatenate(sel_all) if sel_all else np.array([])
    grid_ex = np.concatenate(sel_grid) if sel_grid else np.array([])
    n_cases = int(len(grid_ex))
    mean_all = float(np.mean(all_ex)) if len(all_ex) else None

    t_val = None
    if n_cases >= 2:
        sd = np.std(grid_ex, ddof=1)
        if sd > 0:
            t_val = float(np.mean(grid_ex) / (sd / np.sqrt(n_cases)))

    # ---------- supporting check ----------
    tf = np.concatenate(trend_f) if trend_f else np.array([])
    tx = np.concatenate(trend_x) if trend_x else np.array([])
    rho = None
    sup_pass = None
    if len(tf) >= 3 and np.std(tf) > 0 and np.std(tx) > 0:
        r, _ = stats.spearmanr(tf, tx)
        if np.isfinite(r):
            rho = float(r)
            sup_pass = bool(rho > 0)

    # ---------- decision ----------
    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases with forecast >= 10, below the plan's minimum of 30."
    elif mean_all is None or t_val is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_all > 0 and t_val >= 2:
        status = "confirmed"
        decided = "Confirm rule: mean excess 10-bar return after forecasts >= 10 is above 0 with t >= 2 and at least 30 non-overlapping cases."
    elif mean_all < 0 and t_val <= -2:
        status = "rejected"
        decided = "Reject rule: mean excess 10-bar return after forecasts >= 10 is below 0 with t <= -2 and at least 30 non-overlapping cases."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the t-statistic lies between -2 and 2 (or its sign disagrees with the mean)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_all,
            "statistic": ({"name": "t of the mean on non-overlapping 10-bar samples", "value": t_val}
                          if t_val is not None else None),
            "threshold": thr_words,
        },
        "supporting_check": {
            "name": "Spearman correlation of forecast vs forward 10-bar excess return on trending bars",
            "value": rho,
            "passed": sup_pass,
        },
        "counts": {"non-overlapping cases with forecast >= 10": n_cases},
        "decided_by": decided,
        "reading": ("Situation checked on regime == 'trending' plus near_high raw range position > 0 with a positive forecast; "
                    "the coin's mean 10-bar return is the mean of all its in-window forward 10-bar returns over all its windows; "
                    "the mean uses all bars with forecast >= 10 while the t and the case count use the non-overlapping grid "
                    "(positions 0, 10, 20, ... of each window)."),
    }
