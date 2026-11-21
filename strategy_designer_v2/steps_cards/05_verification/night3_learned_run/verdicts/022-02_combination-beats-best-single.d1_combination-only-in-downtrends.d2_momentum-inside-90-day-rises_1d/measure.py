import numpy as np
import pandas as pd

H = 5
MOM_RAW = "debug_info.components.mom28.last_history_value"
MOM_POST = "debug_info.components.mom28.post_pipeline_value"


def _ols(x, y):
    """Pooled least-squares slope with intercept, and its ordinary t."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n = len(x)
    if n < 3:
        return None, None
    xm = x.mean()
    sxx = ((x - xm) ** 2).sum()
    if sxx <= 0:
        return None, None
    slope = ((x - xm) * (y - y.mean())).sum() / sxx
    intercept = y.mean() - slope * xm
    resid = y - intercept - slope * x
    s2 = (resid ** 2).sum() / (n - 2)
    se = np.sqrt(s2 / sxx)
    t = slope / se if se > 0 else None
    return float(slope), (float(t) if t is not None else None)


def measure(bars):
    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float)

            # 90-day return from prices, inside the window; the regime is the
            # detector's recorded decision where 90 earlier bars are not there.
            ret90 = close / close.shift(90) - 1.0
            reg_trend = df["regime"].astype(str) == "trending"
            in_sit = pd.Series(
                np.where(ret90.notna(), ret90 > 0, reg_trend), index=df.index
            )

            # 28-day return: the recorded raw value, else from prices.
            if MOM_RAW in df.columns:
                r28 = df[MOM_RAW].astype(float)
            else:
                r28 = pd.Series(np.nan, index=df.index)
            r28 = r28.where(r28.notna(), close / close.shift(28) - 1.0)

            active = fc.notna() & (fc != 0)
            side_ok = np.sign(fc) == np.sign(r28)
            agree = active & in_sit & side_ok & r28.notna()
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": (
                "Fewer than 90% of the active bars have a positive 90-day return "
                "and a forecast with the sign of the 28-day return, as the Fidelity's "
                "situation and side require."
            ),
            "reading": (
                "The 90-day return is recomputed from closes inside each window, "
                "and the recorded regime stands in where 90 earlier bars are not recorded."
            ),
        }

    # ---------- 2. Main measure: pooled regression on the 5-bar grid ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        # The coin's normal 5-bar drift: all grid bars of all its windows.
        drift_samples = []
        per_window = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            grid = np.arange(0, n, H)
            grid = grid[grid + H < n]
            fwd = close[grid + H] / close[grid] - 1.0
            drift_samples.extend(list(fwd[np.isfinite(fwd)]))
            per_window.append((df, grid, fwd))
        if not drift_samples:
            continue
        drift = float(np.mean(drift_samples))

        for df, grid, fwd in per_window:
            if len(grid) == 0 or MOM_POST not in df.columns:
                continue
            reg = df["regime"].astype(str).values[grid]
            x = df[MOM_POST].astype(float).values[grid]
            m = (reg == "trending") & np.isfinite(x) & np.isfinite(fwd)
            xs.extend(list(x[m]))
            ys.extend(list(fwd[m] - drift))

    n_cases = len(xs)
    slope, t = _ols(xs, ys)

    # ---------- 3. Supporting check: book minus market rise, before costs ----------
    book_rows = []
    for coin, wins in bars.items():
        coin_rets = []
        frames = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            r = close.pct_change()
            alloc_prev = df["postRebalance_current_allocation"].astype(float).shift(1)
            day = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D")
            frames.append(pd.DataFrame({"day": day, "r": r, "a": alloc_prev}))
            coin_rets.extend(list(r.dropna().values))
        if not coin_rets:
            continue
        mu = float(np.mean(coin_rets))
        for f in frames:
            f = f.dropna(subset=["r", "a"]).copy()
            f["book"] = f["a"] * f["r"]
            f["mkt"] = f["a"] * mu
            f["coin"] = coin
            book_rows.append(f[["day", "coin", "book", "mkt"]])

    if book_rows:
        allb = pd.concat(book_rows, ignore_index=True)
        daily = allb.groupby("day")[["book", "mkt"]].mean()
        support_val = float(daily["book"].mean() - daily["mkt"].mean())
        n_days = int(len(daily))
    else:
        support_val = None
        n_days = 0
    support_pass = (support_val is not None) and (support_val > 0)

    # ---------- 4. Decision ----------
    if n_cases < 200:
        status = "not observable"
        decided = (
            f"Only {n_cases} grid cases on trending bars across all coins, "
            "fewer than the plan's minimum of 200."
        )
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The regression could not be fitted on the grid cases."
    elif slope > 0 and t >= 2:
        if support_pass:
            status = "confirmed"
            decided = (
                "The slope is positive with t >= 2, and the book's mean daily return "
                "minus its gain from the market's rise is above 0."
            )
        else:
            status = "inconclusive"
            decided = (
                "The slope is positive with t >= 2, but the supporting check is not "
                "above 0, so the plan calls it inconclusive."
            )
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "pooled OLS slope of 5-bar drift-adjusted forward return on mom28 forecast, trending grid bars",
            "value": slope,
            "statistic": ({"name": "OLS t of slope", "value": t} if t is not None else None),
            "threshold": "confirm: slope > 0 with t >= 2 (and supporting check > 0); reject: slope < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "book mean daily return minus market-rise gain, before costs",
            "value": support_val,
            "passed": support_pass if support_val is not None else None,
        },
        "counts": {
            "grid cases on trending bars": int(n_cases),
            "book days": n_days,
        },
        "decided_by": decided,
        "reading": (
            "Before costs, the book's daily return is the position held after the "
            "previous bar times the coin's close-to-close return, averaged over coins "
            "per day; the drift is the mean of each coin's non-overlapping 5-bar grid "
            "returns over all its windows; the fewer-than-200-cases rule is applied as "
            "a minimum count (not observable)."
        ),
    }
