import numpy as np
import pandas as pd
from scipy import stats

H = 48


def _ts(s):
    if np.issubdtype(s.dtype, np.number):
        v = s.astype("float64")
        unit = "ms" if v.abs().max() > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def _weekend_end_mask(ts):
    # bar closing at Monday 00:00 UTC: start Sunday 23:00, or a bar stamped Monday 00:00
    sun23 = (ts.dt.dayofweek == 6) & (ts.dt.hour == 23)
    mon00 = (ts.dt.dayofweek == 0) & (ts.dt.hour == 0)
    return (sun23 | mon00).to_numpy()


def measure(bars):
    total_active = 0
    agree = 0
    cases = []  # (coin, signed excess, abs forecast)
    coin_drift = {}

    # coin's mean 48-bar return over all windows, on non-overlapping grids
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].to_numpy(dtype=float)
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                rets.extend(r[np.isfinite(r)].tolist())
        coin_drift[coin] = float(np.mean(rets)) if rets else np.nan

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            ts = _ts(df["timestamp"])
            c = df["close"].to_numpy(dtype=float)
            v = df["volume"].to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            pos = np.arange(n)

            # situation from prices
            r48 = np.full(n, np.nan)
            prior = np.full(n, np.nan)
            vr = np.full(n, np.nan)
            ok = pos >= 167
            r48[ok] = c[pos[ok]] / c[pos[ok] - 48] - 1.0
            prior[ok] = c[pos[ok] - 48] / c[pos[ok] - 168] - 1.0
            cv = np.concatenate([[0.0], np.cumsum(np.nan_to_num(v))])
            recent = np.full(n, np.nan)
            base = np.full(n, np.nan)
            p = pos[ok]
            recent[ok] = (cv[p + 1] - cv[p - 47]) / 48.0
            base[ok] = (cv[p - 47] - cv[p - 167]) / 120.0
            with np.errstate(divide="ignore", invalid="ignore"):
                vr = np.where(base > 0, recent / base, np.nan)

            wend = _weekend_end_mask(ts)
            same_sign = np.sign(r48) * np.sign(prior) > 0
            situ = wend & same_sign & (vr > 1.0)
            side = np.sign(r48)

            active = f != 0
            total_active += int(active.sum())
            agree += int((active & situ & (np.sign(f) == side)).sum())

            # cases: weekend-end bars with non-zero forecast, one per week per coin
            seen = set()
            drift = coin_drift.get(coin, np.nan)
            for i in np.where(active & wend)[0]:
                close_time = ts.iloc[i] + pd.Timedelta(hours=1) if ts.iloc[i].hour == 23 else ts.iloc[i]
                wk = (close_time.isocalendar()[0], close_time.isocalendar()[1])
                if wk in seen:
                    continue
                seen.add(wk)
                if i + H >= n or not np.isfinite(drift):
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r):
                    continue
                cases.append((coin, float(np.sign(f[i]) * (r - drift)), float(abs(f[i]))))

    agreement = float(agree / total_active) if total_active > 0 else 0.0
    passed = total_active > 0 and agreement >= 0.9
    threshold = "confirm: mean > 0 with t >= 2 (and rank correlation > 0); reject: mean < 0 with t <= -2"
    reading = ("The Monday 00:00 case bar is the bar closing at Monday 00:00 UTC, accepted as the bar stamped Sunday 23:00 "
               "or Monday 00:00 because the record's timestamp convention may differ, with the situation computed from "
               "prices on that bar (48-bar return, 120-bar return ending 48 bars earlier, mean volume of the last 48 bars "
               "over bars t-167..t-48), and the coin's mean 48-bar return is taken on the non-overlapping 48-bar grid of all its windows pooled.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean signed excess 48-bar return", "value": None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": len(cases), "active bars": total_active},
            "decided_by": ("Only {:.1%} of the non-zero-forecast bars are weekend-end bars with a heavy-volume weekend move "
                           "extending the prior five-weekday move and a forecast on the weekend move's side, below 90 %.").format(agreement),
            "reading": reading,
        }

    x = np.array([cs[1] for cs in cases], dtype=float)
    a = np.array([cs[2] for cs in cases], dtype=float)
    ncases = int(len(x))
    mean = float(np.mean(x)) if ncases else None
    t = None
    if ncases >= 2:
        sd = float(np.std(x, ddof=1))
        t = float(mean / (sd / np.sqrt(ncases))) if sd > 0 else None
    rho = None
    if ncases >= 3 and np.std(a) > 0 and np.std(x) > 0:
        rho = float(stats.spearmanr(a, x).correlation)
    sup_pass = (rho is not None and rho > 0) if rho is not None else None

    if ncases < 100:
        status = "not observable"
        decided = f"Only {ncases} cases over all coins and windows, below the plan's minimum of 100."
    elif t is not None and mean > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean signed excess return is above 0 with t >= 2 and the rank correlation is above 0."
        else:
            status = "inconclusive"
            decided = "The mean signed excess return meets the confirm rule but the rank correlation is not above 0."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean signed excess return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean signed excess return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean signed excess 48-bar return", "value": mean,
                         "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
                         "threshold": threshold},
        "supporting_check": {"name": "Spearman of abs(forecast) vs signed excess return",
                             "value": rho, "passed": sup_pass},
        "counts": {"cases": ncases},
        "decided_by": decided,
        "reading": reading,
    }
