def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [5, 10, 20, 30]
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            fc = df["forecast"].values
            raw = df.get("debug_info.components.sma_cross.last_history_value", pd.Series(np.nan, index=df.index)).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(df)
            for h in H:
                for i in range(0, n - h, h):
                    rows.append((c, w, h, i, fc[i], raw[i], yr[i], cl[i + h] / cl[i] - 1))
    s = pd.DataFrame(rows, columns=["coin", "win", "h", "pos", "fc", "raw", "yr", "ret"])
    s["ex"] = s["ret"] - s.groupby(["coin", "h"])["ret"].transform("mean")
    out = {}
    def reg(d, x="fc"):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 10 or d[x].std() == 0:
            return (len(d), np.nan, np.nan)
        r = stats.linregress(d[x], d["ex"])
        return (len(d), r.slope, r.slope / r.stderr)
    hz = []
    for h in H:
        d = s[s.h == h]
        n, b, t = reg(d)
        pos = d[d.fc > 0]["ex"]; z = d[d.fc <= 0]["ex"]
        tt = stats.ttest_ind(pos, z, equal_var=False)
        nr, br, trr = reg(d, "raw")
        hz.append(dict(h=h, n=n, slope=b, t=t, n_pos=len(pos), ex_pos=pos.mean(), ex_zero=z.mean(), t_diff=tt.statistic, slope_raw=br, t_raw=trr))
    out["by_horizon"] = pd.DataFrame(hz)
    d10 = s[s.h == 10]
    out["by_coin_h10"] = pd.DataFrame([dict(coin=c, **dict(zip(["n", "slope", "t"], reg(g))), ex_pos=g[g.fc > 0].ex.mean(), ex_zero=g[g.fc <= 0].ex.mean()) for c, g in d10.groupby("coin")])
    out["by_year_h10"] = pd.DataFrame([dict(yr=y, **dict(zip(["n", "slope", "t"], reg(g))), ex_pos=g[g.fc > 0].ex.mean(), ex_zero=g[g.fc <= 0].ex.mean(), share_pos=(g.fc > 0).mean()) for y, g in d10.groupby("yr")])
    d10 = d10.copy()
    d10["bk"] = pd.cut(d10.fc, [-0.1, 0, 5, 10, 15, 20.1])
    out["by_fc_bucket_h10"] = d10.groupby("bk").agg(n=("ex", "size"), mean_ex=("ex", "mean"), sd=("ex", "std"), hit=("ret", lambda x: (x > 0).mean()))
    out["raw_desc"] = d10["raw"].describe()
    dp = d10[d10.fc > 0]
    out["slope_within_pos_h10"] = str(reg(dp))
    return out
