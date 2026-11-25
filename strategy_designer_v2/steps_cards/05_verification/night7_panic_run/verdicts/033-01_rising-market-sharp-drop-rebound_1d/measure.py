import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    RAW = "debug_info.components.scaled_fall.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: a down day (raw vol-scaled 1-day return < 0) in a rising market
    # (the profile: regime "unknown", i.e. the 60-bar price evolution veto did not fire);
    # outcome "rises" -> expected side long (forecast > 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            reg = df["regime"].astype(str)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            situ = (reg == "unknown") & raw.notna() & (raw < 0)
            ok = active & situ & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    sit_passed = True if agreement is None else bool(agreement >= 0.90)

    main_name = "OLS slope of 3-day forward return minus coin's normal 3-day drift on forecast, in-profile grid bars"
    threshold = "confirm: slope t >= 2 with supporting difference > 0; reject: slope t <= -2; else inconclusive"
    sup_name = "mean 3-day forward return after forecast > 0 minus after in-profile forecast = 0"
    reading = ("Rising market read as regime 'unknown' (the detector's recorded decision, its component not being "
               "recorded) and a down day as a negative raw scaled_fall value; one pooled regression over all coins "
               "and windows with OLS t; the normal drift is each coin's mean 3-bar return over the non-overlapping "
               "grid of all its windows (all bars); the supporting difference uses raw forward returns on in-profile "
               "grid bars; grid bars without a 3-bar forward return in their window are left out.")

    if not sit_passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are down days (negative scaled fall) "
                           "in the rising profile (regime 'unknown') with a long forecast."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_all = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            reg = df["regime"].astype(str).to_numpy()
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_all.append(r)
                if reg[i] == "unknown" and np.isfinite(fc[i]):
                    coin_rows.append((r, fc[i]))
        if len(coin_all) == 0:
            continue
        drift = float(np.mean(coin_all))
        for r, f in coin_rows:
            rows.append((r, r - drift, f))

    if rows:
        arr = np.array(rows, dtype=float)
        ret, exc, f = arr[:, 0], arr[:, 1], arr[:, 2]
    else:
        ret = exc = f = np.array([], dtype=float)

    n_inprof = int(len(f))
    n_pos = int((f > 0).sum())
    n_zero = int((f == 0).sum())
    counts = {
        "grid bars with forecast > 0": n_pos,
        "in-profile grid bars": n_inprof,
        "in-profile grid bars with forecast = 0": n_zero,
    }

    slope = None
    t_slope = None
    if n_inprof >= 3 and np.std(f) > 0:
        lr = stats.linregress(f, exc)
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            t_slope = float(lr.slope / lr.stderr)

    diff = None
    if n_pos > 0 and n_zero > 0:
        diff = float(np.mean(ret[f > 0]) - np.mean(ret[f == 0]))
    sup_passed = None if diff is None else bool(diff > 0)

    main = {
        "name": main_name,
        "value": slope,
        "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
        "threshold": threshold,
    }
    sup = {"name": sup_name, "value": diff, "passed": sup_passed}
    sc = {"agreement": None if agreement is None else float(agreement), "passed": True}

    if n_pos < 30 or n_inprof < 60:
        status = "not observable"
        decided = ("The plan's minimum counts are not reached: at least 30 grid bars with forecast > 0 "
                   "(have %d) and 60 in-profile grid bars (have %d) are needed." % (n_pos, n_inprof))
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided = "Confirm rule: slope t >= 2 and the supporting difference is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "Reject rule: slope t <= -2."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "Inconclusive rule: slope t >= 2 but the supporting difference is at or below 0 (or not computable)."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: slope t between -2 and 2."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
