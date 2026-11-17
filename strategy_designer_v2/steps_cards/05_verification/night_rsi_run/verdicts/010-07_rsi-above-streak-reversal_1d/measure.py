import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 14
    LHV = "debug_info.components.rsi_above_age.last_history_value"
    MIN_CASES = 100

    def prep(df):
        df = df.sort_values("timestamp").reset_index(drop=True).copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        for c in ["close", "forecast", "postRebalance_total_value", "postRebalance_current_allocation"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        if LHV in df.columns:
            df[LHV] = pd.to_numeric(df[LHV], errors="coerce")
        else:
            df[LHV] = np.nan
        return df

    data = {coin: {w: prep(df) for w, df in wins.items() if df is not None and len(df) > 0}
            for coin, wins in bars.items()}

    # ---------- 1. Situation check ----------
    # Situation: RSI(14) above 50 in an unbroken run (raw midline age > 0). Expected side: short (forecast < 0).
    n_active = 0
    n_agree = 0
    for coin, wins in data.items():
        for w, df in wins.items():
            active = df["forecast"].notna() & (df["forecast"] != 0)
            situ = df[LHV].notna() & (df[LHV] > 0)
            agree = active & situ & (df["forecast"] < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "pooled OLS slope of 14-bar excess return on RSI>50 run length",
                "value": None,
                "statistic": None,
                "threshold": "confirm if slope < 0 with t <= -2 (and timing gain > 0); reject if slope > 0 with t >= +2",
            },
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the active bars (forecast != 0) are bars with RSI above 50 "
                           "(midline age > 0) carrying a short forecast, as the plan's Fidelity requires."),
            "reading": "Situation taken as last_history_value > 0 with forecast < 0; bars with a missing raw value count as outside the situation.",
        }

    # ---------- 2. Main measure ----------
    # Coin mean 14-bar return over all windows, on the non-overlapping grid of every window.
    grid_rows = []
    coin_mean14 = {}
    for coin, wins in data.items():
        all_rets = []
        for w, df in wins.items():
            n = len(df)
            close = df["close"].values
            for i in range(0, n, H):
                if i + H < n and np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] != 0:
                    r = close[i + H] / close[i] - 1.0
                    all_rets.append(r)
                    grid_rows.append({
                        "coin": coin, "window": w, "ret": r,
                        "forecast": df["forecast"].iloc[i],
                        "age": df[LHV].iloc[i],
                    })
        coin_mean14[coin] = float(np.mean(all_rets)) if all_rets else np.nan

    grid = pd.DataFrame(grid_rows, columns=["coin", "window", "ret", "forecast", "age"])
    if len(grid):
        grid["excess"] = grid["ret"] - grid["coin"].map(coin_mean14)
    else:
        grid["excess"] = []
    sample = grid[(grid["forecast"] < 0) & grid["age"].notna() & grid["excess"].notna()]
    n_rsi_above = int(((grid["age"] > 0) & grid["excess"].notna()).sum()) if len(grid) else 0
    n_sample = int(len(sample))

    slope = None
    t_slope = None
    if n_sample >= 3 and sample["age"].nunique() > 1:
        lr = stats.linregress(sample["age"].values.astype(float), sample["excess"].values.astype(float))
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- 3. Supporting check: timing gain ----------
    book_frames = []
    for coin, wins in data.items():
        dr = []
        for w, df in wins.items():
            r = df["close"] / df["close"].shift(1) - 1.0
            dr.append(r.iloc[1:])
        mu = float(pd.concat(dr).dropna().mean()) if dr else np.nan
        for w, df in wins.items():
            v = df["postRebalance_total_value"]
            book_r = v / v.shift(1) - 1.0
            mkt = df["postRebalance_current_allocation"].shift(1) * mu
            f = pd.DataFrame({"timestamp": df["timestamp"].dt.floor("D"),
                              "book": book_r, "mkt": mkt}).iloc[1:]
            # last bar of each day
            f = f.groupby("timestamp", as_index=False).last()
            f = f.dropna(subset=["book", "mkt"])
            book_frames.append(f)
    timing = None
    if book_frames:
        allb = pd.concat(book_frames)
        if len(allb):
            daily = allb.groupby("timestamp")[["book", "mkt"]].mean()
            timing = float(daily["book"].mean() - daily["mkt"].mean())
    timing_pass = None if timing is None else bool(timing > 0)

    # ---------- 4. Decision ----------
    counts = {"grid cases with RSI above 50": n_rsi_above,
              "grid cases with forecast below 0 (regression sample)": n_sample}
    if n_rsi_above < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n_rsi_above} grid cases with RSI above 50, below the plan's minimum of {MIN_CASES}."
    elif slope is None or t_slope is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed on the grid sample, so neither confirm nor reject is met."
    elif slope < 0 and t_slope <= -2:
        if timing_pass:
            status = "confirmed"
            decided_by = "The slope is negative with t <= -2 and the timing gain is above 0 (confirm rule)."
        else:
            status = "inconclusive"
            decided_by = "The slope is negative with t <= -2 but the timing gain is not above 0 (confirming slope with failed timing check)."
    elif slope > 0 and t_slope >= 2:
        status = "rejected"
        decided_by = "The slope is positive with t >= +2 (reject rule)."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2 and +2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "pooled OLS slope of 14-bar excess return on RSI>50 run length",
            "value": slope,
            "statistic": None if t_slope is None else {"name": "OLS slope t", "value": t_slope},
            "threshold": "confirm if slope < 0 with t <= -2 (and timing gain > 0); reject if slope > 0 with t >= +2",
        },
        "supporting_check": {"name": "book timing gain (mean daily return minus market-rise gain, before costs)",
                             "value": timing, "passed": timing_pass},
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("Pooled the coins present in the record (BNB absent), used grid bars at positions 0,14,28,... of each window "
                    "with a full forward 14-bar return and forecast < 0, regressed excess return on last_history_value by OLS, "
                    "counted 'grid cases with RSI above 50' as grid bars with last_history_value > 0, and treated a shortfall "
                    "of that minimum as 'not observable'."),
    }
