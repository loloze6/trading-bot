import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.sma_cross.last_history_value"
    NW_LAGS = 10

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or RAW not in df.columns:
                continue
            sub = df[["forecast", RAW]].dropna()
            act = sub["forecast"] != 0
            n_active += int(act.sum())
            # situation: 50-day SMA above 200-day SMA (raw spread > 0), expected side long
            n_agree += int(((sub[RAW] > 0) & (sub["forecast"] > 0) & act).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation is the 50-day SMA above the 200-day SMA (raw spread > 0) with a long position, "
                           "but fewer than 90% of the bars with a non-zero forecast are such long bars: the standardised and clipped "
                           "forecast does not follow the sign of the SMA spread."),
            "reading": "The situation is read as the component's raw last_history_value (the SMA spread) being above zero, on the long side.",
        }

    # ---------- 2. build pooled data ----------
    groups = []  # per coin-window: (coin, returns array, indicator array)
    n_spans = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "close" not in df.columns or "forecast" not in df.columns:
                continue
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            if len(close) < 2:
                continue
            r = close[1:] / close[:-1] - 1.0
            f = fc[:-1]
            ok = np.isfinite(r) & np.isfinite(f)
            r = r[ok]
            f = f[ok]
            if len(r) == 0:
                continue
            ind = (f > 0).astype(float)
            # distinct spans: runs of consecutive positive-forecast bars within the window
            if len(ind) > 0:
                starts = (ind[0] == 1) + int(np.sum((ind[1:] == 1) & (ind[:-1] == 0)))
                n_spans += int(starts)
            groups.append((coin, r, ind))

    if not groups:
        return {
            "status": "inconclusive",
            "situation_check": {"agreement": agreement, "passed": passed},
            "main_measure": {"name": "excess mean next-bar return while forecast > 0 vs all bars", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirms, t <= -2 rejects (Newey-West, 10 lags)"},
            "supporting_check": None,
            "counts": {"distinct up-cross spans": 0, "bars with a positive forecast": 0},
            "decided_by": "No usable bars, so the plan's minimum counts are not met.",
            "reading": "none",
        }

    r_all = np.concatenate([g[1] for g in groups])
    i_all = np.concatenate([g[2] for g in groups])
    n_pos = int(i_all.sum())
    N = len(r_all)

    excess = None
    t_stat = None
    if n_pos > 0 and n_pos < N:
        excess = float(r_all[i_all == 1].mean() - r_all.mean())
        # regression r = a + b*I ; excess = b*(1-p); t of excess = t of b (p treated as fixed)
        X = np.column_stack([np.ones(N), i_all])
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ (X.T @ r_all)
        u = r_all - X @ beta
        S = np.zeros((2, 2))
        pos = 0
        for coin, r, ind in groups:
            n = len(r)
            Xg = X[pos:pos + n]
            ug = u[pos:pos + n]
            pos += n
            sg = Xg * ug[:, None]
            S += sg.T @ sg
            for L in range(1, min(NW_LAGS, n - 1) + 1):
                wgt = 1.0 - L / (NW_LAGS + 1.0)
                G = sg[L:].T @ sg[:-L]
                S += wgt * (G + G.T)
        V = XtX_inv @ S @ XtX_inv
        se_b = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        t_stat = float(beta[1] / se_b) if np.isfinite(se_b) and se_b > 0 else None

    # ---------- supporting check: binomial z with per-coin baselines ----------
    obs_up = 0.0
    exp_up = 0.0
    var_up = 0.0
    n_act_tot = 0
    up_all_tot = 0
    for coin in sorted(set(g[0] for g in groups)):
        rc = np.concatenate([g[1] for g in groups if g[0] == coin])
        ic = np.concatenate([g[2] for g in groups if g[0] == coin])
        pc = float(np.mean(rc > 0))
        na = int(ic.sum())
        obs_up += float(np.sum((rc > 0) & (ic == 1)))
        exp_up += na * pc
        var_up += na * pc * (1 - pc)
        n_act_tot += na
        up_all_tot += int(np.sum(rc > 0))
    z = float((obs_up - exp_up) / np.sqrt(var_up)) if var_up > 0 else None
    share_diff = (float(obs_up / n_act_tot - up_all_tot / N) if n_act_tot > 0 else None)
    z_passed = None if z is None else bool(z >= 2)

    counts = {"distinct up-cross spans": int(n_spans), "bars with a positive forecast": int(n_pos)}

    # ---------- decision ----------
    if n_spans < 30 or n_pos < 1000:
        status = "inconclusive"
        decided = "Fewer than 30 distinct up-cross spans or fewer than 1000 bars with a positive forecast, which the plan calls inconclusive."
    elif excess is None or t_stat is None:
        status = "inconclusive"
        decided = "The excess return or its t-statistic could not be computed, so no verdict is reached."
    elif excess > 0 and t_stat >= 2 and z is not None and z >= 2:
        status = "confirmed"
        decided = "The excess mean return is above 0 with t >= 2 and the up-bar share is higher with z >= 2, meeting the confirm rule."
    elif excess < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The excess mean return is below 0 with t <= -2, meeting the reject rule (returns in cross spans below holding)."
    elif excess > 0 and t_stat >= 2:
        status = "inconclusive"
        decided = "The excess mean return is above 0 with t >= 2, but the up-bar share z is below 2, so the confirm rule is not fully met."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "excess mean next-bar return while forecast > 0 vs all bars (pooled)",
            "value": excess,
            "statistic": None if t_stat is None else {"name": "Newey-West t (10 lags)", "value": t_stat},
            "threshold": "excess > 0 with t >= 2 confirms; excess < 0 with t <= -2 rejects",
        },
        "supporting_check": {
            "name": "binomial z of up-bar share while forecast > 0 vs per-coin baseline",
            "value": z,
            "passed": z_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The situation is the raw SMA spread above 0 on the long side; the Newey-West t is the t of the slope in a regression of "
                    "next-bar return on a forecast>0 indicator with lag sums kept within each coin-window; an up bar is a positive next-bar return; "
                    "a span is a run of consecutive positive-forecast bars within one window; and confirmation requires both t >= 2 and z >= 2."),
    }
