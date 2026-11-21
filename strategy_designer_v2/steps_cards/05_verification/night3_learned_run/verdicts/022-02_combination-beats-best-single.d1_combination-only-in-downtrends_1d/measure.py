import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.combo.last_history_value"
    POST = "debug_info.components.combo.post_pipeline_value"
    Z_WIN = 365
    CORR_LB = 365

    def fnum(x):
        if x is None:
            return None
        try:
            x = float(x)
        except Exception:
            return None
        return None if not np.isfinite(x) else x

    def ret90_series(df):
        c = df["close"].astype(float).reset_index(drop=True)
        return c / c.shift(90) - 1.0

    def best_composite(df):
        # Rebuild the "best"-weighting composite from prices inside one window, with the
        # config's settings (z over 365 bars, correlation over the past 365 bars); full windows required.
        c = df["close"].astype(float).reset_index(drop=True)
        hi = df["high"].astype(float).reset_index(drop=True)
        r1 = c.pct_change()
        sigs = {
            "ret28": c / c.shift(28) - 1.0,
            "rev1": -(c / c.shift(1) - 1.0),
            "high90": c / hi.rolling(90, min_periods=90).max() - 1.0,
            "negvol30": -r1.rolling(30, min_periods=30).std(),
        }
        fwd = c.shift(-H) / c - 1.0
        fwd_known = fwd.shift(H)  # forward return from t-5 to t: known at t
        zs, cs = {}, {}
        for k, s in sigs.items():
            m = s.rolling(Z_WIN, min_periods=Z_WIN).mean()
            sd = s.rolling(Z_WIN, min_periods=Z_WIN).std()
            z = (s - m) / sd.replace(0, np.nan)
            zs[k] = z
            zl = z.shift(H)
            cs[k] = zl.rolling(CORR_LB, min_periods=CORR_LB).corr(fwd_known)
        Z = pd.DataFrame(zs)
        C = pd.DataFrame(cs)
        out = pd.Series(np.nan, index=c.index)
        absC = C.abs()
        valid = absC.notna().all(axis=1) & Z.notna().all(axis=1)
        for i in np.where(valid.values)[0]:
            k = absC.iloc[i].idxmax()
            out.iloc[i] = np.sign(C[k].iloc[i]) * Z[k].iloc[i]
        return out

    # ---------- 1. situation check ----------
    n_active, n_agree = 0, 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce")
            r90 = ret90_series(df)
            reg = df["regime"].astype(str) == "mean_reversion"
            sit = np.where(r90.notna(), r90 < 0, reg)
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            side_ok = (np.sign(f) == np.sign(raw)) & raw.notna() & (raw != 0)
            n_active += int(active.sum())
            n_agree += int((active & pd.Series(sit, index=df.index).astype(bool) & side_ok).sum())
    agreement = n_agree / n_active if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    reading = ("The expected side is the sign of the combined score (forecast sign = sign of combo's raw value); the 90-day "
               "return is close[t]/close[t-90]-1 inside the window, with the recorded regime used where the window has fewer "
               "than 90 prior bars; 'best' weighting = the z-scored signal with the largest absolute past 365-bar correlation "
               "to the 5-bar forward return, signed by that correlation, needing full 365-bar windows inside one window; "
               "standard deviations use ddof=1 over the cases used; the deeper half is 90-day return below the median, the "
               "shallower half at or above it; cases with any missing value are left out.")

    mm_name = "t of mean of (zc - zb) x r on decline grid cases"
    mm_thr = "t >= 2 confirms (with supporting check), t <= -2 rejects, otherwise inconclusive; at least 100 grid cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": mm_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "grid cases on decline bars": None},
            "decided_by": ("Fewer than 90% of active bars are negative-90-day-return bars with the forecast on the side of "
                           "the combined score, so the config does not do what the Fidelity's situation says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin mean 5-bar return over all windows (non-overlapping grid)
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            fwd = c.shift(-H) / c - 1.0
            g = fwd.iloc[::H].dropna()
            rets.extend(g.tolist())
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            fwd = c.shift(-H) / c - 1.0
            r90 = ret90_series(df)
            zb_raw = best_composite(df)
            post = pd.to_numeric(df[POST], errors="coerce") if POST in df.columns else pd.Series(np.nan, index=df.index)
            reg = df["regime"].astype(str) == "mean_reversion"
            for i in range(0, len(df), H):
                if not reg.iloc[i]:
                    continue
                rows.append({
                    "r": fwd.iloc[i] - coin_mean[coin],
                    "zc": post.iloc[i],
                    "zb": zb_raw.iloc[i],
                    "r90": r90.iloc[i],
                })
    cases = pd.DataFrame(rows, columns=["r", "zc", "zb", "r90"])
    cases = cases.dropna(subset=["r", "zc", "zb"])
    n = int(len(cases))
    counts = {"grid cases on decline bars": n}

    if n < 100:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": mm_thr},
            "supporting_check": {"name": "deeper-half mean minus shallower-half mean of (zc - zb) x r",
                                 "value": None, "passed": None},
            "counts": counts,
            "decided_by": ("Fewer than 100 grid cases on decline bars with both scores and the forward return "
                           "(the best-single composite needs 365-bar histories inside a window), so the plan's minimum is not reached."),
            "reading": reading,
        }

    sdc = cases["zc"].std(ddof=1)
    sdb = cases["zb"].std(ddof=1)
    zc = cases["zc"] / sdc if sdc > 0 else cases["zc"] * np.nan
    zb = cases["zb"] / sdb if sdb > 0 else cases["zb"] * np.nan
    v = ((zc - zb) * cases["r"]).astype(float)
    cases = cases.assign(v=v).dropna(subset=["v"])
    vv = cases["v"].values
    mean_v = float(np.mean(vv)) if len(vv) else np.nan
    sd_v = float(np.std(vv, ddof=1)) if len(vv) > 1 else np.nan
    t = mean_v / (sd_v / np.sqrt(len(vv))) if (len(vv) > 1 and sd_v > 0) else np.nan

    sc = cases.dropna(subset=["r90"])
    sup_val, sup_pass = None, None
    if len(sc) >= 2:
        med = sc["r90"].median()
        deep = sc.loc[sc["r90"] < med, "v"]
        shal = sc.loc[sc["r90"] >= med, "v"]
        counts["deeper half cases"] = int(len(deep))
        counts["shallower half cases"] = int(len(shal))
        if len(deep) > 0 and len(shal) > 0:
            sup_val = float(deep.mean() - shal.mean())
            sup_pass = bool(sup_val > 0)

    tt = fnum(t)
    if tt is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed, which meets neither the confirm nor the reject rule."
    elif tt >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The main measure's t is 2 or more and the deeper half exceeds the shallower half."
    elif tt >= 2:
        status = "inconclusive"
        decided = "The t is 2 or more but the deeper half does not exceed the shallower half, which the plan calls inconclusive."
    elif tt <= -2:
        status = "rejected"
        decided = "The main measure's t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The main measure's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": mm_name, "value": fnum(mean_v),
                         "statistic": {"name": "t of the mean", "value": tt},
                         "threshold": mm_thr},
        "supporting_check": {"name": "deeper-half mean minus shallower-half mean of (zc - zb) x r",
                             "value": fnum(sup_val), "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
