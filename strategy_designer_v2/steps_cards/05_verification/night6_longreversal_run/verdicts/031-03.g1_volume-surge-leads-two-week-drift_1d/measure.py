import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 14
    RAW = "debug_info.components.vol14_vs_30.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: the situation is the 14-day mean volume above or below its 30-day mean.
    # The side is long when volume swelled (log ratio > 0) and short when it dried up (log ratio < 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # Rebuild missing raw values from the window's own volumes where possible.
            vol = pd.to_numeric(df["volume"], errors="coerce")
            m14 = vol.rolling(14, min_periods=14).mean()
            m30 = vol.rolling(30, min_periods=30).mean()
            with np.errstate(divide="ignore", invalid="ignore"):
                rec = np.log(m14 / m30)
            raw = raw.where(raw.notna(), rec)
            active = fc.notna() & (fc != 0) & raw.notna() & np.isfinite(raw)
            n_active += int(active.sum())
            n_agree += int(
                (active & (np.sign(fc) == np.sign(raw)) & (raw != 0)).sum()
            )
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90

    threshold_txt = (
        "confirm: slope t >= 2 with timing gain > 0; reject: t <= -2; "
        "otherwise inconclusive; at least 300 grid cases with non-zero forecast"
    )
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "slope of demeaned 14-bar forward return on forecast",
                "value": None,
                "statistic": None,
                "threshold": threshold_txt,
            },
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": (
                f"Only {agreement:.1%} of active bars are long when the 14/30-day log volume "
                "ratio is positive and short when it is negative (90% needed)."
            ),
            "reading": "none",
        }

    # ---------- 2. Main measure ----------
    # Grid samples per coin: bars 0, 14, 28, ... of each window, return within the window.
    grid = []
    for coin, wins in bars.items():
        rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            for i in range(0, len(df) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rows.append((c[i + H] / c[i] - 1.0, f[i]))
        if not rows:
            continue
        r = np.array([x[0] for x in rows])
        fv = np.array([x[1] for x in rows])
        # The coin's mean 14-bar return over all windows (non-overlapping grid).
        mu = np.mean(r)
        for ri, fi in zip(r, fv):
            if np.isfinite(fi):
                grid.append((ri - mu, fi))

    y = np.array([g[0] for g in grid], dtype=float)
    x = np.array([g[1] for g in grid], dtype=float)
    n_cases = int(len(y))
    n_nonzero = int(np.sum(x != 0))

    slope, t_slope = None, None
    if n_cases >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_slope = (
            float(res.slope / res.stderr)
            if res.stderr and res.stderr > 0
            else None
        )

    # ---------- 3. Supporting check: timing gain ----------
    # The coin's mean daily return over all windows.
    coin_mu = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            rs.append(c[1:] / c[:-1] - 1.0)
        allr = np.concatenate(rs) if rs else np.array([])
        allr = allr[np.isfinite(allr)]
        coin_mu[coin] = float(np.mean(allr)) if len(allr) else np.nan

    recs = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            pos = pd.to_numeric(
                df["postRebalance_current_allocation"], errors="coerce"
            ).values
            ts = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D").values
            for i in range(len(df) - 1):
                r = c[i + 1] / c[i] - 1.0
                if np.isfinite(r) and np.isfinite(pos[i]):
                    recs.append(
                        (ts[i], pos[i] * r, pos[i] * coin_mu[coin])
                    )

    timing = None
    if recs:
        d = pd.DataFrame(recs, columns=["day", "gain", "market"])
        daily = d.groupby("day")[["gain", "market"]].mean()
        timing = float(daily["gain"].mean() - daily["market"].mean())
    timing_pass = None if timing is None else bool(timing > 0)

    # ---------- 4. Decision ----------
    if n_nonzero < 300:
        status = "not observable"
        decided = (
            f"Only {n_nonzero} grid cases with a non-zero forecast, "
            "below the plan's minimum of 300."
        )
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so it meets neither the confirm nor the reject rule."
    elif t_slope >= 2 and timing_pass:
        status = "confirmed"
        decided = "The slope has t >= 2 and the timing gain is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope has t <= -2."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope has t >= 2 but the timing gain is at or below 0."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of the coin's demeaned 14-bar forward return on the forecast",
            "value": slope,
            "statistic": (
                {"name": "OLS slope t", "value": t_slope}
                if t_slope is not None
                else None
            ),
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "timing gain: book mean daily return minus position x coin mean daily return",
            "value": timing,
            "passed": timing_pass,
        },
        "counts": {
            "grid cases with a non-zero forecast": n_nonzero,
            "grid cases": n_cases,
        },
        "decided_by": decided,
        "reading": (
            "The regression is an OLS with intercept over every grid bar of each window "
            "(positions 0, 14, 28, ... with a full 14-bar return inside the window, "
            "zero-forecast bars included), each coin's mean 14-bar return is taken over "
            "those same grid samples of all its windows, and the timing gain averages "
            "the coins per UTC day before averaging over days."
        ),
    }
