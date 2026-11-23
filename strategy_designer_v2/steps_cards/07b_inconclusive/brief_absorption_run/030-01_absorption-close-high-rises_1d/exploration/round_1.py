def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    H = [1, 3, 5, 10, 20]
    # per coin drift/usual on non-overlapping grids
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            rs = np.array(rs)
            drift[(coin, h)] = rs.mean()
            usual[(coin, h)] = rs.std(ddof=1)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            o, hi, lo, c, v = [df[k].values.astype(float) for k in ["open", "high", "low", "close", "volume"]]
            n = len(c)
            vm = pd.Series(v).shift(1).rolling(20, min_periods=20).mean().values
            vr = v / vm
            rng = hi - lo
            body = np.abs(c - o) / np.where(rng > 0, rng, np.nan)
            loc = np.where(rng > 0, (2 * (c - lo) / np.where(rng > 0, rng, np.nan) - 1), np.nan)
            r5past = pd.Series(c).pct_change(5).values
            r20past = pd.Series(c).pct_change(20).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for t in range(n):
                if np.isnan(vr[t]) or np.isnan(loc[t]):
                    continue
                rec = dict(coin=coin, w=w, t=t, vr=vr[t], body=body[t], loc=loc[t], year=yr[t],
                           p5=r5past[t], p20=r20past[t], dayret=c[t] / o[t] - 1)
                for h in H:
                    rec["f%d" % h] = c[t + h] / c[t] - 1 - drift[(coin, h)] if t + h < n else np.nan
                    rec["cell%d" % h] = t // h
                rows.append(rec)
    d = pd.DataFrame(rows)
    d["absorb"] = (d.vr >= 2) & (d.body <= 0.3)
    out = {}
    def dedup(x, h):
        return x.dropna(subset=["f%d" % h]).groupby(["coin", "w", "cell%d" % h]).head(1)
    # horizons: slope of unusual move on loc, and on loc*vr, absorb days
    res = []
    for h in H:
        a = dedup(d[d.absorb], h)
        y = a["f%d" % h]
        s1 = stats.linregress(a["loc"], y)
        s2 = stats.linregress(a["loc"] * a["vr"], y)
        # signed move
        sm = (np.sign(a["loc"]) * y)
        o_ = dedup(d[~d.absorb & (d.body <= 0.3)], h)
        s3 = stats.linregress(o_["loc"], o_["f%d" % h])
        res.append(dict(h=h, n=len(a), slope_loc=s1.slope, t_loc=s1.slope / s1.stderr,
                        t_locvr=s2.slope / s2.stderr, signed_mean=sm.mean(),
                        t_signed=sm.mean() / (sm.std(ddof=1) / np.sqrt(len(sm))),
                        n_ordflat=len(o_), t_loc_ordflat=s3.slope / s3.stderr))
    out["by_horizon_absorb"] = pd.DataFrame(res)
    a = dedup(d[d.absorb], 5).copy()
    a["side"] = np.where(a["loc"] > 0, "upper", "lower")
    a["locbin"] = pd.cut(a["loc"], [-1.01, -0.6, -0.2, 0.2, 0.6, 1.01])
    out["absorb5_by_locbin"] = a.groupby("locbin")["f5"].agg(["count", "mean", "std"])
    a["vrbin"] = pd.cut(a["vr"], [2, 2.5, 3.5, 100])
    a["signed5"] = np.sign(a["loc"]) * a["f5"]
    out["absorb5_signed_by_vrbin"] = a.groupby("vrbin")["signed5"].agg(["count", "mean", "std"])
    def tt(x):
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    out["absorb5_signed_by_coin"] = a.groupby("coin")["signed5"].apply(tt).unstack()
    out["absorb5_signed_by_year"] = a.groupby("year")["signed5"].apply(tt).unstack()
    out["absorb5_by_side"] = a.groupby("side")["f5"].apply(tt).unstack()
    a["trend20"] = np.where(a["p20"] > 0, "up20", "down20")
    out["absorb5_signed_by_trend20_side"] = a.groupby(["trend20", "side"])["f5"].apply(tt).unstack()
    a10 = dedup(d[d.absorb], 10).copy()
    a10["s"] = np.sign(a10["loc"]) * a10["f10"]
    a10["trend20"] = np.where(a10["p20"] > 0, "up20", "down20")
    out["absorb10_signed_by_trend20"] = a10.groupby("trend20")["s"].apply(tt).unstack()
    return out
