import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 2
    BAND = 2.0
    RAW = "debug_info.components.vol_fall.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # A fall on that hour: the raw product (return / std x volume ratio) is negative.
            # Where the raw value is missing, use the bar's own close-to-close fall.
            fall = np.where(raw.notna(), raw < 0, ret1 < 0)
            fall = pd.Series(fall, index=df.index).astype(bool)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & fall & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean 2-bar unusual move (return minus coin's normal 2-bar drift) over long bets"
    threshold = "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are falling hours "
                           "(negative raw volume-weighted scaled return) with a long forecast, "
                           "as the plan's situation and side require."),
            "reading": "The situation is read as a negative raw component value (a fall on that hour, the volume ratio being positive), falling back to the bar's close-to-close fall where the raw value is missing; the side is long.",
        }

    # ---------- 2. Criterion ----------
    # Normal 2-bar drift per coin: mean of non-overlapping 2-bar returns over all windows.
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            n = len(close)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    rets.append(c1 / c0 - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    case_moves = []
    case_fc = []
    per_coin = {}
    for coin, wins in bars.items():
        cnt = 0
        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            n = len(fc)
            # Detect long bets: a rise of the forecast of at least BAND from its lowest
            # long level since the last bet (from 0 after a flat or side change).
            ref = 0.0
            on_long = False
            bet = np.zeros(n, dtype=bool)
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f <= 0:
                    on_long = False
                    ref = 0.0
                    continue
                if not on_long:
                    on_long = True
                    ref = 0.0
                if f - ref >= BAND:
                    bet[t] = True
                    ref = f
                else:
                    ref = min(ref, f)
            # One case per 2-bar grid cell (first bet in the cell).
            seen = set()
            for t in np.nonzero(bet)[0]:
                cell = t // H
                if cell in seen:
                    continue
                seen.add(cell)
                if t + H >= n:
                    continue
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
                    continue
                if not np.isfinite(drift[coin]):
                    continue
                r = c1 / c0 - 1.0
                case_moves.append(r - drift[coin])
                case_fc.append(fc[t])
                cnt += 1
        per_coin[coin] = cnt

    n_cases = len(case_moves)
    counts = {"independent cases across both coins": int(n_cases)}
    for coin, c in per_coin.items():
        counts[f"cases {coin}"] = int(c)

    moves = np.asarray(case_moves, dtype=float)
    fcs = np.asarray(case_fc, dtype=float)

    mean_move = float(np.mean(moves)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = float(np.std(moves, ddof=1))
        t_val = float(mean_move / (sd / np.sqrt(n_cases))) if sd > 0 else None
    slope = None
    if n_cases > 2 and np.std(fcs) > 0:
        slope = float(stats.linregress(fcs, moves).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    reading = ("Bets are rises of the long forecast of at least 2 points from its lowest long level since the last bet "
               "(from 0 after a flat), one case per 2-bar grid cell of each window (the cell's first bet); the drift is "
               "each coin's mean non-overlapping 2-bar return over all its windows; the slope is ordinary least squares "
               "of the unusual move on the signal bar's forecast; the plan's 30-case minimum, when missed, gives "
               "'not observable' as the workflow requires.")

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} independent cases across both coins, below the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed (zero spread), which meets neither the confirm nor the reject rule."
    elif mean_move > 0 and t_val >= 2:
        if slope_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 and the slope on the forecast is positive."
        else:
            status = "inconclusive"
            decided = "The mean unusual move is positive with t >= 2 but the slope on the forecast is zero or negative."
    elif mean_move < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2: the heavy-volume falls extend rather than rebound."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_move,
            "statistic": None if t_val is None else {"name": "t of the mean", "value": t_val},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "OLS slope of unusual move on signal-bar forecast",
            "value": slope,
            "passed": slope_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
