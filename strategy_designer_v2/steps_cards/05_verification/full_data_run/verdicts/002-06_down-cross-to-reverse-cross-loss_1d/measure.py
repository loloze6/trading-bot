import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LHV = "debug_info.components.sma_cross_spread.last_history_value"
    H = 1
    MIN_COUNT = 300

    # ---------- collect per-coin data ----------
    coin_rows = []      # rows with forecast < 0 and a valid next return
    n_active = 0
    n_agree = 0

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        all_rets = []
        frames = []
        for w in sorted(wins.keys(), key=lambda s: int(str(s).lstrip("w")) if str(s).lstrip("w").isdigit() else str(s)):
            df = wins[w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if LHV in df.columns:
                lhv = pd.to_numeric(df[LHV], errors="coerce").to_numpy(dtype=float)
            else:
                lhv = np.full(len(df), np.nan)
            n = len(df)
            nxt = np.full(n, np.nan)
            if n > H:
                nxt[:-H] = close[H:] / close[:-H] - 1.0
            # grid of positions 0, h, 2h, ... (h = 1: every bar)
            grid = np.arange(0, n, H)
            all_rets.append(nxt[grid])

            # situation check on active bars
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            agree = active & np.isfinite(lhv) & (lhv < 0) & (fc < 0)
            n_agree += int(agree.sum())

            frames.append((fc[grid], nxt[grid]))

        rets = np.concatenate(all_rets) if all_rets else np.array([])
        rets = rets[np.isfinite(rets)]
        mu = float(rets.mean()) if rets.size else np.nan
        for fc, nxt in frames:
            m = np.isfinite(fc) & (fc < 0) & np.isfinite(nxt)
            for f, r in zip(fc[m], nxt[m]):
                coin_rows.append((coin, f, r, mu))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "|forecast|-weighted mean excess short 1-bar return (next return minus coin all-window mean, sign flipped), pooled"
    threshold = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; else inconclusive; fewer than 300 pooled bars with forecast < 0 is not observable"
    reading_base = ("Situation taken as last_history_value of sma_cross_spread < 0 (50-day SMA below 200-day SMA) with forecast < 0 on active bars; "
                    "the weighted mean is sum(-(r-mu)|f|)/sum(|f|) with its t the ordinary t of the values -(r-mu)|f|/mean|f| (each bar once, h=1); "
                    "mu is the coin's mean next-bar return over all its windows; the 300-bar minimum counts bars with forecast < 0 and a valid next return; "
                    "the supporting check passes when the share below the mean exceeds 50% with binomial z >= 2.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are short bars where the 50-day SMA is below the 200-day SMA "
                           "(raw spread < 0), so the config's forecast does not follow the plan's below-cross situation."
                           if n_active > 0 else "No bar has a non-zero forecast, so the situation cannot be matched."),
            "reading": reading_base,
        }

    n = len(coin_rows)
    counts = {"pooled bars with forecast below 0": int(n)}

    if n < MIN_COUNT:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"The pooled count of bars with forecast below 0 is {n}, below the plan's minimum of 300.",
            "reading": reading_base,
        }

    f = np.array([c[1] for c in coin_rows], dtype=float)
    r = np.array([c[2] for c in coin_rows], dtype=float)
    mu = np.array([c[3] for c in coin_rows], dtype=float)
    w = np.abs(f)
    x = -(r - mu)
    wmean = float(np.sum(x * w) / np.sum(w))
    y = x * w / w.mean()
    sd = float(np.std(y, ddof=1)) if n > 1 else np.nan
    t = float(y.mean() / (sd / np.sqrt(n))) if sd and np.isfinite(sd) and sd > 0 else 0.0

    k = int(np.sum(r < mu))
    share = k / n
    z = float((k - 0.5 * n) / np.sqrt(0.25 * n))
    sup_pass = bool(z >= 2.0)

    if wmean > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The weighted mean excess short return is above 0 with t >= 2 and the supporting share check passes."
        else:
            status = "inconclusive"
            decided = "The weighted mean excess short return is above 0 with t >= 2, but the supporting share check fails, so the confirm is not granted."
    elif wmean < 0 and t <= -2:
        status = "rejected"
        decided = "The weighted mean excess short return is below 0 with t <= -2, which reads as reversal during below-cross spans."
    else:
        status = "inconclusive"
        decided = "The t-statistic of the weighted mean excess short return lies between -2 and 2."

    counts["bars with next return below coin mean"] = k

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": wmean,
                         "statistic": {"name": "t of the weighted mean", "value": t},
                         "threshold": threshold},
        "supporting_check": {"name": "share of forecast<0 bars with next return below coin mean, binomial z vs 50%",
                             "value": z, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base + f" (share below mean = {share:.4f}).",
    }
