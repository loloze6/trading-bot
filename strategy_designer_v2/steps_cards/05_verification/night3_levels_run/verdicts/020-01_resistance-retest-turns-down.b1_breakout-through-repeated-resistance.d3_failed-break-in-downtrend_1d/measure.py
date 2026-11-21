import numpy as np
import pandas as pd

H = 10
BAND = 2.0
MIN_CASES = 20

def _col(df, name):
    return df[name] if name in df.columns else pd.Series(np.nan, index=df.index)

def _bets(f):
    """Bar positions of bets: a rise of the forecast on its side of at least BAND."""
    side, ref, out = 0, 0.0, []
    for i, v in enumerate(f):
        if not np.isfinite(v) or v == 0:
            side, ref = 0, 0.0
            continue
        s = 1 if v > 0 else -1
        if s != side:
            side, ref = s, 0.0
        mag = abs(v)
        if mag - ref >= BAND:
            out.append(i)
            ref = mag
        else:
            ref = min(ref, mag)
    return out

def _tstat(x):
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 2:
        return None
    sd = x.std(ddof=1)
    if not np.isfinite(sd) or sd == 0:
        return None
    return float(x.mean() / (sd / np.sqrt(n)))

def measure(bars):
    # ---------- 1. situation check ----------
    n_active, n_agree = 0, 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            brk = pd.to_numeric(_col(df, "debug_info.components.break.last_history_value"), errors="coerce")
            f20 = pd.to_numeric(_col(df, "debug_info.components.fall20.last_history_value"), errors="coerce")
            f20_px = close / close.shift(20) - 1.0
            f20 = f20.where(f20.notna(), f20_px)
            active = fc != 0
            situ = (brk > 0) & (f20 < 0)
            agree = active & situ & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    main_name = "mean drift-removed 10-bar short-side move per short case"
    thr = "confirm: mean > 0 with t >= 2 over >= 20 cases and supporting check passes; reject: t <= -2 over >= 20 cases"
    reading = ("Cases are short bets (forecast rising by >= 2 points in size on the short side, per the workflow's case "
               "definition), the first per 10-bar grid cell of each window counted from its first row, with a full "
               "10-bar return inside the window; drift is the mean 10-bar return on the same grid over all the coin's "
               "windows; the median split puts cases with |forecast| strictly above the median in the larger half.")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "cases": 0},
            "decided_by": ("Fewer than 90% of the active bars are short bars where the close has just crossed a 90-day "
                           "swing-high level (break > 0) during a 20-day fall (20-bar change < 0)."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    moves, sizes = [], []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(df)
            for i in range(0, n - H, H):
                if np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0:
                    grid_rets.append(close[i + H] / close[i] - 1.0)
            seen = set()
            for i in _bets(fc):
                if fc[i] >= 0:
                    continue
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                coin_cases.append((close[i + H] / close[i] - 1.0, abs(fc[i])))
        if not coin_cases:
            continue
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for r, a in coin_cases:
            moves.append(-(r - drift))
            sizes.append(a)

    moves = np.asarray(moves, dtype=float)
    sizes = np.asarray(sizes, dtype=float)
    n_cases = int(len(moves))
    mean_move = float(moves.mean()) if n_cases > 0 else None
    t = _tstat(moves) if n_cases > 0 else None

    sup_val, sup_pass = None, None
    n_large = n_small = 0
    if n_cases > 0:
        med = float(np.median(sizes))
        large = moves[sizes > med]
        small = moves[sizes <= med]
        n_large, n_small = int(len(large)), int(len(small))
        if n_large > 0 and n_small > 0:
            sup_val = float(large.mean() - small.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"cases": n_cases, "larger-forecast half": n_large, "smaller-forecast half": n_small}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} short cases, fewer than the plan's minimum of 20."
    elif t is not None and mean_move > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean short-side unusual move above 0 with t >= 2 over at least 20 cases, and the larger-forecast half moves more."
    elif t is not None and t <= -2:
        status = "rejected"
        decided = "Mean short-side unusual move has t <= -2 over at least 20 cases: price rises beyond its normal drift after these breaks."
    elif t is not None and t >= 2 and not sup_pass:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails (larger-forecast half does not move more), so inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 over at least 20 cases, meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_move,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": thr,
        },
        "supporting_check": {
            "name": "larger minus smaller |forecast| half, mean short-side unusual move",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
