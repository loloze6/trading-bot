import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    MIN_N = 30

    # ---------- 1. situation check ----------
    # Fidelity situation: a bar that fell, with volume above its 30-bar mean and a lower wick; side long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            o = df["open"].astype(float)
            h = df["high"].astype(float)
            l = df["low"].astype(float)
            c = df["close"].astype(float)
            v = df["volume"].astype(float)
            f = pd.to_numeric(df["forecast"], errors="coerce")

            # Fall: the sign of the vol-scaled 1-bar return is the sign of close - previous close.
            fell = c.diff() < 0
            fell_known = c.diff().notna()
            # On the first bar of a window there is no previous close in the window.
            # Fall back on the recorded flush raw value (return x volume ratio, and the ratio is > 0).
            fcol = "debug_info.components.flush.last_history_value"
            if fcol in df.columns:
                fl = pd.to_numeric(df[fcol], errors="coerce")
                fb = (~fell_known) & fl.notna()
                fell = fell.where(~fb, fl < 0)
                fell_known = fell_known | fb

            # Volume above its 30-bar mean (the current bar included).
            vm = v.rolling(30, min_periods=30).mean()
            vr = v / vm
            vr_known = vr.notna()
            vol_hi = vr > 1.0

            # Lower wick, as a share of the bar's range.
            rng = h - l
            wick = (np.minimum(o, c) - l) / rng.replace(0, np.nan)
            wick_known = wick.notna() | (rng == 0)
            has_wick = wick.fillna(0) > 0

            known = fell_known & vr_known & wick_known
            situ = fell & vol_hi & has_wick
            active = f.notna() & (f != 0) & known
            n_active += int(active.sum())
            n_agree += int((active & situ & (f > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {
                "agreement": float(agreement) if agreement is not None else None,
                "passed": False,
            },
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active)},
            "decided_by": ("Fewer than 90% of the active forecast bars are long bars where the bar fell "
                           "on volume above its 30-bar mean with a lower wick, as the Fidelity situation requires."),
            "reading": ("The situation is rebuilt from prices: a fall is close below the previous close "
                        "(or a negative flush raw value on a window's first bar), the volume ratio uses a "
                        "30-bar mean that includes the current bar, and bars where it cannot be computed are left out."),
        }

    # ---------- 2. criterion ----------
    # 3-bar grid returns for each coin and window
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H < n:
                    r = c[i + H] / c[i] - 1.0
                    rows.append((coin, w, f[i], r))
    g = pd.DataFrame(rows, columns=["coin", "win", "forecast", "ret"])
    g = g.dropna(subset=["ret"])
    coin_mean = g.groupby("coin")["ret"].mean()
    g["excess"] = g["ret"] - g["coin"].map(coin_mean)

    q = g[(g["forecast"].notna()) & (g["forecast"] >= 2)].dropna(subset=["excess"])
    nq = int(len(q))

    mean_ex = float(q["excess"].mean()) if nq > 0 else None
    t = None
    if nq > 1:
        sd = q["excess"].std(ddof=1)
        if sd > 0:
            t = float(mean_ex / (sd / np.sqrt(nq)))

    wmean = None
    sup_pass = None
    if nq > 0 and q["forecast"].sum() > 0:
        wmean = float((q["excess"] * q["forecast"]).sum() / q["forecast"].sum())
        sup_pass = bool(wmean > mean_ex)
    sup_value = (wmean - mean_ex) if (wmean is not None and mean_ex is not None) else None

    if nq < MIN_N:
        status = "not observable"
        decided = (f"Only {nq} qualifying grid bars (forecast >= 2), "
                   f"below the plan's minimum of 30 across all coins and windows.")
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero dispersion), so neither rule is met."
    elif mean_ex > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = ("The mean excess 3-bar return is > 0 with t >= 2, and the forecast-weighted mean "
                   "exceeds the unweighted mean.")
    elif mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "The mean excess 3-bar return is < 0 with t <= -2 (continued decline after flushes)."
    elif mean_ex > 0 and t >= 2:
        status = "inconclusive"
        decided = "The t confirms (>= 2), but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean 3-bar excess return over the coin's mean, grid bars with forecast >= 2",
            "value": mean_ex,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "forecast-weighted mean excess minus unweighted mean excess",
            "value": sup_value,
            "passed": sup_pass,
        },
        "counts": {"qualifying grid bars": nq},
        "decided_by": decided,
        "reading": ("The coin's mean 3-bar return is the mean over the same non-overlapping grid "
                    "(positions 0, 3, 6, ... of each window) pooled over all its windows; the plan's "
                    "'fewer than 30 qualifying grid bars' is treated as a minimum count, so it gives "
                    "'not observable'; and the situation check rebuilds the fall, the 30-bar volume ratio "
                    "(current bar included) and the wick from prices."),
    }
