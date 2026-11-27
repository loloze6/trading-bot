import json
import numpy as np
import pandas as pd
from scipy import stats


def _component_series(df, comp_id, field="last_history_value"):
    """Read a recorded component value, whether the column is flattened or stored as a dict/JSON."""
    flat = f"debug_info.components.{comp_id}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    if "debug_info.components" in df.columns:
        out = []
        for v in df["debug_info.components"].values:
            val = np.nan
            d = v
            if isinstance(d, str):
                try:
                    d = json.loads(d)
                except Exception:
                    d = None
            if isinstance(d, dict):
                c = d.get(comp_id)
                if isinstance(c, dict) and c.get(field) is not None:
                    try:
                        val = float(c.get(field))
                    except Exception:
                        val = np.nan
            out.append(val)
        return pd.Series(out, index=df.index, dtype=float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def _short_bets(fc, band=2.0):
    """Short bets of the forecast: a rise of the short forecast of at least the band,
    measured from its lowest short level since its last bet (from 0 after flat or a long)."""
    bets = np.zeros(len(fc), dtype=bool)
    ref = 0.0
    on_short = False
    for i, f in enumerate(fc):
        if not np.isfinite(f) or f >= 0:
            on_short = False
            ref = 0.0
            continue
        s = -f
        if not on_short:
            ref = 0.0
            on_short = True
        if s - ref >= band - 1e-12:
            bets[i] = True
            ref = s
        else:
            ref = min(ref, s)
    return bets


def _clustered_t(values, days):
    n = len(values)
    if n < 2:
        return None
    m = float(np.mean(values))
    dev = pd.Series(values - m).groupby(np.asarray(days)).sum().values
    k = len(dev)
    if k < 2:
        return None
    var = (dev ** 2).sum() * k / (k - 1) / (n ** 2)
    if var <= 0:
        return None
    return m / np.sqrt(var)


def measure(bars):
    reading = ("The situation is taken as zr >= 1 (the recorded raw value of the identical 'rise' component, "
               "recomputed from closes as return / 20-return std if missing) with the regime 'trending' standing "
               "for the falling-calm profile (its detector components are not recorded and the 365-bar percentile "
               "cannot be rebuilt inside a window), on the short side; cases are the workflow's short bets "
               "(band 2) on every bar of the 1-bar grid; the median split puts |forecast| above the median in the "
               "top half and at or below it in the bottom half; the plan's 'fewer than 50 cases or 30 days' is "
               "applied as the minimum counts (not observable).")

    case_rows = []
    n_active = 0
    n_agree = 0

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        # normal drift: mean 1-day return over all windows of the coin
        all_rets = []
        prepared = []
        for w in sorted(wins.keys()):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fwd = close.shift(-1) / close - 1.0
            all_rets.append(fwd.dropna().values)
            prepared.append((w, df, close, fwd))
        if not all_rets:
            continue
        cat = np.concatenate(all_rets)
        drift = float(np.mean(cat)) if len(cat) else np.nan

        for w, df, close, fwd in prepared:
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ret = close / close.shift(1) - 1.0
            zr_px = (ret / ret.rolling(20).std(ddof=1)).values
            zr_rec = _component_series(df, "rise", "last_history_value").values
            zr = np.where(np.isfinite(zr_rec), zr_rec, zr_px)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))

            active = fc != 0
            situation = (np.where(np.isfinite(zr), zr, -np.inf) >= 1.0) & (regime == "trending")
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            bets = _short_bets(fc)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            fv = fwd.values
            for i in np.where(bets)[0]:
                if not np.isfinite(fv[i]) or not np.isfinite(drift):
                    continue
                case_rows.append({
                    "coin": coin,
                    "day": ts.iloc[i].strftime("%Y-%m-%d"),
                    "absf": abs(fc[i]),
                    "unusual": -(fv[i] - drift),
                })

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean short-direction next-day unusual move (return minus coin drift)"
    main_thr = "confirm: mean > 0 with day-clustered t >= 2; reject: t <= -2"
    sup_name = "top-minus-bottom half (median |forecast|) mean unusual move"

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": 0, "distinct days": 0},
            "decided_by": "No active bar in the record: fewer than 50 cases on fewer than 30 distinct days.",
            "reading": reading,
        }

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Under 90 % of the active bars are large up days (zr >= 1) in the falling-calm regime "
                           "with a short forecast, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows)
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_u = float(cases["unusual"].mean()) if n_cases else None
    t_main = _clustered_t(cases["unusual"].values, cases["day"].values) if n_cases else None
    t_main = None if t_main is None or not np.isfinite(t_main) else float(t_main)

    diff = None
    welch = None
    if n_cases >= 2:
        med = float(cases["absf"].median())
        top = cases.loc[cases["absf"] > med, "unusual"].values
        bot = cases.loc[cases["absf"] <= med, "unusual"].values
        if len(top) > 0 and len(bot) > 0:
            diff = float(np.mean(top) - np.mean(bot))
            if len(top) >= 2 and len(bot) >= 2:
                wt = stats.ttest_ind(top, bot, equal_var=False).statistic
                welch = float(wt) if np.isfinite(wt) else None
    sup_passed = None if diff is None else bool(diff > 0)

    main = {"name": main_name, "value": mean_u,
            "statistic": None if t_main is None else {"name": "t of the mean, cases of one day taken together",
                                                       "value": t_main},
            "threshold": main_thr}
    supporting = {"name": sup_name, "value": diff, "passed": sup_passed}
    if welch is not None:
        counts_extra = {}
    sc = {"agreement": float(agreement), "passed": True}

    if n_cases < 50 or n_days < 30:
        which = []
        if n_cases < 50:
            which.append(f"{n_cases} cases (minimum 50)")
        if n_days < 30:
            which.append(f"{n_days} distinct days (minimum 30)")
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": supporting, "counts": counts,
                "decided_by": "Minimum count not reached: " + " and ".join(which) + ".",
                "reading": reading}

    if t_main is None:
        status, why = "inconclusive", "The main measure's t cannot be computed, so no confirm or reject rule is met."
    elif t_main <= -2:
        status, why = "rejected", "The mean unusual move is negative with t <= -2: the large rises continue."
    elif t_main >= 2 and mean_u > 0:
        if diff is not None and diff > 0:
            status, why = "confirmed", ("Mean unusual move positive with t >= 2 and the top-minus-bottom "
                                        "difference above 0.")
        elif welch is not None and welch <= -2:
            status, why = "rejected", ("Main measure confirms but the top-minus-bottom difference has a "
                                       "Welch t <= -2.")
        else:
            status, why = "inconclusive", ("Main t >= 2 but the top-minus-bottom difference is at or below 0 "
                                           "with a Welch t above -2.")
    else:
        status, why = "inconclusive", "The main measure's t is between -2 and 2."

    supporting["welch_t"] = welch
    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": supporting, "counts": counts,
            "decided_by": why, "reading": reading}
