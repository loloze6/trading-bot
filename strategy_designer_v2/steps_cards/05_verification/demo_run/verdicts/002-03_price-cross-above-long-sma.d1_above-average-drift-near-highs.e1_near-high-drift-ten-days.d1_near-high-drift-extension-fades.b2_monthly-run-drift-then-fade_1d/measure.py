import json
import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10

    def _comp(df, cid, key):
        col = f"debug_info.components.{cid}.{key}"
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        if "debug_info.components" in df.columns:
            out = []
            for cell in df["debug_info.components"].values:
                v = np.nan
                try:
                    d = cell
                    if isinstance(d, str):
                        d = json.loads(d)
                    if isinstance(d, dict) and cid in d and isinstance(d[cid], dict):
                        x = d[cid].get(key, np.nan)
                        v = float(x) if x is not None else np.nan
                except Exception:
                    v = np.nan
                out.append(v)
            return pd.Series(out, index=df.index, dtype=float)
        return pd.Series(np.nan, index=df.index, dtype=float)

    def _s(df):
        s = _comp(df, "run", "post_pipeline_value")
        if s.isna().all():
            s = _comp(df, "run", "last_history_value")
        return s

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            reg = df["regime"].astype(str).values
            s = _s(df).values
            active = fc != 0
            n_active += int(active.sum())
            # expected side: the graded 30-day value's shape g(s) = 6s - 10 sign(s)(|s|/10)^3
            with np.errstate(invalid="ignore"):
                g = 6.0 * s - 10.0 * np.sign(s) * (np.abs(s) / 10.0) ** 3
            exp_side = np.sign(g)
            ok = active & (reg == "trending") & np.isfinite(s) & (np.sign(fc) == exp_side) & (exp_side != 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of 10-bar excess forward return on forecast (trending grid bars)"
    main_thr = "confirm needs t >= 2 (with check negative, t <= -2); reject if t <= -2 (or check positive, t >= +2)"
    check_name = "mean excess return s>=14 minus 8<=s<14 (Welch t)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of active bars are trending-regime bars whose forecast sign matches the "
                          "graded 30-day value's shape, so the config does not do what the Fidelity says.",
            "reading": "Situation taken as regime == 'trending' (the detector's ma200 > 0 decision, not recorded raw) "
                       "and expected side as the sign of 6s - 10 sign(s)(|s|/10)^3 with s = run's standardised value.",
        }

    # ---------- main measure ----------
    xs, ys, ss = [], [], []
    for coin, wins in bars.items():
        all_rets = []
        cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            reg = df["regime"].astype(str).values
            s = _s(df).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                if reg[i] == "trending":
                    cases.append((fc[i], r, s[i]))
        if len(all_rets) == 0:
            continue
        mu = float(np.mean(all_rets))
        for f, r, sv in cases:
            if np.isfinite(f):
                xs.append(float(f))
                ys.append(r - mu)
                ss.append(float(sv) if np.isfinite(sv) else np.nan)

    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    s_arr = np.array(ss, dtype=float)
    n_main = int(len(x))

    slope, t_main = None, None
    if n_main >= 3 and np.var(x) > 0:
        xm, ym = x.mean(), y.mean()
        sxx = np.sum((x - xm) ** 2)
        b = np.sum((x - xm) * (y - ym)) / sxx
        a = ym - b * xm
        resid = y - a - b * x
        se = np.sqrt(np.sum(resid ** 2) / (n_main - 2) / sxx)
        slope = float(b)
        t_main = float(b / se) if se > 0 else None

    # ---------- supporting check ----------
    hi = y[np.isfinite(s_arr) & (s_arr >= 14)]
    mid = y[np.isfinite(s_arr) & (s_arr >= 8) & (s_arr < 14)]
    n_hi, n_mid = int(len(hi)), int(len(mid))
    diff, t_chk = None, None
    if n_hi >= 2 and n_mid >= 2:
        diff = float(hi.mean() - mid.mean())
        tt = stats.ttest_ind(hi, mid, equal_var=False).statistic
        t_chk = float(tt) if np.isfinite(tt) else None

    counts = {"non-overlapping cases (main)": n_main,
              "cases with s >= 14": n_hi,
              "cases with 8 <= s < 14": n_mid}

    reading = ("Situation is regime == 'trending' and expected side is the sign of the graded shape of s "
               "(run's standardised value); the coin's mean 10-bar return is taken over all grid bars of all its "
               "windows; a tier below 20 cases is treated as a minimum count not reached (not observable).")

    chk_passed = None
    if diff is not None and t_chk is not None and n_hi >= 20 and n_mid >= 20:
        chk_passed = bool(diff < 0 and t_chk <= -2)

    result = {
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": t_main} if t_main is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": check_name, "value": diff, "passed": chk_passed,
                             "t": t_chk} if True else None,
        "counts": counts,
        "reading": reading,
    }
    # keep only plain types in supporting_check
    result["supporting_check"] = {"name": check_name + (f" (t={t_chk:.3f})" if t_chk is not None else ""),
                                  "value": diff, "passed": chk_passed}

    if n_main < 100:
        result["status"] = "not observable"
        result["decided_by"] = f"The main measure needs at least 100 non-overlapping cases; only {n_main} were found."
        return result
    if n_hi < 20 or n_mid < 20:
        result["status"] = "not observable"
        result["decided_by"] = (f"The check needs at least 20 cases in each tier; found {n_hi} (s >= 14) "
                                f"and {n_mid} (8 <= s < 14).")
        return result
    if t_main is None or t_chk is None:
        result["status"] = "inconclusive"
        result["decided_by"] = "A t-statistic could not be computed, so neither the confirm nor the reject rule is met."
        return result

    if t_main <= -2 or (diff > 0 and t_chk >= 2):
        result["status"] = "rejected"
        if t_main <= -2:
            result["decided_by"] = "Reject rule: the main slope has t <= -2."
        else:
            result["decided_by"] = "Reject rule: the supporting check is positive with t >= +2 (extreme runs followed by larger rises)."
    elif t_main >= 2 and diff < 0 and t_chk <= -2:
        result["status"] = "confirmed"
        result["decided_by"] = "Confirm rule: the main slope has t >= 2 and the supporting check is negative with t <= -2."
    else:
        result["status"] = "inconclusive"
        result["decided_by"] = ("Inconclusive rule: enough cases, but neither confirm (slope t >= 2 with check t <= -2) "
                                "nor reject (slope t <= -2 or check t >= +2) holds.")
    return result
