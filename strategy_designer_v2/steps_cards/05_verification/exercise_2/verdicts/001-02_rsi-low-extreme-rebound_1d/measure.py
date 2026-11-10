import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    MIN_POOLED = 30
    MIN_PER_COIN = 8
    COINS_NEEDED = 2  # "at least 2 of the 3 coins", kept literally

    # Gather every bar with a forecast and a forward 5-bar return, never across windows.
    rows = []
    for coin, wins in bars.items():
        for win, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(d)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            for i in range(n):
                if np.isfinite(fc[i]) and np.isfinite(fwd[i]):
                    rows.append((coin, win, i, fc[i], fwd[i]))

    base = {
        "main_measure": {
            "name": "top-quintile forecast fwd 5-bar return minus forecast-0 fwd 5-bar return",
            "value": None,
            "threshold": "above 0 with t-statistic >= 2 (non-overlapping), positive in >= 2 coins",
        },
        "supporting_check": {
            "name": "Spearman rank corr of forecast vs fwd 5-bar return, positive-forecast bars",
            "value": None,
            "passed": None,
        },
        "cases": 0,
        "reading": (
            "Top quintile means positive forecasts at or above the 80th percentile of all positive forecasts "
            "pooled across coins and windows; non-overlapping samples are chosen greedily in time within each "
            "window and group (a bar is kept only if at least 5 bars after the last kept bar of that group); the "
            "t-statistic is Welch's two-sample t; the supporting check uses all positive-forecast bars and passes "
            "if the correlation is above 0; with only 2 coins in the record the '2 of the 3 coins' rules are kept "
            "at 2 coins."
        ),
    }

    if not rows:
        base["status"] = "inconclusive"
        base["decided_by"] = "No usable bars, so the test is inconclusive."
        return base

    df = pd.DataFrame(rows, columns=["coin", "win", "i", "fc", "fwd"])
    pos = df[df["fc"] > 0]
    zero = df[df["fc"] == 0]

    # Supporting check
    if len(pos) >= 3 and pos["fc"].nunique() > 1:
        rho = stats.spearmanr(pos["fc"], pos["fwd"]).correlation
        if np.isfinite(rho):
            base["supporting_check"]["value"] = float(rho)
            base["supporting_check"]["passed"] = bool(rho > 0)

    if len(pos) == 0:
        base["status"] = "inconclusive"
        base["decided_by"] = "No positive forecasts, so fewer than 30 top-quintile cases: inconclusive."
        return base

    q80 = float(np.quantile(pos["fc"].to_numpy(), 0.8))
    top = pos[pos["fc"] >= q80]

    def non_overlap(sub):
        keep = []
        for (_, _), g in sub.sort_values(["coin", "win", "i"]).groupby(["coin", "win"], sort=True):
            last = -10 ** 9
            for idx, i in zip(g.index, g["i"]):
                if i - last >= H:
                    keep.append(idx)
                    last = i
        return sub.loc[keep]

    top_no = non_overlap(top)
    zero_no = non_overlap(zero)

    n_top = len(top_no)
    base["cases"] = int(n_top)

    excess = None
    tstat = None
    if n_top > 0 and len(zero_no) > 0:
        excess = float(top_no["fwd"].mean() - zero_no["fwd"].mean())
        if n_top >= 2 and len(zero_no) >= 2:
            t = stats.ttest_ind(top_no["fwd"], zero_no["fwd"], equal_var=False).statistic
            tstat = float(t) if np.isfinite(t) else None
    base["main_measure"]["value"] = excess

    coins = sorted(bars.keys())
    per_coin = {}
    for c in coins:
        tc = top_no[top_no["coin"] == c]
        zc = zero_no[zero_no["coin"] == c]
        ex = float(tc["fwd"].mean() - zc["fwd"].mean()) if len(tc) > 0 and len(zc) > 0 else None
        per_coin[c] = {"n_top": int(len(tc)), "n_zero": int(len(zc)), "excess": ex}

    n_pos_coins = sum(1 for v in per_coin.values() if v["excess"] is not None and v["excess"] > 0)
    n_nonpos_coins = sum(1 for v in per_coin.values() if v["excess"] is not None and v["excess"] <= 0)
    min_coin_n = min(v["n_top"] for v in per_coin.values()) if per_coin else 0

    tstr = "nan" if tstat is None else f"{tstat:.2f}"
    if n_top < MIN_POOLED or min_coin_n < MIN_PER_COIN:
        status = "inconclusive"
        decided = (f"Inconclusive: {n_top} pooled non-overlapping top-quintile cases (need 30) and "
                   f"at least {min_coin_n} per coin (need 8).")
    elif excess is None:
        status = "inconclusive"
        decided = "Inconclusive: no non-overlapping forecast-0 samples to compare against."
    elif excess > 0 and tstat is not None and tstat >= 2 and n_pos_coins >= COINS_NEEDED:
        status = "confirmed"
        decided = (f"Confirmed: pooled excess {excess:.4f} > 0 with t = {tstr} >= 2, "
                   f"positive in {n_pos_coins} coins (need 2).")
    elif excess <= 0 and n_nonpos_coins >= COINS_NEEDED:
        status = "rejected"
        decided = (f"Rejected: pooled excess {excess:.4f} <= 0 and non-positive in "
                   f"{n_nonpos_coins} coins (need 2).")
    else:
        status = "inconclusive"
        decided = (f"Inconclusive: pooled excess {excess:.4f}, t = {tstr}, positive in {n_pos_coins} "
                   f"and non-positive in {n_nonpos_coins} coins, meeting neither confirm nor reject.")

    base["status"] = status
    base["decided_by"] = decided
    return base
