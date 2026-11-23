import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    FC = "forecast"
    RAW = "debug_info.components.fade.last_history_value"

    def prep(df):
        df = df.copy()
        ts = pd.to_datetime(df["timestamp"], utc=True)
        df["_ts"] = ts
        df["_hour"] = ts.dt.hour
        df["_wd"] = ts.dt.dayofweek  # Monday=0 ... Saturday=5, Sunday=6
        df = df.reset_index(drop=True)
        close = df["close"].astype(float)
        r1 = close / close.shift(1) - 1.0
        df["_r1"] = r1
        # VolatilityScaledReturnComponent(period=1, vol_period=24), recomputed from prices
        vol = r1.rolling(24, min_periods=24).std()
        raw = r1 / vol
        raw = raw.replace([np.inf, -np.inf], np.nan)
        df["_raw_re"] = raw
        # standardise: value*10 / mean(|last 60 raw values|, bar t left out), 0 until 20 past values, cap +-20
        absmean = raw.abs().shift(1).rolling(60, min_periods=20).mean()
        std = raw * 10.0 / absmean
        std = std.where(absmean > 0, 0.0)
        std = std.where(absmean.notna(), 0.0)
        std = std.clip(-20, 20)
        df["_fc_re"] = (-std).clip(-20, 20)  # negate, weighted mean of one component, clip
        df["_fwd"] = close.shift(-H) / close - 1.0
        return df

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            d = prep(df)
            prepared[coin][w] = d
            fc = d[FC].astype(float)
            active = fc.notna() & (fc != 0)
            situ = (d["_hour"] == 0) & d["_wd"].isin([5, 6])
            if RAW in d.columns:
                raw = d[RAW].astype(float)
                raw = raw.where(raw.notna(), d["_r1"])
            else:
                raw = d["_r1"]
            expected_sign = -np.sign(raw)
            ok = active & situ & (np.sign(fc) == expected_sign) & (expected_sign != 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    main_name = "t of the slope of the 24-bar excess return on the recorded forecast, weekend 00:00 cases"
    thr = "confirm: slope > 0 with t >= 2 over >= 1000 weekend cases and weekend slope > weekday slope; reject: slope < 0 with t <= -2 over >= 1000 cases"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on expected side": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are Saturday/Sunday 00:00 UTC bars faded against that hour's move, as the Fidelity's situation and side require.",
            "reading": "Situation taken as bars stamped 00:00 UTC on Saturday or Sunday, expected side minus the sign of the recorded raw component value (1-hour return from prices where missing).",
        }

    # ---------- criterion ----------
    we_x, we_y, wd_x, wd_y = [], [], [], []
    for coin, wins in prepared.items():
        grid = []
        for w, d in wins.items():
            g = d["_fwd"].iloc[::H].dropna()
            grid.append(g.values)
        grid = np.concatenate(grid) if grid else np.array([])
        if grid.size == 0:
            continue
        coin_mean = float(np.mean(grid))
        for w, d in wins.items():
            fwd = d["_fwd"] - coin_mean
            h0 = d["_hour"] == 0
            we = h0 & d["_wd"].isin([5, 6])
            wk = h0 & d["_wd"].isin([0, 1, 2, 3, 4])
            fc = d[FC].astype(float)
            m = we & fwd.notna() & fc.notna()
            we_x.append(fc[m].values)
            we_y.append(fwd[m].values)
            m2 = wk & fwd.notna() & d["_fc_re"].notna() & d["_raw_re"].notna()
            wd_x.append(d["_fc_re"][m2].values)
            wd_y.append(fwd[m2].values)

    def cat(l):
        return np.concatenate(l) if l else np.array([])

    we_x, we_y, wd_x, wd_y = cat(we_x), cat(we_y), cat(wd_x), cat(wd_y)
    n_we, n_wd = int(we_x.size), int(wd_x.size)

    def reg(x, y):
        if x.size < 3 or np.std(x) == 0:
            return None, None
        res = stats.linregress(x, y)
        t = res.slope / res.stderr if res.stderr and res.stderr > 0 else None
        return float(res.slope), (float(t) if t is not None else None)

    s_we, t_we = reg(we_x, we_y)
    s_wd, t_wd = reg(wd_x, wd_y)
    diff = (s_we - s_wd) if (s_we is not None and s_wd is not None) else None
    sup_pass = (bool(diff > 0) if diff is not None else None)

    counts = {"weekend cases": n_we, "weekday cases": n_wd}
    if n_we < 1000 or t_we is None:
        status = "not observable"
        decided = "Fewer than the plan's minimum of 1000 weekend cases (or no slope could be estimated)."
    elif s_we > 0 and t_we >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Weekend slope positive with t >= 2 over at least 1000 weekend cases and the weekend slope exceeds the weekday slope."
        else:
            status = "inconclusive"
            decided = "Weekend t >= 2 but the weekend slope does not exceed the weekday slope."
    elif s_we < 0 and t_we <= -2:
        status = "rejected"
        decided = "Weekend slope negative with t <= -2 over at least 1000 cases: the hour's move continues."
    else:
        status = "inconclusive"
        decided = "Weekend t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": (float(s_we) if s_we is not None else None),
            "statistic": ({"name": "OLS slope t", "value": float(t_we)} if t_we is not None else None),
            "threshold": thr,
        },
        "supporting_check": {
            "name": "weekend slope minus weekday slope (> 0)",
            "value": (float(diff) if diff is not None else None),
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "Cases are all Saturday/Sunday (weekend) and Monday-Friday (weekday) bars stamped 00:00 UTC with a 24-bar forward return inside their window (forecast 0 included), the coin mean is over its non-overlapping 24-bar grid of all windows, and the weekday forecast is rebuilt as return/rolling 24-bar std (ddof 1, current bar included), standardised over the previous 60 bars' raw values on every bar (min 20), negated and clipped to +-20.",
    }
