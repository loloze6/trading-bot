import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    BOUNCE = "debug_info.components.bounce.last_history_value"
    DEPTH = "debug_info.components.depth90.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            depth = pd.to_numeric(df[DEPTH], errors="coerce").values if DEPTH in df.columns else np.full(len(df), np.nan)
            bounce = pd.to_numeric(df[BOUNCE], errors="coerce").values if BOUNCE in df.columns else np.full(len(df), np.nan)
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                # 90-day return: recorded raw value, else recomputed from prices
                r90 = depth[i]
                if not np.isfinite(r90) and i >= 90 and close[i - 90] > 0:
                    r90 = close[i] / close[i - 90] - 1
                # one-day rise scaled by 20-day vol: recorded raw value, else sign of 1-day return
                b = bounce[i]
                if not np.isfinite(b) and i >= 1 and close[i - 1] > 0:
                    b = close[i] / close[i - 1] - 1
                if np.isfinite(r90) and r90 < 0 and np.isfinite(b) and b > 0 and fc[i] < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 5-day move after short bets (fall positive)"
    main_thr = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2"
    sup_name = "OLS slope of unusual move on depth90 raw 90-day return"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are short bars where the 90-day return is negative and the day's volatility-scaled return is positive, as the Fidelity's situation and side require.",
            "reading": "Situation taken as depth90 raw < 0 (or 90-bar price return < 0) and bounce raw > 0 with forecast < 0, the graded dead zone meaning any positive bounce counts.",
        }

    # ---------- 2. criterion ----------
    # normal drift per coin: non-overlapping 5-bar returns on the grid of each window, all windows together
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(close) - H, H):
                if np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0:
                    rets.append(close[i + H] / close[i] - 1)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    moves, depths_for_reg, moves_for_reg = [], [], []
    case_coins = set()
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            depth = pd.to_numeric(df[DEPTH], errors="coerce").values if DEPTH in df.columns else np.full(len(df), np.nan)
            # bets on the short side: rise of |forecast| by >= band from its lowest level since last bet
            ref = 0.0
            side = 0
            bet = np.zeros(len(df), dtype=bool)
            for i in range(len(df)):
                f = fc[i]
                s = int(np.sign(f))
                if s != side:
                    ref = 0.0
                    side = s
                if s == 0:
                    ref = 0.0
                    continue
                m = abs(f)
                if m - ref >= BAND:
                    if s < 0:
                        bet[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
            # one case per non-overlapping 5-bar grid cell
            for start in range(0, len(df), H):
                idx = [i for i in range(start, min(start + H, len(df))) if bet[i]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= len(df):
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                if not np.isfinite(drift[coin]):
                    continue
                r = close[t + H] / close[t] - 1
                u = -(r - drift[coin])
                moves.append(u)
                case_coins.add(coin)
                if np.isfinite(depth[t]):
                    depths_for_reg.append(depth[t])
                    moves_for_reg.append(u)

    n = len(moves)
    n_coins = len(case_coins)
    mean = float(np.mean(moves)) if n > 0 else None
    t_mean = None
    if n > 1:
        sd = float(np.std(moves, ddof=1))
        t_mean = float(mean / (sd / np.sqrt(n))) if sd > 0 else None

    slope, t_slope = None, None
    if len(moves_for_reg) > 2 and np.std(depths_for_reg) > 0:
        lr = stats.linregress(np.array(depths_for_reg), np.array(moves_for_reg))
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    counts = {"cases": int(n), "coins with cases": int(n_coins), "cases in regression": int(len(moves_for_reg))}

    sup_passed = None
    if slope is not None and t_slope is not None:
        sup_passed = bool(slope > 0 and t_slope >= 2)

    if n < 30 or n_coins < 3:
        status = "not observable"
        decided = f"The plan's minimum of 30 cases from at least 3 coins is not reached ({n} cases from {n_coins} coins)."
    elif (mean is not None and t_mean is not None and mean < 0 and t_mean <= -2) or (t_slope is not None and t_slope <= -2):
        status = "rejected"
        if mean is not None and t_mean is not None and mean < 0 and t_mean <= -2:
            decided = "Reject rule: the mean unusual move is negative with t <= -2 (bounces keep rising beyond drift)."
        else:
            decided = "Reject rule: the depth slope has t <= -2 (deeper falls are followed by the larger fades)."
    elif mean is not None and t_mean is not None and mean > 0 and t_mean >= 2 and sup_passed:
        status = "confirmed"
        decided = "Confirm rule: the mean unusual move is positive with t >= 2 and the depth slope is positive with t >= 2."
    else:
        status = "inconclusive"
        if mean is not None and t_mean is not None and mean > 0 and t_mean >= 2:
            decided = "Inconclusive rule: the mean unusual move meets the confirm level but the depth slope t is not >= 2 with a positive slope."
        else:
            decided = "Inconclusive rule: the mean unusual move t lies between -2 and 2 (or is not positive at t >= 2) and no reject rule holds."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": {"name": "t of the mean", "value": t_mean} if t_mean is not None else None,
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name + (f" (t = {t_slope:.3f})" if t_slope is not None else ""),
                             "value": slope, "passed": sup_passed},
        "counts": counts,
        "decided_by": decided,
        "reading": "A case is the first short bet (|forecast| rising >= 2 from its lowest level on the short side since the last bet, reset at flat or side change) in each 5-bar grid cell counted from each window's first row, cases whose 5-bar return would leave the window are dropped, the coins counted are those with at least one case, the slope t is the OLS slope over its standard error on cases with a recorded depth90 value, and too few cases gives 'not observable' as the workflow requires.",
    }
