import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.high_prox.last_history_value"
    PPV = "debug_info.components.high_prox.post_pipeline_value"
    MIN_CASES = 300

    # ---------- 1. Situation check ----------
    # Situation: graded proximity of close to its 90-day closing high, high included:
    # raw proximity 1/(1+D) is defined, in (0, 1]. Expected side: long (outcome is a rise).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            in_situation = raw.notna() & np.isfinite(raw) & (raw > 0) & (raw <= 1.0 + 1e-9)
            on_side = fc > 0
            n_active += int(active.sum())
            n_agree += int((active & in_situation & on_side).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are long bars where the close's proximity to its "
                           "90-day closing high is defined (the plan's graded, always-long situation)."),
            "reading": "Situation taken as a valid raw proximity in (0, 1] with a positive forecast.",
        }

    # ---------- 2. Main measure ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # normal drift: mean 5-bar return on the non-overlapping grids of all the coin's windows
        grid_rets = []
        per_window = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if PPV in df.columns:
                x = pd.to_numeric(df[PPV], errors="coerce").to_numpy(dtype=float)
            else:
                x = np.full(len(df), np.nan)
            n = len(close)
            for i in range(0, n, H):
                if i + H < n:
                    r = close[i + H] / close[i] - 1.0
                    if np.isfinite(r):
                        grid_rets.append(r)
                        per_window.append((r, x[i]))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for r, xv in per_window:
            if np.isfinite(xv):
                xs.append(xv)
                ys.append(r - drift)
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    n_cases = int(len(xs))

    slope, t_val = None, None
    if n_cases >= 3 and np.var(xs) > 0:
        lr = stats.linregress(xs, ys)
        slope = float(lr.slope)
        t_val = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- 3. Supporting check: timing gain before costs ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_parts = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            pos = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").to_numpy(dtype=float)
            ts = pd.to_datetime(df["timestamp"], utc=True).to_numpy()
            r = close[1:] / close[:-1] - 1.0
            p = pos[:-1]
            ok = np.isfinite(r)
            coin_rets.extend(r[ok].tolist())
            ok2 = ok & np.isfinite(p)
            for tt, pp, rr in zip(ts[1:][ok2], p[ok2], r[ok2]):
                coin_parts.append((tt, pp, rr))
        if len(coin_rets) == 0:
            continue
        mu = float(np.mean(coin_rets))
        for tt, pp, rr in coin_parts:
            rows.append((tt, coin, pp * rr, pp * mu))
    timing = None
    if rows:
        d = pd.DataFrame(rows, columns=["day", "coin", "gain", "market"])
        d["day"] = pd.to_datetime(d["day"], utc=True).dt.floor("D")
        daily = d.groupby("day")[["gain", "market"]].mean()
        timing = float(daily["gain"].mean() - daily["market"].mean())
    timing_passed = None if timing is None else bool(timing > 0)

    # ---------- 4. Decision ----------
    if n_cases < MIN_CASES or t_val is None:
        status = "not observable"
        decided_by = f"Fewer than {MIN_CASES} grid cases ({n_cases}), the plan's minimum count, so the data cannot show the idea."
    elif t_val >= 2 and timing_passed:
        status = "confirmed"
        decided_by = "The slope's t is 2 or more over at least 300 cases and the timing gain before costs is above 0."
    elif t_val <= -2:
        status = "rejected"
        decided_by = "The slope's t is -2 or less over at least 300 cases: nearer the high is followed by smaller 5-day returns."
    elif t_val >= 2:
        status = "inconclusive"
        decided_by = "The slope's t is 2 or more but the timing gain before costs is 0 or below."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2 and 2 over at least 300 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "OLS slope of 5-bar forward return minus normal drift on post_pipeline_value",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_val} if t_val is not None else None,
            "threshold": "t >= 2 over at least 300 cases confirms (with timing gain > 0); t <= -2 over at least 300 cases rejects",
        },
        "supporting_check": {
            "name": "timing gain before costs (mean daily book return minus position x coin mean daily return)",
            "value": timing,
            "passed": timing_passed,
        },
        "counts": {"grid cases": n_cases},
        "decided_by": decided_by,
        "reading": ("Slope is an OLS with intercept on grid bars 0,5,10,... of each window (pooled), normal drift is each coin's mean "
                    "grid 5-bar return over all its windows, and the timing gain uses each bar as a day, the book's daily return being "
                    "the mean over coins of position x next-bar return."),
    }
