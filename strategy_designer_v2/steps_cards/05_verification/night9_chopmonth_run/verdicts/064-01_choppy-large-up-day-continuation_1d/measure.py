import json
import numpy as np
import pandas as pd


def _component_raw(df, comp_id):
    """Recorded raw value (last_history_value) of a strategy component, NaN where not recorded."""
    col = f"debug_info.components.{comp_id}.last_history_value"
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce").reset_index(drop=True)
    out = np.full(len(df), np.nan)
    if "debug_info.components" in df.columns:
        vals = df["debug_info.components"].tolist()
        for i, v in enumerate(vals):
            d = v
            if isinstance(d, str):
                try:
                    d = json.loads(d)
                except Exception:
                    d = None
            if isinstance(d, dict):
                c = d.get(comp_id)
                if isinstance(c, dict) and c.get("last_history_value") is not None:
                    try:
                        out[i] = float(c.get("last_history_value"))
                    except Exception:
                        pass
    return pd.Series(out)


def _recompute_jump(close):
    r = close.pct_change()
    vol = r.rolling(30).std()
    return r / vol


def _bets_long(fc, band=2.0):
    """Long bets: rise of the forecast of at least the band from its lowest long level since the last bet."""
    bets = np.zeros(len(fc), dtype=bool)
    ref = 0.0
    for i, f in enumerate(fc):
        if not np.isfinite(f) or f <= 0:
            ref = 0.0
            continue
        if f - ref >= band - 1e-12:
            bets[i] = True
            ref = f
        else:
            ref = min(ref, f)
    return bets


def measure(bars):
    H = 5
    THR = 2.0

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        for w, df0 in wins.items():
            df = df0.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).reset_index(drop=True)
            jump = _component_raw(df, "jump_size")
            rec = _recompute_jump(close)
            jump = jump.where(jump.notna(), rec)
            active = fc != 0
            situ = (jump >= THR - 1e-9) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
            prepared[(coin, w)] = (df, close, fc)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if n_active == 0 else (agreement >= 0.90)
    situation_check = {"agreement": agreement, "passed": bool(passed)}

    main_name = "mean strength of long cases over 5 bars (unusual move / usual 5-bar move)"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": "Fewer than 90% of the bars with a nonzero forecast are long bets on days whose 1-day return is at least 2 times the 30-day standard deviation of daily returns, as the plan's situation requires.",
            "reading": "none",
        }

    # ---------- coin drift and usual move (non-overlapping 5-bar grid, all windows) ----------
    coin_rets = {}
    for (coin, w), (df, close, fc) in prepared.items():
        c = close.values
        idx = np.arange(0, len(c) - H, H)
        r = c[idx + H] / c[idx] - 1.0
        r = r[np.isfinite(r)]
        coin_rets.setdefault(coin, []).extend(r.tolist())
    coin_stats = {}
    for coin, rs in coin_rets.items():
        rs = np.asarray(rs, dtype=float)
        if len(rs) >= 2:
            coin_stats[coin] = (float(np.mean(rs)), float(np.std(rs, ddof=1)))

    # ---------- cases ----------
    cases = []  # (day, strength, unusual, forecast)
    for (coin, w), (df, close, fc) in prepared.items():
        if coin not in coin_stats:
            continue
        drift, usual = coin_stats[coin]
        if not np.isfinite(usual) or usual <= 0:
            continue
        bets = _bets_long(fc.values)
        c = close.values
        ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        n = len(c)
        for start in range(0, n, H):
            cell = np.where(bets[start:start + H])[0]
            if len(cell) == 0:
                continue
            t = start + int(cell[0])
            if t + H >= n:
                continue
            r = c[t + H] / c[t] - 1.0
            if not np.isfinite(r):
                continue
            unusual = r - drift
            day = ts.iloc[t].strftime("%Y-%m-%d") if pd.notna(ts.iloc[t]) else str(t)
            cases.append((day, unusual / usual, unusual, float(fc.values[t])))

    n_cases = len(cases)
    days = sorted(set(x[0] for x in cases))
    n_days = len(days)
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_s = None
    t_stat = None
    if n_cases > 0:
        s = np.array([x[1] for x in cases])
        mean_s = float(np.mean(s))
        dev = pd.Series(s - mean_s).groupby([x[0] for x in cases]).sum().values
        D = len(dev)
        if D >= 2:
            var = (D / (D - 1)) * np.sum(dev ** 2) / (n_cases ** 2)
            se = np.sqrt(var)
            t_stat = float(mean_s / se) if se > 0 else None

    supp_val = None
    supp_pass = None
    if n_cases > 0:
        f = np.array([x[3] for x in cases])
        u = np.array([x[2] for x in cases])
        med = np.median(f)
        hi = u[f > med]
        lo = u[f <= med]
        if len(hi) > 0 and len(lo) > 0:
            supp_val = float(np.mean(hi) - np.mean(lo))
            supp_pass = bool(supp_val > 0)
        else:
            supp_pass = False

    main = {
        "name": main_name,
        "value": mean_s,
        "statistic": {"name": "t of the mean, cases grouped by day", "value": t_stat} if t_stat is not None else None,
        "threshold": threshold,
    }
    supporting = {
        "name": "mean unusual move above-median forecast minus at/below-median",
        "value": supp_val,
        "passed": supp_pass,
    }
    reading = ("A case is the first long bet (forecast rise of at least 2 points from its lowest long level since the last bet) "
               "in each 5-bar grid cell of a window, the day t uses the day-summed deviations with a D/(D-1) correction, "
               "the supporting check uses the unusual move (not divided by the usual move), and fewer than 30 cases or 30 days is reported as not observable.")

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = f"The plan's minimum of 30 cases on 30 distinct days is not reached ({n_cases} cases on {n_days} days)."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean strength could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_s > 0 and t_stat >= 2:
        if supp_pass:
            status = "confirmed"
            decided = "The mean strength is above 0 with t >= 2 and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "The mean strength is above 0 with t >= 2 but the supporting check fails."
    elif mean_s < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean strength is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean strength is between -2 and 2."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
