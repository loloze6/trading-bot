import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW = "debug_info.components.post_settle_move.last_history_value"

    def _prep(df):
        d = df.copy().reset_index(drop=True)
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
        d["close"] = pd.to_numeric(d["close"], errors="coerce")
        return d

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            d = _prep(df)
            prepared[coin][w] = d
            # raw move: recorded vol-scaled return, else the 1-bar return from prices (same sign)
            price_ret = d["close"] / d["close"].shift(1) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                raw = raw.where(raw.notna(), price_ret)
            else:
                raw = price_ret
            active = d["forecast"] != 0
            situation = d["timestamp"].dt.hour == 0  # bar 00:00-01:00, the coming bar starts at 01:00
            expected_sign = -np.sign(raw)  # against the move
            ok = situation & (np.sign(d["forecast"]) == expected_sign) & (expected_sign != 0)
            n_active += int(active.sum())
            n_agree += int((active & ok).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the non-zero-forecast bars are the 00:00-01:00 UTC bar with a forecast "
                           "against that hour's move, as the Fidelity's situation and side require."),
            "reading": "The situation bar is the bar starting at 00:00 UTC (closing at 01:00), the side is opposite the sign of its vol-scaled 1-hour return.",
        }

    # ---------- 2. criterion ----------
    fc_all, ex_all = [], []
    for coin, wins in prepared.items():
        # coin's normal 24-bar drift: non-overlapping grid of each window, pooled over all windows
        grid_rets = []
        for w, d in wins.items():
            c = d["close"].values
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                grid_rets.append(r[np.isfinite(r)])
        if not grid_rets:
            continue
        gr = np.concatenate(grid_rets)
        if len(gr) == 0:
            continue
        drift = float(np.mean(gr))

        for w, d in wins.items():
            c = d["close"].values
            sig = (d["regime"].astype(str) == "mean_reversion") & (d["forecast"] != 0)
            pos = np.where(sig.values)[0]
            if len(pos) == 0:
                continue
            days = d["timestamp"].dt.floor("D").values[pos]
            _, first = np.unique(days, return_index=True)
            pos = pos[np.sort(first)]
            pos = pos[pos + H < len(c)]
            if len(pos) == 0:
                continue
            fwd = c[pos + H] / c[pos] - 1.0
            f = d["forecast"].values[pos]
            m = np.isfinite(fwd) & np.isfinite(f)
            fc_all.append(f[m])
            ex_all.append(fwd[m] - drift)

    fc = np.concatenate(fc_all) if fc_all else np.array([])
    ex = np.concatenate(ex_all) if ex_all else np.array([])
    n_cases = int(len(fc))
    big = np.abs(fc) >= 10
    n_big = int(big.sum())

    slope, t = None, None
    if n_cases >= 3 and np.std(fc) > 0:
        lr = stats.linregress(fc, ex)
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr > 0 else None

    supp = float(np.mean(np.sign(fc[big]) * ex[big])) if n_big > 0 else None
    supp_pass = (supp > 0) if supp is not None else None

    counts = {"cases pooled over coins and windows": n_cases, "cases with |forecast| >= 10": n_big}

    if n_cases < 500:
        status = "not observable"
        decided = f"Fewer than 500 pooled cases ({n_cases})."
    elif n_big < 100:
        status = "not observable"
        decided = f"Fewer than 100 cases with |forecast| >= 10 ({n_big})."
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed."
    elif slope > 0 and t >= 2 and supp_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2 and the mean signed drift-adjusted return over |forecast| >= 10 is above 0."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope has t >= 2 but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "pooled OLS slope of drift-adjusted 24-bar return on forecast",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
            "threshold": "confirm: slope > 0 with t >= 2 (and supporting check > 0); reject: slope < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "mean sign(forecast) x drift-adjusted 24-bar return, |forecast| >= 10",
            "value": supp,
            "passed": supp_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are the first mean_reversion bar with non-zero forecast per coin per UTC day, the forward return is "
                    "close 24 rows later in the same window, the drift is the coin's mean 24-bar return on each window's "
                    "non-overlapping grid pooled over all windows, and the slope is from an OLS with intercept."),
    }
