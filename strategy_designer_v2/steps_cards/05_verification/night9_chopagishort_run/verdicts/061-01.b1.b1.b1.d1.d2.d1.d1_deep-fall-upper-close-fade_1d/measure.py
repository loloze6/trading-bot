import json
import numpy as np
import pandas as pd


def _component_raw(df, comp_id):
    """Return the raw (last_history_value) series of a strategy component, NaN where not recorded."""
    flat = f"debug_info.components.{comp_id}.last_history_value"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    out = pd.Series(np.nan, index=df.index, dtype=float)
    if "debug_info.components" in df.columns:
        for idx, v in df["debug_info.components"].items():
            d = v
            if isinstance(d, str):
                try:
                    d = json.loads(d)
                except Exception:
                    d = None
            if isinstance(d, dict):
                c = d.get(comp_id)
                if isinstance(c, dict) and c.get("last_history_value") is not None:
                    try:
                        out.at[idx] = float(c.get("last_history_value"))
                    except Exception:
                        pass
    return out


def _prep(df):
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df.sort_values("timestamp").reset_index(drop=True)
    for c in ["open", "high", "low", "close", "forecast"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["forecast"] = df["forecast"].fillna(0.0)
    return df


def _short_bets(f, band=2.0):
    """Bets on the short side: a rise of the short forecast's size of at least `band`
    from its lowest size since the last bet (from 0 after a flat or change of side)."""
    bets = np.zeros(len(f), dtype=bool)
    ref = 0.0
    prev_short = False
    for i, x in enumerate(f):
        if x < 0:
            m = -x
            if not prev_short:
                ref = 0.0
            if m - ref >= band - 1e-12:
                bets[i] = True
                ref = m
            else:
                ref = min(ref, m)
            prev_short = True
        else:
            ref = 0.0
            prev_short = False
    return bets


def measure(bars):
    H = 5
    # ---------- prepare ----------
    data = {}
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            data[(coin, w)] = _prep(df)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for (coin, w), df in data.items():
        rng = df["high"] - df["low"]
        loc = (df["close"] - df["low"]) / rng.where(rng > 0)
        ret5 = df["close"] / df["close"].shift(5) - 1.0
        raw = _component_raw(df, "fall_depth")
        ret5 = ret5.where(ret5.notna(), raw)  # same sign as the 5-day return
        regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
        profile_ok = regime.str.lower() != "chop"
        situation = (loc >= 0.5) & (ret5 < 0) & profile_ok
        situation = situation.fillna(False).astype(bool)
        active = df["forecast"] != 0
        n_active += int(active.sum())
        n_agree += int((active & situation & (df["forecast"] < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 5-bar move of short cases, in the short's direction"
    main_thr = "positive with t >= 2 to confirm; negative with t <= -2 to reject"
    reading = ("Profile part of the situation is read as the recorded regime not being 'chop' (its components are not "
               "recorded and the 365-bar volatility percentile cannot be rebuilt), each grid cell's case is its first "
               "bet bar, the day-pooled t uses a D/(D-1) cluster correction, thirds are floor(n/3) cases by |forecast|, "
               "and fewer than 30 distinct case days is reported as 'not observable' as the workflow's minimum-count rule asks.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "distinct case days": 0},
            "decided_by": (f"Only {agreement:.1%} of the active bars are short bars where the close is in the upper half "
                           "of the range after a negative 5-day return inside the choppy agitated profile (below 90 %)."),
            "reading": reading,
        }

    # ---------- coin normal drift ----------
    drift = {}
    coin_rets = {}
    for (coin, w), df in data.items():
        c = df["close"].values
        pos = np.arange(0, len(c) - H, H)
        r = c[pos + H] / c[pos] - 1.0
        coin_rets.setdefault(coin, []).extend([x for x in r if np.isfinite(x)])
    for coin, lst in coin_rets.items():
        drift[coin] = float(np.mean(lst)) if len(lst) > 0 else np.nan

    # ---------- cases ----------
    rows = []
    for (coin, w), df in data.items():
        f = df["forecast"].values
        bets = _short_bets(f)
        c = df["close"].values
        n = len(df)
        for start in range(0, n, H):
            idx = [i for i in range(start, min(start + H, n)) if bets[i]]
            if not idx:
                continue
            i = idx[0]
            if i + H >= n:
                continue
            r = c[i + H] / c[i] - 1.0
            d = drift.get(coin, np.nan)
            if not (np.isfinite(r) and np.isfinite(d)):
                continue
            u = -(r - d)
            rows.append({"coin": coin, "window": w, "ts": df["timestamp"].iloc[i],
                         "day": df["timestamp"].iloc[i].floor("D"), "absf": abs(f[i]), "u": u})
    cases = pd.DataFrame(rows)
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = float(cases["u"].mean()) if n_cases else None
    t_val = None
    if n_cases >= 2:
        dev = cases["u"] - mean_u
        s = dev.groupby(cases["day"]).sum().values
        D = len(s)
        if D >= 2:
            var = (s ** 2).sum() / (n_cases ** 2) * D / (D - 1)
            se = np.sqrt(var)
            t_val = float(mean_u / se) if se > 0 else None

    diff = None
    check_pass = None
    if n_cases >= 3:
        cs = cases.sort_values(["absf", "ts", "coin"], kind="mergesort").reset_index(drop=True)
        k = n_cases // 3
        bottom = cs["u"].iloc[:k].mean()
        top = cs["u"].iloc[n_cases - k:].mean()
        diff = float(top - bottom)
        check_pass = bool(diff > 0)

    counts = {"distinct case days": n_days, "cases": n_cases, "active bars": int(n_active)}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days across coins and windows, below the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2:
        if check_pass:
            status = "confirmed"
            decided = "Mean unusual move positive with t >= 2 and top-third minus bottom-third difference above 0."
        else:
            status = "inconclusive"
            decided = "Mean unusual move positive with t >= 2 but the top-third minus bottom-third difference is not above 0."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2: the price rises after these closes."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": mean_u,
                         "statistic": ({"name": "t of the mean, cases of one day pooled", "value": t_val}
                                       if t_val is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": "top third minus bottom third by |forecast|, mean unusual move",
                             "value": diff, "passed": check_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
