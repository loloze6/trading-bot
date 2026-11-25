import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LOC = "debug_info.components.close_loc.last_history_value"
    PROFILE_REGIME = "unknown"  # the regime left when neither 'chop' veto fires: falling and agitated

    # ---------- coin mean daily return over all windows (pooled, inside windows only) ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            if len(c) > 1:
                rets.append(c[1:] / c[:-1] - 1.0)
        coin_mu[coin] = float(np.mean(np.concatenate(rets))) if rets else np.nan

    # ---------- gather per-bar data ----------
    active_total = 0
    active_ok = 0
    top, mid = [], []
    timing = []
    for coin, wins in bars.items():
        mu = coin_mu[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            h = df["high"].astype(float)
            l = df["low"].astype(float)
            nxt = c.shift(-1) / c - 1.0  # inside this window only
            fc = df["forecast"].astype(float).fillna(0.0)
            regime = df["regime"].astype(str)
            rng = (h - l)
            loc_price = np.where(rng > 0, (c - l) / rng.where(rng > 0, np.nan), np.nan)
            loc_price = pd.Series(loc_price)
            raw = df[LOC].astype(float) if LOC in df.columns else pd.Series(np.nan, index=df.index)
            loc_raw = raw.where(raw.notna(), loc_price)

            # situation check: profile bar (regime detector's decision), close above the low
            # (graded location > 0), short side
            in_profile = regime == PROFILE_REGIME
            situ = in_profile & (loc_raw > 0)
            active = fc != 0
            active_total += int(active.sum())
            active_ok += int((active & situ & (fc < 0)).sum())

            # main measure: profile bars where close_loc is recorded
            rec = raw.notna() & in_profile & nxt.notna()
            ab = nxt - mu
            top.extend(ab[rec & (raw >= 2.0 / 3.0)].tolist())
            mid.extend(ab[rec & (raw >= 1.0 / 3.0) & (raw < 2.0 / 3.0)].tolist())

            # supporting check: timing gain on bars in a position
            pos = df["postRebalance_current_allocation"].astype(float)
            m = pos.notna() & (pos != 0) & nxt.notna()
            timing.extend((pos[m] * nxt[m] - pos[m] * mu).tolist())

    agreement = active_ok / active_total if active_total > 0 else 0.0
    passed = bool(active_total > 0 and agreement >= 0.9)

    reading = ("The profile is read from the recorded regime ('unknown', the regime left when neither chop veto fires, "
               "since the detector's components are not recorded) with the situation being any close above the day's low "
               "on the short side; the groups are top = raw close location >= 2/3 and middle = 1/3 <= location < 2/3 "
               "on profile bars where close_loc is recorded, every bar used (1-bar horizon, no overlap), the timing gain "
               "pooled over all coins' bars in a position, and the plan's 'fewer than 30 per group' minimum is reported "
               "as not observable as the workflow requires.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(active_total), "active bars in situation on short side": int(active_ok)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars of the falling agitated "
                           "profile with a close above the day's low, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    n_top, n_mid = len(top), len(mid)
    diff = float(np.mean(top) - np.mean(mid)) if n_top > 0 and n_mid > 0 else None
    t = None
    if n_top >= 2 and n_mid >= 2:
        tt = stats.ttest_ind(np.array(top), np.array(mid), equal_var=False).statistic
        t = float(tt) if np.isfinite(tt) else None

    tim = float(np.mean(timing)) if len(timing) > 0 else None
    sup_pass = (tim > 0) if tim is not None else None

    counts = {"bars in top group": int(n_top), "bars in middle group": int(n_mid),
              "bars in a position": int(len(timing))}

    if n_top < 30 or n_mid < 30:
        status = "not observable"
        decided = "The plan's minimum of 30 bars in each of the two groups is not reached."
    elif t is None:
        status = "inconclusive"
        decided = "The Welch t could not be computed, so it meets neither the confirm nor the reject rule."
    elif t <= -2:
        if sup_pass:
            status = "confirmed"
            decided = "The top-minus-middle Welch t is -2 or less and the timing gain is above 0 (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The Welch t is -2 or less but the timing gain is 0 or below (inconclusive rule)."
    elif t >= 2:
        status = "rejected"
        decided = "The top-minus-middle Welch t is +2 or more (reject rule)."
    else:
        status = "inconclusive"
        decided = "The top-minus-middle Welch t lies between -2 and +2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "top-minus-middle close-location group mean next-day return net of coin mean",
            "value": diff,
            "statistic": {"name": "Welch t", "value": t} if t is not None else None,
            "threshold": "confirm at Welch t <= -2 (with timing gain > 0), reject at Welch t >= +2",
        },
        "supporting_check": {
            "name": "mean timing gain per bar in a position (position x (next return - coin mean))",
            "value": tim,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
