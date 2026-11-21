import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    MIN_CASES = 300
    RAW_COL = "debug_info.components.rsi_side.last_history_value"

    def _rsi_from_close(close, period=14):
        # Wilder RSI computed inside one window only (fallback when raw value is missing)
        delta = close.diff()
        gain = delta.clip(lower=0.0)
        loss = (-delta).clip(lower=0.0)
        avg_g = gain.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
        avg_l = loss.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
        rs = avg_g / avg_l
        rsi = 100.0 - 100.0 / (1.0 + rs)
        rsi = rsi.where(avg_l != 0, 100.0)
        rsi = rsi.where(~(avg_g.isna() | avg_l.isna()))
        return rsi

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW_COL in df.columns:
                raw = pd.to_numeric(df[RAW_COL], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # RSI distance from 50: raw = (50 - RSI) * sf, so (RSI - 50) has sign -sign(raw)
            dist = -np.sign(raw)
            if raw.isna().any():
                rsi = _rsi_from_close(close)
                dist = dist.where(~raw.isna(), np.sign(rsi - 50.0))
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & dist.notna() & (dist != 0) & (np.sign(fc) == dist)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "mean of forecast/10 x (coin 7-bar return - coin mean 7-bar return), non-overlapping cases"
    threshold = "confirm: positive with t >= 2 and supporting difference positive; reject: negative with t <= -2 and supporting difference negative"
    reading = ("Non-overlapping cases are positions 0,7,14,... of each window with close[t+7] inside the window; "
               "each coin's mean 7-bar return is taken over these same cases in all its windows; cases with forecast 0 "
               "stay in the main measure (product 0) and are left out of both groups of the supporting check; "
               "the 300-case minimum counts all cases across coins.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "independent cases": None},
            "decided_by": ("Fewer than 90% of active bars have a forecast whose sign matches the side of RSI(14) "
                           "relative to 50 (long above, short below), as the Fidelity's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                if not np.isfinite(fc[t]):
                    continue
                rows.append((coin, float(fc[t]), float(c1 / c0 - 1.0)))

    cases = pd.DataFrame(rows, columns=["coin", "forecast", "ret"])
    n_cases = int(len(cases))
    counts = {"independent cases": n_cases}
    for coin in bars.keys():
        counts["cases " + str(coin)] = int((cases["coin"] == coin).sum()) if n_cases else 0

    main_value = None
    t_main = None
    diff = None
    t_diff = None
    if n_cases > 0:
        coin_mean = cases.groupby("coin")["ret"].transform("mean")
        cases["excess"] = cases["ret"] - coin_mean
        prod = cases["forecast"] / 10.0 * cases["excess"]
        main_value = float(prod.mean())
        if n_cases > 1:
            sd = float(prod.std(ddof=1))
            if sd > 0:
                t_main = float(main_value / (sd / np.sqrt(n_cases)))
        pos = cases.loc[cases["forecast"] > 0, "excess"].values
        neg = cases.loc[cases["forecast"] < 0, "excess"].values
        counts["cases forecast > 0"] = int(len(pos))
        counts["cases forecast < 0"] = int(len(neg))
        if len(pos) > 0 and len(neg) > 0:
            diff = float(pos.mean() - neg.mean())
            if len(pos) > 1 and len(neg) > 1:
                tt = stats.ttest_ind(pos, neg, equal_var=False)
                if np.isfinite(tt.statistic):
                    t_diff = float(tt.statistic)

    sup_passed = None
    if diff is not None and main_value is not None:
        sup_passed = bool(np.sign(diff) == np.sign(main_value) and diff != 0 and main_value != 0)

    supporting = {
        "name": "mean excess 7-bar return forecast>0 minus forecast<0 (Welch t), same sign as main",
        "value": diff,
        "passed": sup_passed,
    }
    if t_diff is not None:
        supporting["welch_t"] = t_diff

    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n_cases} independent cases across the coins, below the plan's minimum of 300."
    elif (main_value is not None and t_main is not None and main_value > 0 and t_main >= 2
          and diff is not None and diff > 0):
        status = "confirmed"
        decided_by = "The main measure is positive with t >= 2 and the supporting difference is positive."
    elif (main_value is not None and t_main is not None and main_value < 0 and t_main <= -2
          and diff is not None and diff < 0):
        status = "rejected"
        decided_by = "The main measure is negative with t <= -2 and the supporting difference is negative."
    else:
        status = "inconclusive"
        if t_main is None or abs(t_main) < 2:
            decided_by = "The main measure's |t| is below 2, which the plan calls inconclusive."
        else:
            decided_by = ("The main measure passes |t| >= 2 but the supporting difference does not have its sign, "
                          "which the plan calls inconclusive.")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": main_value,
            "statistic": ({"name": "ordinary t of the mean", "value": t_main} if t_main is not None else None),
            "threshold": threshold,
        },
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
