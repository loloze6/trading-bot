import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    POS = "postRebalance_current_allocation"
    RAW = "debug_info.components.fall30.last_history_value"

    def to_day(ts):
        s = pd.Series(ts)
        if pd.api.types.is_numeric_dtype(s):
            mx = s.abs().max()
            unit = "ms" if mx > 1e11 else "s"
            dt = pd.to_datetime(s, unit=unit, utc=True)
        else:
            dt = pd.to_datetime(s, utc=True)
        return dt.dt.floor("D").values

    # ---- build per-bar frame, returns inside each window only ----
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            out = pd.DataFrame({
                "coin": coin,
                "window": w,
                "day": to_day(d["timestamp"]),
                "forecast": pd.to_numeric(d[FC], errors="coerce") if FC in d else np.nan,
                "pos": pd.to_numeric(d[POS], errors="coerce") if POS in d else np.nan,
                "raw": pd.to_numeric(d[RAW], errors="coerce") if RAW in d else np.nan,
                "regime": d["regime"].astype(str) if "regime" in d else "",
                "ret1": close.shift(-1) / close - 1.0,
            })
            rows.append(out)
    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "t of mean daily timing gain on bars in a position",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 confirm, t <= -2 reject, over at least 100 days in a position"},
            "supporting_check": None,
            "counts": {"days in a position": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }
    all_df = pd.concat(rows, ignore_index=True)

    # ---- situation check ----
    active = all_df[all_df["forecast"].notna() & (all_df["forecast"] != 0)]
    n_active = len(active)
    if n_active > 0:
        in_sit = (
            (active["regime"].str.strip().str.lower() == "unknown")
            & active["raw"].notna()
            & (active["raw"] < 0)
            & (active["forecast"] < 0)
        )
        agreement = float(in_sit.mean())
    else:
        agreement = None
    passed_sit = agreement is not None and agreement >= 0.9

    reading = ("The falling calm profile is read from the recorded regime ('unknown' = no veto fired, since the "
               "detector's components are not recorded and the 365-bar volatility percentile cannot be rebuilt inside "
               "a window), the situation is that profile with the 30-day change below 0 on the short side; bars in a "
               "position are those with a nonzero position after the trade; the drift is the coin's mean one-bar "
               "return over all its windows; the supporting split uses position bars with a negative forecast, deeper "
               "half = forecast at or below the median; fewer than 100 days in a position is treated as the plan's "
               "minimum count, so 'not observable'.")

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "t of mean daily timing gain on bars in a position",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 confirm, t <= -2 reject, over at least 100 days in a position"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are short bars inside the falling calm "
                           "profile with the coin below its close of 30 days ago."),
            "reading": reading,
        }

    # ---- drift: coin's mean one-bar return over all its windows ----
    drift = all_df.groupby("coin")["ret1"].mean()
    all_df["excess"] = all_df["ret1"] - all_df["coin"].map(drift)

    # ---- main measure ----
    inpos = all_df[all_df["pos"].notna() & (all_df["pos"] != 0) & all_df["excess"].notna()].copy()
    inpos["gain"] = inpos["pos"] * inpos["excess"]
    daily = inpos.groupby("day")["gain"].sum()
    n_days = int(len(daily))
    mean_gain = float(daily.mean()) if n_days > 0 else None
    if n_days > 1:
        sd = float(daily.std(ddof=1))
        t = float(mean_gain / (sd / np.sqrt(n_days))) if sd > 0 else None
    else:
        t = None

    # ---- supporting check ----
    sup = inpos[inpos["forecast"].notna() & (inpos["forecast"] < 0)]
    diff = None
    n_deep = n_shallow = 0
    if len(sup) > 0:
        med = float(sup["forecast"].median())
        deep = sup[sup["forecast"] <= med]["excess"]
        shallow = sup[sup["forecast"] > med]["excess"]
        n_deep, n_shallow = int(len(deep)), int(len(shallow))
        if n_deep > 0 and n_shallow > 0:
            diff = float(deep.mean() - shallow.mean())
    sup_passed = (diff < 0) if diff is not None else None

    counts = {
        "days in a position": n_days,
        "bars in a position": int(len(inpos)),
        "deeper half bars": n_deep,
        "shallower half bars": n_shallow,
    }

    main = {
        "name": "t of mean daily timing gain on bars in a position (position x (next-day return - coin drift), summed per day)",
        "value": mean_gain,
        "statistic": {"name": "t of the mean over days", "value": t} if t is not None else None,
        "threshold": "t >= 2 confirm, t <= -2 reject, over at least 100 days in a position",
    }
    support = {
        "name": "deeper-half minus shallower-half next-day excess return",
        "value": diff,
        "passed": sup_passed,
    }

    if n_days < 100:
        status = "not observable"
        decided = f"Only {n_days} days in a position, below the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The timing-gain t could not be computed (no variation across days)."
    elif t >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "Timing gain t >= 2 over at least 100 days in a position and the deeper half is lower than the shallower half."
        else:
            status = "inconclusive"
            decided = "Timing gain t >= 2 but the deeper half is not lower than the shallower half."
    elif t <= -2:
        status = "rejected"
        decided = "Timing gain t <= -2 over at least 100 days in a position: the shorts are followed by rebounds against the drift."
    else:
        status = "inconclusive"
        decided = "Timing gain t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
