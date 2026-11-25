import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.day_fall.last_history_value"
    MIN_CASES = 100

    # ---------- coin mean daily return over all windows (within windows only) ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce")
            r = (c.shift(-1) / c - 1.0).iloc[:-1]
            rets.append(r.dropna())
        allr = pd.concat(rets) if rets else pd.Series(dtype=float)
        coin_mu[coin] = float(allr.mean()) if len(allr) else np.nan

    # ---------- situation check + sample collection ----------
    n_active = 0
    n_agree = 0
    xs, ys = [], []
    timing_rows = []  # (date, coin, gain, market_gain)

    for coin, wins in bars.items():
        mu = coin_mu[coin]
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            regime = d["regime"].astype(str)

            # the day's own percent return: recorded raw value, else recomputed from prices
            price_ret = c / c.shift(1) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                day_ret = raw.where(raw.notna(), price_ret)
            else:
                day_ret = price_ret

            agitated = regime == "unknown"  # the veto sends calm bars (vol percentile <= 0.5) to "chop"
            situation = agitated & (day_ret < 0)

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            nxt = c.shift(-1) / c - 1.0

            # main measure sample: forecast > 0, next-day return inside the window
            m = (fc > 0) & nxt.notna()
            xs.extend(fc[m].tolist())
            ys.extend((nxt[m] - mu).tolist())

            # timing gain, before costs
            alloc = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce")
            ok = nxt.notna() & alloc.notna()
            dates = pd.to_datetime(d["timestamp"], utc=True).dt.floor("D")
            for i in np.where(ok.values)[0]:
                timing_rows.append((dates.iloc[i], coin,
                                    float(alloc.iloc[i] * nxt.iloc[i]),
                                    float(alloc.iloc[i] * mu)))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of next-day excess return on forecast (forecast > 0 bars)"
    threshold = "confirm: slope > 0 with t >= 2 (and timing gain > 0); reject: slope < 0 with t <= -2"
    reading = ("Agitated profile read as regime 'unknown' (the volatility-percentile veto sends the rest to 'chop'), "
               "the day's fall as a negative recorded raw value (price return where not recorded); the timing gain is "
               "computed before costs as position after the bar's trade x next-bar return minus position x the coin's "
               "all-window mean daily return, averaged over coins per day then over days; the slope's t is the OLS t.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"bars with forecast > 0": int(len(xs)), "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are agitated down days with a long "
                           "forecast: the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    # ---------- supporting check: timing gain ----------
    timing = None
    if timing_rows:
        tr = pd.DataFrame(timing_rows, columns=["date", "coin", "gain", "mkt"])
        daily = tr.groupby("date")[["gain", "mkt"]].mean()
        timing = float(daily["gain"].mean() - daily["mkt"].mean())
    timing_pass = None if timing is None else bool(timing > 0)

    n_cases = len(xs)
    counts = {"bars with forecast > 0": int(n_cases)}

    slope, tval = None, None
    x = np.asarray(xs, float)
    y = np.asarray(ys, float)
    if n_cases >= 3 and np.ptp(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    main = {"name": main_name, "value": slope,
            "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
            "threshold": threshold}
    supp = {"name": "book timing gain before costs (mean daily)", "value": timing, "passed": timing_pass}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} bars with forecast > 0, below the plan's minimum of 100."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2 and timing_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the timing gain is above 0 (confirm rule)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 (reject rule)."
    elif slope > 0 and tval >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the timing gain is not above 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
