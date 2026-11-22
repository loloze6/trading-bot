import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.vol_fall.last_history_value"
    H = 2
    BAND = 2.0
    MIN_CASES = 30
    VOL_WIN = 720

    def prep(df):
        df = df.copy()
        if "timestamp" in df.columns:
            df = df.sort_values("timestamp", kind="mergesort")
        return df.reset_index(drop=True)

    def raw_values(df):
        # The component's raw value; recomputed from the prices where it is missing.
        close = df["close"].astype(float)
        r = close.pct_change()
        sd = r.rolling(VOL_WIN, min_periods=VOL_WIN).std()
        vr = df["volume"].astype(float) / df["volume"].astype(float).rolling(VOL_WIN, min_periods=VOL_WIN).mean()
        recomputed = (r / sd) * vr
        if RAW in df.columns:
            raw = pd.to_numeric(df[RAW], errors="coerce")
            return raw.where(raw.notna(), recomputed)
        return recomputed

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in bars:
        for w in bars[coin]:
            df = prep(bars[coin][w])
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            raw = raw_values(df).values
            active = f != 0
            n_active += int(active.sum())
            # situation (adapted): a falling hour, i.e. raw product < 0; expected side: long
            agree = active & np.isfinite(raw) & (raw < 0) & (f > 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {
                "name": "mean unusual 2-bar move after bets",
                "value": None,
                "statistic": None,
                "threshold": "mean > 0 with t >= 2 on at least 30 cases (confirm); mean < 0 with t <= -2 (reject)",
            },
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are falling hours (raw product below 0) with a long forecast, as the plan's situation and side require.",
            "reading": "Situation taken as a falling hour (raw volume-weighted scaled return below 0) on the long side, from last_history_value (recomputed from prices if missing).",
        }

    # ---------- 2. criterion ----------
    case_moves = []
    case_vr = []
    for coin in bars:
        # normal 2-bar drift of the coin over all its windows (non-overlapping grid)
        grid_rets = []
        prepped = {}
        for w in bars[coin]:
            df = prep(bars[coin][w])
            prepped[w] = df
            c = df["close"].astype(float).values
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                rr = c[idx + H] / c[idx] - 1.0
                grid_rets.extend(list(rr[np.isfinite(rr)]))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in prepped.items():
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = df["close"].astype(float).values
            vol = df["volume"].astype(float)
            vr_all = (vol / vol.rolling(VOL_WIN, min_periods=VOL_WIN).mean()).values
            n = len(f)
            # bets: a rise of the long forecast of at least the band from its lowest level since the last bet
            is_bet = np.zeros(n, dtype=bool)
            base = 0.0
            for i in range(n):
                fi = f[i]
                if fi <= 0:
                    base = 0.0
                    continue
                if fi - base >= BAND:
                    is_bet[i] = True
                    base = fi
                else:
                    base = min(base, fi)
            # once per non-overlapping 2-bar grid cell: first bet bar of the cell
            for start in range(0, n, H):
                cell = np.where(is_bet[start:start + H])[0]
                if len(cell) == 0:
                    continue
                t = start + int(cell[0])
                if t + H >= n:
                    continue
                ret = c[t + H] / c[t] - 1.0
                if not np.isfinite(ret):
                    continue
                case_moves.append(ret - drift)  # long side
                case_vr.append(vr_all[t])

    moves = np.array(case_moves, dtype=float)
    vrs = np.array(case_vr, dtype=float)
    n_cases = int(len(moves))

    mean_move = float(np.mean(moves)) if n_cases > 0 else None
    if n_cases > 1:
        sd = float(np.std(moves, ddof=1))
        t_stat = float(mean_move / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0
    else:
        t_stat = None

    # supporting check: volume-ratio median split
    ok = np.isfinite(vrs)
    sv = vrs[ok]
    sm = moves[ok]
    split_diff = None
    split_pass = None
    n_top = n_bot = 0
    if len(sv) >= 2:
        med = float(np.median(sv))
        top = sm[sv > med]
        bot = sm[sv < med]
        n_top, n_bot = int(len(top)), int(len(bot))
        if n_top > 0 and n_bot > 0:
            split_diff = float(np.mean(top) - np.mean(bot))
            split_pass = bool(split_diff > 0)
    if split_pass is None:
        split_pass_eff = False
    else:
        split_pass_eff = split_pass

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases, below the plan's minimum of 30 cases."
    elif mean_move > 0 and t_stat is not None and t_stat >= 2 and split_pass_eff:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 on at least 30 cases and the high-minus-low volume split is positive."
    elif mean_move < 0 and t_stat is not None and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2 on at least 30 cases."
    elif t_stat is not None and t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the volume split is not positive (or could not be computed), so the plan's inconclusive rule applies."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2 on at least 30 cases, the plan's inconclusive rule."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": True},
        "main_measure": {
            "name": "mean unusual 2-bar move after bets (long, minus normal drift, before costs)",
            "value": mean_move,
            "statistic": ({"name": "t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": "mean > 0 with t >= 2 on at least 30 cases (confirm); mean < 0 with t <= -2 on at least 30 cases (reject)",
        },
        "supporting_check": {
            "name": "mean unusual move, top minus bottom half by volume ratio",
            "value": split_diff,
            "passed": split_pass,
        },
        "counts": {
            "cases": n_cases,
            "cases with a volume ratio": int(len(sv)),
            "top half": n_top,
            "bottom half": n_bot,
        },
        "decided_by": decided,
        "reading": "A case is the first bet bar (long forecast rising >= 2 points from its lowest level since the last bet) in each non-overlapping 2-bar cell from each window's first row, with its 2-bar return inside the window; the normal drift is the coin's mean 2-bar return on the same grid over all its windows; the volume ratio is volume over the trailing 720-bar mean including the bar, computed within the window (cases without 720 bars of history left out of the split), and cases exactly at the median are left out of both halves.",
    }
