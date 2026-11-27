import json
import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0

    def _ts(s):
        if pd.api.types.is_numeric_dtype(s):
            v = pd.to_numeric(s, errors="coerce")
            unit = "ms" if v.abs().max() > 1e11 else "s"
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True, errors="coerce")

    def _comp(df, cid, field="last_history_value"):
        flat = f"debug_info.components.{cid}.{field}"
        if flat in df.columns:
            return pd.to_numeric(df[flat], errors="coerce").to_numpy(dtype=float)
        out = np.full(len(df), np.nan)
        if "debug_info.components" in df.columns:
            for i, d in enumerate(df["debug_info.components"].tolist()):
                if isinstance(d, str):
                    try:
                        d = json.loads(d)
                    except Exception:
                        d = None
                if isinstance(d, dict):
                    c = d.get(cid)
                    if isinstance(c, dict) and c.get(field) is not None:
                        try:
                            out[i] = float(c.get(field))
                        except Exception:
                            pass
        return out

    # ---------- pass 1: situation check, drift, cases ----------
    act_total = 0
    act_agree = 0
    coin_grid_rets = {}
    raw_cases = []  # (coin, day, ret, loc_entry)

    for coin in sorted(bars.keys()):
        grid_rets = []
        for win in sorted(bars[coin].keys()):
            df = bars[coin][win]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            high = pd.to_numeric(df["high"], errors="coerce").to_numpy(dtype=float)
            low = pd.to_numeric(df["low"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            ts = _ts(df["timestamp"])
            n = len(df)

            # r5 from prices (inside the window)
            r5 = np.full(n, np.nan)
            if n > H:
                r5[H:] = close[H:] / close[:-H] - 1.0
            # close location: recorded raw value, else from prices
            rng = high - low
            with np.errstate(divide="ignore", invalid="ignore"):
                loc_p = np.where(rng > 0, (close - low) / rng, np.nan)
            loc_rec = _comp(df, "high_close")
            loc = np.where(np.isfinite(loc_rec), loc_rec, loc_p)

            for i in range(n):
                if fc[i] != 0 and np.isfinite(r5[i]) and np.isfinite(loc[i]):
                    act_total += 1
                    if fc[i] < 0 and r5[i] < 0 and loc[i] > 0.5:
                        act_agree += 1

            # grid returns for the coin's normal drift
            for p in range(0, n - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] > 0:
                    grid_rets.append(close[p + H] / close[p] - 1.0)

            # bets on the short side
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                s = -fc[i] if fc[i] < 0 else 0.0
                if s == 0.0:
                    ref = 0.0
                    continue
                if s - ref >= BAND:
                    bet[i] = True
                    ref = s
                else:
                    ref = min(ref, s)

            # one case per 5-bar grid cell: the cell's first bet
            seen = set()
            for i in range(n):
                if not bet[i]:
                    continue
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                ret = close[i + H] / close[i] - 1.0
                day = ts.iloc[i].strftime("%Y-%m-%d") if pd.notna(ts.iloc[i]) else f"{coin}-{win}-{i}"
                raw_cases.append((coin, day, ret, float(loc_rec[i]) if np.isfinite(loc_rec[i]) else np.nan))
        coin_grid_rets[coin] = grid_rets

    agreement = (act_agree / act_total) if act_total > 0 else None
    passed = (agreement is not None and agreement >= 0.9) or act_total == 0

    reading = ("Situation computed as r5 (close/close 5 bars before - 1, inside the window) < 0 and close location > 0.5 "
               "with the short side, over active bars where both are computable (the profile is a further restriction, not "
               "required); a case is the first short bet (rise of |forecast| of at least 2 from its lowest level since the "
               "last bet) in each 5-bar grid cell of its window, with a full 5-bar return inside the window; the day-pooled t "
               "uses per-day sums of deviations from the mean with a D/(D-1) correction; the supporting split puts cases "
               "above the median high_close in the upper half and the rest in the lower half; the plan's minimum of 30 "
               "distinct days is applied as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(act_total)},
            "decided_by": ("Fewer than 90 % of the active bars are bars with a negative 5-day return and a close in the upper "
                           "half of the range on the short side, as the plan's situation requires."),
            "reading": reading,
        }

    drift = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in coin_grid_rets.items()}
    u, days, locs = [], [], []
    for coin, day, ret, le in raw_cases:
        d = drift.get(coin, np.nan)
        if not np.isfinite(d):
            continue
        u.append(-(ret - d))
        days.append(day)
        locs.append(le)
    u = np.asarray(u, dtype=float)
    locs = np.asarray(locs, dtype=float)
    n_cases = int(len(u))
    n_days = int(len(set(days)))

    mean_u = float(np.mean(u)) if n_cases else None
    t_val = None
    if n_cases > 1 and n_days > 1:
        dev = pd.Series(u - mean_u).groupby(pd.Series(days)).sum().to_numpy()
        var = (n_days / (n_days - 1.0)) * float(np.sum(dev ** 2)) / (n_cases ** 2)
        se = np.sqrt(var)
        if se > 0:
            t_val = float(mean_u / se)

    diff = None
    sup_pass = None
    m = np.isfinite(locs)
    if m.sum() >= 2:
        med = float(np.median(locs[m]))
        up = u[m][locs[m] > med]
        lo = u[m][locs[m] <= med]
        if len(up) and len(lo):
            diff = float(np.mean(up) - np.mean(lo))
            sup_pass = bool(diff > 0)

    counts = {"cases": n_cases, "distinct days with cases": n_days}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct days with cases, below the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The day-pooled t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_val >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 and the upper-minus-lower difference is above 0."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2: prices rise more than their drift after high closes."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the upper-minus-lower difference is at or below 0 (or could not be computed)."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": True},
        "main_measure": {
            "name": "mean unusual 5-bar move in the short direction",
            "value": mean_u,
            "statistic": ({"name": "t of the mean, cases of one day pooled", "value": t_val} if t_val is not None else None),
            "threshold": "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "upper-half minus lower-half mean unusual move (median high_close split)",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
