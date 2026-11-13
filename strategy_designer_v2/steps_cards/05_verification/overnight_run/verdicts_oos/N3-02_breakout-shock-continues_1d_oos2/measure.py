import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    FC = "forecast"
    SHOCK_RAW = "debug_info.components.shock.last_history_value"

    def merge_signals(idx_list):
        # keep a signal only if it is at least H bars after the last kept case
        kept, last = [], None
        for i in idx_list:
            if last is None or i - last >= H:
                kept.append(i)
                last = i
        return kept

    # ---------- situation check ----------
    n_active, n_agree = 0, 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df[FC], errors="coerce")
            prior_max = close.shift(1).rolling(20, min_periods=20).max()
            newhigh_px = close >= prior_max
            regime_tr = df["regime"].astype(str).str.lower().eq("trending") if "regime" in df.columns else pd.Series(False, index=df.index)
            newhigh = np.where(prior_max.notna(), newhigh_px, regime_tr)
            ret1 = close.pct_change()
            if SHOCK_RAW in df.columns:
                raw = pd.to_numeric(df[SHOCK_RAW], errors="coerce")
                ret1 = raw.where(raw.notna(), ret1)
            upday = (ret1 > 0).values
            active = (fc != 0) & fc.notna()
            for i in np.where(active.values)[0]:
                n_active += 1
                if bool(newhigh[i]) and bool(upday[i]) and fc.iloc[i] > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long, up-day bars closing at a new 20-day closing high (or no active bars at all), so the config does not do what the plan's situation says.",
            "reading": "Situation recomputed from closes within each window (close >= max of prior 20 closes, falling back to regime == 'trending' where fewer than 20 prior bars exist) plus a positive one-day return.",
        }

    # ---------- coin mean 5-bar return (all bars, all windows pooled) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            fwd = close.shift(-H) / close - 1
            allr.append(fwd.dropna().values)
        allr = np.concatenate(allr) if allr else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---------- cases ----------
    main_ex, inside_ex = [], []
    for coin, wins in bars.items():
        cm = coin_mean[coin]
        if not np.isfinite(cm):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df[FC], errors="coerce")
            fwd = close.shift(-H) / close - 1
            r1 = close.pct_change()
            std = 10.0 * r1 / r1.abs().rolling(60, min_periods=20).mean()

            sig = [i for i in range(len(df)) if pd.notna(fc.iloc[i]) and fc.iloc[i] >= 10]
            for i in merge_signals(sig):
                if pd.notna(fwd.iloc[i]):
                    main_ex.append(fwd.iloc[i] - cm)

            sig_in = [i for i in range(len(df))
                      if pd.notna(std.iloc[i]) and std.iloc[i] >= 10 and pd.notna(fc.iloc[i]) and fc.iloc[i] == 0]
            for i in merge_signals(sig_in):
                if pd.notna(fwd.iloc[i]):
                    inside_ex.append(fwd.iloc[i] - cm)

    main_ex = np.array(main_ex, dtype=float)
    inside_ex = np.array(inside_ex, dtype=float)
    n_cases = int(main_ex.size)
    n_inside = int(inside_ex.size)

    mean_ex = float(np.mean(main_ex)) if n_cases > 0 else None
    t_val = None
    if n_cases >= 2:
        sd = np.std(main_ex, ddof=1)
        t_val = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else None

    diff = None
    if n_cases > 0 and n_inside > 0:
        diff = float(np.mean(main_ex) - np.mean(inside_ex))
    sup_passed = None if diff is None else bool(diff > 0)

    reading = ("Signals are merged when they fall fewer than 5 bars after the last kept case in the same window (the same merge applied to the inside-range group), "
               "the coin's mean 5-bar return is the mean of all overlapping 5-bar forward returns of every bar in all its windows, "
               "the standardised return is 10 x the one-day return over the rolling mean absolute one-day return of the last 60 bars (min 20, within window), "
               "and the t is the ordinary one-sample t of the mean excess return.")

    counts = {"non-overlapping cases pooled across coins": n_cases,
              "inside-range shock-up cases": n_inside}

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping new-high shock cases pooled across coins, fewer than the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero dispersion), so the result meets neither confirm nor reject."
    elif mean_ex > 0 and t_val >= 2 and sup_passed is True:
        status = "confirmed"
        decided = "Mean excess 5-bar return is positive with t >= 2 and exceeds the inside-range shock-up mean excess, meeting the confirm rule."
    elif mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean excess 5-bar return is negative with t <= -2, meeting the reject rule (reversal after shock-up new highs)."
    else:
        status = "inconclusive"
        if t_val >= 2:
            decided = "t >= 2 but the supporting difference versus inside-range shock-up days is not positive (or not computable), so neither confirm nor reject is met."
        else:
            decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean excess 5-bar forward return after shock-up new-high cases (forecast >= 10)",
            "value": mean_ex,
            "statistic": None if t_val is None else {"name": "one-sample t of the mean", "value": t_val},
            "threshold": "confirm if mean > 0 with t >= 2 (and supporting difference > 0); reject if mean < 0 with t <= -2; at least 30 non-overlapping cases",
        },
        "supporting_check": {
            "name": "mean excess after new-high cases minus mean excess after inside-range shock-up days",
            "value": diff,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
