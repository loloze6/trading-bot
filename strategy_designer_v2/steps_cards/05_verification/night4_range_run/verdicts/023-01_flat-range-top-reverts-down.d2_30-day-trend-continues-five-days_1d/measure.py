import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    PERIOD = 30
    THR = 0.5
    RAW = "debug_info.components.ret30.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    def num(df, col):
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        return pd.Series(np.nan, index=df.index)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = num(df, "close")
            high = num(df, "high")
            low = num(df, "low")
            fc = num(df, "forecast")
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)

            net = close - close.shift(PERIOD)
            rng = high.rolling(PERIOD, min_periods=PERIOD).max() - low.rolling(PERIOD, min_periods=PERIOD).min()
            ratio = (net.abs() / rng).where(rng > 0)
            # where the ratio cannot be rebuilt (window start, no history), the detector's recorded regime stands in
            in_sit = np.where(ratio.notna(), ratio >= THR - 1e-12, regime == "trending")

            raw = num(df, RAW)
            ret_recomp = close / close.shift(PERIOD) - 1.0
            side_val = raw.where(raw.notna(), ret_recomp)
            exp_side = np.sign(side_val)
            # where neither is available, fall back to the recorded regime as situation, side unknown -> no agreement
            active = fc.notna() & (fc != 0)
            for i in np.where(active.values)[0]:
                n_active += 1
                s = exp_side.iloc[i]
                if bool(in_sit[i]) and pd.notna(s) and s != 0 and np.sign(fc.iloc[i]) == s:
                    n_agree += 1

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "Pearson correlation of forecast with next 5-bar return minus normal drift"
    thr_text = "confirm: r > 0 with t >= 2 and timing part > 0; reject: r < 0 with t <= -2; at least 30 independent cases"
    reading = ("The situation is rebuilt as |close[t]-close[t-30]| over the max high minus min low of the last 30 bars "
               "(the recorded regime stands in where a window has under 30 bars of history) with the side the sign of "
               "the raw 30-bar return; the normal drift is each coin's mean 5-bar return on the non-overlapping grid of "
               "all its windows; 'before costs' is the position after each bar's trade times the next bar's return, "
               "averaged over coins per day, with the market part the same position times the coin's mean daily return.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_text},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the non-zero-forecast bars are bars where the 30-bar net move over the "
                           "30-bar high-low range is at least 0.5 with the forecast's sign equal to the 30-bar move's sign."),
            "reading": reading,
        }

    # ---------- 2. main measure ----------
    case_rows = []  # (coin, forecast, fwd ret)
    drift = {}
    daily_mean = {}
    for coin, wins in bars.items():
        grid_rets = []
        d_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = num(df, "close")
            fwd = close.shift(-H) / close - 1.0
            grid = np.arange(0, len(df), H)
            g = fwd.iloc[grid]
            grid_rets.extend(g.dropna().tolist())
            d_rets.extend((close.shift(-1) / close - 1.0).dropna().tolist())
            fc = num(df, "forecast")
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            for i in grid:
                f = fc.iloc[i]
                r = fwd.iloc[i]
                if regime.iloc[i] == "trending" and pd.notna(f) and f != 0 and pd.notna(r):
                    case_rows.append((coin, float(f), float(r)))
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan
        daily_mean[coin] = float(np.mean(d_rets)) if d_rets else np.nan

    xs = np.array([c[1] for c in case_rows], dtype=float)
    ys = np.array([c[2] - drift[c[0]] for c in case_rows], dtype=float)
    ok = np.isfinite(xs) & np.isfinite(ys)
    xs, ys = xs[ok], ys[ok]
    n_cases = int(len(xs))

    r_val = None
    t_val = None
    if n_cases >= 3 and np.std(xs) > 0 and np.std(ys) > 0:
        r_val = float(stats.pearsonr(xs, ys)[0])
        if abs(r_val) < 1:
            t_val = float(r_val * np.sqrt((n_cases - 2) / (1 - r_val ** 2)))
        else:
            t_val = float(np.sign(r_val) * np.inf)

    # ---------- supporting check: timing part ----------
    recs = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = num(df, "close")
            alloc = num(df, ALLOC)
            nxt = close.shift(-1) / close - 1.0
            ts = pd.to_datetime(df["timestamp"], utc=True)
            day = ts.dt.floor("D")
            tmp = pd.DataFrame({"day": day, "alloc": alloc, "ret": nxt})
            # last bar of each day; its gain runs to the next bar within the window
            tmp = tmp.groupby("day", sort=True).last().reset_index()
            tmp = tmp.dropna(subset=["alloc", "ret"])
            tmp["gain"] = tmp["alloc"] * tmp["ret"]
            tmp["mkt"] = tmp["alloc"] * daily_mean[coin]
            tmp["coin"] = coin
            recs.append(tmp[["day", "coin", "gain", "mkt"]])
    timing = None
    if recs:
        allr = pd.concat(recs, ignore_index=True).dropna()
        if len(allr):
            per_day = allr.groupby("day")[["gain", "mkt"]].mean()
            timing = float(per_day["gain"].mean() - per_day["mkt"].mean())
    sup_pass = None if timing is None else bool(timing > 0)

    # ---------- decision ----------
    if n_cases < 30 or t_val is None:
        status = "not observable"
        decided = f"Only {n_cases} independent cases (or no defined correlation), fewer than the plan's minimum of 30."
    elif r_val > 0 and t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "The correlation is positive with t >= 2 and the timing part is above 0."
    elif r_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "The correlation is negative with t <= -2."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 while the timing part is at or below 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The correlation's t is between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": r_val,
            "statistic": None if t_val is None else {"name": "correlation t", "value": t_val},
            "threshold": thr_text,
        },
        "supporting_check": {
            "name": "book mean daily return before costs minus market-rise gain (timing part)",
            "value": timing,
            "passed": sup_pass,
        },
        "counts": {"independent cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
