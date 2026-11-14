import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LHV = "debug_info.components.drop.last_history_value"
    THRESH = 16.0
    MIN_N = 100

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp") if "timestamp" in df.columns else df
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            ret1 = close.pct_change()  # one-day return, inside this window only
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce")
                raw = raw.where(raw.notna(), ret1)
            else:
                raw = ret1
            active = fc.notna() & (fc != 0)
            situation = raw < 0  # graded situation: a one-day drop (only drops count)
            agree = active & situation & (fc > 0)  # long side expected (rebound = rise)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are one-day drops held long, "
                          "so the config does not take the plan's situation (a drop) on the long side.",
            "reading": "The adapted graded situation is read as any one-day drop (negative component value or "
                       "close-to-close return), on the long side.",
        }

    # ---------- 2. criterion ----------
    q_rets = []          # next-bar returns on qualifying bars
    q_excess = []        # next-bar return minus coin's mean daily return
    all_pos = 0
    all_n = 0
    for coin, wins in bars.items():
        coin_rets = []
        coin_q = []
        for w, df in wins.items():
            df = df.sort_values("timestamp") if "timestamp" in df.columns else df
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if len(close) < 2:
                continue
            nxt = close[1:] / close[:-1] - 1.0
            fc_t = fc[:-1]
            ok = np.isfinite(nxt)
            coin_rets.append(nxt[ok])
            qm = ok & np.isfinite(fc_t) & (fc_t >= THRESH)
            coin_q.append(nxt[qm])
        if not coin_rets:
            continue
        cr = np.concatenate(coin_rets)
        cq = np.concatenate(coin_q) if coin_q else np.array([])
        if cr.size == 0:
            continue
        all_pos += int((cr > 0).sum())
        all_n += int(cr.size)
        cmean = float(cr.mean())
        q_rets.append(cq)
        q_excess.append(cq - cmean)

    q = np.concatenate(q_rets) if q_rets else np.array([])
    qe = np.concatenate(q_excess) if q_excess else np.array([])
    n_q = int(q.size)

    p1 = float((q > 0).mean()) if n_q > 0 else None
    p2 = all_pos / all_n if all_n > 0 else None

    hit_excess = None
    z = None
    if n_q > 0 and all_n > 0:
        hit_excess = p1 - p2
        pp = (int((q > 0).sum()) + all_pos) / (n_q + all_n)
        se = np.sqrt(pp * (1 - pp) * (1.0 / n_q + 1.0 / all_n))
        z = float(hit_excess / se) if se > 0 else 0.0

    sup_val = None
    sup_t = None
    sup_pass = None
    if n_q >= 2:
        sup_val = float(qe.mean())
        sd = qe.std(ddof=1)
        sup_t = float(sup_val / (sd / np.sqrt(n_q))) if sd > 0 else None
        sup_pass = bool(sup_val > 0)
    elif n_q == 1:
        sup_val = float(qe.mean())
        sup_pass = bool(sup_val > 0)

    if n_q < MIN_N:
        status = "not observable"
        decided = f"Only {n_q} qualifying bars (forecast >= 16) against the plan's minimum of 100."
    elif z >= 2 and hit_excess > 0:
        status = "confirmed"
        decided = "The hit-rate excess is positive with z >= 2 over at least 100 qualifying bars."
    elif z <= -2 and hit_excess < 0:
        status = "rejected"
        decided = "The hit-rate excess is negative with z <= -2 over at least 100 qualifying bars."
    else:
        status = "inconclusive"
        decided = "The z of the hit-rate excess lies strictly between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": "hit rate of next-bar return on forecast>=16 bars minus all-bar hit rate",
            "value": None if hit_excess is None else float(hit_excess),
            "statistic": None if z is None else {"name": "two-proportion z", "value": float(z)},
            "threshold": "positive with z >= 2 to confirm, negative with z <= -2 to reject, over at least 100 qualifying bars",
        },
        "supporting_check": {
            "name": "mean next-bar return minus coin mean daily return (t = %s)" %
                    ("null" if sup_t is None else f"{sup_t:.3f}"),
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"qualifying bars": n_q, "all bars": int(all_n)},
        "decided_by": decided,
        "reading": "Qualifying bars are pooled over all coins in the record (not only 6) and compared by a pooled "
                   "two-proportion z-test against the share of positive next-bar returns over all bars of all windows "
                   "of all coins, a zero return counts as not positive, the supporting excess is each bar's return minus "
                   "its own coin's mean daily return with an ordinary t of the mean and is counted as passed when positive, "
                   "and fewer than 100 qualifying bars gives 'not observable'.",
    }
