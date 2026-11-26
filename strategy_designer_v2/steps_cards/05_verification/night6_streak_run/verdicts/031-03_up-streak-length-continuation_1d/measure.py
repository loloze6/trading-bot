import numpy as np
import pandas as pd

H = 5
RAW = "debug_info.components.up_streak.last_history_value"


def _to_day(ts):
    s = pd.Series(ts)
    if np.issubdtype(s.dtype, np.number):
        v = s.dropna()
        unit = "ms" if (len(v) and v.abs().max() > 1e11) else "s"
        t = pd.to_datetime(s, unit=unit, utc=True)
    else:
        t = pd.to_datetime(s, utc=True)
    return t.dt.floor("D").dt.strftime("%Y-%m-%d").values


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            price_up = (close > close.shift(1))
            # situation: current run of higher closes n > 0 (raw value), prices when the raw value is missing
            situ = np.where(raw.notna(), raw > 0, price_up.fillna(False))
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & pd.Series(situ, index=df.index).astype(bool) & (fc > 0)).sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    threshold_txt = "confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2; else inconclusive"
    mm_name = "OLS slope of 5-bar forward excess return on forecast (non-overlapping grid)"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("fewer than 90 % of the bars with a non-zero forecast are bars of an up run of closes "
                           "(raw streak length > 0) with a long forecast, as the Fidelity's situation and side require"),
            "reading": "situation taken as raw up_streak value > 0 (close above previous close when the raw value is missing), expected side long",
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            days = _to_day(df["timestamp"])
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                if np.isfinite(fc[i]):
                    rows.append((coin, days[i], float(fc[i]), r))
        coin_rets[coin] = float(np.mean(allr)) if allr else np.nan

    d = pd.DataFrame(rows, columns=["coin", "day", "fc", "ret"])
    if len(d):
        d["ex"] = d["ret"] - d["coin"].map(coin_rets)
        d = d[np.isfinite(d["ex"])]
    pos = d[d["fc"] > 0] if len(d) else d
    n_pos = int(len(pos))
    n_pos_days = int(pos["day"].nunique()) if n_pos else 0
    counts = {
        "grid bars with a positive forecast": n_pos,
        "distinct days of grid bars with a positive forecast": n_pos_days,
        "grid bars in the sample": int(len(d)),
        "distinct days in the sample": int(d["day"].nunique()) if len(d) else 0,
    }

    # slope with day-clustered t
    slope, tstat = None, None
    if len(d) >= 3 and d["fc"].var() > 0:
        x = d["fc"].values
        y = d["ex"].values
        xc = x - x.mean()
        sxx = float(np.sum(xc ** 2))
        b = float(np.sum(xc * (y - y.mean())) / sxx)
        a = y.mean() - b * x.mean()
        e = y - a - b * x
        sc = pd.Series(xc * e).groupby(d["day"].values).sum().values
        G, N = len(sc), len(y)
        if G > 1:
            var = (G / (G - 1)) * ((N - 1) / (N - 2)) * float(np.sum(sc ** 2)) / sxx ** 2
            if var > 0:
                tstat = float(b / np.sqrt(var))
        slope = b

    # supporting check
    sup_val, sup_pass = None, None
    if n_pos > 0:
        cut = pos["fc"].quantile(2.0 / 3.0)
        top = pos[pos["fc"] >= cut]
        zero = d[d["fc"] == 0]
        if len(top) and len(zero):
            sup_val = float(top["ex"].mean() - zero["ex"].mean())
            sup_pass = bool(sup_val > 0)

    main = {"name": mm_name, "value": slope,
            "statistic": ({"name": "OLS slope t, clustered by day", "value": tstat} if tstat is not None else None),
            "threshold": threshold_txt}
    supp = {"name": "mean excess 5-bar return, top third of positive forecasts minus forecast 0",
            "value": sup_val, "passed": sup_pass}
    reading = ("excess return = 5-bar return minus the coin's mean 5-bar return on the non-overlapping grid of all its windows; "
               "slope from OLS with intercept and CR1 standard error clustered by UTC day; top third = positive-forecast grid bars "
               "at or above their 2/3 quantile; the plan's minimum counts, when not reached, give 'not observable'.")

    if n_pos < 200 or n_pos_days < 150:
        status = "not observable"
        decided = (f"the plan's minimum of 200 grid bars with a positive forecast over 150 distinct days is not reached "
                   f"({n_pos} bars over {n_pos_days} days)")
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "the slope or its t could not be computed, so neither the confirm nor the reject rule is met"
    elif slope > 0 and tstat >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "the slope is positive with t >= 2 and the supporting check passes"
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = "the slope is negative with t <= -2: longer streaks are followed by weaker 5-day returns"
    elif slope > 0 and tstat >= 2:
        status = "inconclusive"
        decided = "the slope is positive with t >= 2 but the supporting check fails"
    else:
        status = "inconclusive"
        decided = "|t| < 2, which the plan rules inconclusive"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
