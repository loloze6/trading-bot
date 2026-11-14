import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LHV = "debug_info.components.sma_cross.last_history_value"
    NW_LAGS = 10
    T_THR = 2.0
    Z_THR = 2.0
    MIN_SPANS = 30
    MIN_POS_BARS = 1000

    def wkey(w):
        try:
            return int(str(w).lstrip("w"))
        except Exception:
            return 10 ** 9

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce")
                in_sit = raw.notna() & (raw > 0)  # SMA50 above SMA200
            else:
                in_sit = pd.Series(False, index=df.index)  # missing column is not a value
            n_active += int(active.sum())
            n_agree += int((active & in_sit & (fc > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean next-bar return while forecast > 0 minus mean next-bar return over all bars (pooled)"
    main_thr = "confirm: excess > 0 with Newey-West(10) t >= 2; reject: excess < 0 with t <= -2"
    sup_name = "up-bar share while forecast > 0 vs coin's own up-bar share (binomial z)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars where the 50-day SMA is above "
                           "the 200-day SMA (sma_cross raw value > 0)"
                           if n_active > 0 else "No bar has a non-zero forecast, so the situation cannot be checked"),
            "reading": "Situation taken as sma_cross last_history_value > 0 with a long (positive) forecast; missing raw values count as outside the situation.",
        }

    # ---------- 2. build per-window next-bar returns ----------
    segments = []  # list of (coin, ret array, active array)
    all_rets = []
    coin_stats = {}
    n_spans = 0
    for coin, wins in bars.items():
        prev_end_ts = None
        prev_end_pos = False
        coin_all = []
        coin_act = []
        for w in sorted(wins.keys(), key=wkey):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp") if "timestamp" in df.columns else df
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            ret = np.full(len(close), np.nan)
            if len(close) > 1:
                ret[:-1] = close[1:] / close[:-1] - 1.0
            pos = np.where(np.isnan(fc), False, fc > 0)

            # spans: runs of forecast > 0, merged across windows that are contiguous in time
            ts = pd.to_datetime(df["timestamp"]) if "timestamp" in df.columns else None
            step = None
            if ts is not None and len(ts) > 1:
                step = ts.diff().dropna().median()
            for i in range(len(pos)):
                if pos[i] and (i == 0 or not pos[i - 1]):
                    cont = False
                    if i == 0 and prev_end_pos and prev_end_ts is not None and ts is not None and step is not None:
                        gap = ts.iloc[0] - prev_end_ts
                        cont = gap <= step * 1.5
                    if not cont:
                        n_spans += 1
            if ts is not None and len(ts) > 0:
                prev_end_ts = ts.iloc[-1]
                prev_end_pos = bool(pos[-1])

            valid = ~np.isnan(ret)
            act = pos & valid
            all_rets.append(ret[valid])
            coin_all.append(ret[valid])
            coin_act.append(ret[act])
            segments.append((coin, ret, act))
        ca = np.concatenate(coin_all) if coin_all else np.array([])
        cp = np.concatenate(coin_act) if coin_act else np.array([])
        coin_stats[coin] = (ca, cp)

    all_r = np.concatenate(all_rets) if all_rets else np.array([])
    pos_r = np.concatenate([s[1][s[2]] for s in segments]) if segments else np.array([])
    n_pos = int(len(pos_r))
    n_all = int(len(all_r))

    counts = {
        "distinct up-cross spans pooled across coins": int(n_spans),
        "bars with a positive forecast": n_pos,
        "all bars (next-bar returns)": n_all,
    }

    # ---------- main measure ----------
    value = None
    t_nw = None
    if n_pos > 1 and n_all > 0:
        mu_all = float(np.mean(all_r))
        dbar = float(np.mean(pos_r)) - mu_all
        value = dbar
        # residuals around the mean of active excess returns
        g = np.zeros(NW_LAGS + 1)
        for coin, ret, act in segments:
            e = np.where(act, ret - mu_all - dbar, 0.0)
            g[0] += np.sum(e[act] ** 2)
            for l in range(1, NW_LAGS + 1):
                if len(e) > l:
                    both = act[l:] & act[:-l]
                    g[l] += np.sum(e[l:][both] * e[:-l][both])
        g /= n_pos
        lrv = g[0] + 2.0 * sum((1.0 - l / (NW_LAGS + 1.0)) * g[l] for l in range(1, NW_LAGS + 1))
        if lrv > 0:
            t_nw = dbar / np.sqrt(lrv / n_pos)

    # ---------- supporting check ----------
    k = 0
    expected = 0.0
    var = 0.0
    for coin, (ca, cp) in coin_stats.items():
        if len(ca) == 0 or len(cp) == 0:
            continue
        p = float(np.mean(ca > 0))
        k += int(np.sum(cp > 0))
        expected += len(cp) * p
        var += len(cp) * p * (1 - p)
    z = None
    share_diff = None
    if n_pos > 0:
        share_diff = (k - expected) / n_pos
        if var > 0:
            z = (k - expected) / np.sqrt(var)
    sup_passed = None if z is None else bool(z >= Z_THR)

    # ---------- decision ----------
    if n_spans < MIN_SPANS:
        status = "not observable"
        decided = f"Only {n_spans} distinct up-cross spans pooled across coins, below the plan's minimum of {MIN_SPANS}."
    elif n_pos < MIN_POS_BARS:
        status = "not observable"
        decided = f"Only {n_pos} bars with a positive forecast, below the plan's minimum of {MIN_POS_BARS}."
    elif value is None or t_nw is None:
        status = "inconclusive"
        decided = "The excess return or its Newey-West t could not be computed."
    elif value > 0 and t_nw >= T_THR:
        if sup_passed:
            status = "confirmed"
            decided = "Excess mean return is above 0 with t >= 2 and the up-bar share is higher with z >= 2."
        else:
            status = "inconclusive"
            decided = "Excess mean return is above 0 with t >= 2, but the up-bar share check fails (z < 2)."
    elif value < 0 and t_nw <= -T_THR:
        status = "rejected"
        decided = "Excess mean return is below 0 with t <= -2: returns in cross spans are lower than holding."
    else:
        status = "inconclusive"
        decided = "The Newey-West t of the excess mean return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": None if value is None else float(value),
            "statistic": None if t_nw is None else {"name": "Newey-West t (10 lags)", "value": float(t_nw)},
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": sup_name,
            "value": None if z is None else float(z),
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Situation is sma_cross raw value > 0 with a positive forecast; next-bar returns stay inside each window "
                    "and the all-bars baseline pools every coin and window; Newey-West autocovariances use only pairs of "
                    "positive-forecast bars in the same window; an up-cross span is a run of positive forecast, merged across "
                    "time-contiguous windows; the binomial z sums each coin's expected up count from its own pooled up share; "
                    "unmet minimum counts give 'not observable' as the workflow requires."),
    }
