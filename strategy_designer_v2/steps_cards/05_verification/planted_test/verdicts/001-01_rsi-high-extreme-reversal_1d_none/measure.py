import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    COMP_COL = "debug_info.components.rsi_high.last_history_value"
    SCALING = 0.4
    EXTREME = -10.0
    MIN_CASES = 30
    T_THR = 2.0
    MIN_NEG_COINS = 2

    # ---------- 1. Situation check: RSI(14) above 50, short side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            if "forecast" not in df.columns or COMP_COL not in df.columns:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[COMP_COL], errors="coerce")
            ok = fc.notna() & raw.notna()
            active = ok & (fc != 0)
            rsi = 50.0 - raw / SCALING
            situation = rsi > 50.0
            agree = active & situation & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = ("pooled excess forward 5-bar return after forecast <= -10 "
                 "(minus same coin/window mean forward 5-bar return), non-overlapping")
    threshold_txt = ("confirm if excess < 0 with t <= -2 and negative in >= 2 coins; "
                     "reject if excess > 0 with t >= +2; inconclusive if -2 < t < +2 "
                     "or fewer than 30 non-overlapping extreme cases")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars "
                           "with RSI(14) above 50, so the config does not trade the plan's "
                           "situation (high RSI, short side)."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    pooled = []
    per_coin = {}
    for coin, wins in bars.items():
        coin_vals = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            fwd = close.shift(-H) / close - 1.0  # within window only
            baseline = fwd.mean(skipna=True)  # all bars of this coin/window with a defined forward return
            if not np.isfinite(baseline):
                continue
            pos = np.arange(len(df))
            grid = (pos % H) == 0
            sel = grid & fc.notna().values & (fc.values <= EXTREME) & fwd.notna().values
            ex = (fwd.values[sel] - baseline).astype(float)
            ex = ex[np.isfinite(ex)]
            coin_vals.extend(ex.tolist())
        per_coin[coin] = coin_vals
        pooled.extend(coin_vals)

    pooled = np.asarray(pooled, dtype=float)
    n = int(len(pooled))
    mean = float(pooled.mean()) if n > 0 else None
    t = None
    if n >= 2:
        sd = pooled.std(ddof=1)
        if sd > 0:
            t = float(mean / (sd / np.sqrt(n)))

    coin_means = {c: (float(np.mean(v)) if len(v) > 0 else None) for c, v in per_coin.items()}
    n_neg_coins = int(sum(1 for m in coin_means.values() if m is not None and m < 0))
    supp_passed = bool(n_neg_coins >= MIN_NEG_COINS)

    counts = {"non-overlapping extreme cases pooled": n,
              "coins with negative excess": n_neg_coins,
              "coins in record": int(len(per_coin))}
    for c, v in per_coin.items():
        counts["extreme cases " + str(c)] = int(len(v))

    if n < MIN_CASES:
        status = "inconclusive"
        decided = "Fewer than 30 non-overlapping extreme cases pooled, so the plan's inconclusive rule applies."
    elif t is None or not np.isfinite(t):
        status = "inconclusive"
        decided = "The t-statistic cannot be computed, so no confirm or reject rule is met (inconclusive)."
    elif mean < 0 and t <= -T_THR and supp_passed:
        status = "confirmed"
        decided = ("The pooled excess forward return is negative with t <= -2 and is negative "
                   "in at least 2 coins, meeting the confirm rule.")
    elif mean > 0 and t >= T_THR:
        status = "rejected"
        decided = "The pooled excess forward return is positive with t >= +2, meeting the reject rule (continuation)."
    elif -T_THR < t < T_THR:
        status = "inconclusive"
        decided = "The t-statistic lies strictly between -2 and +2, meeting the inconclusive rule."
    else:
        status = "inconclusive"
        decided = ("t <= -2 but the excess return is negative in fewer than 2 coins, so neither "
                   "confirm nor reject is met (inconclusive).")

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "number of coins with negative mean excess forward return (need >= 2)",
            "value": n_neg_coins,
            "passed": supp_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The holding baseline is the mean forward 5-bar return over every bar of the "
                    "coin/window that has one, extreme cases are grid bars (positions 0,5,10,... "
                    "per window) with forecast <= -10, and with only the coins present in the "
                    "record the rule 'negative in at least 2 of the 3 coins' needs at least 2 "
                    "of those coins negative, with a coin that has no cases not counting as negative."),
    }
