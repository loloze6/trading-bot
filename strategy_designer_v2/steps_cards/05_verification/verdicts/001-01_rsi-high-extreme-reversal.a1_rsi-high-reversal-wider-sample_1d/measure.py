import numpy as np
import pandas as pd


def _wilder_rsi(close, period=14):
    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = (-delta).clip(lower=0.0)
    avg_gain = gain.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100.0 - 100.0 / (1.0 + rs)
    rsi = rsi.where(avg_loss != 0, 100.0)
    rsi[avg_gain.isna() | avg_loss.isna()] = np.nan
    return rsi


def measure(bars):
    H = 5
    THR = -5.0
    MIN_CASES = 30
    comp_col = "debug_info.components.rsi_high.last_history_value"

    # ---------- decide how to read the component's raw value (from its scale only) ----------
    all_raw = []
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w]
            if comp_col in df.columns:
                all_raw.append(pd.to_numeric(df[comp_col], errors="coerce").dropna().values)
    all_raw = np.concatenate(all_raw) if len(all_raw) else np.array([])
    if all_raw.size > 0 and all_raw.min() >= 0 and all_raw.max() <= 100 and np.median(all_raw) > 20:
        raw_mode = "rsi"
    elif all_raw.size > 0 and np.nanmax(np.abs(all_raw)) > 15:
        raw_mode = "fifty_minus_rsi"
    else:
        raw_mode = "recompute"

    # ---------- situation check ----------
    active_n = 0
    agree_n = 0
    for coin in bars:
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if raw_mode == "rsi":
                rsi = pd.to_numeric(df[comp_col], errors="coerce") if comp_col in df.columns else pd.Series(np.nan, index=df.index)
            elif raw_mode == "fifty_minus_rsi":
                rsi = 50.0 - pd.to_numeric(df[comp_col], errors="coerce") if comp_col in df.columns else pd.Series(np.nan, index=df.index)
            else:
                rsi = _wilder_rsi(close, 14)
            mask = fc.notna() & (fc != 0) & rsi.notna()
            active_n += int(mask.sum())
            agree_n += int((mask & (rsi > 50) & (fc < 0)).sum())
    agreement = float(agree_n / active_n) if active_n > 0 else 0.0
    passed = bool(active_n > 0 and agreement >= 0.9)

    reading_base = (
        f"Situation RSI>50 with a short forecast, RSI read as '{raw_mode}' from the component column's scale "
        "(recomputed as 14-bar Wilder RSI inside each window if it looks standardised); cases are grid bars 0,5,10,... "
        "of each window with forecast <= -5 and a 5-bar forward return inside the window; the coin mean is the mean "
        "5-bar return on the same grid over all its windows; a coin with no case does not count as negative in the "
        "4-of-6 check; fewer than 30 cases is reported as not observable."
    )

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {
                "name": "pooled mean 5-bar excess return of extreme high-RSI cases",
                "value": None,
                "statistic": None,
                "threshold": "mean < 0 with t <= -2 on at least 30 cases (confirm); mean > 0 with t >= +2 (reject)",
            },
            "supporting_check": None,
            "counts": {"active bars": active_n, "active bars in situation on short side": agree_n},
            "decided_by": f"Only {agreement:.1%} of active bars are bars with RSI above 50 and a short forecast, below the 90% required by the plan's situation.",
            "reading": reading_base,
        }

    # ---------- main measure ----------
    excess_all = []
    per_coin_mean = {}
    per_coin_n = {}
    for coin in bars:
        grid_rets = []
        case_rets = []
        for w in bars[coin]:
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[t]) and fc[t] <= THR:
                    case_rets.append(r)
        if len(grid_rets) == 0:
            continue
        mu = float(np.mean(grid_rets))
        ex = [r - mu for r in case_rets]
        excess_all.extend(ex)
        per_coin_n[coin] = len(ex)
        per_coin_mean[coin] = float(np.mean(ex)) if len(ex) else None

    n_cases = len(excess_all)
    if n_cases >= 2:
        arr = np.array(excess_all)
        mean_ex = float(arr.mean())
        sd = float(arr.std(ddof=1))
        t_stat = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else (0.0 if mean_ex == 0 else float(np.sign(mean_ex) * np.inf))
    elif n_cases == 1:
        mean_ex, t_stat = float(excess_all[0]), None
    else:
        mean_ex, t_stat = None, None

    neg_coins = int(sum(1 for c, m in per_coin_mean.items() if m is not None and m < 0))
    support_pass = neg_coins >= 4

    counts = {"cases": n_cases, "coins with negative mean excess": neg_coins}
    for c in per_coin_n:
        counts[f"cases {c}"] = per_coin_n[c]

    if n_cases < MIN_CASES or t_stat is None:
        status = "not observable"
        decided = f"Only {n_cases} extreme cases (forecast <= -5 on the 5-bar grid), below the plan's minimum of 30."
    elif mean_ex < 0 and t_stat <= -2 and support_pass:
        status = "confirmed"
        decided = "Pooled mean excess return is below 0 with t <= -2 on at least 30 cases and at least 4 of 6 coins are negative."
    elif mean_ex > 0 and t_stat >= 2:
        status = "rejected"
        decided = "Pooled mean excess return is above 0 with t >= +2 on at least 30 cases: price rises more than usual after extreme high RSI."
    elif t_stat <= -2 and not support_pass:
        status = "inconclusive"
        decided = "t <= -2 but fewer than 4 of the 6 coins have a negative mean excess return (coin check fails)."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "pooled mean 5-bar excess return of extreme high-RSI cases",
            "value": mean_ex,
            "statistic": {"name": "ordinary t of the mean", "value": t_stat} if t_stat is not None and np.isfinite(t_stat) else None,
            "threshold": "mean < 0 with t <= -2 on at least 30 cases (confirm); mean > 0 with t >= +2 on at least 30 cases (reject)",
        },
        "supporting_check": {
            "name": "coins with negative mean excess return (need >= 4 of 6)",
            "value": neg_coins,
            "passed": bool(support_pass),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
