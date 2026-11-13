import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    MIN_CASES = 30
    SHOCK_COL = "debug_info.components.shock.last_history_value"

    def merge_signals(idx_list, h):
        cases, last = [], None
        for i in idx_list:
            if last is None or i - last >= h:
                cases.append(i)
                last = i
        return cases

    active_total = 0
    active_agree = 0
    case_excess = []
    inside_excess = []
    per_coin_cases = {}

    for coin, wins in bars.items():
        # coin's mean 5-bar return pooled over all its windows (all bars with a valid forward return)
        all_fwd = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fwd = close.shift(-H) / close - 1.0
            all_fwd.append(fwd.dropna().values)
            prepared.append((df, close, fwd))
        if not prepared:
            continue
        pooled = np.concatenate(all_fwd) if all_fwd else np.array([])
        coin_mean = float(np.mean(pooled)) if pooled.size > 0 else np.nan
        n_coin = 0

        for df, close, fwd in prepared:
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            r1 = close / close.shift(1) - 1.0

            # --- situation: new 21-bar closing high (current + prior 20) on an up day, long side ---
            rmax = close.rolling(21, min_periods=21).max()
            new_high = close >= rmax * (1 - 1e-12)
            if "regime" in df.columns:
                reg_tr = df["regime"].astype(str).str.lower().eq("trending")
                new_high = new_high.where(rmax.notna(), reg_tr)
            else:
                new_high = new_high.where(rmax.notna(), False)
            if SHOCK_COL in df.columns:
                raw = pd.to_numeric(df[SHOCK_COL], errors="coerce")
                up = (raw > 0).where(raw.notna(), r1 > 0)
            else:
                up = r1 > 0
            situation = new_high.astype(bool) & up.fillna(False).astype(bool)

            act = fc.notna() & (fc != 0)
            active_total += int(act.sum())
            active_agree += int((act & situation & (fc > 0)).sum())

            if np.isnan(coin_mean):
                continue

            # --- main cases: forecast >= 10, merged within 5 bars ---
            sig = list(np.where((fc >= 10).values)[0])
            for i in merge_signals(sig, H):
                v = fwd.iloc[i]
                if pd.notna(v):
                    case_excess.append(float(v - coin_mean))
                    n_coin += 1

            # --- inside-range shocks: standardised 1-day return >= 10 while forecast is 0 ---
            denom = r1.abs().rolling(60, min_periods=20).mean()
            stdz = 10.0 * r1 / denom
            ins = (stdz >= 10) & fc.notna() & (fc == 0)
            sig_in = list(np.where(ins.fillna(False).values)[0])
            for i in merge_signals(sig_in, H):
                v = fwd.iloc[i]
                if pd.notna(v):
                    inside_excess.append(float(v - coin_mean))
        per_coin_cases[coin] = n_coin

    reading = ("New high = close >= max of the current and prior 20 closes inside the window (falling back to "
               "regime=='trending' on the first 20 bars), up day = raw shock value (else price return) > 0; the "
               "coin mean is over all bars' overlapping 5-bar returns pooled across its windows; signals are merged "
               "when less than 5 bars after the last kept case, which keeps its return; the inside-range "
               "standardised return is 10 x r / rolling mean |r| (60 bars incl. current, min 20, inside the window), "
               "with the same merging; t is the ordinary one-sample t of the pooled mean.")

    if active_total == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean excess 5-bar return after shock-up new highs", "value": None,
                             "statistic": None, "threshold": "positive with t >= 2 (reject: negative with t <= -2)"},
            "supporting_check": None,
            "counts": {"non-overlapping cases pooled across coins": 0},
            "decided_by": "No bar has a non-zero forecast, so neither the situation nor the criterion can be observed.",
            "reading": reading,
        }

    agreement = active_agree / active_total
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean excess 5-bar return after shock-up new highs", "value": None,
                             "statistic": None, "threshold": "positive with t >= 2 (reject: negative with t <= -2)"},
            "supporting_check": None,
            "counts": {"active bars": int(active_total)},
            "decided_by": ("Fewer than 90% of the non-zero forecast bars are long bars on a new 21-bar closing high "
                           "up day, as the plan's situation requires."),
            "reading": reading,
        }

    n = len(case_excess)
    arr = np.array(case_excess, dtype=float)
    mean = float(arr.mean()) if n > 0 else None
    tval = None
    if n >= 2:
        sd = float(arr.std(ddof=1))
        tval = float(mean / (sd / np.sqrt(n))) if sd > 0 else None

    n_in = len(inside_excess)
    if n > 0 and n_in > 0:
        diff = float(mean - np.mean(inside_excess))
        sup_pass = bool(diff > 0)
    else:
        diff, sup_pass = None, None

    counts = {"non-overlapping cases pooled across coins": int(n),
              "inside-range cases": int(n_in)}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} non-overlapping cases pooled across coins, fewer than the plan's minimum of 30."
    elif tval is None:
        status = "inconclusive"
        decided = "The t-statistic is undefined (zero dispersion), so neither confirm nor reject is met."
    elif mean > 0 and tval >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "Mean excess 5-bar return is positive with t >= 2 and exceeds the inside-range shock mean."
    elif mean < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean excess 5-bar return is negative with t <= -2: prices reverse after shock-up new highs."
    else:
        status = "inconclusive"
        if tval >= 2:
            decided = "t >= 2 but the supporting difference against inside-range shocks is not positive, so confirm is not met."
        else:
            decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "mean excess 5-bar return after shock-up new highs (forecast >= 10)",
                         "value": mean,
                         "statistic": ({"name": "one-sample t", "value": tval} if tval is not None else None),
                         "threshold": "confirm: positive with t >= 2; reject: negative with t <= -2"},
        "supporting_check": {"name": "new-high mean excess minus inside-range shock mean excess",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
