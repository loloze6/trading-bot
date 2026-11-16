import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    LHV = "debug_info.components.above_sma200.last_history_value"

    # ---------- 1. Situation check: close above SMA200 (raw distance > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns or LHV not in df.columns:
                continue
            d = df[["forecast", LHV]].dropna()
            act = d["forecast"] != 0
            n_active += int(act.sum())
            n_agree += int((act & (d[LHV] > 0) & (d["forecast"] > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed_sit = bool(n_active > 0 and agreement >= 0.90)

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "OLS slope of demeaned forward 24-bar return on forecast",
                "value": None,
                "statistic": None,
                "threshold": "confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2",
            },
            "supporting_check": None,
            "counts": {"active_bars": int(n_active)},
            "decided_by": (
                "Fewer than 90% of active bars (forecast != 0) are bars where the close is above "
                "its 200-bar SMA with a long forecast, so the config does not follow the plan's situation."
                if n_active > 0 else
                "No active bars: the config never takes the plan's long position while above the SMA200."
            ),
            "reading": "Situation taken as raw percent distance from SMA200 > 0 with forecast > 0.",
        }

    # ---------- 2. Criterion ----------
    xs, ys, fwd_all, fc_all = [], [], [], []
    windows_with_pos = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            close = df["close"].to_numpy(dtype=float)
            fc = df["forecast"].to_numpy(dtype=float)
            n = len(df)
            idx = np.arange(0, n - H, H)  # grid 0, 24, 48, ... with a full forward window
            idx = idx[idx + H < n]
            if len(idx) == 0:
                continue
            fwd = close[idx + H] / close[idx] - 1.0
            f = fc[idx]
            ok = np.isfinite(fwd) & np.isfinite(f)
            fwd, f = fwd[ok], f[ok]
            if len(fwd) == 0:
                continue
            dm = fwd - fwd.mean()
            xs.append(f)
            ys.append(dm)
            fwd_all.append(fwd)
            fc_all.append(f)
            if (f > 0).sum() > 0:
                windows_with_pos += 1

    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    fwd = np.concatenate(fwd_all) if fwd_all else np.array([])
    f = np.concatenate(fc_all) if fc_all else np.array([])

    n_pos = int((f > 0).sum())
    n_sampled = int(len(f))

    slope, tstat = None, None
    if len(x) >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tstat = float(lr.slope / lr.stderr) if lr.stderr > 0 else None

    # supporting check: two-proportion z, share positive among forecast>0 vs all sampled
    z, sup_passed, diff = None, None, None
    if n_pos > 0 and n_sampled > 0:
        p1 = float((fwd[f > 0] > 0).mean())
        p2 = float((fwd > 0).mean())
        pp = ((fwd[f > 0] > 0).sum() + (fwd > 0).sum()) / (n_pos + n_sampled)
        se = np.sqrt(pp * (1 - pp) * (1.0 / n_pos + 1.0 / n_sampled))
        diff = p1 - p2
        if se > 0:
            z = float(diff / se)
            sup_passed = bool(z >= 1.96)

    # decision
    if n_pos < 150 or windows_with_pos < 3:
        status = "inconclusive"
        decided_by = (f"Inconclusive: {n_pos} pooled non-overlapping sampled cases with forecast > 0 "
                      f"(minimum 150) and {windows_with_pos} of 6 windows with such cases (minimum 3).")
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided_by = "Inconclusive: the slope's t-statistic could not be computed."
    elif slope > 0 and tstat >= 2:
        status = "confirmed"
        decided_by = "Confirm: the slope is positive with t >= 2."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided_by = "Reject: the slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed_sit},
        "main_measure": {
            "name": "OLS slope of forward 24-bar return minus window mean, on forecast",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": tstat} if tstat is not None else None,
            "threshold": "confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; otherwise inconclusive",
        },
        "supporting_check": {
            "name": "two-proportion z: share of positive 24-bar returns, forecast > 0 vs all sampled bars",
            "value": z,
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping sampled cases with forecast > 0 pooled": n_pos,
            "windows containing such cases": int(windows_with_pos),
            "sampled bars": n_sampled,
        },
        "decided_by": decided_by,
        "reading": ("The window's mean 24-bar return is taken as the mean forward 24-bar return over that window's "
                    "non-overlapping sampled bars (grid 0, 24, 48, ... with a full forward window), the slope's t is "
                    "the OLS t on the pooled samples, and the supporting check, which has no threshold in the plan, "
                    "counts as passed when z >= 1.96."),
    }
