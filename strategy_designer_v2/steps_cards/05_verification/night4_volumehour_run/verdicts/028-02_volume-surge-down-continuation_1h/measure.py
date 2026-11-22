import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 6
    BAND = 2.0
    VOLP = 720
    LHV = "debug_info.components.vw_fall.last_history_value"

    def win_key(w):
        s = "".join(ch for ch in str(w) if ch.isdigit())
        return (int(s) if s else 0, str(w))

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys(), key=win_key):
            df = bars[coin][w].reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # raw sign = sign of the hour's return (volume ratio > 0); recompute where not recorded
            fall = np.where(raw.notna(), raw < 0, ret1 < 0)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & pd.Series(fall, index=df.index) & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": ("Fewer than 90% of the active bars are short bars after a down hour "
                           "(negative raw volume-weighted scaled return), which the plan's Fidelity "
                           "situation and short side require."),
            "reading": "Situation taken as the raw component value below 0 (a fall on any volume), side short.",
        }

    # ---------- 2. criterion ----------
    unusual_all = []
    vr_all = []
    for coin in sorted(bars.keys()):
        wins = sorted(bars[coin].keys(), key=win_key)
        # normal 6-bar drift over all windows of the coin, on the grid 0, 6, 12, ...
        grid_rets = []
        for w in wins:
            close = pd.to_numeric(bars[coin][w]["close"], errors="coerce").to_numpy()
            n = len(close)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w in wins:
            df = bars[coin][w].reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            vol = pd.to_numeric(df["volume"], errors="coerce")
            vratio = (vol / vol.rolling(VOLP, min_periods=VOLP).mean()).to_numpy()
            n = len(df)
            # short bets: forecast falls by >= BAND below its least-short level since last bet
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f >= 0:
                    ref = 0.0
                    continue
                m = -f
                if m - ref >= BAND:
                    bet[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
            seen_cells = set()
            for i in np.nonzero(bet)[0]:
                cell = i // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                unusual_all.append(-(r - drift))
                vr_all.append(vratio[i])

    u = np.asarray(unusual_all, dtype=float)
    vr = np.asarray(vr_all, dtype=float)
    n_cases = int(len(u))
    mean_u = float(np.mean(u)) if n_cases > 0 else None
    if n_cases > 1:
        sd = float(np.std(u, ddof=1))
        t = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None
    else:
        t = None

    ok = np.isfinite(vr) & np.isfinite(u)
    n_rho = int(ok.sum())
    rho = None
    if n_rho >= 3:
        rr = stats.spearmanr(vr[ok], u[ok]).correlation
        rho = float(rr) if np.isfinite(rr) else None
    rho_pass = None if rho is None else bool(rho > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} cases pooled over BTC and ETH, below the plan's minimum of 30."
    elif t is not None and mean_u > 0 and t >= 2:
        if rho_pass:
            status = "confirmed"
            decided = "Mean unusual fall above 0 with t >= 2 over at least 30 cases, and the volume-ratio rank correlation is positive."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the volume-ratio rank correlation is 0 or below (or not computable)."
    elif t is not None and mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is a rise, with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 over at least 30 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean 6-bar unusual fall after a short bet (drift removed, sign flipped)",
            "value": mean_u,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": "mean > 0 with t >= 2 over at least 30 pooled cases to confirm; t <= -2 to reject",
        },
        "supporting_check": {
            "name": "Spearman rank correlation of signal-hour volume ratio with unusual fall",
            "value": rho,
            "passed": rho_pass,
        },
        "counts": {"cases": n_cases, "cases_with_volume_ratio": n_rho},
        "decided_by": decided,
        "reading": ("A case is the first short bet (forecast more negative by >= 2 from its least-short level since the last bet, "
                    "reset at flat) in each 6-bar grid cell of a window, the drift is the coin's mean 6-bar grid return over all its "
                    "windows, and the volume ratio is recomputed as volume over its trailing 720-bar mean including the bar, "
                    "within the window, with cases lacking 720 bars of history left out of the correlation only."),
    }
