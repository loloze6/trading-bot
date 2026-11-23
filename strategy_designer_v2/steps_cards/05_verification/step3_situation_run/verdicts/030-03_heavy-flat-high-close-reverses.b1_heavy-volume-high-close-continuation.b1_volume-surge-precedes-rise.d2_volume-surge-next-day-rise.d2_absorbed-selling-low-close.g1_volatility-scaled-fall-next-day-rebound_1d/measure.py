import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.fall_depth.last_history_value"
    TOL = 1e-9

    def zfall_from_prices(close):
        r = close.pct_change()
        sd = r.rolling(20, min_periods=20).std(ddof=1).shift(1)
        sd2 = r.rolling(20, min_periods=20).std(ddof=1)
        # Use the std including the bar when the shifted one is unavailable (the engine's exact window is not recorded).
        sd = sd.fillna(sd2)
        return r / sd

    frames = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["_ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("_ts").reset_index(drop=True)
            close = d["close"].astype(float)
            d["_ret1"] = close.shift(-1) / close - 1.0
            recomputed = zfall_from_prices(close)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                d["_z"] = raw.where(raw.notna(), recomputed)
            else:
                d["_z"] = recomputed
            d["_coin"] = coin
            d["_win"] = w
            d["_fc"] = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            d["_day"] = d["_ts"].dt.floor("D")
            frames.append(d[["_ts", "_day", "_coin", "_win", "_fc", "_z", "_ret1", "regime"]])

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean excess next-day return on case bars", "value": None,
                             "statistic": None, "threshold": "t >= 2 to confirm, t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"cases (case days)": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }

    allb = pd.concat(frames, ignore_index=True)

    # ---- Situation check: active bars must be falls of 2+ usual moves, held long ----
    active = allb[allb["_fc"] != 0]
    n_active = len(active)
    if n_active > 0:
        ok = (active["_z"] <= -2.0 + TOL) & (active["_fc"] > 0)
        agreement = float(ok.mean())
    else:
        agreement = None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean excess next-day return on case bars", "value": None,
                             "statistic": None, "threshold": "t >= 2 to confirm, t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("No active bars in the record." if agreement is None else
                           "Fewer than 90% of the active bars are long positions on days whose volatility-scaled "
                           "return is -2 or below, as the plan's situation requires."),
            "reading": "The situation is read from the recorded raw fall_depth value (recomputed from prices where missing): value <= -2 with forecast > 0.",
        }

    # ---- Coin mean daily return over all windows ----
    coin_mean = allb.dropna(subset=["_ret1"]).groupby("_coin")["_ret1"].mean()

    # ---- Cases ----
    cases = allb[(allb["regime"] == "mean_reversion") & (allb["_fc"] > 0)].dropna(subset=["_ret1"]).copy()
    cases["_ex"] = cases["_ret1"] - cases["_coin"].map(coin_mean)
    n_cases = int(len(cases))
    n_days = int(cases["_day"].nunique()) if n_cases else 0

    threshold = "mean above 0 with t >= 2 (and supporting check) confirms; below 0 with t <= -2 rejects; at least 30 case days"
    counts = {"cases (case days)": n_days, "case bars": n_cases}

    mean_ex = float(cases["_ex"].mean()) if n_cases else None
    t = None
    if n_days >= 2:
        D = cases.groupby("_day")["_ex"].sum()
        sd = D.std(ddof=1)
        if sd > 0:
            t = float(D.mean() / (sd / np.sqrt(len(D))))

    # ---- Supporting check ----
    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        med = cases["_fc"].median()
        up = cases[cases["_fc"] > med]
        lo = cases[cases["_fc"] <= med]
        if len(up) == 0:
            up = cases[cases["_fc"] >= med]
            lo = cases[cases["_fc"] < med]
        if len(up) > 0 and len(lo) > 0:
            sup_val = float(up["_ex"].mean() - lo["_ex"].mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {"name": "mean excess next-day return on case bars (close[t+1]/close[t]-1 minus coin mean daily return)",
            "value": mean_ex,
            "statistic": {"name": "t of the mean, cases of one day summed", "value": t} if t is not None else None,
            "threshold": threshold}
    support = {"name": "upper-half minus lower-half mean excess return, split at median forecast",
               "value": sup_val, "passed": sup_pass}
    reading = ("Cases are bars in regime mean_reversion with forecast > 0 and a next bar in the same window; "
               "the t uses per-day sums of the excess returns over the case days; the median split puts forecasts "
               "above the median in the upper half and at or below it in the lower half (>= vs < if the upper half would be empty).")

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} case days, below the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t could not be computed (no variation across case days)."
    elif mean_ex > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean excess next-day return above 0 with t >= 2 and the upper half beating the lower half."
    elif mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "Mean excess next-day return below 0 with t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
