import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 168
    REG_P = 1440
    RISE_P = 336
    RISE_COL = "debug_info.components.rise14d.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            # Regime: 1440-bar return > 0, recomputed from prices inside the window where possible,
            # otherwise the detector's recorded decision (its component is not recorded).
            ret60 = close / close.shift(REG_P) - 1.0
            reg_rec = (df["regime"].astype(str) == "trending")
            regime_ok = np.where(ret60.notna(), ret60 > 0, reg_rec)
            # Rise: the recorded raw 336-bar return, else recomputed from prices.
            rise_rec = pd.to_numeric(df[RISE_COL], errors="coerce") if RISE_COL in df.columns \
                else pd.Series(np.nan, index=df.index)
            rise_px = close / close.shift(RISE_P) - 1.0
            rise = rise_rec.where(rise_rec.notna(), rise_px)
            rise_ok = (rise > 0).fillna(False).values
            active = (fc.fillna(0) != 0).values
            on_side = (fc > 0).fillna(False).values
            sit = np.asarray(regime_ok, dtype=bool) & rise_ok & on_side
            n_active += int(active.sum())
            n_agree += int((active & sit).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "t of pooled slope of demeaned forward 168-bar return on forecast (trending grid bars)"
    threshold = "confirm if t >= 2 and slope positive in >= 4 of 6 coins; reject if t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars where the 1440-bar "
                           "return is above 0 and the 336-bar return is above 0, as the Fidelity requires."
                           if n_active > 0 else "No bar carries a non-zero forecast."),
            "reading": "Regime recomputed from the 1440-bar in-window return where available, else the recorded regime; rise from the recorded raw value, else from prices.",
        }

    # ---------- 2. Criterion ----------
    per_coin = {}
    for coin, wins in bars.items():
        all_fwd = []
        rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                fwd = c1 / c0 - 1.0
                all_fwd.append(fwd)
                if str(df["regime"].iloc[i]) == "trending":
                    f = pd.to_numeric(pd.Series([df["forecast"].iloc[i]]), errors="coerce").iloc[0]
                    if np.isfinite(f):
                        rows.append((fwd, float(f)))
        if len(all_fwd) == 0:
            continue
        mu = float(np.mean(all_fwd))
        per_coin[coin] = [(fwd - mu, f) for fwd, f in rows]

    ys, xs = [], []
    coin_slopes = {}
    for coin, rows in per_coin.items():
        if rows:
            y = np.array([r[0] for r in rows]); x = np.array([r[1] for r in rows])
            ys.append(y); xs.append(x)
            if len(x) >= 3 and np.std(x) > 0:
                coin_slopes[coin] = float(stats.linregress(x, y).slope)
            else:
                coin_slopes[coin] = None
        else:
            coin_slopes[coin] = None
    y = np.concatenate(ys) if ys else np.array([])
    x = np.concatenate(xs) if xs else np.array([])
    n_total = int(len(x))
    n_pos = int((x > 0).sum())

    slope = None
    tval = None
    if n_total >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tval = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    n_coins_pos = int(sum(1 for s in coin_slopes.values() if s is not None and s > 0))
    check_pass = n_coins_pos >= 4

    counts = {"independent trending grid bars": n_total,
              "trending grid bars with forecast above 0": n_pos,
              "coins with positive slope": n_coins_pos}

    if n_total < 100 or n_pos < 30:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_total} trending grid bars (need 100) and "
                   f"{n_pos} with forecast above 0 (need 30).")
    elif tval is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and check_pass:
        status = "confirmed"
        decided = "The slope t is at least 2 and the slope is positive in at least 4 of the 6 coins."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope t is at most -2."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope t is at least 2 but the slope is positive in fewer than 4 coins."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": tval,
                         "statistic": {"name": "OLS slope t", "value": tval} if tval is not None else None,
                         "threshold": threshold},
        "supporting_check": {"name": "coins with positive slope (need at least 4 of 6)",
                             "value": n_coins_pos, "passed": bool(check_pass)},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Grid bars are positions 0,168,... of each window kept when the recorded regime is trending and the "
                    "forward return stays inside the window; the coin mean is the mean of its grid 168-bar returns over all "
                    "windows; the pooled OLS includes an intercept; a coin with no computable slope counts as not positive; "
                    "the plan's 'inconclusive' for too few cases is reported as 'not observable' per the workflow."),
    }
