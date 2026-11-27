import json
import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    BAND = 2.0
    COMP = "swing_rise"

    def _parse(v):
        if isinstance(v, dict):
            return v
        if isinstance(v, str):
            try:
                d = json.loads(v)
                return d if isinstance(d, dict) else None
            except Exception:
                return None
        return None

    def comp_val(df, cid, field):
        col = f"debug_info.components.{cid}.{field}"
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").reset_index(drop=True)
        if "debug_info.components" in df.columns:
            out = []
            for v in df["debug_info.components"].tolist():
                d = _parse(v)
                val = np.nan
                if d is not None:
                    c = d.get(cid)
                    c = _parse(c) if not isinstance(c, dict) else c
                    if isinstance(c, dict) and c.get(field) is not None:
                        try:
                            val = float(c.get(field))
                        except Exception:
                            val = np.nan
                out.append(val)
            return pd.Series(out, dtype=float)
        return pd.Series(np.nan, index=range(len(df)), dtype=float)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            raw = comp_val(df, COMP, "last_history_value")
            post = comp_val(df, COMP, "post_pipeline_value")
            r = close.pct_change()
            vsr_px = (close / close.shift(14) - 1) / (r.rolling(30).std() * np.sqrt(14))
            vsr = raw.where(raw.notna(), vsr_px)
            regime = df["regime"].astype(str).str.lower() if "regime" in df.columns else pd.Series("", index=df.index)
            situation = (vsr >= 2.0) & (regime == "trending")
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            prepared[(coin, w)] = (close.values, fc.values, post.values, ts)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "mean unusual 7-bar move of long cases (return minus coin's normal 7-bar drift)"
    thr = "confirm: mean > 0 with day-clustered t >= 2 and correlation > 0; reject: mean < 0 with t <= -2"
    sup_name = "correlation of entry swing_rise post_pipeline_value with unusual move"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": "fewer than 90% of bars with a non-zero forecast are long bars where the 14-day swing-scaled rise is >= 2 in the choppy calm (trending, not vetoed) regime, as the Fidelity requires",
            "reading": "situation = swing_rise last_history_value (recomputed from closes where missing) >= 2 and regime 'trending' (the profile vetoes send other bars to chop), side long.",
        }

    # ---------- normal drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w in wins:
            if (coin, w) not in prepared:
                continue
            close = prepared[(coin, w)][0]
            for i in range(0, len(close) - H, H):
                a, b = close[i], close[i + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- cases ----------
    cases = []  # (unusual, entry_post, day)
    for (coin, w), (close, fc, post, ts) in prepared.items():
        n = len(close)
        low = 0.0
        taken_cells = set()
        for t in range(n):
            f = fc[t]
            if not np.isfinite(f) or f <= 0:
                low = 0.0
                continue
            if f - low >= BAND:
                low = f
                cell = t // H
                if cell in taken_cells:
                    continue
                taken_cells.add(cell)
                if t + H >= n:
                    continue
                a, b = close[t], close[t + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0) or not np.isfinite(drift[coin]):
                    continue
                u = (b / a - 1) - drift[coin]
                day = ts.iloc[t].strftime("%Y-%m-%d") if pd.notna(ts.iloc[t]) else f"{w}_{t}"
                cases.append((u, post[t], day))
            else:
                low = min(low, f)

    n_cases = len(cases)
    days = sorted(set(c[2] for c in cases))
    n_days = len(days)
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_u = float(np.mean([c[0] for c in cases])) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        u = np.array([c[0] for c in cases])
        dev = u - u.mean()
        s = pd.Series(dev).groupby([c[2] for c in cases]).sum().values
        G = len(s)
        var = (G / (G - 1)) * np.sum(s ** 2) / n_cases ** 2
        if var > 0:
            t_val = float(u.mean() / np.sqrt(var))

    corr = None
    pairs = [(c[0], c[1]) for c in cases if np.isfinite(c[1])]
    if len(pairs) >= 3:
        x = np.array([p[1] for p in pairs]); y = np.array([p[0] for p in pairs])
        if np.std(x) > 0 and np.std(y) > 0:
            corr = float(stats.pearsonr(x, y)[0])
    sup_pass = None if corr is None else bool(corr > 0)

    reading = ("situation = swing_rise last_history_value (recomputed from closes where missing) >= 2 with regime 'trending' as the profile filter; "
               "a case is the first long bet (forecast rise >= 2 points from its low on the long side) in each 7-bar grid cell of a window, "
               "day-clustered t uses per-day summed deviations with a G/(G-1) correction, and the correlation is Pearson.")

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = f"minimum counts not reached: {n_cases} cases (need 30) on {n_days} distinct days (need 20)."
    elif t_val is None:
        status = "inconclusive"
        decided = "the t of the mean unusual move could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "mean unusual move positive with t >= 2 and correlation above 0: the confirm rule."
        else:
            status = "inconclusive"
            decided = "confirming t but the correlation is 0 or below (or not computable): inconclusive by the plan."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "mean unusual move negative with t <= -2: the reject rule."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2: inconclusive by the plan."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t_val} if t_val is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": corr, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
