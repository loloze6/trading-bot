import numpy as np
import pandas as pd
import json


def measure(bars):
    LIFT_ID = "lift"

    def to_time(s):
        if np.issubdtype(s.dtype, np.number):
            mx = float(np.nanmax(s.values)) if len(s) else 0.0
            unit = "ms" if mx > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    def get_lift(df):
        col = "debug_info.components.%s.last_history_value" % LIFT_ID
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        if "debug_info.components" in df.columns:
            out = []
            for v in df["debug_info.components"].values:
                val = np.nan
                try:
                    d = v
                    if isinstance(d, str):
                        d = json.loads(d)
                    if isinstance(d, dict) and LIFT_ID in d and isinstance(d[LIFT_ID], dict):
                        x = d[LIFT_ID].get("last_history_value")
                        if x is not None:
                            val = float(x)
                except Exception:
                    val = np.nan
                out.append(val)
            return pd.Series(out, index=df.index, dtype=float)
        return pd.Series(np.nan, index=df.index, dtype=float)

    def recompute_lift(df):
        c = df["close"].astype(float)
        l = df["low"].astype(float)
        std = c.pct_change().rolling(30, min_periods=30).std()
        return ((c - l) / c) / std

    # ---- build per-coin data and drift ----
    frames = []
    for coin, wins in bars.items():
        coin_rets = []
        per = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            d["close"] = pd.to_numeric(d["close"], errors="coerce")
            d["fwd"] = d["close"].shift(-1) / d["close"] - 1.0
            coin_rets.append(d["fwd"].dropna().values)
            lift = get_lift(d)
            rec = recompute_lift(d)
            d["lift_raw"] = lift.where(lift.notna(), rec)
            d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            d["day"] = to_time(d["timestamp"]).dt.floor("D")
            d["coin"] = coin
            d["window"] = w
            per.append(d[["coin", "window", "day", "forecast", "regime", "lift_raw", "fwd"]])
        if not per:
            continue
        allr = np.concatenate(coin_rets) if coin_rets else np.array([])
        drift = float(np.mean(allr)) if len(allr) else np.nan
        for d in per:
            d = d.copy()
            d["drift"] = drift
            frames.append(d)

    reading = ("Situation = recorded raw lift (recomputed from prices if missing) >= 2.0 on bars where the "
               "regime detector chose mean_reversion (its vetoes are the falling-calm profile, whose 60- and "
               "365-bar inputs cannot be rebuilt inside a window), expected side short; cases = every bar with "
               "forecast < 0 that has a next bar in its window; drift = coin's mean 1-bar return over all its "
               "windows; t clusters deviations by UTC day; supporting split: upper = raw lift strictly above the "
               "cases' median, lower = at or below.")

    if not frames:
        return {"status": "not observable",
                "situation_check": {"agreement": None, "passed": False},
                "main_measure": {"name": "mean next-day unusual move, signed for the short", "value": None,
                                 "statistic": None, "threshold": "t >= 2 to confirm, t <= -2 to reject"},
                "supporting_check": None,
                "counts": {"distinct case days": 0},
                "decided_by": "No bars in the record.",
                "reading": reading}

    data = pd.concat(frames, ignore_index=True)

    # ---- situation check ----
    active = data[data["forecast"] != 0]
    n_active = len(active)
    if n_active > 0:
        ok = ((active["regime"].astype(str) == "mean_reversion")
              & (active["lift_raw"] >= 2.0)
              & (active["forecast"] < 0))
        agreement = float(ok.mean())
    else:
        agreement = None
    passed = agreement is not None and agreement >= 0.9

    if n_active > 0 and not passed:
        return {"status": "mismatch",
                "situation_check": {"agreement": agreement, "passed": False},
                "main_measure": {"name": "mean next-day unusual move, signed for the short", "value": None,
                                 "statistic": None, "threshold": "t >= 2 to confirm, t <= -2 to reject"},
                "supporting_check": None,
                "counts": {"active bars": int(n_active)},
                "decided_by": ("Fewer than 90% of active bars are short bars of the falling-calm profile with the "
                               "close at least 2 usual moves above the low."),
                "reading": reading}

    # ---- main measure ----
    cases = data[(data["forecast"] < 0) & data["fwd"].notna() & data["drift"].notna()].copy()
    cases["unusual"] = -(cases["fwd"] - cases["drift"])
    n = len(cases)
    n_days = int(cases["day"].nunique()) if n else 0

    mean_u = float(cases["unusual"].mean()) if n else None
    t = None
    if n >= 2 and n_days >= 2:
        dev = cases["unusual"] - mean_u
        s = dev.groupby(cases["day"]).sum().values
        var = float(np.sum(s ** 2)) / (n ** 2) * n_days / (n_days - 1)
        if var > 0:
            t = mean_u / np.sqrt(var)

    # ---- supporting check ----
    sup_val = None
    sup_pass = None
    sc = cases[cases["lift_raw"].notna()]
    if len(sc) >= 2:
        med = sc["lift_raw"].median()
        up = sc.loc[sc["lift_raw"] > med, "unusual"]
        lo = sc.loc[sc["lift_raw"] <= med, "unusual"]
        if len(up) > 0 and len(lo) > 0:
            sup_val = float(up.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"distinct case days": n_days, "cases": int(n)}

    if n_days < 30:
        status = "not observable"
        decided = "Fewer than 30 distinct case days across all coins (%d)." % n_days
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed (zero variance)."
    elif mean_u > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move positive with t >= 2 and upper-minus-lower difference above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the upper-half-minus-lower-half difference is at or below 0."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": bool(passed)},
        "main_measure": {"name": "mean next-day unusual move, signed for the short, before costs",
                         "value": mean_u,
                         "statistic": ({"name": "t of the mean, cases grouped by day", "value": float(t)}
                                       if t is not None else None),
                         "threshold": "positive with t >= 2 to confirm; negative with t <= -2 to reject"},
        "supporting_check": {"name": "upper-half minus lower-half mean unusual move (split at raw lift median)",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
