import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 6
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.rise_fade.last_history_value"
    EPS = 1e-9

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            # volume ratio: this bar's volume / mean of the last 720 bars (current included)
            vmean = vol.rolling(720, min_periods=720).mean()
            vratio = vol / vmean
            in_band = (vratio >= 0.5 - EPS) & (vratio <= 1.5 + EPS)
            # where the 720-bar mean cannot be rebuilt inside the window, use the detector's decision
            reg_fallback = df["regime"].astype(str) == "mean_reversion"
            quiet = np.where(vratio.notna(), in_band, reg_fallback)
            # rise: raw scaled return > 0, else the bar's own return from prices
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            ret1 = close / close.shift(1) - 1
            rise = np.where(raw.notna(), raw > 0, ret1 > 0)
            situation = np.asarray(quiet, dtype=bool) & np.asarray(rise, dtype=bool)
            active = (fc.notna() & (fc != 0)).values
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0).values).sum())

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean short-signed unusual 6-bar move", "value": None,
                             "statistic": None, "threshold": "t >= 2 (confirm) / t <= -2 (reject) over at least 30 cases"},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": "The forecast is never active, so there are fewer than 30 cases.",
            "reading": "none",
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active_bars": n_active},
            "decided_by": ("Fewer than 90% of the active bars are short bets on hourly rises with volume "
                           "between 0.5 and 1.5 times its 720-bar mean, as the Fidelity states."),
            "reading": "none",
        }

    # ---------- 2. drift per coin: mean 6-bar return on the non-overlapping grid, all windows ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            n = len(c)
            for p in range(0, n - H, H):
                r = c[p + H] / c[p] - 1
                if np.isfinite(r):
                    rets.append(r)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases: short bets, once per 6-bar grid cell ----------
    unusual = []
    absfc = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            n = len(fc)
            ref = 0.0
            prev_short = False
            used_cells = set()
            for t in range(n):
                f = fc[t]
                if f < 0:
                    s = -f
                    if not prev_short:
                        ref = 0.0
                    if s - ref >= BAND - EPS:
                        ref = s
                        cell = t // H
                        if cell not in used_cells:
                            used_cells.add(cell)
                            if t + H < n:
                                r = c[t + H] / c[t] - 1
                                if np.isfinite(r) and np.isfinite(drift[coin]):
                                    unusual.append(-(r - drift[coin]))
                                    absfc.append(abs(f))
                    else:
                        ref = min(ref, s)
                    prev_short = True
                else:
                    ref = 0.0
                    prev_short = False

    unusual = np.asarray(unusual, dtype=float)
    absfc = np.asarray(absfc, dtype=float)
    ncases = int(len(unusual))

    mean_u = float(np.mean(unusual)) if ncases > 0 else None
    tval = None
    if ncases > 1:
        sd = float(np.std(unusual, ddof=1))
        if sd > 0:
            tval = float(mean_u / (sd / np.sqrt(ncases)))

    # supporting check
    sup_val = None
    sup_pass = None
    n_hi = n_lo = 0
    if ncases > 0:
        med = float(np.median(absfc))
        hi = absfc > med
        lo = ~hi
        if hi.sum() == 0 or lo.sum() == 0:
            hi = absfc >= med
            lo = ~hi
        n_hi, n_lo = int(hi.sum()), int(lo.sum())
        if n_hi > 0 and n_lo > 0:
            sup_val = float(unusual[hi].mean() - unusual[lo].mean())
            sup_pass = bool(sup_val >= 0)

    main = {
        "name": "mean short-signed unusual 6-bar move of short bets",
        "value": mean_u,
        "statistic": {"name": "t of the mean", "value": tval} if tval is not None else None,
        "threshold": "positive with t >= 2 to confirm, negative with t <= -2 to reject, over at least 30 cases",
    }
    sup = {"name": "larger-forecast half minus smaller-forecast half mean unusual move (>= 0)",
           "value": sup_val, "passed": sup_pass}
    counts = {"cases": ncases, "larger_half_cases": n_hi, "smaller_half_cases": n_lo}
    reading = ("Bets are falls of the forecast of at least 2 points from its lowest short level since the last bet "
               "(reset at flat), the first bet in each 6-bar cell counted from each window's first row, the drift is "
               "the coin's mean 6-bar return on that grid pooled over all windows, the median split puts cases strictly "
               "above the median in the larger half (or at/above it if that leaves a half empty), and the volume band "
               "is rebuilt from volume over 720 bars including the current one, falling back to the recorded regime "
               "where a window has fewer than 720 bars of history.")

    if ncases < MIN_CASES:
        status = "not observable"
        decided = f"Only {ncases} cases across both coins and all windows, fewer than the plan's minimum of 30."
    elif tval is not None and mean_u > 0 and tval >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The mean short-signed unusual move is positive with t >= 2 over at least 30 cases and the larger-forecast half gives back at least as much."
    elif tval is not None and mean_u < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean short-signed unusual move is negative with t <= -2 over at least 30 cases: the price keeps rising after quiet-volume spikes."
    elif tval is not None and mean_u > 0 and tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the larger-rise half does not show a giveback at least as large as the smaller-rise half."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
