import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    CL_RAW = "debug_info.components.close_loc.last_history_value"
    CL_POST = "debug_info.components.close_loc.post_pipeline_value"

    def standardise(raw, window=60, min_periods=20):
        # value(t) * 10 / mean(|last `window` raw values, t left out)|, capped -20..20
        a = np.abs(raw)
        denom = a.shift(1).rolling(window, min_periods=min_periods).mean()
        out = raw * 10.0 / denom
        out = out.where(denom > 0)
        return out.clip(-20, 20)

    # ---------- per-coin preparation ----------
    coin_frames = {}
    for coin, wins in bars.items():
        rets_all = []
        frames = []
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d["day"] = d["ts"].dt.floor("D")
            close = d["close"].astype(float)
            d["r_next"] = close.shift(-1) / close - 1.0
            rets_all.append(d["r_next"].dropna())
            # raw close location (reference "high"): 0 at high, 1 at low
            rng = (d["high"] - d["low"]).astype(float)
            price_raw = (d["high"] - d["close"]) / rng.replace(0, np.nan)
            if CL_RAW in d.columns:
                raw = d[CL_RAW].astype(float).where(d[CL_RAW].notna(), price_raw)
            else:
                raw = price_raw
            z = standardise(raw)
            # where the window is too short to rebuild, use the recorded value after transforms
            if CL_POST in d.columns:
                z = z.where(z.notna(), d[CL_POST].astype(float))
            d["z_cl"] = z
            d["coin"] = coin
            d["window"] = w
            frames.append(d)
        if not frames:
            continue
        allr = pd.concat(rets_all) if rets_all else pd.Series(dtype=float)
        mu = float(allr.mean()) if len(allr) else np.nan
        cdf = pd.concat(frames, ignore_index=True)
        cdf["coin_mean"] = mu
        coin_frames[coin] = cdf

    if not coin_frames:
        return {"status": "not observable", "situation_check": {"agreement": None, "passed": False},
                "main_measure": None, "supporting_check": None, "counts": {"agitated days with a non-zero forecast": 0},
                "decided_by": "No bars in the record.", "reading": "none"}

    allb = pd.concat(coin_frames.values(), ignore_index=True)
    allb["forecast"] = allb["forecast"].astype(float)

    # ---------- situation check ----------
    active = allb[allb["forecast"].fillna(0) != 0].copy()
    agitated = active["regime"].astype(str) != "chop"
    expected_sign = np.sign(active["z_cl"] - 10.0)  # long when close nearer the low than usual
    on_side = (expected_sign == np.sign(active["forecast"])) & (expected_sign != 0)
    n_active = len(active)
    agreement = float((agitated & on_side).sum() / n_active) if n_active else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The agitated situation is read as regime not 'chop' and the expected side as the sign of the "
               "rebuilt standardised close location minus 10; the 300-day minimum is counted as distinct UTC days "
               "with at least one non-zero forecast and a next-day return, and the supporting check's thirds are "
               "the forecast tertiles pooled over all coins' active bars, the difference judged by its sign with "
               "Welch t reported.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the non-zero forecasts fall on agitated bars with the side given by "
                           "the close's place versus its usual place (long when nearer the low)."),
            "reading": reading,
        }

    # ---------- main measure ----------
    m = active.dropna(subset=["r_next", "coin_mean"]).copy()
    m["excess"] = m["r_next"] - m["coin_mean"]
    m["prod"] = m["forecast"] * m["excess"]
    daily = m.groupby("day")["prod"].sum()
    n_days = int(len(daily))
    if n_days >= 2 and daily.std(ddof=1) > 0:
        mean_main = float(daily.mean())
        t_main = float(mean_main / (daily.std(ddof=1) / np.sqrt(n_days)))
    else:
        mean_main = float(daily.mean()) if n_days else None
        t_main = None

    # ---------- supporting check ----------
    diff = None
    t_sup = None
    if len(m) >= 3:
        q_lo, q_hi = np.quantile(m["forecast"], [1 / 3, 2 / 3])
        top = m.loc[m["forecast"] >= q_hi, "excess"]
        bot = m.loc[m["forecast"] <= q_lo, "excess"]
        if len(top) >= 2 and len(bot) >= 2:
            diff = float(top.mean() - bot.mean())
            t_sup = float(stats.ttest_ind(top, bot, equal_var=False).statistic)
    sup_passed = None if diff is None else bool(diff > 0)

    counts = {"agitated days with a non-zero forecast": n_days}

    main = {
        "name": "mean of forecast x (next-day return minus coin mean), summed per day",
        "value": mean_main,
        "statistic": None if t_main is None else {"name": "t of the mean (per-day cases)", "value": t_main},
        "threshold": "confirm t >= 2 (with top-minus-bottom third difference > 0); reject t <= -2",
    }
    supporting = {
        "name": "next-day excess return, top third minus bottom third of forecasts (Welch t "
                + ("n/a" if t_sup is None else f"{t_sup:.3f}") + ")",
        "value": diff,
        "passed": sup_passed,
    }

    if n_days < 300:
        status = "not observable"
        decided = f"Only {n_days} agitated days with a non-zero forecast, below the plan's minimum of 300."
    elif t_main is None:
        status = "inconclusive"
        decided = "The main t could not be computed."
    elif t_main >= 2 and sup_passed:
        status = "confirmed"
        decided = "The main t is >= 2 and the top-minus-bottom third difference is above 0."
    elif t_main <= -2:
        status = "rejected"
        decided = "The main t is <= -2: low closes are followed by further falls."
    elif t_main >= 2:
        status = "inconclusive"
        decided = "The main t is >= 2 but the supporting difference is at or below 0."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
