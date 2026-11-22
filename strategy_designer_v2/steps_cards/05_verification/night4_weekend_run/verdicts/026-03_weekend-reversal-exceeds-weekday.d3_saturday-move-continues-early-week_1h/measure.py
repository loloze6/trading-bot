import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 48
    FC = "forecast"
    RAW = "debug_info.components.sat_move.last_history_value"

    n_active = 0
    n_agree = 0
    cases_f = []
    cases_r = []
    cases_coin = []
    drift = {}

    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            close = df["close"].astype(float).values
            n = len(df)

            # normal drift grid: positions 0, H, 2H, ... of each window
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 != 0:
                    grid_rets.append(c1 / c0 - 1.0)

            # situation bar: the bar closing at Monday 00:00 UTC (start time Sunday 23:00)
            close_time = ts + pd.Timedelta(hours=1)
            is_sit = ((close_time.dt.weekday == 0) & (close_time.dt.hour == 0)).values

            # Saturday's return: close at Sunday 00:00 / close at Saturday 00:00 - 1
            ts_to_close = pd.Series(close, index=ts.values)
            ts_to_close = ts_to_close[~ts_to_close.index.duplicated(keep="last")]
            sat_ret = np.full(n, np.nan)
            for i in np.where(is_sit)[0]:
                t = ts.iloc[i]
                k1 = (t - pd.Timedelta(hours=24)).to_datetime64()
                k0 = (t - pd.Timedelta(hours=48)).to_datetime64()
                c1 = ts_to_close.get(k1, np.nan)
                c0 = ts_to_close.get(k0, np.nan)
                if not (np.isfinite(c0) and np.isfinite(c1)) and i >= 48:
                    c1, c0 = close[i - 24], close[i - 48]
                if np.isfinite(c0) and np.isfinite(c1) and c0 != 0:
                    sat_ret[i] = c1 / c0 - 1.0
            # fallback to the component's raw sign where prices could not give it
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
                fill = np.isnan(sat_ret) & is_sit & np.isfinite(raw)
                sat_ret[fill] = raw[fill]

            fc = pd.to_numeric(df[FC], errors="coerce").values if FC in df.columns else np.full(n, np.nan)
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            ok = active & is_sit & np.isfinite(sat_ret) & (np.sign(fc) == np.sign(sat_ret)) & (sat_ret != 0)
            n_agree += int(ok.sum())

            # cases: every situation bar with a forecast and a 48-bar forward return in the window
            for i in np.where(is_sit)[0]:
                if i + H >= n or not np.isfinite(fc[i]):
                    continue
                c0, c1 = close[i], close[i + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 != 0:
                    coin_cases.append((float(fc[i]), c1 / c0 - 1.0))
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan
        for f, r in coin_cases:
            cases_f.append(f)
            cases_r.append(r)
            cases_coin.append(coin)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = agreement >= 0.9
    main_name = "OLS slope of 48-bar return minus drift on the Monday 00:00 forecast"
    thr = "confirm: slope > 0 with t >= 2 over >= 500 cases and supporting mean > 0; reject: slope < 0 with t <= -2 over >= 500 cases"
    reading = ("Cases are all coin-week bars closing at Monday 00:00 UTC with a recorded forecast and a 48-row forward return inside the window, "
               "pooled across coins in one OLS with its ordinary slope t; drift is each coin's mean 48-bar return on the 0,48,96,... grid of all its windows; "
               "the supporting mean counts every case, a zero forecast giving 0.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars closing at Monday 00:00 UTC "
                           "with the forecast's sign equal to Saturday's 24-hour return sign."),
            "reading": reading,
        }

    f = np.array(cases_f, dtype=float)
    r = np.array(cases_r, dtype=float)
    d = np.array([drift[c] for c in cases_coin], dtype=float)
    m = np.isfinite(f) & np.isfinite(r) & np.isfinite(d)
    f, x = f[m], (r - d)[m]
    n_cases = int(len(f))

    slope = None
    tval = None
    if n_cases >= 3 and np.std(f) > 0:
        lr = stats.linregress(f, x)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
    sup = float(np.mean(np.sign(f) * x)) if n_cases > 0 else None
    sup_pass = (sup is not None and sup > 0)

    if n_cases < 500:
        status = "not observable"
        decided = f"The plan's minimum of 500 cases is not reached ({n_cases} cases)."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm: the slope is positive with t >= 2 over at least 500 cases and the supporting mean is above 0."
    elif slope > 0 and tval >= 2:
        status = "inconclusive"
        decided = "Inconclusive: a positive slope with t >= 2 whose supporting mean is not above 0."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "Reject: the slope is negative with t <= -2 over at least 500 cases."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the slope has |t| < 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean of forecast sign x (48-bar return - drift)",
            "value": sup,
            "passed": (bool(sup_pass) if sup is not None else None),
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
