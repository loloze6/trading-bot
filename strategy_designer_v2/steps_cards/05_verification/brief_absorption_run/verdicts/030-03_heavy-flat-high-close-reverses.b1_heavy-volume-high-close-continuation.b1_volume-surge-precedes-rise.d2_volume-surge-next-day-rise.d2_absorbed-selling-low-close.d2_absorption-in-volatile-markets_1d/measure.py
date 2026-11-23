import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.absorb.last_history_value"
    REGIME = "mean_reversion"

    # ---------- collect per-coin frames ----------
    frames = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            d["coin"] = coin
            d["window"] = w
            d["close"] = pd.to_numeric(d["close"], errors="coerce")
            d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce")
            d["raw"] = pd.to_numeric(d[RAW], errors="coerce") if RAW in d.columns else np.nan
            d["next_ret"] = d["close"].shift(-1) / d["close"] - 1.0
            d["prev_ret"] = d["close"] / d["close"].shift(1) - 1.0
            if "postRebalance_total_value" in d.columns:
                v = pd.to_numeric(d["postRebalance_total_value"], errors="coerce")
                d["book_ret"] = v / v.shift(1) - 1.0
            else:
                d["book_ret"] = np.nan
            if "postRebalance_current_allocation" in d.columns:
                d["pos_held"] = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce").shift(1)
            else:
                d["pos_held"] = np.nan
            d["is_regime"] = d["regime"].astype(str) == REGIME
            frames.append(d)

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "slope t of de-meaned next-day return on forecast",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 confirm, t <= -2 reject, on at least 300 active bars"},
            "supporting_check": {"name": "book timing gain", "value": None, "passed": None},
            "counts": {"regime-active bars pooled": 0},
            "decided_by": "No bars in the record, so fewer than 300 regime-active bars pooled.",
            "reading": "none",
        }

    all_df = pd.concat(frames, ignore_index=True)

    # ---------- situation check ----------
    active = all_df[all_df["forecast"].fillna(0) != 0]
    n_active = int(len(active))
    if n_active > 0:
        in_situation = (active["is_regime"]) & (active["raw"] > 0) & (active["forecast"] > 0)
        agreement = float(in_situation.mean())
    else:
        agreement = None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("Situation bars are those where the detector chose the volatility regime (20-day vol over its "
               "60-day mean >= 1, recorded as regime 'mean_reversion') and the component's raw product "
               "(close distance from high x volume ratio x vol ratio) is positive, on the long side; "
               "regime-active bars are bars with regime 'mean_reversion', the coin's mean daily return is pooled "
               "over all its windows, the slope t is the OLS t with an intercept, and the timing gain uses each "
               "coin's postRebalance_total_value day returns averaged across coins per day minus the held "
               "position times the coin's mean daily return averaged the same way.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "slope t of de-meaned next-day return on forecast",
                             "value": None, "statistic": None,
                             "threshold": "t >= 2 confirm, t <= -2 reject, on at least 300 active bars"},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bars in the high-volatility "
                           "regime with a positive heavy-volume low-close product, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- coin mean daily return over all windows ----------
    coin_mu = all_df.groupby("coin")["next_ret"].mean()
    all_df["mu"] = all_df["coin"].map(coin_mu)

    # ---------- main measure ----------
    reg = all_df[all_df["is_regime"]].copy()
    reg = reg.dropna(subset=["next_ret", "forecast", "mu"])
    y = (reg["next_ret"] - reg["mu"]).to_numpy(dtype=float)
    x = reg["forecast"].to_numpy(dtype=float)
    n = int(len(reg))

    slope = None
    t_val = None
    if n >= 3 and np.nanstd(x) > 0:
        X = np.column_stack([np.ones(n), x])
        beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
        resid = y - X @ beta
        dof = n - 2
        s2 = float(resid @ resid) / dof
        cov = s2 * np.linalg.inv(X.T @ X)
        se = float(np.sqrt(cov[1, 1]))
        slope = float(beta[1])
        t_val = float(slope / se) if se > 0 else None

    # ---------- supporting check: timing gain ----------
    b = all_df.dropna(subset=["book_ret", "pos_held", "mu"]).copy()
    b["mkt_part"] = b["pos_held"] * b["mu"]
    timing = None
    if len(b) > 0:
        daily = b.groupby(["window", "timestamp"])[["book_ret", "mkt_part"]].mean()
        timing = float(daily["book_ret"].mean() - daily["mkt_part"].mean())
    timing_pass = None if timing is None else bool(timing > 0)

    counts = {"regime-active bars pooled": n}

    # ---------- decision ----------
    if n < 300:
        status = "not observable"
        decided_by = f"Only {n} regime-active bars pooled, fewer than the plan's minimum of 300."
    elif t_val is None:
        status = "inconclusive"
        decided_by = "The slope t could not be computed (no variation in the forecast), so neither rule is met."
    elif t_val >= 2:
        if timing_pass:
            status = "confirmed"
            decided_by = "The slope t is 2 or more on at least 300 active bars and the timing gain is above 0."
        else:
            status = "inconclusive"
            decided_by = "The slope t is 2 or more but the timing gain is at or below 0."
    elif t_val <= -2:
        status = "rejected"
        decided_by = "The slope t is -2 or less on at least 300 active bars."
    else:
        status = "inconclusive"
        decided_by = "The slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {"name": "slope of next-day return minus coin mean on forecast, regime-active bars pooled",
                         "value": slope,
                         "statistic": None if t_val is None else {"name": "OLS slope t", "value": t_val},
                         "threshold": "t >= 2 (with timing gain > 0) confirms, t <= -2 rejects, on at least 300 active bars"},
        "supporting_check": {"name": "book timing gain (mean daily return minus position x coin mean daily return)",
                             "value": timing, "passed": timing_pass},
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
