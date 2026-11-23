import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.excess_power.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: the raw joint reading (w - wbar) x z, negated (counter-bet) and clipped at 0 (long only).
    # So the situation on its side: raw value < 0 (counter-reading points up), forecast > 0 (long).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw < 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars where the raw joint "
                          "reading (w - wbar) x z is negative, as the plan's negated, long-only counter-bet requires.",
            "reading": "The situation on its side is taken as raw component value < 0 with forecast > 0.",
        }

    # ---------- 2. Criterion ----------
    # Non-overlapping 5-bar grid per window, from its first row.
    rows = []  # (coin, forecast, fwd_return)
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float) \
                if "forecast" in df.columns else np.full(len(df), np.nan)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, fc[i], c1 / c0 - 1.0))

    g = pd.DataFrame(rows, columns=["coin", "forecast", "ret"])
    if len(g) > 0:
        drift = g.groupby("coin")["ret"].mean()
        g["excess"] = g["ret"] - g["coin"].map(drift)
    else:
        g["excess"] = []

    reg = g.dropna(subset=["forecast", "excess"])
    pos = reg[reg["forecast"] > 0]
    n_grid = int(len(reg))
    n_pos = int(len(pos))

    slope = None
    tstat = None
    if n_grid >= 3 and reg["forecast"].nunique() > 1:
        lr = stats.linregress(reg["forecast"].to_numpy(float), reg["excess"].to_numpy(float))
        slope = float(lr.slope)
        if lr.stderr is not None and np.isfinite(lr.stderr) and lr.stderr > 0:
            tstat = float(lr.slope / lr.stderr)

    sup_val = float(pos["excess"].mean()) if n_pos > 0 else None
    sup_pass = (bool(sup_val > 0) if sup_val is not None else None)

    counts = {"grid bars with forecast > 0": n_pos, "grid bars in regression": n_grid}

    if n_pos < 100:
        status = "not observable"
        decided_by = f"The plan's minimum of 100 grid bars with forecast > 0 is not reached ({n_pos})."
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided_by = "The slope or its t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tstat >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "Confirm: the slope is positive with t >= 2 and the mean excess 5-bar return on forecast > 0 grid bars is above 0."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided_by = "Reject: the slope is negative with t <= -2."
    elif slope > 0 and tstat >= 2:
        status = "inconclusive"
        decided_by = "Inconclusive: a confirming slope (positive, t >= 2) whose supporting check fails."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: the slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": passed},
        "main_measure": {
            "name": "pooled OLS slope of next 5-bar return minus coin drift on forecast",
            "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tstat} if tstat is not None else None),
            "threshold": "confirm if slope > 0 with t >= 2 (and supporting check passes); reject if slope < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "mean next 5-bar return minus coin drift on grid bars with forecast > 0, above 0",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": "The coin's normal drift is its mean next 5-bar return over all its grid bars (positions 0, 5, 10, ... of each "
                   "window) pooled across windows, the slope is an OLS with intercept over all grid bars with a forecast, and the "
                   "plan's 'at least 100 grid bars with forecast > 0' minimum is applied as a minimum count giving 'not observable'.",
    }
