import numpy as np
import pandas as pd

H = 3
BAND = 2.0
MIN_DAYS = 30
RAW_COL = "debug_info.components.scaled_rise.last_history_value"
PROFILE_REGIME = "unknown"


def _sorted_frame(df):
    d = df.copy()
    d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
    d = d.sort_values("timestamp").reset_index(drop=True)
    return d


def _short_bets(fc):
    """Bars where the short forecast rises in size by at least the band, measured from its
    lowest size on the short side since the last bet (from 0 after a flat or a change of side)."""
    bets = np.zeros(len(fc), dtype=bool)
    ref = 0.0
    prev_short = False
    for i, f in enumerate(fc):
        if not np.isfinite(f) or f >= 0:
            ref = 0.0
            prev_short = False
            continue
        m = -f
        if not prev_short:
            ref = 0.0
        ref = min(ref, m)
        if m - ref >= BAND - 1e-12:
            bets[i] = True
            ref = m
        prev_short = True
    return bets


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for win in sorted(bars[coin]):
            d = _sorted_frame(bars[coin][win])
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if RAW_COL in d.columns:
                raw = pd.to_numeric(d[RAW_COL], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            close = pd.to_numeric(d["close"], errors="coerce")
            ret3 = close / close.shift(H) - 1.0
            rise = raw.where(raw.notna(), ret3) > 0
            in_profile = d["regime"].astype(str) == PROFILE_REGIME
            ok = active & in_profile & rise & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean short-direction unusual 3-day move of bets",
                             "value": None, "statistic": None,
                             "threshold": "mean > 0 with t >= 2 to confirm; t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"cases": 0, "distinct case days": 0},
            "decided_by": "No active bars: fewer than 30 distinct case days.",
            "reading": "Profile taken from the recorded regime ('unknown' = falling agitated), since its detector components are not recorded.",
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean short-direction unusual 3-day move of bets",
                             "value": None, "statistic": None,
                             "threshold": "mean > 0 with t >= 2 to confirm; t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": "Fewer than 90% of active bars are short bars inside the falling agitated profile after a 3-day rise, as the Fidelity requires.",
            "reading": "Profile taken from the recorded regime ('unknown' = falling agitated); rise from the scaled_rise raw value (> 0), or the 3-bar price return where it is missing.",
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, unusual_short, abs_forecast)
    for coin in sorted(bars):
        # normal drift: mean 3-bar return over non-overlapping grids of all windows
        grid_rets = []
        frames = {}
        for win in sorted(bars[coin]):
            d = _sorted_frame(bars[coin][win])
            frames[win] = d
            c = pd.to_numeric(d["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for win, d in frames.items():
            c = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            bets = _short_bets(fc)
            n = len(d)
            for start in range(0, n, H):
                idx = [j for j in range(start, min(start + H, n)) if bets[j]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                u = -(r - drift)
                day = d["timestamp"].iloc[t].strftime("%Y-%m-%d")
                cases.append((coin, day, u, abs(float(fc[t]))))

    n_cases = len(cases)
    days = sorted(set(cs[1] for cs in cases))
    n_days = len(days)
    counts = {"cases": n_cases, "distinct case days": n_days}
    threshold = "confirm: mean > 0 with t >= 2 and slope > 0; reject: t <= -2; at least 30 distinct case days"
    reading = ("Profile taken from the recorded regime ('unknown' = falling agitated) and rise from the scaled_rise raw value; "
               "a case is the first short bet in each non-overlapping 3-bar grid cell of a window, its return taken from that bet bar's close "
               "3 bars ahead inside the window; the day-clustered t uses a G/(G-1) correction so that one case per day gives the ordinary t.")

    mean_u = None
    t_stat = None
    slope = None
    if n_cases > 0:
        u = np.array([cs[2] for cs in cases], dtype=float)
        x = np.array([cs[3] for cs in cases], dtype=float)
        mean_u = float(u.mean())
        dev = u - mean_u
        sums = {}
        for (cs, dv) in zip(cases, dev):
            sums[cs[1]] = sums.get(cs[1], 0.0) + dv
        G = len(sums)
        s2 = float(np.sum(np.square(list(sums.values()))))
        if G > 1 and s2 > 0:
            se = np.sqrt(G / (G - 1.0) * s2) / n_cases
            t_stat = float(mean_u / se)
        if n_cases >= 2 and np.var(x) > 0:
            xm = x - x.mean()
            slope = float(np.sum(xm * (u - u.mean())) / np.sum(xm * xm))

    main = {"name": "mean short-direction unusual 3-day move of bets (vs coin's normal drift)",
            "value": mean_u,
            "statistic": ({"name": "t with same-day cases summed", "value": t_stat} if t_stat is not None else None),
            "threshold": threshold}
    support = {"name": "OLS slope of unusual short move on |forecast|",
               "value": slope,
               "passed": (bool(slope > 0) if slope is not None else None)}

    if n_days < MIN_DAYS:
        return {"status": "not observable",
                "situation_check": {"agreement": float(agreement), "passed": True},
                "main_measure": main, "supporting_check": support, "counts": counts,
                "decided_by": f"Only {n_days} distinct case days, fewer than the plan's minimum of 30.",
                "reading": reading}

    if t_stat is None:
        status = "inconclusive"
        decided = "The t could not be computed (no spread across case days), so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_stat >= 2 and slope is not None and slope > 0:
        status = "confirmed"
        decided = "Mean unusual short move above 0 with t >= 2 and slope on |forecast| above 0."
    elif t_stat <= -2:
        status = "rejected"
        decided = "Mean unusual short move has t <= -2: the coin rose more than its drift after the rises."
    elif mean_u > 0 and t_stat >= 2:
        status = "inconclusive"
        decided = "Confirming t >= 2 but the slope on |forecast| is at or below 0 (or not computable)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {"status": status,
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": main, "supporting_check": support, "counts": counts,
            "decided_by": decided, "reading": reading}
