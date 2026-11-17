import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LHV = "debug_info.components.wkend_move.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    def to_dt(s):
        if np.issubdtype(s.dtype, np.number):
            unit = "ms" if s.abs().max() > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    # ---------- prepare per coin / window ----------
    prepared = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            d["_ts"] = to_dt(d["timestamp"])
            close = d["close"].astype(float)
            r_prev = close / close.shift(1) - 1.0            # one-day return of bar t
            r_next = close.shift(-1) / close - 1.0           # horizon 1 bar, inside the window
            vol20 = r_prev.rolling(20, min_periods=20).std()
            z = r_prev / vol20
            z = z.replace([np.inf, -np.inf], np.nan)
            d["_r_next"] = r_next
            d["_z"] = z
            d["_dow"] = d["_ts"].dt.dayofweek
            if LHV in d.columns:
                d["_raw"] = pd.to_numeric(d[LHV], errors="coerce")
            else:
                d["_raw"] = np.nan
            prepared.setdefault(coin, {})[w] = d

    # coin mean daily return over all windows together
    coin_mu = {}
    for coin, wins in prepared.items():
        rr = pd.concat([d["_r_next"] for d in wins.values()]).dropna()
        coin_mu[coin] = float(rr.mean()) if len(rr) else np.nan

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in prepared.items():
        for w, d in wins.items():
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            raw = d["_raw"].where(d["_raw"].notna(), d["_z"])
            weekend = d["_dow"].isin([5, 6])
            expected = -np.sign(raw)
            agree = active & weekend & raw.notna() & (expected != 0) & (np.sign(fc) == expected)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of position x (next-bar return - coin mean daily return) on weekend bars"
    main_thr = "t >= 2 confirms (with supporting t >= 2); t <= -2 rejects"
    supp_name = "Welch t of per-unit fade -z_t x (r_{t+1} - coin mean), weekend minus weekday"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on expected side": int(n_agree)},
            "decided_by": "Fewer than 90% of active bars are Saturday/Sunday bars whose forecast sign is opposite "
                          "to the bar's vol-scaled one-day return, so the config does not trade the plan's weekend fade.",
            "reading": "Weekend bars are those whose timestamp falls on Saturday or Sunday; expected side is minus "
                       "the sign of the recorded raw component value (recomputed from closes where missing).",
        }

    # ---------- main measure and supporting check ----------
    gains = []
    fade_we = []
    fade_wd = []
    for coin, wins in prepared.items():
        mu = coin_mu[coin]
        for w, d in wins.items():
            is_we = d["regime"].astype(str) == "mean_reversion"
            alloc = pd.to_numeric(d[ALLOC], errors="coerce")
            excess = d["_r_next"] - mu
            g = alloc * excess
            gains.append(g[is_we].dropna().values)
            fade = -d["_z"] * excess
            fade_we.append(fade[is_we].dropna().values)
            fade_wd.append(fade[~is_we].dropna().values)

    gains = np.concatenate(gains) if gains else np.array([])
    fade_we = np.concatenate(fade_we) if fade_we else np.array([])
    fade_wd = np.concatenate(fade_wd) if fade_wd else np.array([])

    n_main = int(len(gains))
    n_we = int(len(fade_we))
    n_wd = int(len(fade_wd))

    main_mean = float(np.mean(gains)) if n_main > 0 else None
    if n_main > 1 and np.std(gains, ddof=1) > 0:
        main_t = float(np.mean(gains) / (np.std(gains, ddof=1) / np.sqrt(n_main)))
    else:
        main_t = None

    if n_we > 1 and n_wd > 1:
        st = stats.ttest_ind(fade_we, fade_wd, equal_var=False)
        supp_t = float(st.statistic) if np.isfinite(st.statistic) else None
        supp_diff = float(np.mean(fade_we) - np.mean(fade_wd))
    else:
        supp_t = None
        supp_diff = None

    counts = {
        "weekend bars (main measure)": n_main,
        "weekend bars (supporting check)": n_we,
        "weekday bars (supporting check)": n_wd,
    }

    reading = ("Weekend bars are the bars with regime mean_reversion (bar just closed is Saturday or Sunday), "
               "weekday bars all others; z_t is the bar's close-to-close return over the std of the last 20 daily "
               "returns including it, inside each window; every bar with a next close in its window is one case.")

    supp_passed = None if supp_t is None else bool(supp_t >= 2)

    def out(status, decided):
        return {
            "status": status,
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": main_mean,
                             "statistic": None if main_t is None else {"name": "t of the mean", "value": main_t},
                             "threshold": main_thr},
            "supporting_check": {"name": supp_name, "value": supp_t, "passed": supp_passed},
            "counts": counts,
            "decided_by": decided,
            "reading": reading + (" Supporting weekend-minus-weekday mean difference: %s." % supp_diff),
        }

    if n_main < 300 or n_we < 300 or n_wd < 300:
        return out("not observable",
                   "The plan's minimum of 300 weekend bars and 300 weekday bars for each test is not reached.")

    if main_t is None or supp_t is None:
        return out("inconclusive", "A t-statistic could not be computed, so neither confirm nor reject rule is met.")

    if main_t <= -2 or supp_t <= -2:
        return out("rejected", "Reject rule met: the main measure's t is <= -2 or the supporting check's t is <= -2.")
    if main_t >= 2 and supp_t >= 2:
        return out("confirmed", "Confirm rule met: the main measure's t is >= 2 and the supporting check's t is >= 2.")
    return out("inconclusive", "Neither rule met: at least one t lies between -2 and 2 and none is <= -2.")
