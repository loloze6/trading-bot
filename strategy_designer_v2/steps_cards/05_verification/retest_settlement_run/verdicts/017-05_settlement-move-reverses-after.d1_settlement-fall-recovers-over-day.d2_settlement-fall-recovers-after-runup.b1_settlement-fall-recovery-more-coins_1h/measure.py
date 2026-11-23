import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    BAND = 2.0
    MIN_CASES = 100
    RAW = "debug_info.components.fall_x_runup.last_history_value"

    def prep(df):
        d = df.copy()
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        d = d.sort_values("timestamp").reset_index(drop=True)
        d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce")
        d["close"] = pd.to_numeric(d["close"], errors="coerce")
        return d

    data = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            data[(coin, w)] = prep(df)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for (coin, w), d in data.items():
        ts = d["timestamp"]
        diffs = ts.diff().dropna()
        bar_len = diffs.median() if len(diffs) else pd.Timedelta(hours=1)
        if pd.isna(bar_len) or bar_len <= pd.Timedelta(0):
            bar_len = pd.Timedelta(hours=1)
        end = ts + bar_len
        settle = end.dt.hour.isin([0, 16]).values & (end.dt.minute == 0).values

        c = d["close"]
        fall2 = (c / c.shift(2) - 1).values
        rise168 = (c / c.shift(168) - 1).values
        price_cond = np.where(np.isnan(fall2) | np.isnan(rise168), False,
                              (np.nan_to_num(fall2) < 0) & (np.nan_to_num(rise168) > 0))
        if RAW in d.columns:
            raw = pd.to_numeric(d[RAW], errors="coerce").values
            comp_cond = np.where(np.isnan(raw), price_cond, np.nan_to_num(raw) > 0)
        else:
            comp_cond = price_cond
        situation = settle & comp_cond

        f = d["forecast"].values
        active = ~np.isnan(f) & (f != 0)
        n_active += int(active.sum())
        n_agree += int((active & situation & (np.nan_to_num(f) > 0)).sum())

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "forecast-weighted mean excess 24-bar return", "value": None,
                             "statistic": None, "threshold": "above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": "No bar has a non-zero forecast, so there are no cases (fewer than the 100 cases the plan requires).",
            "reading": "none",
        }

    agreement = n_agree / n_active
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": None,
            "decided_by": (f"Only {agreement:.1%} of active bars are settlement bars (bar closing at 00:00 or 16:00 UTC) "
                           "with a 2-bar fall after a positive 168-bar return and a long forecast; the plan's situation "
                           "and the config's active bars disagree."),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    # normal 24-bar drift per coin, non-overlapping grid, all windows together
    drift = {}
    for coin in bars.keys():
        rets = []
        for (c_, w), d in data.items():
            if c_ != coin:
                continue
            cl = d["close"].values
            for p in range(0, len(cl) - H, H):
                a, b = cl[p], cl[p + H]
                if np.isfinite(a) and np.isfinite(b) and a != 0:
                    rets.append(b / a - 1)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    case_f = []
    case_x = []
    for (coin, w), d in data.items():
        f = d["forecast"].fillna(0.0).values
        cl = d["close"].values
        n = len(f)
        is_bet = np.zeros(n, dtype=bool)
        ref_long, ref_short = 0.0, 0.0
        for i in range(n):
            v = f[i]
            if v > 0:
                ref_short = 0.0
                if v - ref_long >= BAND:
                    is_bet[i] = True
                    ref_long = v
                else:
                    ref_long = min(ref_long, v)
            elif v < 0:
                ref_long = 0.0
                if ref_short - v >= BAND:
                    is_bet[i] = True
                    ref_short = v
                else:
                    ref_short = max(ref_short, v)
            else:
                ref_long, ref_short = 0.0, 0.0
        seen_cells = set()
        for i in np.where(is_bet)[0]:
            cell = i // H
            if cell in seen_cells:
                continue
            seen_cells.add(cell)
            if i + H >= n:
                continue
            a, b = cl[i], cl[i + H]
            if not (np.isfinite(a) and np.isfinite(b)) or a == 0 or not np.isfinite(drift.get(coin, np.nan)):
                continue
            excess = (b / a - 1) - drift[coin]
            case_f.append(float(f[i]))
            case_x.append(float(np.sign(f[i]) * excess))

    case_f = np.array(case_f, dtype=float)
    case_x = np.array(case_x, dtype=float)
    n_cases = int(len(case_f))

    reading = ("Cases are holding-period bets (forecast rise of >= 2 points from its lowest level on its side since the "
               "last bet, from 0 after a flat), the first per 24-bar grid cell from each window's first row, dropped when "
               "the 24-bar return leaves the window; the weighted-mean t is the ordinary t of f_i*x_i/mean(f) over cases.")

    wmean = None
    tval = None
    corr = None
    if n_cases >= 1:
        w_abs = np.abs(case_f)
        if w_abs.sum() > 0:
            wmean = float(np.sum(w_abs * case_x) / np.sum(w_abs))
            if n_cases >= 2:
                y = w_abs * case_x / w_abs.mean()
                sd = y.std(ddof=1)
                tval = float(y.mean() / (sd / np.sqrt(n_cases))) if sd > 0 else None
        if n_cases >= 2 and np.std(case_f) > 0 and np.std(case_x) > 0:
            corr = float(stats.pearsonr(case_f, case_x)[0])

    corr_pass = None if corr is None else bool(corr > 0)

    main = {
        "name": "forecast-weighted mean excess 24-bar return",
        "value": wmean,
        "statistic": {"name": "t of the weighted mean", "value": tval} if tval is not None else None,
        "threshold": "above 0 with t >= 2 to confirm (with correlation > 0); below 0 with t <= -2 to reject",
    }
    supp = {"name": "Pearson correlation of case forecast and excess return", "value": corr, "passed": corr_pass}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases over all coins and windows, fewer than the plan's minimum of 100."
    elif wmean is None or tval is None:
        status = "inconclusive"
        decided = "The weighted mean or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif wmean > 0 and tval >= 2:
        if corr_pass:
            status = "confirmed"
            decided = "The forecast-weighted mean excess return is above 0 with t >= 2 and the correlation is above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the correlation is 0 or below (or undefined), which the plan calls inconclusive."
    elif wmean < 0 and tval <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
