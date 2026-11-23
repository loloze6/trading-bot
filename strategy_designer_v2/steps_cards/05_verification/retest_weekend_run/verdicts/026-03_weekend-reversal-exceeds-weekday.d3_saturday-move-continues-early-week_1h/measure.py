import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 48
    MIN_CASES = 300
    RAW = "debug_info.components.sat_ret.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(d["close"], errors="coerce").values
            # the bar whose next bar starts Monday 00:00 UTC is the Sunday 23:00 bar
            nxt = ts + pd.Timedelta(hours=1)
            sit = ((nxt.dt.dayofweek == 0) & (nxt.dt.hour == 0)).values
            raw = (pd.to_numeric(d[RAW], errors="coerce").values
                   if RAW in d.columns else np.full(len(d), np.nan))
            # price-based Saturday return: close at end of Saturday vs close at end of Friday
            cmap = pd.Series(close, index=ts.values)
            cmap = cmap[~cmap.index.duplicated(keep="last")]
            sat_end = cmap.reindex((ts - pd.Timedelta(hours=24)).values).values
            fri_end = cmap.reindex((ts - pd.Timedelta(hours=48)).values).values
            price_ret = sat_end / fri_end - 1.0
            side = np.where(np.isfinite(raw), np.sign(raw), np.sign(price_ret))
            side = np.where(np.isfinite(side), side, 0.0)
            active = fc != 0
            n_active += int(active.sum())
            ok = active & sit & (side != 0) & (np.sign(fc) == side)
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    main_name = "OLS slope of 48-bar excess return on forecast, pooled"
    thr = "confirm: slope > 0 with t >= 2 and supporting mean > 0; reject: slope < 0 with t <= -2"
    sup_name = "mean of sign(forecast) x (48-bar return - coin mean 48-bar return)"
    reading = ("Situation bars are those whose next bar starts Monday 00:00 UTC, with the expected side from the "
               "sign of the recorded raw Saturday return (prices at Saturday/Friday 23:00 bars when missing); "
               "48-bar returns are by row position within a window, the coin's mean 48-bar return is taken on the "
               "non-overlapping grid 0, 48, 96, ... of all its windows, cases are trending bars with |forecast| >= 2 "
               "and a full 48-bar return in the window, and the slope's t is the ordinary OLS t.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": 0, "active_bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are Sunday-last-bar bars on the side "
                           "of Saturday's return, so the config does not do what the plan's Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    xs, ys, coins_of = [], [], []
    for coin, wins in bars.items():
        grid_rets = []
        case_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            reg = d["regime"].astype(str).values
            n = len(d)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            g = fwd[np.arange(0, n, H)]
            grid_rets.extend(list(g[np.isfinite(g)]))
            is_case = (reg == "trending") & np.isfinite(fc) & (np.abs(fc) >= 2) & np.isfinite(fwd)
            for i in np.where(is_case)[0]:
                case_rows.append((fc[i], fwd[i]))
        if len(grid_rets) == 0 or len(case_rows) == 0:
            continue
        mu = float(np.mean(grid_rets))
        for f, r in case_rows:
            xs.append(f)
            ys.append(r - mu)
            coins_of.append(coin)

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    n_cases = int(len(x))

    slope, t_slope, sup = None, None, None
    if n_cases >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else 0.0
    if n_cases > 0:
        sup = float(np.mean(np.sign(x) * y))

    counts = {"cases": n_cases}
    for c in sorted(set(coins_of)):
        counts["cases_" + str(c)] = int(sum(1 for k in coins_of if k == c))

    sup_passed = None if sup is None else bool(sup > 0)

    if n_cases < MIN_CASES or slope is None:
        status = "not observable"
        decided = f"Only {n_cases} cases, below the plan's minimum of {MIN_CASES} cases for a verdict."
    elif slope > 0 and t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the supporting mean is above 0 (confirm rule)."
    elif slope < 0 and t_slope <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: Saturday's move is reversed early in the week (reject rule)."
    elif slope > 0 and t_slope >= 2:
        status = "inconclusive"
        decided = "The slope is positive with t >= 2 but the supporting mean is not above 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The slope has |t| < 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name, "value": sup, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
