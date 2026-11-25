import numpy as np
import pandas as pd
from scipy import stats


def _to_day(ts):
    s = pd.Series(ts)
    if np.issubdtype(s.dtype, np.number):
        mx = float(np.nanmax(s.values)) if len(s) else 0.0
        unit = "ms" if mx > 1e11 else "s"
        dt = pd.to_datetime(s, unit=unit, utc=True)
    else:
        dt = pd.to_datetime(s, utc=True)
    return dt.dt.floor("D").astype(str).values


def measure(bars):
    POS = "postRebalance_current_allocation"
    RAW = "debug_info.components.close_loc.last_history_value"

    # ---------- per-coin mean daily return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        rets = np.concatenate(rets) if rets else np.array([])
        coin_mean[coin] = float(np.mean(rets)) if len(rets) else np.nan

    # ---------- situation check + collect measure rows ----------
    n_active = 0
    n_agree = 0
    rows = []  # (coin, day, pos, forecast, excess, agitated)
    for coin, wins in bars.items():
        mu = coin_mean[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            reg = df["regime"].astype(str).values
            hi = pd.to_numeric(df["high"], errors="coerce").values.astype(float)
            lo = pd.to_numeric(df["low"], errors="coerce").values.astype(float)
            cl = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            rng = hi - lo
            with np.errstate(divide="ignore", invalid="ignore"):
                loc = np.where(rng > 0, (cl - lo) / rng, np.nan)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values.astype(float)
                loc = np.where(np.isfinite(raw), raw, loc)
            agitated = (reg != "chop") & (reg != "nan") & (reg != "None")
            active = np.isfinite(f) & (f != 0)
            situ = agitated & np.isfinite(loc) & (loc >= 0) & (loc <= 1)
            n_active += int(active.sum())
            n_agree += int((active & situ & (f < 0)).sum())

            pos = pd.to_numeric(df[POS], errors="coerce").values.astype(float)
            days = _to_day(df["timestamp"].values)
            nxt = np.full(len(cl), np.nan)
            nxt[:-1] = cl[1:] / cl[:-1] - 1.0
            for i in range(len(df)):
                if not active[i]:
                    continue
                if not (np.isfinite(nxt[i]) and np.isfinite(pos[i]) and np.isfinite(mu)):
                    continue
                rows.append((coin, days[i], pos[i], f[i], nxt[i] - mu, bool(agitated[i])))

    agreement = float(n_agree / n_active) if n_active else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    reading = ("Agitation is read from the recorded regime (not 'chop', the volatility-percentile veto, whose component "
               "is not recorded and cannot be rebuilt within windows shorter than its 365-bar lookback) and the expected "
               "side is short; the main measure uses every bar with a nonzero forecast and a next bar in the same window, "
               "drift is each coin's mean daily return pooled over all its windows, the day-clustered t sums deviations "
               "per UTC day with a K/(K-1) factor, and the minimum count is the agitated measure bars with a nonzero "
               "position, with coins counted among them.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are agitated-regime bars with a short "
                           "forecast, as the plan's Fidelity requires (agitated situation, short side)."),
            "reading": reading,
        }

    if rows:
        d = pd.DataFrame(rows, columns=["coin", "day", "pos", "fc", "ex", "agit"])
    else:
        d = pd.DataFrame(columns=["coin", "day", "pos", "fc", "ex", "agit"])

    inpos = d[(d["agit"]) & (d["pos"] != 0)] if len(d) else d
    n_bars = int(len(inpos))
    n_coins = int(inpos["coin"].nunique()) if len(inpos) else 0

    # main measure
    mean_val = None
    t_val = None
    n_days = 0
    if len(d) > 0:
        x = (d["pos"] * d["ex"]).values.astype(float)
        N = len(x)
        m = float(np.mean(x))
        dev = pd.Series(x - m).groupby(d["day"].values).sum()
        K = int(len(dev))
        n_days = K
        if K > 1:
            se = np.sqrt(K / (K - 1.0) * float(np.sum(dev.values ** 2))) / N
            t_val = float(m / se) if se > 0 else None
        mean_val = m

    # supporting check
    slope = None
    if len(d) > 2 and np.std(d["fc"].values) > 0:
        lr = stats.linregress(d["fc"].values.astype(float), d["ex"].values.astype(float))
        slope = float(lr.slope)
    slope_pass = None if slope is None else bool(slope > 0)

    counts = {"agitated bars in a position": n_bars, "coins": n_coins,
              "measure bars": int(len(d)), "days": int(n_days)}

    if n_bars < 300 or n_coins < 3:
        status = "not observable"
        decided = (f"The plan's minimum of 300 agitated bars in a position across at least 3 coins is not reached "
                   f"({n_bars} bars, {n_coins} coins).")
    elif t_val is None or mean_val is None:
        status = "inconclusive"
        decided = "The day-clustered t of the main measure could not be computed."
    elif mean_val > 0 and t_val >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "The mean position-times-excess-return is above 0 with t >= 2 and the supporting slope is positive."
        else:
            status = "inconclusive"
            decided = "The main measure confirms (mean > 0, t >= 2) but the supporting slope is not positive."
    elif mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean position-times-excess-return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies strictly between -2 and 2 (or its sign disagrees with the rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean of position x (next-day return minus coin mean daily return)",
            "value": mean_val,
            "statistic": None if t_val is None else {"name": "t of the mean, cases of one day taken together", "value": t_val},
            "threshold": "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; otherwise inconclusive",
        },
        "supporting_check": {"name": "slope of next-day excess return on forecast > 0",
                             "value": slope, "passed": slope_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
