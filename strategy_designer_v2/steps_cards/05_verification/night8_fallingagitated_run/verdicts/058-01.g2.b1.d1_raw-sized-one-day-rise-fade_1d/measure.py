import numpy as np
import pandas as pd

H = 3
BAND = 2.0
COMP = "debug_info.components.rise_in_usual_moves.last_history_value"


def _ts(s):
    if np.issubdtype(s.dtype, np.number):
        v = float(np.nanmax(np.abs(s.values))) if len(s) else 0.0
        unit = "ns" if v > 1e17 else "us" if v > 1e14 else "ms" if v > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def _raw(df):
    close = df["close"].astype(float)
    r1 = close.pct_change(1)
    recomputed = r1 / r1.rolling(30).std()
    if COMP in df.columns:
        raw = pd.to_numeric(df[COMP], errors="coerce")
        return raw.where(raw.notna(), recomputed)
    return recomputed


def _bets(fc):
    # short-side bets: a rise of the short size of at least BAND from its lowest level since the last bet
    m = np.where(fc < 0, -fc, 0.0)
    ref = 0.0
    out = np.zeros(len(m), dtype=bool)
    for i, x in enumerate(m):
        if not np.isfinite(x) or x <= 0:
            ref = 0.0
            continue
        if x - ref >= BAND - 1e-12:
            out[i] = True
            ref = x
        else:
            ref = min(ref, x)
    return out


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            raw = _raw(df)
            profile = df["regime"].astype(str) == "unknown"
            active = fc != 0
            situ = profile & (raw > 0) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars inside the falling "
                           "agitated profile (regime 'unknown') on an up day (raw 1-day return over 30-day std > 0)"
                           if n_active > 0 else "The forecast is never non-zero, so no bar shows the plan's situation."),
            "reading": "The profile is read from the recorded regime ('unknown' = neither veto to 'chop' fired), the rise from the component's raw value > 0, the side as short.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin in sorted(bars):
        # coin's normal 3-bar drift over all windows, non-overlapping grid
        grid_rets = []
        prepared = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(close)
            for k in range(0, n - H, H):
                if close[k] > 0 and np.isfinite(close[k]) and np.isfinite(close[k + H]):
                    grid_rets.append(close[k + H] / close[k] - 1.0)
            prepared.append(df)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for df in prepared:
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ts = _ts(df["timestamp"])
            bet = _bets(fc)
            n = len(close)
            for k in range(0, n, H):
                cell = np.where(bet[k:min(k + H, n)])[0]
                if len(cell) == 0:
                    continue
                t = k + int(cell[0])
                if t + H >= n:
                    continue
                if not (close[t] > 0 and np.isfinite(close[t + H])):
                    continue
                r = close[t + H] / close[t] - 1.0
                rows.append({
                    "coin": coin,
                    "day": ts.iloc[t].strftime("%Y-%m-%d"),
                    "u": -(r - drift),
                    "fc": float(fc[t]),
                })

    cases = pd.DataFrame(rows, columns=["coin", "day", "u", "fc"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = float(cases["u"].mean()) if n_cases else None
    t_stat = None
    if n_cases >= 2:
        dev = cases["u"] - mean_u
        s_day = dev.groupby(cases["day"]).sum()
        se = float(np.sqrt((s_day ** 2).sum())) / n_cases
        t_stat = float(mean_u / se) if se > 0 else None

    big = cases[cases["fc"] <= -10]
    small = cases[(cases["fc"] > -10) & (cases["fc"] <= -2)]
    sup_val = None
    sup_pass = None
    if len(big) > 0 and len(small) > 0:
        sup_val = float(big["u"].mean() - small["u"].mean())
        sup_pass = bool(sup_val > 0)

    counts = {"cases": n_cases, "distinct days": n_days,
              "cases with forecast <= -10": int(len(big)),
              "cases with forecast between -2 and -10": int(len(small))}

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = (f"The plan's minimum of 30 cases and 20 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed (zero standard error)."
    elif mean_u > 0 and t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is positive with t >= 2 and the large-rise group's mean exceeds the small-rise group's."
        else:
            status = "inconclusive"
            decided = "The mean unusual move is positive with t >= 2 but the supporting check fails (or a group is empty), so it is inconclusive."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2: the price rises further after the rises."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean unusual 3-bar move of short cases (short direction)",
            "value": mean_u,
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t_stat}
                          if t_stat is not None else None),
            "threshold": "confirm if mean > 0 with t >= 2 (and supporting check passes); reject if mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "mean unusual move, forecast <= -10 minus forecast in [-10, -2]",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("A case is the first short bet (forecast short size rising >= 2 from its lowest since the last bet) in each "
                    "3-bar grid cell of a window, its return taken from that bar's close 3 bars ahead within the window, groups "
                    "split on the case bar's forecast (<= -10 vs > -10 and <= -2), and the day-clustered standard error is "
                    "sqrt(sum of squared per-day summed deviations) / number of cases; the profile is the recorded regime 'unknown'."),
    }
