def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            h = df["high"].astype(float).values; l = df["low"].astype(float).values
            n = len(c)
            if n < 100: continue
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            s = pd.Series(r1)
            vol20 = s.rolling(20, min_periods=20).std().values
            rng = pd.Series((h-l)/c)
            quiet = (rng.rolling(30, min_periods=30).mean()/rng.rolling(180, min_periods=120).mean()).values
            ret42 = pd.Series(c).pct_change(42).values
            vs42 = ret42/(vol20*np.sqrt(42))
            lastz = r1/vol20
            ts = pd.to_datetime(df["timestamp"])
            hour = ts.dt.hour.values; wd = ts.dt.weekday.values; yr = ts.dt.year.values
            fc = df["forecast"].astype(float).values
            for H in (1, 6, 18, 36, 72):
                for t in range(0, n-H, H):
                    rows.append((coin, w, H, t, c[t+H]/c[t]-1, fc[t], vs42[t], quiet[t], lastz[t], vol20[t], hour[t], wd[t], yr[t]))
    D = pd.DataFrame(rows, columns=["coin","w","H","t","fwd","fc","vs42","quiet","lastz","vol","hour","wd","yr"])
    D["ex"] = D["fwd"] - D.groupby(["coin","H"])["fwd"].transform("mean")
    D["usual"] = D.groupby(["coin","H"])["fwd"].transform("std")
    D["exz"] = D["ex"]/D["usual"]
    out = {}
    # momentum slope by horizon, strength
    res = []
    for H, g in D.groupby("H"):
        g = g.dropna(subset=["fc","ex"])
        sl = stats.linregress(g["fc"], g["ex"])
        side = np.sign(g["fc"]); m = side != 0
        unus = (side[m]*g["ex"][m]); 
        res.append((H, len(g), sl.slope, sl.slope/sl.stderr, unus.mean(), (side[m]*g["exz"][m]).mean(), g["usual"].mean()))
    out["fc_slope_by_horizon"] = pd.DataFrame(res, columns=["H","n","slope","t","unusual_mean","strength","usual"])
    # forecast quintiles at H=18 and H=72
    for H in (18, 72):
        g = D[D.H==H].dropna(subset=["fc"]).copy()
        g["q"] = pd.qcut(g["fc"].rank(method="first"), 5, labels=False)
        out[f"fc_quintile_H{H}"] = g.groupby("q").agg(fc=("fc","mean"), ex=("ex","mean"), sd=("ex","std"), n=("ex","size")).assign(t=lambda x: x.ex/(x.sd/np.sqrt(x.n)))
    # quiet: abs move and direction of last bar
    g = D[D.H==18].dropna(subset=["quiet","lastz"]).copy()
    g["qq"] = pd.qcut(g["quiet"], 5, labels=False)
    g["absz"] = (g["fwd"].abs()/g["usual"])
    g["dirz"] = np.sign(g["lastz"])*g["exz"]
    g["lastdir_wt"] = g["lastz"]*g["exz"]
    out["quiet_quintile_H18"] = g.groupby("qq").agg(quiet=("quiet","mean"), absz=("absz","mean"), dirz=("dirz","mean"), dsd=("dirz","std"), n=("dirz","size")).assign(t=lambda x: x.dirz/(x.dsd/np.sqrt(x.n)))
    # last-bar size quintiles (reversal/continuation) H=6 and 18
    for H in (6, 18):
        g = D[D.H==H].dropna(subset=["lastz"]).copy()
        g["q"] = pd.qcut(g["lastz"], 5, labels=False)
        out[f"lastbar_quintile_H{H}"] = g.groupby("q").agg(lastz=("lastz","mean"), exz=("exz","mean"), sd=("exz","std"), n=("exz","size")).assign(t=lambda x: x.exz/(x.sd/np.sqrt(x.n)))
    # vol level vs momentum strength H=18
    g = D[D.H==18].dropna(subset=["fc","vol"]).copy()
    g["vr"] = g.groupby("coin")["vol"].rank(pct=True)
    g["vq"] = pd.cut(g["vr"], [0,1/3,2/3,1], labels=False)
    g["sz"] = np.sign(g["fc"])*g["exz"]
    out["momentum_by_vol_tercile_H18"] = g.groupby("vq").agg(sz=("sz","mean"), sd=("sz","std"), n=("sz","size")).assign(t=lambda x: x.sz/(x.sd/np.sqrt(x.n)))
    g["yq"] = g["yr"]
    out["momentum_by_year_H18"] = g.groupby("yq").agg(sz=("sz","mean"), sd=("sz","std"), n=("sz","size")).assign(t=lambda x: x.sz/(x.sd/np.sqrt(x.n)))
    # hour and weekday, H=1 and H=6
    g = D[D.H==1]
    out["hour_H1"] = g.groupby("hour").agg(exz=("exz","mean"), sd=("exz","std"), n=("exz","size")).assign(t=lambda x: x.exz/(x.sd/np.sqrt(x.n)))
    g = D[D.H==6]
    out["weekday_H6"] = g.groupby("wd").agg(exz=("exz","mean"), sd=("exz","std"), n=("exz","size"), ex=("ex","mean")).assign(t=lambda x: x.exz/(x.sd/np.sqrt(x.n)))
    # book
    br = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            br.append(d[["book_return","coin_return"]].assign(coin=coin, yr=pd.to_datetime(d["day"]).dt.year))
    B = pd.concat(br)
    out["book_by_coin"] = B.groupby("coin")[["book_return","coin_return"]].agg(["mean","std"])
    out["book_by_year"] = B.groupby("yr")[["book_return","coin_return"]].mean()
    return out
