import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    FC = "forecast"
    REG = "regime"

    def _clean(df):
        df = df.copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df = df.sort_values("timestamp").reset_index(drop=True)
        return df

    # ---------- 1. Situation check: choppy market, up close, short side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = _clean(df)
            close = df["close"].astype(float)
            fc = df[FC].astype(float)
            reg = df[REG].astype(str)
            # up day from prices (close above prior close, inside the window);
            # on the window's first bar the prior close is not recorded: fall back on the detector's decision
            prev = close.shift(1)
            up = (close > prev)
            up = up.where(prev.notna(), reg == "mean_reversion")
            # choppy profile: 60-bar price evolution (percent) between -10 and +10, from prices;
            # where 60 prior bars are not in the window, fall back on the detector not having chosen "chop"
            c60 = close.shift(60)
            evo = (close / c60 - 1.0) * 100.0
            choppy = (evo >= -10) & (evo <= 10)
            choppy = choppy.where(c60.notna(), reg != "chop")
            active = fc.notna() & (fc != 0)
            agree = active & up.astype(bool) & choppy.astype(bool) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of (10-day return minus coin drift) x forecast/10 on grid cases"
    main_thr = "confirm: above 0 with t >= 2 (and check passes); reject: below 0 with t <= -2"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on short side": n_agree},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are choppy up-close bars with a "
                           "short forecast, so the config does not do what the plan's Fidelity says"
                           if n_active > 0 else "the record holds no bar with a non-zero forecast"),
            "reading": "up close and choppy profile (|60-bar change| <= 10%) recomputed from prices inside each "
                       "window, falling back on the recorded regime where the window lacks the prior bars.",
        }

    # ---------- 2. Criterion ----------
    drift_samples = {}
    cases = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = _clean(df)
            close = df["close"].astype(float).values
            fc = df[FC].astype(float).values
            reg = df[REG].astype(str).values
            ts = df["timestamp"]
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                drift_samples.setdefault(coin, []).append(r)
                f = fc[i]
                up = (i > 0 and np.isfinite(close[i - 1]) and close[i] > close[i - 1]) or \
                     (i == 0 and reg[i] == "mean_reversion")
                if reg[i] == "mean_reversion" and up and np.isfinite(f) and f < 0:
                    cases.append({"coin": coin, "day": ts.iloc[i].floor("D"), "r": r, "f": f})

    drift = {c: float(np.mean(v)) for c, v in drift_samples.items() if len(v) > 0}
    if len(cases) > 0:
        cdf = pd.DataFrame(cases)
        cdf["ex"] = cdf["r"] - cdf["coin"].map(drift)
        cdf["prod"] = cdf["ex"] * cdf["f"] / 10.0
    else:
        cdf = pd.DataFrame(columns=["coin", "day", "r", "f", "ex", "prod"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    counts = {"distinct case days": n_days, "cases": n_cases}

    mean_val = None
    t_val = None
    if n_cases > 0:
        mean_val = float(cdf["prod"].mean())
        if n_days > 1:
            dev = cdf["prod"] - mean_val
            S = dev.groupby(cdf["day"]).sum().values
            var_mean = (S ** 2).sum() / (n_cases ** 2) * (n_days / (n_days - 1))
            if var_mean > 0:
                t_val = float(mean_val / np.sqrt(var_mean))

    # supporting check
    sc_val = None
    sc_t = None
    sc_pass = None
    if n_cases > 0:
        a = cdf["f"].abs()
        med = float(a.median())
        deep = cdf.loc[a > med, "ex"].astype(float).values
        shallow = cdf.loc[a <= med, "ex"].astype(float).values
        if len(deep) >= 2 and len(shallow) >= 2:
            sc_val = float(deep.mean() - shallow.mean())
            tt = stats.ttest_ind(deep, shallow, equal_var=False)
            sc_t = float(tt.statistic) if np.isfinite(tt.statistic) else None
            sc_pass = bool(sc_val < 0 and sc_t is not None and sc_t <= -1)
        else:
            sc_pass = False
    supporting = {
        "name": "deeper-half minus shallower-half mean 10-day return minus drift (Welch t <= -1)",
        "value": sc_val,
        "passed": sc_pass,
        "welch_t": sc_t,
    }

    if n_days < 30:
        status = "not observable"
        decided = f"fewer than 30 distinct case days ({n_days}), the plan's minimum count, so the data could not show the idea"
    elif t_val is None:
        status = "inconclusive"
        decided = "the main measure's t could not be computed, so neither the confirm nor the reject rule is met"
    elif mean_val > 0 and t_val >= 2:
        if sc_pass:
            status = "confirmed"
            decided = "the main measure is above 0 with t >= 2 and the supporting check passes (confirm rule)"
        else:
            status = "inconclusive"
            decided = "the main measure is above 0 with t >= 2 but the supporting check fails (inconclusive rule)"
    elif mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "the main measure is below 0 with t <= -2 (reject rule)"
    else:
        status = "inconclusive"
        decided = "the main measure's t is between -2 and 2 (inconclusive rule)"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": ({"name": "t of the mean, cases of one day summed", "value": t_val}
                          if t_val is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are grid bars (0, 10, 20, ... of each window, with 10 bars ahead inside it) whose recorded "
                    "regime is mean_reversion, whose close is above the prior close and whose forecast is below 0; the "
                    "coin's drift is the mean 10-day return over all grid bars of all its windows; the deeper half is "
                    "|forecast| strictly above the median, the rest the shallower half; the plan's 'fewer than 30 "
                    "distinct case days' is applied as the minimum count giving 'not observable'."),
    }
