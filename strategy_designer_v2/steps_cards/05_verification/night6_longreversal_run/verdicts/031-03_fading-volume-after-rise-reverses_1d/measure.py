import json
import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 30
    REGIME = "mean_reversion"
    COMP = "vol_drop"
    FLAT_COL = "debug_info.components.%s.last_history_value" % COMP

    def comp_raw(df):
        # raw value of the config's strategy component (recorded only on its regime's bars)
        if FLAT_COL in df.columns:
            return pd.to_numeric(df[FLAT_COL], errors="coerce")
        out = pd.Series(np.nan, index=df.index, dtype=float)
        if "debug_info.components" not in df.columns:
            return out
        for idx, v in df["debug_info.components"].items():
            d = v
            if isinstance(d, str):
                try:
                    d = json.loads(d)
                except Exception:
                    d = None
            if isinstance(d, dict):
                c = d.get(COMP)
                if isinstance(c, dict):
                    val = c.get("last_history_value")
                    try:
                        out.loc[idx] = float(val)
                    except Exception:
                        pass
        return out

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            in_regime = df["regime"].astype(str) == REGIME
            raw = comp_raw(df)
            active = fc != 0
            situ = in_regime & (raw < 0)          # rise regime and recent volume below the run's mean
            agree = active & situ & (fc < 0)       # expected side: short
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if n_active == 0 else bool(agreement >= 0.9)

    reading = ("The rise regime is read from the recorded `regime` column (the detector's 90-day/365-day component is not "
               "recorded and its 455-bar history cannot be rebuilt inside a window), the volume drop from vol_drop's raw "
               "value below 0, the expected side short; regime grid cases include bars with forecast 0; the coin's mean "
               "30-day return is taken over the 30-bar grid of all its windows; the plan's 'fewer than 30 regime grid "
               "cases' is applied as a minimum count (not observable).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are bars of the rise regime with recent "
                           "volume below the 90-day mean and a short forecast."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_rets.append(r)
                if reg[i] == REGIME and np.isfinite(fc[i]):
                    coin_cases.append((r, float(fc[i])))
        if len(coin_rets) == 0:
            continue
        mu = float(np.mean(coin_rets))
        for r, f in coin_cases:
            rows.append((coin, r - mu, f))

    n_cases = len(rows)
    ex = np.array([r[1] for r in rows], dtype=float)
    f = np.array([r[2] for r in rows], dtype=float)

    short_mask = f <= -2.0
    n_short = int(short_mask.sum())
    short_mean = float(np.mean(ex[short_mask])) if n_short > 0 else None
    check_passed = (short_mean < 0) if short_mean is not None else False

    slope = None
    t = None
    if n_cases >= 3 and np.std(f) > 0:
        lr = stats.linregress(f, ex)
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            t = float(lr.slope / lr.stderr)

    counts = {"regime grid cases": n_cases, "short-bet cases (forecast <= -2)": n_short}
    main = {
        "name": "slope of 30-day excess return on forecast, regime grid bars",
        "value": slope,
        "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
        "threshold": "confirm: slope > 0 with t >= 2.0; reject: slope < 0 with t <= -2.0; else inconclusive",
    }
    support = {"name": "mean excess 30-day return on forecast <= -2 cases below 0",
               "value": short_mean, "passed": bool(check_passed) if short_mean is not None else False}

    if n_cases < 30:
        status = "not observable"
        decided = "Fewer than 30 regime grid cases across all coins and windows (%d)." % n_cases
    elif t is None or slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so |t| < 2.0 is not exceeded."
    elif slope > 0 and t >= 2.0:
        if check_passed:
            status = "confirmed"
            decided = "Slope above 0 with t >= 2.0 and the short-bet cases' mean excess return below 0."
        else:
            status = "inconclusive"
            decided = "A confirming slope (t >= 2.0) whose supporting check fails."
    elif slope < 0 and t <= -2.0:
        status = "rejected"
        decided = "Slope below 0 with t <= -2.0: a deeper volume drop is followed by a higher excess return."
    else:
        status = "inconclusive"
        decided = "The slope's |t| is below 2.0."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement) if agreement is not None else None, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
