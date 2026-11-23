import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    BAND = 2.0
    RAW = "debug_info.components.absorb.last_history_value"

    def fnum(x):
        if x is None:
            return None
        try:
            x = float(x)
        except Exception:
            return None
        return x if np.isfinite(x) else None

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].sort_values("timestamp").reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            hi = pd.to_numeric(df["high"], errors="coerce").values
            lo = pd.to_numeric(df["low"], errors="coerce").values
            cl = pd.to_numeric(df["close"], errors="coerce").values
            rng = hi - lo
            with np.errstate(divide="ignore", invalid="ignore"):
                cloc = np.where(rng > 0, (2 * cl - hi - lo) / rng, 0.0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            # situation: close in the upper half of the bar (signed close location x volume ratio > 0)
            situ = np.where(np.isfinite(raw), raw > 0, cloc > 0)
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (f > 0)).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": fnum(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90 % of the bars with a non-zero forecast are long-side bars "
                          "with a positive raw signed close-location x volume-ratio value, as the Fidelity's situation requires.",
            "reading": "The situation is read as a positive raw component value (close in the upper half of the bar), "
                       "the side as long, from the plan's Fidelity.",
        }

    # ---------- 2. criterion ----------
    case_rows = []  # (coin, forecast, return)
    drift = {}
    for coin in sorted(bars):
        grid_rets = []
        coin_cases = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].sort_values("timestamp").reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            cl = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            # normal drift: non-overlapping grid returns
            for p in range(0, n - H, H):
                r = cl[p + H] / cl[p] - 1
                if np.isfinite(r):
                    grid_rets.append(r)
            # long-side bets
            base = 0.0
            bets = []
            for i in range(n):
                fi = f[i]
                if fi <= 0:
                    base = 0.0
                    continue
                base = min(base, fi)
                if fi - base >= BAND:
                    bets.append(i)
                    base = fi
            seen = set()
            for i in bets:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H < n:
                    r = cl[i + H] / cl[i] - 1
                    if np.isfinite(r):
                        coin_cases.append((f[i], r))
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan
        for fc, r in coin_cases:
            if np.isfinite(drift[coin]):
                case_rows.append((fc, r - drift[coin]))

    n_cases = len(case_rows)
    um = np.array([c[1] for c in case_rows], dtype=float)
    fc = np.array([c[0] for c in case_rows], dtype=float)

    mean = float(um.mean()) if n_cases > 0 else None
    if n_cases > 1:
        sd = float(um.std(ddof=1))
        t = mean / (sd / np.sqrt(n_cases)) if sd > 0 else None
    else:
        t = None

    sup_val = None
    sup_pass = None
    if n_cases > 1:
        med = np.median(fc)
        top = um[fc > med]
        bot = um[fc <= med]
        if len(top) > 0 and len(bot) > 0:
            sup_val = float(top.mean() - bot.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases pooled over all coins and windows, fewer than the plan's minimum of 30."
    elif t is not None and mean > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 and the top-half minus bottom-half difference is above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting check (top half minus bottom half > 0) fails, which the plan calls inconclusive."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": fnum(agreement), "passed": True},
        "main_measure": {
            "name": "mean 10-bar unusual move after long cases",
            "value": fnum(mean),
            "statistic": {"name": "t of the mean", "value": fnum(t)} if t is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; fewer than 30 cases is not observable",
        },
        "supporting_check": {
            "name": "mean unusual move, larger-forecast half minus smaller half",
            "value": fnum(sup_val),
            "passed": sup_pass,
        },
        "counts": {"cases": int(n_cases)},
        "decided_by": decided,
        "reading": "A case is the first long bet (forecast rise of at least 2 points from its lowest positive level since the last bet, from 0 after a flat) in each 10-bar grid cell counted from the window's first row, dropped if its 10-bar return leaves the window; the normal drift is each coin's mean non-overlapping 10-bar grid return over all its windows; the median split puts cases with forecast above the median in the larger half and the rest in the smaller half.",
    }
