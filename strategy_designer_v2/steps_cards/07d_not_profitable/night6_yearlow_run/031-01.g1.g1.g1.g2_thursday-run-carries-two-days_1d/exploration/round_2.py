def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]; coins = list(bars.keys())
    windows = sorted({w for c in coins for w in bars[c].keys()}, key=lambda s: int(s[1:]))
    rows = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            pa = b["postRebalance_current_allocation"].shift(1)
            r = b["postRebalance_total_value"].pct_change()
            rows.append(pd.DataFrame({"day": b["timestamp"].dt.floor("D"), "ret": r, "pa": pa, "coin": c, "w": w}))
    cd = pd.concat(rows)
    cd["rl"] = np.where(cd.pa > 1e-9, cd.ret, 0.0); cd.loc[cd.ret.isna(), "rl"] = np.nan
    def chain(skip=None):
        out = []
        for w in windows:
            if w == skip: continue
            x = cd[cd.w == w]
            out.append(x.groupby("day")["rl"].mean().dropna().sort_index())
        return pd.concat(out).reset_index(drop=True)
    def st(r):
        v = (1 + r).cumprod(); dd = v / v.cummax() - 1
        yr = v.iloc[-1] ** (365 / len(r)) - 1
        return pd.Series({"sharpe": r.mean() / r.std() * np.sqrt(365), "yearly": yr, "maxdd": dd.min(), "calmar": yr / -dd.min()})
    res = {}
    res["long_only_full"] = st(chain())
    lo = pd.DataFrame({w: st(chain(w)) for w in windows}).T
    res["long_only_leave_one_out_min"] = lo.min()
    days_in = (cd.pa > 1e-9).mean()
    res["long_only_share_coin_bars_in_position"] = float(days_in)
    res["long_only_mean_daily_per_day_in_position"] = float(chain().mean() / days_in * 1)  # approx (bars=days)
    # condition check: positive vol-scaled 14d return on all weekdays vs Thursday
    cs = []
    for c in coins:
        dp = []
        for w, b in bars[c].items():
            cl = b.sort_values("timestamp")["close"].values; g = cl[::2]; dp.append(g[1:] / g[:-1] - 1)
        drift = np.concatenate(dp).mean()
        for w, b in bars[c].items():
            b = b.sort_values("timestamp").reset_index(drop=True); cl = b.close
            r1 = cl.pct_change(); s = (cl / cl.shift(14) - 1) / r1.rolling(20).std()
            z = (s - s.rolling(60, min_periods=20).mean()) / s.rolling(60, min_periods=20).std()
            df = pd.DataFrame({"s": s, "z": z, "r2": cl.shift(-2) / cl - 1 - drift, "wd": b.timestamp.dt.weekday,
                               "day": b.timestamp.dt.floor("D"), "pos": np.arange(len(b))})
            cs.append(df)
    A = pd.concat(cs).dropna()
    A = A[A.pos % 2 == 0]
    A["side"] = np.where(A.s > 0, "rise", "fall")
    A["thu"] = np.where(A.wd == 3, "thu", "other")
    def summ(d):
        g = d.groupby("day").r2.sum()
        return pd.Series({"n": len(d), "days": len(g), "mean_r2": d.r2.mean(), "t_day": g.mean() / g.std() * np.sqrt(len(g))})
    res["rise_fall_by_thu"] = A.groupby(["thu", "side"]).apply(summ)
    A["zq"] = pd.qcut(A.s, 5, labels=False)
    res["s_quintile_by_thu"] = A.groupby(["thu", "zq"]).apply(summ)
    return res
