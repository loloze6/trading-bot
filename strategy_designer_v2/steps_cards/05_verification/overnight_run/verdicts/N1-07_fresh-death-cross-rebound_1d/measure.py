import numpy as np
import pandas as pd


def measure(bars):
    SPREAD = "debug_info.components.cross_depth.last_history_value"
    H = 10

    def fnum(x):
        if x is None:
            return None
        try:
            x = float(x)
        except Exception:
            return None
        if not np.isfinite(x):
            return None
        return x

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            if SPREAD in df.columns:
                s = pd.to_numeric(df[SPREAD], errors="coerce").values
            else:
                s = np.full(len(df), np.nan)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            run = 0
            sit = np.zeros(len(df), dtype=bool)
            for i in range(len(df)):
                v = s[i]
                if np.isfinite(v) and v < 0:
                    run += 1
                else:
                    run = 0
                # age = -run; fresh death cross when 1 <= run <= 20
                # (a run touching the window start is a lower bound on age; kept if <= 20)
                sit[i] = (run >= 1) and (run <= 20)
            for i in range(len(df)):
                f = fc[i]
                if np.isfinite(f) and f != 0:
                    n_active += 1
                    if sit[i] and f > 0:
                        n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": fnum(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 percent of active bars are long bars in which SMA50 has been "
                           "below SMA200 for 1 to 20 bars (fresh death cross), as the Fidelity requires."
                           if n_active > 0 else "The record has no active bars to compare with the plan's situation."),
            "reading": "Age of the death cross was taken as the length of the current run of negative SMA50-SMA200 spread within the window; a run that starts at the window's first row counts as fresh if it is at most 20 bars long.",
        }

    # ---------- 2. criterion ----------
    hold10 = {}
    hold1 = {}
    for coin, wins in bars.items():
        r10_all = []
        r1_all = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            n = len(c)
            for i in range(0, n, H):
                if i + H < n and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    r10_all.append(c[i + H] / c[i] - 1.0)
            for i in range(n - 1):
                if np.isfinite(c[i]) and np.isfinite(c[i + 1]) and c[i] > 0:
                    r1_all.append(c[i + 1] / c[i] - 1.0)
        hold10[coin] = float(np.mean(r10_all)) if len(r10_all) else np.nan
        hold1[coin] = float(np.mean(r1_all)) if len(r1_all) else np.nan

    excess = []
    clusters = []
    sup_num = 0.0
    sup_den = 0.0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            n = len(df)
            c = pd.to_numeric(df["close"], errors="coerce").values
            if "regime" in df.columns:
                reg = (df["regime"].astype(str) == "mean_reversion").values
            else:
                reg = np.zeros(n, dtype=bool)
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").values
            ev = np.full(n, -1)
            k = -1
            for i in range(n):
                if reg[i]:
                    if i == 0 or not reg[i - 1]:
                        k += 1
                    ev[i] = k
            for i in range(0, n, H):
                if reg[i] and i + H < n and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0 \
                        and np.isfinite(hold10[coin]):
                    excess.append(c[i + H] / c[i] - 1.0 - hold10[coin])
                    clusters.append(str(coin) + "|" + str(w) + "|" + str(int(ev[i])))
            for i in range(n - 1):
                if reg[i] and np.isfinite(alloc[i]) and np.isfinite(c[i]) and np.isfinite(c[i + 1]) \
                        and c[i] > 0 and np.isfinite(hold1[coin]):
                    r1 = c[i + 1] / c[i] - 1.0
                    sup_num += alloc[i] * (r1 - hold1[coin])
                    sup_den += alloc[i]

    excess = np.array(excess, dtype=float)
    n_blocks = int(len(excess))
    uniq = sorted(set(clusters))
    n_events = int(len(uniq))

    mean_ex = float(np.mean(excess)) if n_blocks > 0 else np.nan
    t = np.nan
    if n_blocks > 1 and n_events > 1:
        cl = np.array(clusters)
        resid = excess - mean_ex
        sums = np.array([resid[cl == g].sum() for g in uniq])
        G = float(n_events)
        var = (G / (G - 1.0)) * np.sum(sums ** 2) / (n_blocks ** 2)
        if var > 0:
            t = mean_ex / np.sqrt(var)

    sup_val = (sup_num / sup_den) if sup_den > 0 else np.nan
    if np.isfinite(sup_val) and np.isfinite(mean_ex):
        sup_passed = bool(np.sign(sup_val) == np.sign(mean_ex))
    else:
        sup_passed = None

    if n_events < 15 or n_blocks < 30:
        status = "not observable"
        decided = ("Minimum not reached: " + str(n_events) + " distinct death-cross events (need 15) and "
                   + str(n_blocks) + " non-overlapping 10-bar blocks (need 30).")
    elif np.isfinite(t) and mean_ex > 0 and t >= 2 and np.isfinite(sup_val) and sup_val > 0:
        status = "confirmed"
        decided = "Mean excess 10-bar return is above 0 with clustered t >= +2 and the position-weighted excess is positive."
    elif np.isfinite(t) and mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "Mean excess 10-bar return is below 0 with clustered t <= -2."
    else:
        status = "inconclusive"
        decided = "Enough events and blocks, but the numbers meet neither the confirm rule nor the reject rule (t between -2 and +2, or confirm's supporting check not positive)."

    return {
        "status": status,
        "situation_check": {"agreement": fnum(agreement), "passed": True},
        "main_measure": {
            "name": "mean 10-bar forward return on fresh-death-cross bars minus coin's mean 10-bar return",
            "value": fnum(mean_ex),
            "statistic": {"name": "t clustered by cross event", "value": fnum(t)},
            "threshold": "confirm if above 0 with t >= +2 and supporting check positive; reject if below 0 with t <= -2",
        },
        "supporting_check": {
            "name": "allocation-weighted 1-bar return on regime bars minus coin's mean 1-bar return",
            "value": fnum(sup_val),
            "passed": sup_passed,
        },
        "counts": {
            "distinct death-cross events": n_events,
            "non-overlapping 10-bar blocks": n_blocks,
        },
        "decided_by": decided,
        "reading": ("Regime bars are those labelled mean_reversion, blocks are the window grid bars 0,10,20,... on those bars, "
                    "holding is the coin's mean grid 10-bar return over all its windows, an event is one contiguous run of regime "
                    "bars in a window and the clustered t uses the CR1 cluster variance of the mean, both minimums (15 events and "
                    "30 blocks) must be reached, and the supporting check is sum(alloc x (1-bar return - coin's mean 1-bar return)) "
                    "/ sum(alloc) over regime bars."),
    }
