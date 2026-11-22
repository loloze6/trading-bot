import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    BAND = 2.0
    RG = "debug_info.components.run_gain.last_history_value"
    VF = "debug_info.components.vol_fade.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            prev = np.concatenate([[np.nan], close[:-1]])
            rg = (pd.to_numeric(df[RG], errors="coerce").values
                  if RG in df.columns else np.full(len(df), np.nan))
            up_close = close > prev
            # first row of a window has no previous close: fall back on the raw run gain
            situ = np.where(np.isnan(prev), np.nan_to_num(rg, nan=0.0) > 0, up_close)
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean drift-adjusted 18-bar return of short cases, sign flipped"
    main_thr = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2"
    sup_name = "OLS coefficient of vol_fade (raw) in drift-adjusted 18-bar return ~ run_gain + vol_fade"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases overall": 0, "active bars": n_active},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are up-close bars of a rising streak "
                           "with a short (negative) forecast, as the plan's Fidelity requires."),
            "reading": "The situation is taken as a bar that closed above the previous close (raw run_gain > 0 on a window's first row), on the short side.",
        }

    # ---------- 2. drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                r = c[i + H] / c[i] - 1.0
                if np.isfinite(r):
                    rets.append(r)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    unusual, adj, xrg, xvf = [], [], [], []
    for coin, wins in bars.items():
        d = drift.get(coin, np.nan)
        if not np.isfinite(d):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            rg = (pd.to_numeric(df[RG], errors="coerce").values
                  if RG in df.columns else np.full(len(df), np.nan))
            vf = (pd.to_numeric(df[VF], errors="coerce").values
                  if VF in df.columns else np.full(len(df), np.nan))
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            for i in range(n):
                if f[i] >= 0:
                    ref = 0.0
                    continue
                mag = -f[i]
                if mag - ref >= BAND - 1e-12:
                    bet[i] = True
                    ref = mag
                else:
                    ref = min(ref, mag)
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r):
                    continue
                a = r - d
                unusual.append(-a)
                adj.append(a)
                xrg.append(rg[t])
                xvf.append(vf[t])

    unusual = np.array(unusual, dtype=float)
    n_cases = int(len(unusual))
    mean_u = float(np.mean(unusual)) if n_cases > 0 else None
    t_u = None
    if n_cases > 1:
        sd = float(np.std(unusual, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    # ---------- 4. regression ----------
    adj = np.array(adj, dtype=float)
    xrg = np.array(xrg, dtype=float)
    xvf = np.array(xvf, dtype=float)
    ok = np.isfinite(adj) & np.isfinite(xrg) & np.isfinite(xvf)
    n_reg = int(ok.sum())
    coef_vf, t_vf = None, None
    if n_reg > 3:
        X = np.column_stack([np.ones(n_reg), xrg[ok], xvf[ok]])
        y = adj[ok]
        try:
            XtX_inv = np.linalg.inv(X.T @ X)
            beta = XtX_inv @ X.T @ y
            resid = y - X @ beta
            s2 = float(resid @ resid) / (n_reg - 3)
            se = np.sqrt(np.diag(XtX_inv) * s2)
            coef_vf = float(beta[2])
            t_vf = float(beta[2] / se[2]) if se[2] > 0 else 0.0
        except np.linalg.LinAlgError:
            coef_vf, t_vf = None, None

    sup_passed = None if t_vf is None else bool(t_vf <= -2)
    counts = {"cases overall": n_cases, "cases in regression": n_reg}
    reading = ("A case is the workflow's short bet (forecast at least 2 points more negative than its least-negative "
               "level since the last bet, reset at flat), first one per 18-bar grid cell of each window; the regression "
               "uses the unflipped drift-adjusted return with an intercept and classical OLS t; fewer than 30 cases is "
               "reported as not observable; the situation is an up-close bar on the short side.")

    if n_cases < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases overall ({n_cases}), the plan's minimum."
    elif t_u is None or t_vf is None:
        status = "inconclusive"
        decided = "The main t or the vol_fade coefficient t could not be computed, so neither rule is met."
    elif (mean_u < 0 and t_u <= -2) or (t_vf >= 2):
        status = "rejected"
        decided = "Reject rule met: the main mean is below 0 with t <= -2, or the vol_fade coefficient has t >= +2."
    elif mean_u > 0 and t_u >= 2 and t_vf <= -2:
        status = "confirmed"
        decided = "Confirm rule met: the main mean is above 0 with t >= 2 and the vol_fade coefficient has t <= -2."
    else:
        status = "inconclusive"
        decided = "Neither the confirm nor the reject rule is met: a result in between."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": None if t_u is None else {"name": "t of the mean", "value": t_u},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": coef_vf,
                             "t": t_vf, "passed": sup_passed} if True else None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
