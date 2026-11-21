import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.fall72.last_history_value"
    H = 2

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    per_coin = {}
    for coin, wins in bars.items():
        per_coin[coin] = []
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            coming_hour = (ts + pd.Timedelta(hours=1)).dt.hour
            close = df["close"].astype(float)
            fc = pd.to_numeric(df[FC], errors="coerce")
            # Raw 72-bar price change: recorded value, else recomputed from prices in this window.
            recomputed = close / close.shift(72) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").fillna(recomputed)
            else:
                raw = recomputed
            situation = coming_hour.isin([21, 22]) & (raw < 0)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
            per_coin[coin].append((df, ts, coming_hour, close, fc))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are long bars whose coming bar starts at 21:00 "
                           "or 22:00 UTC after a 72-bar price fall, so the config does not do what the "
                           "plan's Fidelity says."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    case_fc, case_ex = [], []
    for coin, items in per_coin.items():
        # Coin's mean 2-bar return over all windows, on the non-overlapping grid 0,2,4,... of each window.
        grid_rets = []
        for df, ts, ch, close, fc in items:
            c = close.values
            n = len(c)
            for p in range(0, n - H, H):
                r = c[p + H] / c[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        mu = float(np.mean(grid_rets))
        for df, ts, ch, close, fc in items:
            c = close.values
            n = len(c)
            f = fc.values
            chv = ch.values
            dates = ts.dt.date.values
            seen = set()
            for t in range(n - H):
                if chv[t] != 21 or not np.isfinite(f[t]) or f[t] <= 0:
                    continue
                if dates[t] in seen:
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r):
                    continue
                seen.add(dates[t])
                case_fc.append(float(f[t]))
                case_ex.append(float(r - mu))

    case_fc = np.array(case_fc)
    case_ex = np.array(case_ex)
    n_cases = int(len(case_fc))

    main_val, main_t = None, None
    if n_cases >= 2:
        prod = case_fc * case_ex
        main_val = float(prod.mean())
        sd = prod.std(ddof=1)
        main_t = float(main_val / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    n_top = n_bot = 0
    diff, welch_t = None, None
    if n_cases >= 3:
        q1, q2 = np.quantile(case_fc, [1 / 3, 2 / 3])
        bot = case_ex[case_fc <= q1]
        top = case_ex[case_fc >= q2]
        n_bot, n_top = int(len(bot)), int(len(top))
        if n_bot >= 2 and n_top >= 2:
            diff = float(top.mean() - bot.mean())
            welch_t = float(stats.ttest_ind(top, bot, equal_var=False).statistic)

    sup_passed = None if diff is None else bool(diff > 0)
    counts = {"cases overall": n_cases, "cases in top tercile": n_top, "cases in bottom tercile": n_bot}

    main_block = {
        "name": "mean of forecast x excess 2-bar return at 21:00 cases, pooled",
        "value": main_val,
        "statistic": None if main_t is None else {"name": "ordinary t", "value": main_t},
        "threshold": "t >= +2 to confirm (with top-minus-bottom > 0); t <= -2 to reject",
    }
    sup_block = {
        "name": "top minus bottom forecast tercile, mean excess 2-bar return (Welch t)",
        "value": diff,
        "passed": sup_passed,
    }
    reading = ("Cases are bars whose timestamp + 1h is 21:00 UTC with forecast > 0, first per UTC date per window, "
               "return taken positionally close[t+2]/close[t]-1 inside the window; the coin mean uses the "
               "non-overlapping 0,2,4,... grid of all its windows; terciles are pooled forecast cut points with "
               "bottom <= lower cut and top >= upper cut.")

    if n_cases < 200 or n_top < 60 or n_bot < 60 or main_t is None or welch_t is None:
        if n_cases < 200:
            why = f"Only {n_cases} cases overall, below the plan's minimum of 200."
        else:
            why = f"A tercile has fewer than 60 cases (top {n_top}, bottom {n_bot})."
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": main_block,
            "supporting_check": sup_block,
            "counts": counts,
            "decided_by": why,
            "reading": reading,
        }

    if main_t <= -2 or welch_t <= -2:
        status = "rejected"
        decided = (f"Reject rule met: main t = {main_t:.2f} (<= -2) or top-minus-bottom Welch t = "
                   f"{welch_t:.2f} (<= -2).")
    elif main_t >= 2 and diff > 0:
        status = "confirmed"
        decided = f"Confirm rule met: main t = {main_t:.2f} >= +2 and top-minus-bottom difference {diff:.5f} > 0."
    else:
        status = "inconclusive"
        decided = (f"Neither rule met: main t = {main_t:.2f}, top-minus-bottom difference {diff:.5f} "
                   f"with Welch t {welch_t:.2f}.")

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main_block,
        "supporting_check": sup_block,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
