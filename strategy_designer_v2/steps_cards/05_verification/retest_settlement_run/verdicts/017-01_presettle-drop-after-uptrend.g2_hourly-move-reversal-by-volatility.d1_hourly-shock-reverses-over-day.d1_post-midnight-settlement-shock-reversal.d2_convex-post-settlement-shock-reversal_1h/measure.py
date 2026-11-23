import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW_COL = "debug_info.components.post_settle_move.last_history_value"

    def prep(df):
        df = df.copy().reset_index(drop=True)
        ts = pd.to_datetime(df["timestamp"], utc=True)
        df["_hour"] = ts.dt.hour.values
        df["_minute"] = ts.dt.minute.values
        close = pd.to_numeric(df["close"], errors="coerce").astype(float)
        df["_close"] = close
        ret = close / close.shift(1) - 1.0
        vol = ret.rolling(24, min_periods=24).std()
        raw_re = ret / vol.replace(0.0, np.nan)
        if RAW_COL in df.columns:
            raw = pd.to_numeric(df[RAW_COL], errors="coerce")
            raw = raw.where(raw.notna(), raw_re)
        else:
            raw = raw_re
        df["_raw"] = raw.astype(float)
        df["_fc"] = pd.to_numeric(df["forecast"], errors="coerce").astype(float)
        fwd = close.shift(-H) / close - 1.0
        df["_r24"] = fwd
        return df

    prepped = {}
    for coin, wins in bars.items():
        prepped[coin] = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            prepped[coin][w] = prep(df)

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in prepped.items():
        for w, df in wins.items():
            act = df["_fc"].notna() & (df["_fc"] != 0)
            n_active += int(act.sum())
            sit = (df["_hour"] == 0) & (df["_minute"] == 0)
            side_ok = np.sign(df["_fc"]) == -np.sign(df["_raw"])
            n_agree += int((act & sit & side_ok & df["_raw"].notna()).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of y = forecast x (r24 - d) over 00:00 bars with |forecast| >= 2"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"
    reading = ("d is each coin's mean 24-bar return on the non-overlapping grid (positions 0, 24, 48, ... of each window) "
               "pooled over all its windows; cases need close[t+24] inside the same window; the raw move is the recorded "
               "last_history_value (recomputed from closes where missing); the top third is the floor(n/3) cases with the "
               "largest |raw|, the rest are the bottom two thirds; the plan's 'fewer than 100 cases' rule is reported as "
               "not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases with |forecast| >= 2": None},
            "decided_by": (f"only {agreement:.1%} of active bars are 00:00-stamped bars with a forecast opposite to the "
                           "hour's vol-scaled move, below the 90% the plan's situation and fade side require"),
            "reading": reading,
        }

    # ---------- drift per coin ----------
    drift = {}
    for coin, wins in prepped.items():
        vals = []
        for w, df in wins.items():
            c = df["_close"].values
            idx = np.arange(0, len(c) - H, H)
            if len(idx) == 0:
                continue
            r = c[idx + H] / c[idx] - 1.0
            vals.append(r[np.isfinite(r)])
        allv = np.concatenate(vals) if vals else np.array([])
        drift[coin] = float(np.mean(allv)) if len(allv) else np.nan

    # ---------- cases ----------
    rows = []
    for coin, wins in prepped.items():
        d = drift[coin]
        for w, df in wins.items():
            m = ((df["_hour"] == 0) & (df["_minute"] == 0) & (df["_fc"].abs() >= 2)
                 & df["_r24"].notna() & np.isfinite(df["_r24"]))
            sub = df.loc[m]
            for _, r in sub.iterrows():
                if not np.isfinite(d):
                    continue
                rows.append((float(r["_fc"]), float(r["_r24"]) - d, float(r["_raw"])))

    n_cases = len(rows)
    counts = {"cases with |forecast| >= 2": int(n_cases), "active bars": int(n_active)}

    if n_cases < 100:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"only {n_cases} cases with |forecast| >= 2, below the plan's minimum of 100",
            "reading": reading,
        }

    fc = np.array([r[0] for r in rows])
    ex = np.array([r[1] for r in rows])
    raw = np.array([r[2] for r in rows])
    y = fc * ex
    mean_y = float(np.mean(y))
    sd = float(np.std(y, ddof=1))
    t = float(mean_y / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    # ---------- supporting check ----------
    sup_val = None
    sup_pass = None
    okr = np.isfinite(raw)
    fc_s, ex_s, raw_s = fc[okr], ex[okr], np.abs(raw[okr])
    n_s = len(raw_s)
    k = n_s // 3
    top_v = bot_v = None
    if k >= 1 and n_s - k >= 1:
        order = np.argsort(-raw_s, kind="mergesort")
        top, bot = order[:k], order[k:]
        def per_unit(ix):
            den = np.sum(raw_s[ix])
            return float(np.sum(np.sign(fc_s[ix]) * ex_s[ix]) / den) if den > 0 else np.nan
        top_v, bot_v = per_unit(top), per_unit(bot)
        if np.isfinite(top_v) and np.isfinite(bot_v):
            sup_val = float(top_v - bot_v)
            sup_pass = bool(top_v > bot_v)
    counts["top third cases"] = int(k)
    counts["bottom two thirds cases"] = int(n_s - k)

    if mean_y > 0 and t >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "mean of y is above 0 with t >= 2 and the top third's faded return per unit of move exceeds the bottom two thirds'"
    elif mean_y < 0 and t <= -2:
        status = "rejected"
        decided = "mean of y is below 0 with t <= -2"
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check failed (top third per unit of move not larger)"
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_y,
                         "statistic": {"name": "one-sample t", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": "faded return per unit of move, top third minus bottom two thirds",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
