import json
import numpy as np
import pandas as pd


COMP = "depth_below_low"


def _to_dt(s):
    if np.issubdtype(s.dtype, np.number):
        v = s.dropna()
        unit = "ms" if (len(v) and v.abs().median() > 1e11) else "s"
        return pd.to_datetime(s, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def _comp_series(df, comp, field):
    col = f"debug_info.components.{comp}.{field}"
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    if "debug_info.components" in df.columns:
        out = []
        for v in df["debug_info.components"].values:
            d = v
            if isinstance(d, str):
                try:
                    d = json.loads(d)
                except Exception:
                    d = None
            val = np.nan
            if isinstance(d, dict):
                c = d.get(comp)
                if isinstance(c, dict):
                    x = c.get(field)
                    try:
                        val = float(x) if x is not None else np.nan
                    except Exception:
                        val = np.nan
            out.append(val)
        return pd.Series(out, index=df.index, dtype=float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def _bets(fc):
    """Bet bars: rise of the forecast on the long side of >= 2 points from its
    lowest long level since the last bet (from 0 after a flat or side change)."""
    flags = np.zeros(len(fc), dtype=bool)
    ref = 0.0
    prev_pos = False
    for i, f in enumerate(fc):
        if not np.isfinite(f) or f <= 0:
            ref = 0.0
            prev_pos = False
            continue
        if not prev_pos:
            ref = 0.0
        if f - ref >= 2.0 - 1e-12:
            flags[i] = True
            ref = f
        else:
            ref = min(ref, f)
        prev_pos = True
    return flags


def measure(bars):
    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    frames = {}
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys(), key=lambda x: (len(str(x)), str(x))):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            df = df.copy().reset_index(drop=True)
            df["_ts"] = _to_dt(df["timestamp"])
            df = df.sort_values("_ts").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            raw = _comp_series(df, COMP, "last_history_value")
            post = _comp_series(df, COMP, "post_pipeline_value")
            regime = df["regime"].astype(str)
            low = pd.to_numeric(df["low"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            prior_low = low.shift(1).rolling(10, min_periods=10).min()
            price_break = close < prior_low
            # break below prior 10-day low: raw depth > 0 where recorded, else from prices
            brk = np.where(raw.notna(), raw > 0, price_break.fillna(False))
            situation = (regime == "mean_reversion").values & brk.astype(bool)
            active = fc.values != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc.values > 0)).sum())
            df["_fc"] = fc.values
            df["_post"] = post.values
            df["_close"] = close.values
            frames[(coin, w)] = df

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    main_name = "mean unusual 1-day move after a long bet (close to next close minus coin's mean daily return)"
    thr = "positive with t >= 2 over at least 30 distinct case days to confirm; negative with t <= -2 to reject"
    sup_name = "mean unusual move of deeper half minus shallower half (split at median post_pipeline_value of depth_below_low)"
    reading = ("Bets are taken on every bar (1-bar grid) as long rises of the forecast of >= 2 points from its lowest long level since the last bet; "
               "the regime part of the situation is read from the recorded `regime` column; the day-clustered t uses per-day summed deviations with a G/(G-1) correction; "
               "the deeper half is the cases strictly above the median depth and the shallower half those at or below it; a count below 30 days is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "distinct case days": 0},
            "decided_by": (f"Only {agreement:.1%} of the {n_active} active bars are long bars in the mean_reversion regime with the close below the prior "
                           "10-day low, under the 90 % needed: the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    # ---------- drift per coin ----------
    drift = {}
    for coin in bars.keys():
        rs = []
        for (c, w), df in frames.items():
            if c != coin:
                continue
            cl = df["_close"].values
            r = cl[1:] / cl[:-1] - 1.0
            rs.append(r[np.isfinite(r)])
        drift[coin] = float(np.concatenate(rs).mean()) if rs and sum(len(x) for x in rs) else np.nan

    # ---------- cases ----------
    rows = []
    for (coin, w), df in frames.items():
        cl = df["_close"].values
        fwd = np.full(len(df), np.nan)
        if len(df) > 1:
            fwd[:-1] = cl[1:] / cl[:-1] - 1.0
        flags = _bets(df["_fc"].values)
        for i in np.where(flags)[0]:
            if not np.isfinite(fwd[i]) or not np.isfinite(drift[coin]):
                continue
            rows.append({
                "coin": coin,
                "day": df["_ts"].iloc[i].strftime("%Y-%m-%d"),
                "u": fwd[i] - drift[coin],
                "depth": df["_post"].iloc[i],
            })
    cases = pd.DataFrame(rows, columns=["coin", "day", "u", "depth"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = float(cases["u"].mean()) if n_cases else None
    t = None
    if n_cases and n_days >= 2:
        e = cases["u"] - mean_u
        S = e.groupby(cases["day"]).sum().values
        G = len(S)
        var = (S ** 2).sum() / (n_cases ** 2) * G / (G - 1)
        if var > 0:
            t = float(mean_u / np.sqrt(var))

    diff = None
    sup_pass = None
    d = cases.dropna(subset=["depth"]) if n_cases else cases
    if len(d) >= 2:
        med = d["depth"].median()
        deep = d.loc[d["depth"] > med, "u"]
        shal = d.loc[d["depth"] <= med, "u"]
        if len(deep) and len(shal):
            diff = float(deep.mean() - shal.mean())
            sup_pass = bool(diff > 0)

    counts = {"cases": n_cases, "distinct case days": n_days}
    stat = {"name": "t of the mean, cases of one day taken together", "value": t} if t is not None else None
    sup = {"name": sup_name, "value": diff, "passed": sup_pass}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct case days, under the plan's minimum of 30."
    elif t is not None and mean_u > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 over at least 30 case days and the deeper half beats the shallower half."
    elif t is not None and mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2 over at least 30 case days."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the deeper half does not beat the shallower half, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u, "statistic": stat, "threshold": thr},
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
