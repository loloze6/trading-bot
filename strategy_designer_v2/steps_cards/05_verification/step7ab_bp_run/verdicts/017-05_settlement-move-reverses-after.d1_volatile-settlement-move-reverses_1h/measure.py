import numpy as np
import pandas as pd


def _to_utc(ts):
    s = pd.Series(ts)
    if np.issubdtype(s.dtype, np.number):
        mx = float(s.max()) if len(s) else 0.0
        unit = "ms" if mx > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 8
    RAW = "debug_info.components.pre_move.last_history_value"

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin in sorted(bars.keys()):
        prepared[coin] = {}
        for w in sorted(bars[coin].keys(), key=lambda x: (len(str(x)), str(x))):
            df = bars[coin][w].reset_index(drop=True).copy()
            ts = _to_utc(df["timestamp"]).reset_index(drop=True)
            close_hour = ((ts + pd.Timedelta(hours=1)).dt.hour).values
            settle = np.isin(close_hour, [0, 8, 16])
            close = df["close"].astype(float).reset_index(drop=True)
            r1 = close.pct_change()
            vol24 = r1.rolling(24, min_periods=24).std()
            vol_mean = vol24.rolling(720, min_periods=720).mean()
            ratio = (vol24 / vol_mean).values
            ret2 = (close / close.shift(2) - 1.0).values
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            raw = df[RAW].astype(float).values if RAW in df.columns else np.full(len(df), np.nan)
            f = df["forecast"].astype(float).fillna(0.0).values

            active = f != 0
            for i in np.where(active)[0]:
                n_active += 1
                if not settle[i]:
                    continue
                if np.isfinite(ratio[i]):
                    vol_ok = ratio[i] >= 1.0
                else:
                    vol_ok = regime[i] == "mean_reversion"
                if not vol_ok:
                    continue
                move = raw[i] if np.isfinite(raw[i]) else ret2[i]
                if not np.isfinite(move) or move == 0:
                    continue
                if np.sign(f[i]) == -np.sign(move):
                    n_agree += 1
            prepared[coin][w] = (close.values, f, settle)

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("A settlement bar is one whose close (start + 1h) falls at 00, 08 or 16 UTC; 24-bar volatility is the std "
               "of 1-bar simple returns, compared with its 720-bar mean from the window's prices, falling back to the "
               "recorded regime where the window holds too few bars; the expected side is opposite to the sign of the "
               "raw pre_move value (or the 2-bar return); cases are settlement bars with non-zero forecast, one per "
               "8-bar grid cell (first in the cell), with t+8 inside the window; the coin's mean 8-bar return pools "
               "the grid returns of all its windows; the larger half is |forecast| above the median, the smaller half "
               "at or below it.")

    main_name = "mean of forecast/10 x (8-bar return minus coin mean 8-bar return) over settlement cases"
    thr = "t >= 2 confirms (with check), t <= -2 rejects, otherwise inconclusive; at least 500 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are settlement bars in high 24-bar "
                           "volatility with a forecast opposite to the pre-settlement 2-bar move, as the Fidelity states."),
            "reading": reading,
        }

    # ---------- criterion ----------
    vals, fabs, unusual = [], [], []
    for coin, wins in prepared.items():
        grid_rets = []
        for w, (c, f, settle) in wins.items():
            n = len(c)
            for p in range(0, n - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        if len(grid_rets) == 0:
            continue
        mu = float(np.mean(grid_rets))
        for w, (c, f, settle) in wins.items():
            n = len(c)
            seen = set()
            for i in np.where((f != 0) & settle)[0]:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H])) or c[i] == 0:
                    continue
                ex = c[i + H] / c[i] - 1.0 - mu
                vals.append(f[i] / 10.0 * ex)
                fabs.append(abs(f[i]))
                unusual.append(np.sign(f[i]) * ex)

    vals = np.array(vals, dtype=float)
    fabs = np.array(fabs, dtype=float)
    unusual = np.array(unusual, dtype=float)
    n_cases = int(len(vals))

    mean_v = float(np.mean(vals)) if n_cases > 0 else None
    t = None
    if n_cases > 1:
        sd = float(np.std(vals, ddof=1))
        t = float(mean_v / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    diff = None
    chk = None
    n_large = n_small = 0
    if n_cases > 1:
        med = float(np.median(fabs))
        large = fabs > med
        small = ~large
        n_large, n_small = int(large.sum()), int(small.sum())
        if n_large > 0 and n_small > 0:
            diff = float(np.mean(unusual[large]) - np.mean(unusual[small]))
            chk = bool(diff > 0)

    if n_cases < 500:
        status = "not observable"
        decided = f"Only {n_cases} cases over all coins and windows, fewer than the plan's minimum of 500."
    elif t is not None and t >= 2 and chk is True:
        status = "confirmed"
        decided = "The main-measure t is 2 or more and the larger-half minus smaller-half difference is above 0."
    elif t is not None and t <= -2:
        status = "rejected"
        decided = "The main-measure t is -2 or less."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "A t of 2 or more with the supporting check failing is inconclusive."
    else:
        status = "inconclusive"
        decided = "The main-measure t lies between -2 and 2, which is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_v,
                         "statistic": ({"name": "ordinary t of the mean", "value": t} if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "mean unusual move in forecast direction, larger minus smaller |forecast| half",
                             "value": diff, "passed": chk},
        "counts": {"cases": n_cases, "active bars": int(n_active),
                   "larger half": n_large, "smaller half": n_small},
        "decided_by": decided,
        "reading": reading,
    }
