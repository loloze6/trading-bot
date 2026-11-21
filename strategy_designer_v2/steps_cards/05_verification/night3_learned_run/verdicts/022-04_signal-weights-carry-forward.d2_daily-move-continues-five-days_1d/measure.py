import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.day_move.last_history_value"
    ALLOC = "postRebalance_current_allocation"
    VAL = "postRebalance_total_value"

    # ---------- 1. situation check ----------
    # The situation is the sign of the last day's move. A rise is expected after an up day (long)
    # and a fall after a down day (short), so the forecast's sign must equal the sign of that move.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            price_move = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = df[RAW].astype(float)
                raw = raw.where(raw.notna(), price_move)
            else:
                raw = price_move
            fc = df["forecast"].astype(float)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (np.sign(raw) == np.sign(fc)) & (raw != 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast have a forecast whose sign "
                           "equals the sign of the last day's move, which the plan's situation and its "
                           "expected continuation require."),
            "reading": "The situation was read as the sign of the 1-bar return (raw component value, or the close-to-close return where it is missing).",
        }

    # ---------- 2. main measure: pooled regression on the 5-bar grid ----------
    grid_rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            for i in range(0, n, H):
                if i + H < n:
                    r = close[i + H] / close[i] - 1.0
                    grid_rows.append((coin, fc[i], r))
    g = pd.DataFrame(grid_rows, columns=["coin", "forecast", "ret"]).dropna()
    if len(g) > 0:
        g["ret_dm"] = g["ret"] - g.groupby("coin")["ret"].transform("mean")
    n_grid = int(len(g))
    n_grid_nonzero = int((g["forecast"] != 0).sum()) if n_grid else 0

    slope = None
    t_slope = None
    if n_grid >= 3 and g["forecast"].nunique() > 1:
        x = g["forecast"].values
        y = g["ret_dm"].values
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- 3. supporting check: book mean daily return minus market gain ----------
    # Coin mean daily return over all its windows.
    mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp")
            c = df["close"].astype(float)
            rets.append((c / c.shift(1) - 1.0).dropna())
        allr = pd.concat(rets) if rets else pd.Series(dtype=float)
        mu[coin] = float(allr.mean()) if len(allr) else np.nan

    recs = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("ts")
            d["day"] = d["ts"].dt.floor("D")
            last = d.groupby("day").tail(1).reset_index(drop=True)
            v = last[VAL].astype(float)
            a = last[ALLOC].astype(float)
            book = v / v.shift(1) - 1.0
            mkt = a.shift(1) * mu[coin]
            tmp = pd.DataFrame({"day": last["day"], "book": book, "mkt": mkt}).dropna()
            recs.append(tmp)
    supp_value = None
    supp_pass = None
    if recs:
        allrec = pd.concat(recs)
        if len(allrec):
            daily = allrec.groupby("day")[["book", "mkt"]].mean()
            supp_value = float(daily["book"].mean() - daily["mkt"].mean())
            supp_pass = bool(supp_value > 0)

    # ---------- 4. decision ----------
    counts = {"grid cases with a non-zero forecast": n_grid_nonzero, "grid cases": n_grid}
    if n_grid_nonzero < 300 or t_slope is None:
        status = "not observable"
        decided_by = "Fewer than the plan's minimum of 300 grid cases with a non-zero forecast (or no slope could be estimated)."
    elif t_slope >= 2 and supp_pass:
        status = "confirmed"
        decided_by = "The slope's t is 2 or more and the book's mean daily return minus its market gain is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "The slope's t is -2 or less: large days are followed by reversals."
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = "The slope's t is 2 or more but the supporting check fails."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of demeaned 5-bar forward return on forecast, pooled 5-bar grid",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": "confirm if t >= 2 (with the supporting check), reject if t <= -2, otherwise inconclusive",
        },
        "supporting_check": {
            "name": "book mean daily return minus market-rise gain",
            "value": supp_value,
            "passed": supp_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("The regression is OLS with an intercept on every grid bar with a full 5-bar forward return, "
                    "zero forecasts included; the coin's mean 5-bar return is the mean of its grid returns over all windows; "
                    "the book's daily return is the change in postRebalance_total_value per coin, averaged across coins each day, "
                    "and its market gain is the previous bar's allocation times the coin's mean daily return."),
    }
