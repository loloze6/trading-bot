import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    L = 20
    FC = "forecast"
    REC = "debug_info.components.recency.last_history_value"

    # ---------- per-window derived series ----------
    frames = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            c = pd.to_numeric(d["close"], errors="coerce")
            sma = c.rolling(L, min_periods=L).mean()
            dist = c / sma - 1.0
            # new 20-day closing high: close at or above the max of the prior 20 closes
            prior_max = c.shift(1).rolling(L, min_periods=L).max()
            new_high = (c >= prior_max).astype(float)
            new_high[prior_max.isna()] = np.nan
            # bars since the last new high, within the window
            bsh_p = pd.Series(np.nan, index=d.index)
            last = None
            known = False
            for i in range(len(d)):
                nh = new_high.iloc[i]
                if not np.isnan(nh):
                    known = True
                    if nh == 1.0:
                        last = i
                if last is not None:
                    bsh_p.iloc[i] = i - last
                elif known:
                    bsh_p.iloc[i] = np.inf if i - (L) >= L else np.nan
            high_recent = pd.Series(np.nan, index=d.index)
            ok = bsh_p.notna()
            high_recent[ok] = (bsh_p[ok] < L).astype(float)
            # fallback on the recorded BarsSinceHigh raw value (same component as the detector's bsh)
            if REC in d.columns:
                rec = pd.to_numeric(d[REC], errors="coerce")
                fill = high_recent.isna() & rec.notna()
                high_recent[fill] = (rec[fill] > 0).astype(float)
            fwd = c.shift(-H) / c - 1.0
            out = pd.DataFrame({
                "coin": coin, "window": w, "pos": np.arange(len(d)),
                "forecast": pd.to_numeric(d[FC], errors="coerce"),
                "dist": dist, "high_recent": high_recent, "fwd": fwd,
            })
            frames.append(out)
    if not frames:
        return {"status": "not observable", "situation_check": {"agreement": None, "passed": False},
                "main_measure": None, "supporting_check": None, "counts": {}, "decided_by": "no data",
                "reading": "none"}
    allb = pd.concat(frames, ignore_index=True)

    # ---------- situation check ----------
    act = allb[allb["forecast"].notna() & (allb["forecast"] != 0)]
    chk = act[act["dist"].notna() & act["high_recent"].notna()]
    if len(chk) > 0:
        good = (chk["dist"] > 0) & (chk["high_recent"] == 1.0) & (chk["forecast"] > 0)
        agreement = float(good.mean())
    else:
        agreement = 0.0
    passed = agreement >= 0.9
    reading = ("Situation recomputed from prices (close above its 20-bar SMA and a close at or above the prior "
               "20 closes' max within the last 20 bars, with the recorded recency raw value > 0 used where the "
               "window's prices are too short), active bars without a computable SMA left out; the coin mean "
               "5-bar return is taken over all of the coin's bars in all its windows; blocks are the window grid "
               "positions 0,5,10,... with an active forecast; the t is the ordinary t of the forecast-weighted "
               "excess returns (same sign as the weighted mean); the supporting check uses the same grid and "
               "excess over the coin mean and does not enter the decision rule.")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"active bars checked": int(len(chk))},
            "decided_by": ("Fewer than 90% of active bars are long bars with the close above SMA20 and a new "
                           "20-day closing high within 20 bars, so the config does not trade the plan's situation."),
            "reading": reading,
        }

    # ---------- main measure ----------
    coin_mean = allb.dropna(subset=["fwd"]).groupby("coin")["fwd"].mean()
    allb["excess"] = allb["fwd"] - allb["coin"].map(coin_mean)
    grid = allb[allb["pos"] % H == 0]
    blocks = grid[grid["forecast"].notna() & (grid["forecast"] > 0) & grid["excess"].notna()]
    n = int(len(blocks))
    value, tval = None, None
    if n > 0:
        f = blocks["forecast"].values.astype(float)
        x = blocks["excess"].values.astype(float)
        value = float(np.sum(f * x) / np.sum(f))
        if n > 1:
            wx = f * x
            sd = np.std(wx, ddof=1)
            tval = float(np.mean(wx) / (sd / np.sqrt(n))) if sd > 0 else None

    # ---------- supporting check ----------
    sup = grid[(grid["forecast"] == 0) & (grid["high_recent"] == 1.0) & (grid["dist"] < 0) & grid["excess"].notna()]
    sup_val = float(sup["excess"].mean()) if len(sup) > 0 else None
    sup_pass = (sup_val <= 0) if sup_val is not None else None

    counts = {"non-overlapping active 5-bar blocks": n, "supporting flat blocks": int(len(sup))}

    if n < 100:
        status = "not observable"
        decided = f"Only {n} non-overlapping active 5-bar blocks, fewer than the plan's minimum of 100."
    elif tval is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif value > 0 and tval >= 2:
        status = "confirmed"
        decided = "The forecast-weighted mean excess return is positive with t >= 2."
    elif value < 0 and tval <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess return is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies strictly between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "forecast-weighted mean forward 5-bar excess return over the coin mean",
            "value": value,
            "statistic": {"name": "t of the mean weighted excess return", "value": tval} if tval is not None else None,
            "threshold": "confirm if positive with t >= 2, reject if negative with t <= -2, else inconclusive",
        },
        "supporting_check": {
            "name": "mean forward 5-bar excess return on flat bars with recent high but close below SMA20 <= 0",
            "value": sup_val,
            "passed": bool(sup_pass) if sup_pass is not None else None,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
