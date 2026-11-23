import numpy as np
import pandas as pd


def measure(bars):
    H = 12
    RAW = "debug_info.components.wkend.last_history_value"

    def _ts(df):
        return pd.to_datetime(df["timestamp"], utc=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = _ts(df)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            # raw component value; where missing, rebuild its sign from the 48-bar return
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            ret48 = np.full(len(df), np.nan)
            if len(df) > 48:
                ret48[48:] = close[48:] / close[:-48] - 1.0
            side_val = np.where(np.isnan(raw), ret48, raw)
            situation = ((ts.dt.weekday == 6) & (ts.dt.hour == 23)).values
            active = fc != 0
            expected_side = np.sign(side_val)
            agree = active & situation & (np.sign(fc) == expected_side) & (expected_side != 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean signed 12-bar excess return, top fifth of |forecast| cases"
    thr_words = "confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2; at least 100 top-fifth cases"
    reading = ("Situation bars are those starting Sunday 23:00 UTC, side from the sign of the raw component (48-bar price return where not recorded); "
               "cases are trending bars with nonzero forecast, first one per coin and calendar date, with a 12-bar return inside their window; "
               "the top/bottom fifth are the floor(N/5) cases with the largest/smallest |forecast| pooled over coins, ties broken by coin and time; "
               "the coin mean is over grid bars 0,12,24,... of every window.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr_words},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on expected side": n_agree},
            "decided_by": ("Fewer than 90% of nonzero-forecast bars are Sunday 23:00 bars whose forecast sign matches "
                           "the sign of the weekend move (continuation), as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = _ts(df)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            mask = (df["regime"].astype(str) == "trending").values & np.isfinite(fc) & (fc != 0)
            for i in np.where(mask)[0]:
                if i + H < n:
                    r = close[i + H] / close[i] - 1.0
                    if np.isfinite(r):
                        coin_cases.append((coin, ts.iloc[i], fc[i], r))
        if len(grid_rets) == 0:
            continue
        mu = float(np.mean(grid_rets))
        seen = set()
        for (c, t, f, r) in sorted(coin_cases, key=lambda x: x[1]):
            key = t.normalize()
            if key in seen:
                continue
            seen.add(key)
            rows.append({"coin": c, "ts": t, "absf": abs(f),
                         "val": float(np.sign(f) * (r - mu))})

    N = len(rows)
    k = N // 5
    cases = pd.DataFrame(rows) if N else pd.DataFrame(columns=["coin", "ts", "absf", "val"])
    if N:
        cases = cases.sort_values(["absf", "coin", "ts"], ascending=[False, True, True], kind="mergesort").reset_index(drop=True)
    top = cases.iloc[:k]["val"].values.astype(float) if k > 0 else np.array([])
    bottom = cases.iloc[N - k:]["val"].values.astype(float) if k > 0 else np.array([])

    def _mt(x):
        if len(x) < 2:
            return (float(np.mean(x)) if len(x) else None), None
        m = float(np.mean(x))
        s = float(np.std(x, ddof=1))
        return m, (m / (s / np.sqrt(len(x))) if s > 0 else None)

    m_top, t_top = _mt(top)
    m_bot = float(np.mean(bottom)) if len(bottom) else None
    diff = (m_top - m_bot) if (m_top is not None and m_bot is not None) else None
    check_pass = (diff > 0) if diff is not None else None

    counts = {"cases": int(N), "cases in the top fifth": int(len(top)), "cases in the bottom fifth": int(len(bottom))}

    if len(top) < 100:
        status = "not observable"
        decided = f"Only {len(top)} cases in the top fifth, below the plan's minimum of 100."
    elif t_top is None:
        status = "inconclusive"
        decided = "The t of the main mean could not be computed (zero spread), so |t| is not at least 2."
    elif m_top > 0 and t_top >= 2 and check_pass:
        status = "confirmed"
        decided = "The main mean is positive with t >= 2 and the top-minus-bottom fifth difference is above 0."
    elif m_top < 0 and t_top <= -2:
        status = "rejected"
        decided = "The main mean is negative with t <= -2."
    elif m_top > 0 and t_top >= 2:
        status = "inconclusive"
        decided = "The main mean confirms (positive, t >= 2) but the supporting check fails (top minus bottom fifth not above 0)."
    else:
        status = "inconclusive"
        decided = "The |t| of the main mean is below 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name,
                         "value": m_top,
                         "statistic": ({"name": "t of the mean", "value": float(t_top)} if t_top is not None else None),
                         "threshold": thr_words},
        "supporting_check": {"name": "top-fifth mean minus bottom-fifth mean > 0",
                             "value": (float(diff) if diff is not None else None),
                             "passed": (bool(check_pass) if check_pass is not None else None)},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
