import numpy as np
import pandas as pd
from scipy import stats


def _to_day(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype(float)
        unit = "ms" if np.nanmax(np.abs(v.values)) > 1e11 else "s"
        dt = pd.to_datetime(v, unit=unit, utc=True)
    else:
        dt = pd.to_datetime(s, utc=True)
    return dt.dt.strftime("%Y-%m-%d").values


def measure(bars):
    RAW = "debug_info.components.depth.last_history_value"
    POST = "debug_info.components.depth.post_pipeline_value"

    # ---------- situation check ----------
    n_active = 0
    n_active_eval = 0
    n_agree = 0
    n_active_uncomputable = 0

    # ---------- coin mean daily return over all its windows ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(allr)) if len(allr) else np.nan

    case_vals, case_excess, case_post, case_days = [], [], [], []

    for coin, wins in bars.items():
        mu = coin_mu[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            f = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            raw = (pd.to_numeric(df[RAW], errors="coerce").values.astype(float)
                   if RAW in df.columns else np.full(n, np.nan))
            post = (pd.to_numeric(df[POST], errors="coerce").values.astype(float)
                    if POST in df.columns else np.full(n, np.nan))
            days = _to_day(df["timestamp"])

            # day move (percent) and 60-bar profile trend (percent), inside the window
            day_move = np.full(n, np.nan)
            day_move[1:] = (c[1:] / c[:-1] - 1.0) * 100.0
            trend60 = np.full(n, np.nan)
            if n > 60:
                trend60[60:] = (c[60:] / c[:-60] - 1.0) * 100.0
            # depth: recorded raw value, else recomputed from closes (20 closes incl. current)
            depth = raw.copy()
            cs = pd.Series(c)
            hi20 = cs.rolling(20, min_periods=20).max().values
            rec_depth = (c - hi20) / hi20
            depth = np.where(np.isfinite(depth), depth, rec_depth)

            # next-day return inside the window
            nxt = np.full(n, np.nan)
            nxt[:-1] = c[1:] / c[:-1] - 1.0

            for i in range(n):
                if not np.isfinite(f[i]) or f[i] == 0:
                    continue
                n_active += 1
                if not (np.isfinite(day_move[i]) and np.isfinite(trend60[i]) and np.isfinite(depth[i])):
                    n_active_uncomputable += 1
                    continue
                n_active_eval += 1
                situ = (day_move[i] > 0) and (abs(trend60[i]) <= 10.0) and (depth[i] < 0)
                if situ and f[i] < 0:
                    n_agree += 1

            for i in range(n):
                if not np.isfinite(f[i]) or f[i] >= 0:
                    continue
                if not np.isfinite(nxt[i]) or not np.isfinite(mu):
                    continue
                ex = nxt[i] - mu
                case_vals.append((abs(f[i]) / 10.0) * (-ex))
                case_excess.append(ex)
                case_post.append(post[i])
                case_days.append(days[i])

    agreement = (n_agree / n_active_eval) if n_active_eval > 0 else None
    reading = ("Choppy is read as the 60-bar close-to-close return within -10 % and +10 % (the config's veto bounds), "
               "an up day as a 1-bar return above 0 and the depth as the raw component below 0, with active bars whose "
               "60-bar return cannot be computed inside the window left out of the agreement share; the main value is the "
               "per-case mean and its t is the ordinary t over the per-day sums of the cases; thirds are cut on the cases "
               "sorted by post_pipeline_value (most negative = deepest) into three near-equal groups.")

    main_name = "depth-weighted short gain vs holding, next day, mean per case"
    threshold = "confirm if t >= 2 with check < 0; reject if t <= -2"

    if agreement is not None and agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars checked": int(n_active_eval)},
            "decided_by": ("Fewer than 90 % of short bars are choppy up days closing below the 20-day high: "
                           "the config's forecast does not follow the plan's situation and short side."),
            "reading": reading,
        }

    situation = {"agreement": float(agreement) if agreement is not None else None,
                 "passed": bool(agreement is not None and agreement >= 0.9)}

    vals = np.array(case_vals, dtype=float)
    n_cases = int(len(vals))
    day_arr = np.array(case_days)
    n_days = int(len(np.unique(day_arr))) if n_cases else 0

    mean_val = float(np.mean(vals)) if n_cases else None
    t_val = None
    if n_days >= 2:
        ds = pd.Series(vals).groupby(day_arr).sum().values
        sd = np.std(ds, ddof=1)
        if sd > 0:
            t_val = float(np.mean(ds) / (sd / np.sqrt(len(ds))))

    # supporting check
    check_val = None
    pm = np.isfinite(np.array(case_post, dtype=float)) if n_cases else np.array([], dtype=bool)
    if n_cases and pm.sum() >= 3:
        p = np.array(case_post, dtype=float)[pm]
        e = np.array(case_excess, dtype=float)[pm]
        order = np.argsort(p, kind="mergesort")
        groups = np.array_split(order, 3)
        deep, shallow = groups[0], groups[-1]
        if len(deep) and len(shallow):
            check_val = float(np.mean(e[deep]) - np.mean(e[shallow]))
    check_passed = (check_val < 0) if check_val is not None else None

    counts = {"cases": n_cases, "distinct days": n_days}
    main = {"name": main_name, "value": mean_val,
            "statistic": ({"name": "t of the mean over per-day sums", "value": t_val} if t_val is not None else None),
            "threshold": threshold}
    support = {"name": "deepest third minus shallowest third, mean excess next-day return",
               "value": check_val, "passed": check_passed}

    if n_cases < 200 or n_days < 150:
        status = "not observable"
        decided = (f"The plan needs at least 200 cases on at least 150 distinct days; the record has "
                   f"{n_cases} cases on {n_days} days.")
    elif t_val is None:
        status = "inconclusive"
        decided = "The main-measure t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and check_passed:
        status = "confirmed"
        decided = "The main-measure t is 2 or more and the deepest-minus-shallowest check is below 0."
    elif t_val <= -2:
        status = "rejected"
        decided = "The main-measure t is -2 or less: deep up-day closes are followed by rises in proportion to depth."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The main-measure t is 2 or more but the supporting check is at or above 0 (or missing)."
    else:
        status = "inconclusive"
        decided = "The main-measure t is between -2 and 2."

    return {
        "status": status,
        "situation_check": situation,
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
