import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    RAW = "debug_info.components.scaled_adv.last_history_value"

    # ---------- 1. situation check: 10-day vol-scaled advance > 0, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # where the raw value is not recorded, its sign is the sign of the 240-bar return
            ret240 = close / close.shift(240) - 1.0
            raw = raw.where(raw.notna(), ret240)
            active = fc.notna() & (fc != 0)
            situation = raw > 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean excess 72-bar return of top-quintile forecast>0 cases"
    main_thr = "confirm: mean > 0 with t >= 2 (and check passes); reject: t <= -2"
    sup_name = "Welch difference top quintile minus other forecast>0 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars (forecast != 0) are long bars with a positive "
                          "volatility-scaled 240-bar advance, as the plan's Fidelity requires.",
            "reading": "The situation is a positive raw scaled_adv value (240-bar return > 0), the side long.",
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_means = {}
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                rows.append((coin, fc[t], r))
        coin_means[coin] = float(np.mean(all_rets)) if all_rets else np.nan

    df = pd.DataFrame(rows, columns=["coin", "forecast", "ret"])
    df["excess"] = df["ret"] - df["coin"].map(coin_means)
    pos = df[(df["forecast"] > 0) & df["forecast"].notna() & df["excess"].notna()].copy()

    coins = list(bars.keys())
    if len(pos) > 0:
        q80 = float(np.quantile(pos["forecast"].to_numpy(), 0.8))
        top = pos[pos["forecast"] >= q80]
        rest = pos[pos["forecast"] < q80]
    else:
        q80 = None
        top = pos.iloc[0:0]
        rest = pos.iloc[0:0]

    counts = {"top-quintile cases pooled": int(len(top))}
    per_coin = {}
    for c in coins:
        per_coin[c] = int((top["coin"] == c).sum())
        counts["top-quintile cases " + str(c)] = per_coin[c]
    counts["other forecast>0 cases"] = int(len(rest))

    x = top["excess"].to_numpy(dtype=float)
    y = rest["excess"].to_numpy(dtype=float)

    main_val, main_t = None, None
    if len(x) >= 2:
        main_val = float(np.mean(x))
        sd = float(np.std(x, ddof=1))
        main_t = float(main_val / (sd / np.sqrt(len(x)))) if sd > 0 else None
    elif len(x) == 1:
        main_val = float(x[0])

    diff, welch_t = None, None
    if len(x) >= 2 and len(y) >= 2:
        diff = float(np.mean(x) - np.mean(y))
        tt = stats.ttest_ind(x, y, equal_var=False)
        welch_t = float(tt.statistic) if np.isfinite(tt.statistic) else None
    check_pass = None if (diff is None or welch_t is None) else bool(diff > 0 and welch_t >= 1)

    reading = ("Top quintile = forecast>0 grid cases (pooled over coins) with forecast >= the pooled 80th "
               "percentile (ties at the cutoff included); the coin's mean 72-bar return is the mean over all "
               "its non-overlapping grid cases of all windows; the per-coin minimum of 15 applies to every coin "
               "in the record; the plan's 'inconclusive' for too few cases is reported as 'not observable'.")

    main_measure = {"name": main_name, "value": main_val,
                    "statistic": None if main_t is None else {"name": "ordinary t of the mean", "value": main_t},
                    "threshold": main_thr}
    supporting = {"name": sup_name, "value": diff, "passed": check_pass,
                  "welch_t": welch_t}
    supporting = {"name": sup_name + (" (Welch t=%.3f)" % welch_t if welch_t is not None else ""),
                  "value": diff, "passed": check_pass}

    short_coins = [c for c in coins if per_coin[c] < 15]
    if len(top) < 150 or short_coins:
        status = "not observable"
        if len(top) < 150:
            decided = "Fewer than 150 top-quintile cases pooled (%d), below the plan's minimum." % len(top)
        else:
            decided = "Fewer than 15 top-quintile cases for %s, below the plan's per-coin minimum." % ", ".join(map(str, short_coins))
    elif main_t is None:
        status = "inconclusive"
        decided = "The main t could not be computed (zero dispersion), so neither rule is met."
    elif main_t <= -2:
        status = "rejected"
        decided = "The top-quintile mean excess has t <= -2 (reject rule)."
    elif main_val > 0 and main_t >= 2:
        if check_pass:
            status = "confirmed"
            decided = "Mean excess > 0 with t >= 2, and the Welch difference is > 0 with t >= 1 (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The main measure confirms (mean > 0, t >= 2) but the supporting Welch check fails."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2 (or the mean is not positive), meeting neither confirm nor reject."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main_measure,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
