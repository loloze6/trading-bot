import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.scaled_rise.last_history_value"
    BAND = 2.0
    H = 1

    def _scaled_rise_from_prices(df):
        r = df["close"].astype(float) / df["close"].astype(float).shift(1) - 1.0
        sd = r.rolling(20, min_periods=20).std()
        return r / sd.replace(0, np.nan)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[LHV], errors="coerce") if LHV in df.columns else pd.Series(np.nan, index=df.index)
            vsr = raw.where(raw.notna(), _scaled_rise_from_prices(df))
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            active = fc.notna() & (fc != 0)
            situ = (vsr >= 1.0 - 1e-9) & (reg == "mean_reversion")
            agree = active & situ & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    reading_base = ("The situation is checked as raw scaled rise (recorded last_history_value, else recomputed from "
                    "closes) >= 1 on a bar whose regime is mean_reversion (the falling-calm profile vetoes send other bars "
                    "to chop, and the profile's 60-day/365-day inputs cannot be rebuilt inside the ~120-bar windows), "
                    "with a negative forecast; ")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean unusual next-day move of short bets (short direction)",
                             "value": None, "statistic": None,
                             "threshold": "confirm t >= 2 with mean > 0; reject t <= -2"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Only {:.1%} of the active bars are short bars with a scaled rise of at least 1 swing in the "
                           "plan's regime, below the 90 % needed: the config does not trade the Fidelity's situation."
                           ).format(agreement),
            "reading": reading_base + "agreement is the share of active bars meeting all three.",
        }

    # ---------- 2. drift per coin (all windows, daily non-overlapping) ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            idx = np.arange(0, len(c) - H, H)
            r = c[idx + H] / c[idx] - 1.0
            rets.extend(r[np.isfinite(r)].tolist())
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases: short bets ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = df["close"].astype(float).values
            raw = pd.to_numeric(df[LHV], errors="coerce") if LHV in df.columns else pd.Series(np.nan, index=df.index)
            vsr = raw.where(raw.notna(), _scaled_rise_from_prices(df)).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            ref = 0.0
            for t in range(len(df)):
                m = -fc[t] if fc[t] < 0 else 0.0
                if m <= 0:
                    ref = 0.0
                    continue
                if m - ref >= BAND - 1e-12:
                    ref = m
                    if t + H < len(df) and np.isfinite(c[t]) and np.isfinite(c[t + H]) and np.isfinite(drift[coin]):
                        ret = c[t + H] / c[t] - 1.0
                        rows.append({"coin": coin, "day": ts.iloc[t].normalize(),
                                     "unusual": -(ret - drift[coin]), "rise": vsr[t]})
                else:
                    ref = min(ref, m)

    cases = pd.DataFrame(rows, columns=["coin", "day", "unusual", "rise"])
    n = int(len(cases))
    n_days = int(cases["day"].nunique()) if n else 0

    mean_u = float(cases["unusual"].mean()) if n else None
    t_stat = None
    if n >= 2 and n_days >= 2:
        dev = cases["unusual"] - mean_u
        S = dev.groupby(cases["day"]).sum().values
        var_mean = (S ** 2).sum() * n_days / (n_days - 1) / n ** 2
        t_stat = float(mean_u / np.sqrt(var_mean)) if var_mean > 0 else None

    # supporting check
    sup_val = None
    sup_pass = None
    sc = cases.dropna(subset=["rise"])
    if len(sc) >= 2:
        med = sc["rise"].median()
        up = sc.loc[sc["rise"] > med, "unusual"]
        lo = sc.loc[sc["rise"] <= med, "unusual"]
        if len(up) > 0 and len(lo) > 0:
            sup_val = float(up.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)

    counts = {"cases": n, "distinct days": n_days}
    mm = {"name": "mean unusual next-day move of short bets (short direction)",
          "value": mean_u,
          "statistic": {"name": "t of the mean, cases of one day taken together", "value": t_stat} if t_stat is not None else None,
          "threshold": "confirm: mean > 0 with t >= 2 and supporting check passes; reject: t <= -2"}
    sup = {"name": "upper-half minus lower-half mean unusual move, split at median scaled rise",
           "value": sup_val, "passed": sup_pass}

    if n < 30 or n_days < 30:
        status = "not observable"
        decided = "Fewer than 30 cases or cases on fewer than 30 distinct days ({} cases, {} days): decides nothing.".format(n, n_days)
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t could not be computed (zero spread), so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t_stat >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the upper half of rises is faded more than the lower half."
    elif t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move has t <= -2: prices rose further than their drift after the large scaled up days."
    elif mean_u > 0 and t_stat >= 2:
        status = "inconclusive"
        decided = "A confirming t whose supporting check fails is inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    reading = (reading_base +
               "cases are bars where the short forecast deepens by at least 2 points from its shallowest level since the "
               "last bet (from 0 after flat), the drift is the coin's mean daily return over all its windows, and the "
               "median split puts cases above the median in the upper half and those at or below it in the lower half.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": mm,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
