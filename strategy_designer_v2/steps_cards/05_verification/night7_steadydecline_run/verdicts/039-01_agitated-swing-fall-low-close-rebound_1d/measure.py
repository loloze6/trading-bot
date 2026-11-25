import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.fall_low_close.last_history_value"

    act_total = 0
    act_agree = 0
    case_rows = []      # (day, forecast, next_ret, coin)
    book_rows = []      # (day, coin, gain_before_costs, market_gain)
    coin_frames = {}

    # Gather each coin's windows, kept separate.
    for coin, wins in bars.items():
        frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            d["day"] = d["timestamp"].dt.floor("D")
            d["close"] = pd.to_numeric(d["close"], errors="coerce")
            d["fc"] = pd.to_numeric(d["forecast"], errors="coerce")
            d["next_ret"] = d["close"].shift(-1) / d["close"] - 1.0
            d["prev_ret"] = d["close"] / d["close"].shift(1) - 1.0
            if "postRebalance_current_allocation" in d.columns:
                d["alloc"] = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce")
            else:
                d["alloc"] = np.nan
            d["alloc_prev"] = d["alloc"].shift(1)
            if RAW in d.columns:
                d["raw"] = pd.to_numeric(d[RAW], errors="coerce")
            else:
                d["raw"] = np.nan
            frames.append(d)
        if frames:
            coin_frames[coin] = frames

    # Coin's mean daily return over all its windows (every bar is the 1-bar grid).
    coin_mean = {}
    for coin, frames in coin_frames.items():
        r = pd.concat([f["next_ret"] for f in frames]).dropna()
        coin_mean[coin] = float(r.mean()) if len(r) else np.nan

    for coin, frames in coin_frames.items():
        mu = coin_mean[coin]
        for d in frames:
            # Situation check: a down day graded by fall x close-near-low (raw > 0),
            # inside the agitated profile (regime not vetoed to chop), long side.
            fc = d["fc"].fillna(0.0)
            active = fc != 0
            regime = d["regime"].astype(str).str.lower() if "regime" in d.columns else pd.Series("unknown", index=d.index)
            agitated = regime != "chop"
            fall_ok = d["prev_ret"].isna() | (d["prev_ret"] < 0)
            situation = (d["raw"] > 0) & agitated & fall_ok
            act_total += int(active.sum())
            act_agree += int((active & situation & (fc > 0)).sum())

            # Cases: bars with a forecast above 0 and a next-day return in the window.
            m = (fc > 0) & d["next_ret"].notna()
            for day, f, r in zip(d.loc[m, "day"], fc[m], d.loc[m, "next_ret"]):
                case_rows.append((day, float(f), float(r) - mu, coin))

            # Book before costs: position held from t-1 close x return to t close.
            gain = d["alloc_prev"] * d["prev_ret"]
            mkt = d["alloc_prev"] * mu
            ok = gain.notna() & mkt.notna()
            for day, g, mg in zip(d.loc[ok, "day"], gain[ok], mkt[ok]):
                book_rows.append((day, coin, float(g), float(mg)))

    reading = ("Situation = raw FallCloseLocation value > 0 on a bar whose close is below the previous close (first bar of a "
               "window judged on the raw value alone) with regime not 'chop', long side; same-day cases are summed into one "
               "case by summing their forecasts and their excess next-day returns, then an OLS slope with intercept is fitted "
               "across days; the 100-day minimum counts distinct days with any coin's forecast above 0; the book's return "
               "before costs is the position held times the coin's next-bar return, averaged over coins each day.")

    pos_days_all = set()
    for coin, frames in coin_frames.items():
        for d in frames:
            pos_days_all.update(d.loc[d["fc"].fillna(0) > 0, "day"].tolist())
    n_pos_days = len(pos_days_all)

    if act_total == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "slope of next-day excess return on forecast (day-summed cases)",
                             "value": None, "statistic": None,
                             "threshold": "confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2"},
            "supporting_check": None,
            "counts": {"days with a positive forecast": 0},
            "decided_by": "No bar has a non-zero forecast, so fewer than the 100 days with a positive forecast the plan needs.",
            "reading": reading,
        }

    agreement = act_agree / act_total
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "slope of next-day excess return on forecast (day-summed cases)",
                             "value": None, "statistic": None,
                             "threshold": "confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2"},
            "supporting_check": None,
            "counts": {"days with a positive forecast": int(n_pos_days)},
            "decided_by": ("Fewer than 90% of the active bars are long bars on an agitated-profile down day with a positive "
                           "fall-times-close-near-low value, as the Fidelity's situation requires."),
            "reading": reading,
        }

    # Main measure.
    slope = None
    t_slope = None
    n_days = 0
    if case_rows:
        cdf = pd.DataFrame(case_rows, columns=["day", "fc", "xr", "coin"])
        g = cdf.groupby("day").agg(fc=("fc", "sum"), xr=("xr", "sum"))
        n_days = int(len(g))
        if n_days >= 3 and g["fc"].std(ddof=1) > 0:
            lr = stats.linregress(g["fc"].values, g["xr"].values)
            slope = float(lr.slope)
            t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # Supporting check.
    sup_val = None
    sup_pass = None
    if book_rows:
        bdf = pd.DataFrame(book_rows, columns=["day", "coin", "gain", "mkt"])
        daily = bdf.groupby("day").agg(gain=("gain", "mean"), mkt=("mkt", "mean"))
        if len(daily):
            sup_val = float(daily["gain"].mean() - daily["mkt"].mean())
            sup_pass = bool(sup_val > 0)

    counts = {"days with a positive forecast": int(n_pos_days), "days in the regression": int(n_days)}
    main = {"name": "slope of next-day return minus coin mean, on forecast, forecast > 0, day-summed cases",
            "value": slope,
            "statistic": {"name": "t of the OLS slope", "value": t_slope} if t_slope is not None else None,
            "threshold": "confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2"}
    sup = {"name": "book mean daily return before costs minus gain from market's rise",
           "value": sup_val, "passed": sup_pass}
    sc = {"agreement": float(agreement), "passed": True}

    if n_pos_days < 100:
        status = "not observable"
        decided = f"Only {n_pos_days} days with a positive forecast, below the plan's minimum of 100."
    elif slope is None or t_slope is None:
        status = "not observable"
        decided = "The slope or its t could not be computed from the cases, so the data cannot show the idea."
    elif slope > 0 and t_slope >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the supporting check passes (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the supporting check fails (inconclusive rule)."
    elif slope < 0 and t_slope <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
