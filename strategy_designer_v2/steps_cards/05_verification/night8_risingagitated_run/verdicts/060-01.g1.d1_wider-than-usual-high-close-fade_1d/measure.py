import json
import numpy as np
import pandas as pd


def measure(bars):
    BAND = 2.0
    H = 1
    COMP = "range_mult"

    def comp_series(df, cid, field="last_history_value"):
        col = f"debug_info.components.{cid}.{field}"
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce").reset_index(drop=True)
        out = [np.nan] * len(df)
        if "debug_info.components" in df.columns:
            for i, v in enumerate(df["debug_info.components"].tolist()):
                d = v
                if isinstance(d, str):
                    try:
                        d = json.loads(d)
                    except Exception:
                        d = None
                if isinstance(d, dict):
                    c = d.get(cid)
                    if isinstance(c, dict) and field in c:
                        try:
                            out[i] = float(c[field])
                        except Exception:
                            pass
        return pd.Series(out, dtype=float)

    # ---- pass 1: coin drifts (mean 1-bar return over all windows, non-overlapping grid of step 1)
    drifts = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True).values
            if len(c) > H:
                r = c[H::H] / c[:-H:H][: len(c[H::H])] - 1.0
                rets.extend([x for x in r if np.isfinite(x)])
        drifts[coin] = float(np.mean(rets)) if rets else np.nan

    n_active = 0
    n_agree = 0
    cases = []  # (day, move, range_mult)

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if len(df) == 0:
                continue
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            hi = pd.to_numeric(df["high"], errors="coerce")
            lo = pd.to_numeric(df["low"], errors="coerce")
            cl = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            rm_rec = comp_series(df, COMP)
            rng = hi - lo
            cloc = (cl - lo) / rng.replace(0, np.nan)
            rr_calc = rng / rng.rolling(20, min_periods=20).mean()
            rr = rm_rec.where(rm_rec.notna(), rr_calc)

            # situation check
            for i in range(len(df)):
                f = fc.iloc[i]
                if f != 0:
                    n_active += 1
                    ok = (f < 0 and np.isfinite(cloc.iloc[i]) and cloc.iloc[i] > 0.5
                          and np.isfinite(rr.iloc[i]) and rr.iloc[i] >= 1.0)
                    if ok:
                        n_agree += 1

            # short bets: rise of the short magnitude of >= BAND from its lowest level since last bet
            ref = 0.0
            prev_side = 0
            for i in range(len(df)):
                f = fc.iloc[i]
                side = int(np.sign(f))
                if side != prev_side or side == 0:
                    ref = 0.0
                prev_side = side
                if side >= 0:
                    continue
                m = -f
                if m - ref >= BAND:
                    ref = m
                    if i + H < len(df):
                        c0, c1 = cl.iloc[i], cl.iloc[i + H]
                        if np.isfinite(c0) and np.isfinite(c1) and c0 != 0 and np.isfinite(drifts[coin]):
                            r = c1 / c0 - 1.0
                            mv = -(r - drifts[coin])
                            cases.append((ts.iloc[i].floor("D") if pd.notna(ts.iloc[i]) else None,
                                          float(mv), float(rm_rec.iloc[i])))
                else:
                    ref = min(ref, m)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90
    main_name = "mean short-side unusual 1-bar move per case"
    thr = "confirm: mean > 0 with t >= 2 (cases summed per day) and supporting check passes; reject: mean < 0 with t <= -2"
    reading = ("The falling agitated profile is not recomputed (its detector components are not recorded and need more "
               "history than a window) so the check covers the upper-half close and range multiple >= 1 on the short side; "
               "the wider half is cases strictly above the median range_mult and the narrower half those at or below it; "
               "the plan's 'fewer than 30 cases or case-days' rule is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None, "case-days": None},
            "decided_by": (f"only {agreement:.1%} of the {n_active} active bars are short bars with an upper-half close "
                           "and a range of at least its 20-day mean, below the 90% required"),
            "reading": reading,
        }

    cdf = pd.DataFrame(cases, columns=["day", "mv", "rm"])
    cdf = cdf.dropna(subset=["day", "mv"])
    n = len(cdf)
    ndays = int(cdf["day"].nunique()) if n else 0

    mean = float(cdf["mv"].mean()) if n else None
    t = None
    if n > 0 and ndays > 1:
        dev = cdf["mv"] - mean
        ds = dev.groupby(cdf["day"]).sum().values
        var = (ds ** 2).sum() * ndays / (ndays - 1)
        se = np.sqrt(var) / n
        t = float(mean / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    sc = cdf.dropna(subset=["rm"])
    if len(sc) >= 2:
        med = sc["rm"].median()
        wide = sc.loc[sc["rm"] > med, "mv"]
        narrow = sc.loc[sc["rm"] <= med, "mv"]
        if len(wide) > 0 and len(narrow) > 0:
            sup_val = float(wide.mean() - narrow.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"cases": int(n), "case-days": int(ndays), "active bars": int(n_active)}

    if n < 30 or ndays < 30:
        status = "not observable"
        decided = f"fewer than 30 cases or 30 distinct case-days ({n} cases on {ndays} days)"
    elif t is None:
        status = "inconclusive"
        decided = "the t across case-days could not be computed"
    elif mean > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "mean short-side unusual move above 0 with t >= 2 and the wider-minus-narrower difference above 0"
        else:
            status = "inconclusive"
            decided = "main measure meets the confirm rule but the supporting check fails"
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "mean short-side unusual move below 0 with t <= -2 across case-days"
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean,
                         "statistic": ({"name": "t of the mean, cases summed per day", "value": t}
                                       if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "wider-half minus narrower-half mean move (split at median range_mult)",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
