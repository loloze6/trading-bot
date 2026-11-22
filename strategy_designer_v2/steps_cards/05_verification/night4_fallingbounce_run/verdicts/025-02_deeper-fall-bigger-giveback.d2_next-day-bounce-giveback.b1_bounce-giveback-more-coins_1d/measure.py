import numpy as np
import pandas as pd


def measure(bars):
    LH = "debug_info.components.bounce.last_history_value"

    # ---------- per-coin normal drift (mean 1-bar return over all windows) ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp") if "timestamp" in df.columns else df
            c = d["close"].astype(float).reset_index(drop=True)
            r = (c.shift(-1) / c - 1.0).dropna()
            rets.append(r.values)
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---------- situation check + cases ----------
    n_active = 0
    n_agree = 0
    case_um = []
    case_absf = []

    for coin, wins in bars.items():
        mu = coin_mu.get(coin, np.nan)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp") if "timestamp" in df.columns else df
            d = d.reset_index(drop=True)
            c = d["close"].astype(float)
            f = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)

            # 90-bar return from prices where 90 prior bars exist in the window,
            # else the detector's recorded regime decision
            ret90 = c / c.shift(90) - 1.0
            reg = d["regime"].astype(str) if "regime" in d.columns else pd.Series(["unknown"] * len(d))
            falling = pd.Series(
                np.where(ret90.notna(), ret90 < 0.0, reg == "mean_reversion"),
                index=d.index,
            ).astype(bool)

            # today's rise: raw bounce component (> 0), recomputed from prices if not recorded
            r1 = c / c.shift(1) - 1.0
            if LH in d.columns:
                raw = pd.to_numeric(d[LH], errors="coerce")
                rise = pd.Series(np.where(raw.notna(), raw > 0.0, r1 > 0.0), index=d.index)
            else:
                rise = r1 > 0.0
            rise = rise.fillna(False).astype(bool)

            situation = falling & rise
            active = f != 0.0
            n_active += int(active.sum())
            n_agree += int((active & situation & (f < 0.0)).sum())

            # cases: forecast <= -2, horizon 1 bar, every bar independent
            nxt = c.shift(-1) / c - 1.0
            m = (f <= -2.0) & nxt.notna()
            if m.any() and np.isfinite(mu):
                um = -(nxt[m] - mu)
                case_um.extend(um.values.tolist())
                case_absf.extend(f[m].abs().values.tolist())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90

    main_name = "mean unusual move (short direction), next 1 bar, on bars with forecast <= -2"
    thr = "confirm: mean > 0 with t >= 2 and larger-|forecast| half ahead; reject: mean < 0 with t <= -2"
    reading = ("The 90-bar return is recomputed from closes where 90 prior bars exist in the window and taken from the "
               "recorded regime otherwise, the rise is the raw bounce value > 0, and the median split puts cases with "
               "|forecast| strictly above the median in the larger half and the rest in the smaller half.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": int(len(case_um))},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are short bars on a rise day in a coin with a "
                           "negative 90-bar return, so the config does not trade the plan's situation."),
            "reading": reading,
        }

    um = np.array(case_um, dtype=float)
    af = np.array(case_absf, dtype=float)
    n = int(um.size)

    mean = float(np.mean(um)) if n > 0 else None
    t = None
    if n > 1:
        sd = float(np.std(um, ddof=1))
        t = float(mean / (sd / np.sqrt(n))) if sd > 0 else None

    diff = None
    sup_pass = None
    n_large = n_small = 0
    if n > 0:
        med = float(np.median(af))
        large = um[af > med]
        small = um[af <= med]
        n_large, n_small = int(large.size), int(small.size)
        if large.size > 0 and small.size > 0:
            diff = float(np.mean(large) - np.mean(small))
            sup_pass = bool(diff > 0)
        else:
            sup_pass = False

    counts = {"cases": n, "larger half": n_large, "smaller half": n_small}
    main = {"name": main_name, "value": mean,
            "statistic": {"name": "ordinary t of the mean", "value": t} if t is not None else None,
            "threshold": thr}
    sup = {"name": "mean unusual move, larger |forecast| half minus smaller half", "value": diff, "passed": sup_pass}

    if n < 30:
        status = "not observable"
        decided = f"Only {n} cases with forecast <= -2, fewer than the 30 the plan requires."
    elif mean is not None and t is not None and mean > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 and the larger half's mean unusual move exceeds the smaller half's."
    elif mean is not None and t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2: bounces in falling coins keep rising the next day."
    else:
        status = "inconclusive"
        if mean is not None and t is not None and mean > 0 and t >= 2:
            decided = "t >= 2 with a positive mean, but the larger half is not ahead of the smaller half."
        else:
            decided = "Neither the confirm nor the reject rule is met (|t| < 2 or sign and t disagree)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
