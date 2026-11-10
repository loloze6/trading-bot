import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5

    def _greedy_nonoverlap(idx_positions, h):
        # Keep a bar only if it starts at least h bars after the last kept bar.
        kept = []
        last = None
        for p in idx_positions:
            if last is None or p - last >= h:
                kept.append(p)
                last = p
        return kept

    # Build forward returns per coin/window. Returns never cross windows.
    frames = []
    for coin in sorted(bars.keys()):
        for window in sorted(bars[coin].keys()):
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            d = df[["close", "forecast"]].copy().reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            d["fwd"] = close.shift(-H) / close - 1.0
            d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce")
            d["pos"] = np.arange(len(d))
            d["coin"] = coin
            d["window"] = window
            d = d.dropna(subset=["forecast", "fwd"])
            frames.append(d)

    empty = {
        "status": "inconclusive",
        "main_measure": {"name": "top-quintile minus zero-forecast forward 5-bar return",
                         "value": None,
                         "threshold": "> 0 with t-stat >= 2 (pooled, non-overlapping), positive in >= 2 coins"},
        "supporting_check": {"name": "Spearman rank correlation of forecast vs forward 5-bar return (forecast > 0)",
                             "value": None, "passed": None},
        "cases": 0,
        "decided_by": "Fewer than 30 pooled non-overlapping top-quintile cases, so inconclusive.",
        "reading": "none",
    }
    if not frames:
        return empty
    allb = pd.concat(frames, ignore_index=True)

    positive = allb[allb["forecast"] > 0]
    if len(positive) == 0:
        return empty
    q80 = float(np.quantile(positive["forecast"].values, 0.8))

    top_samples, zero_samples, pos_samples = [], [], []
    for (coin, window), g in allb.groupby(["coin", "window"], sort=True):
        g = g.sort_values("pos")
        for mask, store in (
            (g["forecast"] >= q80, top_samples),
            (g["forecast"] == 0, zero_samples),
            (g["forecast"] > 0, pos_samples),
        ):
            sub = g[mask & (g["forecast"] > 0) if store is top_samples else mask]
            keep = set(_greedy_nonoverlap(sub["pos"].tolist(), H))
            sub = sub[sub["pos"].isin(keep)]
            store.append(sub[["coin", "window", "forecast", "fwd"]])

    top = pd.concat(top_samples, ignore_index=True) if top_samples else pd.DataFrame(columns=["coin", "fwd", "forecast"])
    zero = pd.concat(zero_samples, ignore_index=True) if zero_samples else pd.DataFrame(columns=["coin", "fwd", "forecast"])
    posb = pd.concat(pos_samples, ignore_index=True) if pos_samples else pd.DataFrame(columns=["coin", "fwd", "forecast"])

    def _excess_t(a, b):
        a = np.asarray(a, dtype=float)
        b = np.asarray(b, dtype=float)
        if len(a) == 0 or len(b) == 0:
            return None, None
        ex = float(a.mean() - b.mean())
        if len(a) < 2 or len(b) < 2:
            return ex, None
        t, _ = stats.ttest_ind(a, b, equal_var=False)
        t = float(t) if np.isfinite(t) else None
        return ex, t

    pooled_ex, pooled_t = _excess_t(top["fwd"].values, zero["fwd"].values)
    n_top = int(len(top))

    coins = sorted(allb["coin"].unique().tolist())
    per_coin = {}
    for c in coins:
        ex_c, _ = _excess_t(top.loc[top["coin"] == c, "fwd"].values,
                            zero.loc[zero["coin"] == c, "fwd"].values)
        per_coin[c] = {"excess": ex_c, "n_top": int((top["coin"] == c).sum())}

    # Supporting check
    rho = None
    passed = None
    if len(posb) >= 3 and posb["forecast"].nunique() > 1 and posb["fwd"].nunique() > 1:
        r, _ = stats.spearmanr(posb["forecast"].values, posb["fwd"].values)
        if np.isfinite(r):
            rho = float(r)
            passed = bool(rho > 0)

    n_pos_coins = sum(1 for c in coins if per_coin[c]["excess"] is not None and per_coin[c]["excess"] > 0)
    n_nonpos_coins = sum(1 for c in coins if per_coin[c]["excess"] is not None and per_coin[c]["excess"] <= 0)
    min_coin_cases = min((per_coin[c]["n_top"] for c in coins), default=0)

    if n_top < 30 or min_coin_cases < 8 or pooled_ex is None:
        status = "inconclusive"
        decided_by = (f"Too few non-overlapping top-quintile cases ({n_top} pooled, minimum {min_coin_cases} "
                      f"for one coin; need 30 pooled and 8 per coin), so inconclusive.")
    elif pooled_ex > 0 and pooled_t is not None and pooled_t >= 2 and n_pos_coins >= 2:
        status = "confirmed"
        decided_by = (f"Pooled excess return is above 0 with t = {pooled_t:.2f} >= 2 and positive in "
                      f"{n_pos_coins} coins (>= 2), so confirmed.")
    elif pooled_ex <= 0 and n_nonpos_coins >= 2:
        status = "rejected"
        decided_by = (f"Pooled excess return is at or below 0 and non-positive in {n_nonpos_coins} coins (>= 2), "
                      f"so rejected.")
    else:
        status = "inconclusive"
        decided_by = ("The pooled excess return is positive with a t-statistic below 2, or the coins disagree "
                      "beyond the confirm/reject rules, so inconclusive.")

    return {
        "status": status,
        "main_measure": {
            "name": "top-quintile minus zero-forecast forward 5-bar return",
            "value": pooled_ex,
            "threshold": "> 0 with t-stat >= 2 (pooled, non-overlapping), positive in >= 2 coins",
        },
        "supporting_check": {
            "name": "Spearman rank correlation of forecast vs forward 5-bar return (forecast > 0)",
            "value": rho,
            "passed": passed,
        },
        "cases": n_top,
        "decided_by": decided_by,
        "reading": ("Top quintile is forecast >= the 80th percentile of all positive forecasts pooled across coins "
                    "and windows; non-overlap is enforced greedily within each coin-window for each group (top, zero, "
                    "positive) keeping bars at least 5 bars apart; the t-statistic is Welch's two-sample t of top versus "
                    "zero samples; with only the coins present in the record, 'at least 2 of the 3 coins' is applied as "
                    "a count of at least 2 among those coins (so both when two are present); the supporting check "
                    "passes if the Spearman correlation is above 0 and does not enter the decision."),
    }
