import numpy as np
import pandas as pd


def _component(df, cid, field="last_history_value"):
    """Read a recorded component value, from a flattened column or from the nested dict column."""
    col = f"debug_info.components.{cid}.{field}"
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    if "debug_info.components" in df.columns:
        def get(x):
            try:
                if isinstance(x, str):
                    import json
                    x = json.loads(x)
                v = x.get(cid, {})
                if isinstance(v, dict):
                    return v.get(field, np.nan)
                return np.nan
            except Exception:
                return np.nan
        return pd.to_numeric(df["debug_info.components"].map(get), errors="coerce")
    return pd.Series(np.nan, index=df.index)


def measure(bars):
    tol = 1e-9

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            high = pd.to_numeric(df["high"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            ret = close.pct_change()
            sd = ret.rolling(30, min_periods=30).std()
            rng = high - low
            width = (rng / close) / sd
            loc = (close - low) / rng.where(rng > 0)
            active = fc != 0
            computable = width.notna() & loc.notna()
            situ = (width >= 2.0 - tol) & (loc >= 0.9 - tol)
            ok = active & computable
            n_active_uncomputable += int((active & ~computable).sum())
            n_active += int(ok.sum())
            n_agree += int((ok & situ & (fc < 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9) if n_active > 0 else True

    reading = ("Situation checked as width>=2.0 (range/close over the 30-bar ddof-1 std of daily returns, "
               "including the bar) and close location from the low>=0.9, on the short side, leaving the "
               "falling-calm profile to the engine and excluding active bars with under 30 in-window returns; "
               "the coin's normal drift is its mean 1-bar return over all its windows; the day-clustered t uses "
               "per-day summed deviations with a D/(D-1) correction; 'closer to the high' means high_gap at or "
               "below the median of the cases, 'the others' above it.")

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active},
            "decided_by": ("Fewer than 90% of the active bars are short bars on wide (>=2 return std) days "
                           "closing in the top tenth of the range, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        all_r = []
        per_win = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            all_r.append(nxt.dropna().values)
            per_win.append((df, nxt))
        allr = np.concatenate(all_r) if all_r else np.array([])
        if allr.size == 0:
            continue
        drift = float(np.mean(allr))
        for df, nxt in per_win:
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            hg = _component(df, "high_gap")
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            mask = (fc < 0) & nxt.notna()
            for i in np.where(mask.values)[0]:
                rows.append({
                    "day": ts.iloc[i].floor("D") if pd.notna(ts.iloc[i]) else None,
                    "u": -(float(nxt.iloc[i]) - drift),
                    "hg": float(hg.iloc[i]) if pd.notna(hg.iloc[i]) else np.nan,
                })
    cases = pd.DataFrame(rows, columns=["day", "u", "hg"])
    n = int(len(cases))
    n_days = int(cases["day"].nunique()) if n else 0

    mean_u = None
    t = None
    if n > 0:
        mean_u = float(cases["u"].mean())
        dev = cases["u"] - mean_u
        S = dev.groupby(cases["day"]).sum()
        D = len(S)
        if D > 1:
            var = float((S ** 2).sum()) / (n ** 2) * D / (D - 1)
            se = np.sqrt(var)
            t = float(mean_u / se) if se > 0 else None

    sc_value = None
    sc_passed = None
    c = cases.dropna(subset=["hg"])
    if len(c) > 0:
        med = float(c["hg"].median())
        closer = c.loc[c["hg"] <= med, "u"]
        others = c.loc[c["hg"] > med, "u"]
        if len(closer) > 0 and len(others) > 0:
            sc_value = float(closer.mean() - others.mean())
            sc_passed = bool(sc_value >= 0)

    if n < 30:
        status = "not observable"
        decided = f"Only {n} cases, under the plan's minimum of 30 cases."
    elif mean_u is not None and t is not None and mean_u > 0 and t >= 2 and sc_passed is True:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t of 2 or more over at least 30 cases, and the supporting check passes."
    elif mean_u is not None and t is not None and mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t of -2 or less over at least 30 cases."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "Positive t of 2 or more but the supporting check fails (or cannot be computed)."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 (or not computable) over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement) if agreement is not None else None,
                            "passed": bool(passed)},
        "main_measure": {
            "name": "mean unusual 1-bar move in the short direction, before costs",
            "value": mean_u,
            "statistic": {"name": "t of the mean, cases of one day together", "value": t} if t is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 over >= 30 cases and check passes; reject: mean < 0 with t <= -2 over >= 30 cases",
        },
        "supporting_check": {
            "name": "unusual move of cases closer to the high minus the others (split at median high_gap) >= 0",
            "value": sc_value,
            "passed": sc_passed,
        },
        "counts": {"cases": n, "days": n_days},
        "decided_by": decided,
        "reading": reading,
    }
