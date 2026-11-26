import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    BAND = 2.0
    ER_P, ER_S, ER_MAX = 60, 5, 0.3
    BRK_P = 60

    def _er_variants(close):
        c = close.astype(float)
        change = (c - c.shift(ER_P)).abs()
        vol = c.diff().abs().rolling(ER_P, min_periods=ER_P).sum()
        er = change / vol.replace(0, np.nan)
        er_sma = er.rolling(ER_S, min_periods=ER_S).mean()
        er_ema = er.ewm(span=ER_S, adjust=False, min_periods=ER_S).mean()
        return er, er_sma, er_ema

    # ---------- 1. situation check ----------
    n_active = 0
    n_eval = 0
    n_agree = 0
    n_active_regime_fallback = 0
    n_agree_regime_fallback = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            high = pd.to_numeric(df["high"], errors="coerce")
            er, er_sma, er_ema = _er_variants(close)
            prior_high = high.shift(1).rolling(BRK_P, min_periods=BRK_P).max()
            active = fc != 0
            n_active += int(active.sum())
            evaluable = active & prior_high.notna() & er_sma.notna()
            er_ok = (er_sma <= ER_MAX) | (er_ema <= ER_MAX) | (er <= ER_MAX)
            brk_ok = close > prior_high
            sit = er_ok & brk_ok & (fc > 0)
            n_eval += int(evaluable.sum())
            n_agree += int((evaluable & sit).sum())
            # fallback on bars without enough in-window history: the detector's decision and the side
            fb = active & ~evaluable
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            n_active_regime_fallback += int(fb.sum())
            n_agree_regime_fallback += int((fb & (reg == "trending") & (fc > 0)).sum())

    if n_eval > 0:
        agreement = n_agree / n_eval
    elif n_active_regime_fallback > 0:
        agreement = n_agree_regime_fallback / n_active_regime_fallback
    else:
        agreement = None
    passed = agreement is not None and agreement >= 0.9

    reading = ("Situation recomputed from prices on active bars with enough in-window history (ER(60) smoothed "
               "by a 5-bar mean or EMA, or unsmoothed, at or below 0.3, and close strictly above the max high of the "
               "prior 60 bars, forecast > 0), falling back to regime=='trending' only if no bar is evaluable; a case "
               "is the first forecast bet (rise >= 2 points from its lowest positive level since the last bet) in each "
               "10-bar grid cell from each window's first row, cases without 10 bars ahead in the window are dropped, "
               "the per-day clustered t uses D/(D-1) correction, the rank-correlation t is rho*sqrt((n-2)/(1-rho^2)), "
               "and the plan's '30 cases on 30 days' minimum is reported as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": "mean unusual 10-bar move per long case", "value": None,
                             "statistic": None, "threshold": "mean > 0 with day-clustered t >= 2"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "evaluable active bars": int(n_eval)},
            "decided_by": ("Fewer than 90% of active bars are long bars of the plan's situation (ER(60) <= 0.3 "
                           "and close above the prior 60-day high): the config's forecast does not follow the Fidelity."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_rows = []
    for coin, wins in bars.items():
        # normal drift over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            base = 0.0
            bets = []
            for i in range(len(fc)):
                f = fc[i]
                if f <= 0:
                    base = 0.0
                    continue
                if f - base >= BAND:
                    bets.append(i)
                    base = f
                else:
                    base = min(base, f)
            seen_cells = set()
            for i in bets:
                cell = i // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if i + H >= len(c):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                ret = c[i + H] / c[i] - 1.0
                day = ts.iloc[i].strftime("%Y-%m-%d") if pd.notna(ts.iloc[i]) else f"{w}_{i}"
                case_rows.append({"coin": coin, "window": w, "day": day,
                                  "forecast": float(fc[i]), "unusual": ret - drift})

    cases = pd.DataFrame(case_rows, columns=["coin", "window", "day", "forecast", "unusual"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    main_name = "mean unusual 10-bar move per long case (percent)"
    thr = "confirm: mean > 0 with day-clustered t >= 2; reject: t <= -2"

    if n_cases < 30 or n_days < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name,
                             "value": float(cases["unusual"].mean() * 100) if n_cases else None,
                             "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "The plan's minimum of 30 cases on at least 30 distinct days is not reached.",
            "reading": reading,
        }

    u = cases["unusual"].to_numpy(dtype=float)
    mean_u = float(u.mean())
    dev = cases.assign(dev=u - mean_u).groupby("day")["dev"].sum().to_numpy()
    D = len(dev)
    se = np.sqrt(D / (D - 1) * np.sum(dev ** 2)) / n_cases if D > 1 else np.nan
    t_mean = float(mean_u / se) if se and np.isfinite(se) and se > 0 else float("nan")

    rho, _ = stats.spearmanr(cases["forecast"].to_numpy(dtype=float), u)
    rho = float(rho) if np.isfinite(rho) else float("nan")
    if np.isfinite(rho) and abs(rho) < 1:
        t_rho = float(rho * np.sqrt((n_cases - 2) / (1 - rho ** 2)))
    elif np.isfinite(rho):
        t_rho = float(np.sign(rho) * np.inf)
    else:
        t_rho = float("nan")
    corr_pass = bool(np.isfinite(rho) and rho > 0)

    if (np.isfinite(t_mean) and t_mean <= -2) or (np.isfinite(t_rho) and t_rho <= -2):
        status = "rejected"
        if np.isfinite(t_mean) and t_mean <= -2:
            decided = "Reject: the mean unusual move has t <= -2."
        else:
            decided = "Reject: the rank correlation between tightness and unusual move has t <= -2."
    elif mean_u > 0 and np.isfinite(t_mean) and t_mean >= 2 and corr_pass:
        status = "confirmed"
        decided = "Confirm: mean unusual move > 0 with t >= 2 and the rank correlation is above 0."
    else:
        status = "inconclusive"
        if mean_u > 0 and np.isfinite(t_mean) and t_mean >= 2:
            decided = "Inconclusive: positive move with t >= 2 but the rank correlation is at or below 0."
        else:
            decided = "Inconclusive: the results lie between the confirm and reject rules."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean_u * 100.0,
                         "statistic": {"name": "t of the mean, cases of one day taken together",
                                       "value": t_mean if np.isfinite(t_mean) else None},
                         "threshold": thr},
        "supporting_check": {"name": "Spearman rank correlation entry forecast vs unusual move (> 0)",
                             "value": rho if np.isfinite(rho) else None,
                             "passed": corr_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
