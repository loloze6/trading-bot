import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    COMP = "debug_info.components.power_reversal.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: the situation is an upward reversal reading, and the outcome is a rise, so the side is long.
    # The pipeline is standardise (scales, keeps the sign), then negate, then clip at 0.
    # So the reversal points up when the raw component value is below 0.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[COMP], errors="coerce") if COMP in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            ok = active & raw.notna() & (raw < 0) & (f > 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are long bars with a raw reversal reading below 0 "
                           "(negated, an upward reversal), so the forecast does not follow the plan's situation and side."
                           if n_active > 0 else "The record has no active bars, so the forecast never takes the plan's situation."),
            "reading": "The situation is a raw component value below 0, because standardise keeps the sign and the negate turns it positive; the side is long.",
        }

    # ---------- 2. Main measure ----------
    # Non-overlapping 5-bar grid per window; the normal drift is the coin's mean grid return over all its windows.
    cells = []   # rows of (coin, forecast, return)
    drift_samples = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(c)
            for i in range(0, n - H, H):
                if i + H >= n:
                    break
                c0, c1 = c[i], c[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                if np.isfinite(f[i]) and f[i] > 0:
                    cells.append((coin, f[i], r))
        drift_samples[coin] = float(np.mean(allr)) if len(allr) else np.nan

    xs, ws = [], []
    for coin, fv, r in cells:
        d = drift_samples.get(coin, np.nan)
        if np.isfinite(d):
            xs.append(r - d)
            ws.append(fv)
    xs = np.asarray(xs, dtype=float)
    ws = np.asarray(ws, dtype=float)
    n_cells = int(len(xs))

    wmean = None
    tval = None
    if n_cells >= 2 and ws.sum() > 0:
        m = float(np.sum(ws * xs) / np.sum(ws))
        se = np.sqrt(np.sum(ws ** 2 * (xs - m) ** 2)) / np.sum(ws) * np.sqrt(n_cells / (n_cells - 1))
        wmean = m
        tval = float(m / se) if se > 0 else (0.0 if m == 0 else float(np.sign(m) * np.inf))
    elif n_cells == 1:
        wmean = float(xs[0])

    # ---------- 3. Supporting check: the book's mean daily timing gain ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce")
            rs.append((c / c.shift(1) - 1.0).dropna())
        allr = pd.concat(rs) if rs else pd.Series(dtype=float)
        coin_mu[coin] = float(allr.mean()) if len(allr) else np.nan

    book_rows = []
    for coin, wins in bars.items():
        mu = coin_mu.get(coin, np.nan)
        for w, df in wins.items():
            d = df.copy()
            d["_ts"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            d = d.dropna(subset=["_ts"])
            d["_day"] = d["_ts"].dt.floor("D")
            last = d.groupby("_day").tail(1).sort_values("_ts")
            v = pd.to_numeric(last["postRebalance_total_value"], errors="coerce").to_numpy(dtype=float)
            a = pd.to_numeric(last["postRebalance_current_allocation"], errors="coerce").to_numpy(dtype=float)
            days = last["_day"].to_numpy()
            for k in range(1, len(v)):
                if np.isfinite(v[k]) and np.isfinite(v[k - 1]) and v[k - 1] != 0:
                    br = v[k] / v[k - 1] - 1.0
                    mg = a[k - 1] * mu if (np.isfinite(a[k - 1]) and np.isfinite(mu)) else np.nan
                    book_rows.append((days[k], br, mg))

    timing = None
    sup_passed = None
    if book_rows:
        bd = pd.DataFrame(book_rows, columns=["day", "book", "mkt"])
        daily = bd.groupby("day").agg(book=("book", "mean"), mkt=("mkt", "mean"))
        bmean = daily["book"].mean()
        mmean = daily["mkt"].dropna().mean()
        if np.isfinite(bmean) and np.isfinite(mmean):
            timing = float(bmean - mmean)
            sup_passed = bool(timing > 0)

    # ---------- 4. Decision ----------
    if n_cells < 100:
        status = "not observable"
        decided_by = f"Only {n_cells} grid cells have forecast > 0 over all coins and windows, below the plan's minimum of 100."
    elif tval is None or wmean is None:
        status = "inconclusive"
        decided_by = "The t of the weighted mean could not be computed."
    elif wmean > 0 and tval >= 2:
        if sup_passed:
            status = "confirmed"
            decided_by = "The forecast-weighted mean excess 5-bar return is above 0 with t >= 2, and the book's mean daily timing gain is above 0."
        else:
            status = "inconclusive"
            decided_by = "The t is confirming (mean > 0, t >= 2), but the supporting check failed (timing gain not above 0), which the plan rules inconclusive."
    elif wmean < 0 and tval <= -2:
        status = "rejected"
        decided_by = "The forecast-weighted mean excess 5-bar return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided_by = "The t lies between -2 and 2 (or its sign disagrees with the mean), which the plan rules inconclusive."

    def _num(x):
        if x is None:
            return None
        x = float(x)
        return x if np.isfinite(x) else (1e308 if x > 0 else -1e308)

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "forecast-weighted mean excess 5-bar return on forecast>0 grid cells",
            "value": _num(wmean),
            "statistic": {"name": "t of the weighted mean", "value": _num(tval)} if tval is not None else None,
            "threshold": "confirm if mean > 0 with t >= 2 (and timing gain > 0); reject if mean < 0 with t <= -2; at least 100 cells",
        },
        "supporting_check": {
            "name": "book mean daily timing gain > 0",
            "value": _num(timing),
            "passed": sup_passed,
        },
        "counts": {"grid cells with forecast > 0": n_cells},
        "decided_by": decided_by,
        "reading": ("The normal drift is the coin's mean return over the non-overlapping 5-bar grid of all its windows. "
                    "The t of the weighted mean uses the weighted (sandwich) standard error with an n/(n-1) correction. "
                    "The plan's 'below 100 cells' rule is reported as not observable. "
                    "The market gain on day t uses the allocation held after day t-1's trade times the coin's mean daily close return over all windows."),
    }
