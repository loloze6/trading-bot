import numpy as np
import pandas as pd
from scipy import stats


def _ts(series):
    s = series
    if pd.api.types.is_numeric_dtype(s):
        v = float(pd.Series(s).dropna().iloc[0]) if s.notna().any() else 0.0
        unit = "ms" if v > 1e11 else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    RAW = "debug_info.components.mom7.last_history_value"

    # ---------- per coin mean daily return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            r = (c.shift(-1) / c - 1.0).dropna()
            rets.append(r)
        allr = pd.concat(rets) if rets else pd.Series(dtype=float)
        coin_mean[coin] = float(allr.mean()) if len(allr) else np.nan

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    sig_rows = []  # (forecast, excess) on Saturday-signal bars
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            ts = _ts(d["timestamp"])
            close = d["close"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            # situation: the coming bar is a Saturday (bar starting Friday, closing at Saturday's open)
            next_day = (ts + pd.Timedelta(days=1)).dt.weekday
            is_fri_close = (next_day == 5).values
            mom_re = (close / close.shift(7) - 1.0)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                mom = raw.where(raw.notna(), mom_re)
            else:
                mom = mom_re
            rose = (mom > 0).values
            situation = is_fri_close & rose
            active = (fc.fillna(0) != 0).values
            on_side = (fc > 0).values
            n_active += int(active.sum())
            n_agree += int((active & situation & on_side).sum())

            # main measure rows
            nxt = close.shift(-1) / close - 1.0
            excess = nxt - coin_mean[coin]
            reg = d["regime"].astype(str).values
            mask = (reg == "mean_reversion") & excess.notna().values & fc.notna().values
            for f, e in zip(fc.values[mask], excess.values[mask]):
                sig_rows.append((float(f), float(e)))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "forecast-weighted mean next-day excess return on Saturday-signal bars"
    thr = "confirm: weighted mean > 0 with t >= 2 and correlation > 0; reject: weighted mean < 0 with t <= -2"
    reading = ("Situation bars are those whose next day (timestamp + 1 day) is a Saturday with a positive 7-day return "
               "(recorded raw value, else recomputed from closes); the t is the ordinary t of the unweighted mean excess "
               "return over Saturday-signal bars with forecast > 0, the correlation uses all Saturday-signal bars "
               "(regime mean_reversion) with a next-day return, and the plan's minimum of 300 bars is applied as "
               "'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation (forecast long only on Friday-close bars, next day Saturday, after a "
                           "7-day rise) holds on fewer than 90 % of the bars where the forecast is nonzero."
                           if n_active > 0 else "The forecast is never nonzero, so the plan's situation is never traded."),
            "reading": reading,
        }

    arr = np.array(sig_rows, dtype=float) if sig_rows else np.zeros((0, 2))
    f_all = arr[:, 0] if len(arr) else np.array([])
    e_all = arr[:, 1] if len(arr) else np.array([])
    pos = f_all > 0
    f_pos, e_pos = f_all[pos], e_all[pos]
    n_pos = int(pos.sum())

    wmean = float(np.sum(f_pos * e_pos) / np.sum(f_pos)) if n_pos > 0 else None
    if n_pos > 1 and np.std(e_pos, ddof=1) > 0:
        t = float(np.mean(e_pos) / (np.std(e_pos, ddof=1) / np.sqrt(n_pos)))
    else:
        t = None
    if len(f_all) > 2 and np.std(f_all) > 0 and np.std(e_all) > 0:
        corr = float(stats.pearsonr(f_all, e_all)[0])
    else:
        corr = None

    counts = {"Saturday bars with forecast > 0": n_pos,
              "Saturday-signal bars": int(len(f_all))}

    if n_pos < 300:
        status = "not observable"
        decided = f"Only {n_pos} Saturday bars with forecast > 0, below the plan's minimum of 300."
    elif wmean is None or t is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed."
    elif wmean > 0 and t >= 2 and corr is not None and corr > 0:
        status = "confirmed"
        decided = "The weighted mean excess return is positive with t >= 2 and the correlation is above 0."
    elif wmean < 0 and t <= -2:
        status = "rejected"
        decided = "The weighted mean excess return is negative with t <= -2."
    elif wmean > 0 and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the correlation is 0 or below (or undefined), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The numbers meet neither the confirm nor the reject rule (t between -2 and 2, or sign and t disagree)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": wmean,
                         "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "Pearson correlation of forecast and next-day excess return",
                             "value": corr,
                             "passed": (corr > 0) if corr is not None else None},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
