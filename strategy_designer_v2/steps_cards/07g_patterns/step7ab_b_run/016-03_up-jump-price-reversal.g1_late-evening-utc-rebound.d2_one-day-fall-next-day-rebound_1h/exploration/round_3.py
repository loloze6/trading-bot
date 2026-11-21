def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].values.astype(float); n = len(c)
            if n < 900: continue
            lr = np.r_[np.nan, np.diff(np.log(c))]
            ts = pd.to_datetime(df["timestamp"]); yr = ts.dt.year.values
            v168s = pd.Series(lr).rolling(168, min_periods=150).std().values
            v720s = pd.Series(lr).rolling(720, min_periods=600).std().values
            for t in range(0, n, 24):
                if t < 720 or t + 48 >= n: continue
                past = v168s[max(0, t-2000):t+1]; past = past[~np.isnan(past)]
                if len(past) < 300: continue
                trank = (past < v168s[t]).mean()
                rows.append(dict(coin=coin, win=w, yr=yr[t], r24=c[t]/c[t-24]-1,
                    v168=v168s[t], vr=v168s[t]/v720s[t], trank=trank,
                    f24=c[t+24]/c[t]-1, f48=c[t+48]/c[t]-1, f12=c[t+12]/c[t]-1))
    R = pd.DataFrame(rows).dropna()
    def tt(x): return x.mean()/x.std()*np.sqrt(len(x))
    for h in ("f12", "f24", "f48"):
        R[h+"ex"] = R[h] - R.groupby("coin")[h].transform("mean")
        R[h+"rev"] = -np.sign(R["r24"])*R[h+"ex"]
        R[h+"z"] = R[h+"rev"]/R.groupby("coin")[h].transform("std")
    R["trq"] = pd.cut(R["trank"], [-0.01, .2, .4, .6, .8, 1.01], labels=False)
    out["rev by trailing vol rank quintile (bps, 24h)"] = R.groupby("trq").agg(bps=("f24rev", lambda x: x.mean()*1e4), strength=("f24z","mean"), t=("f24z", tt), n=("f24z","count"))
    out["rev by trailing vol rank, 12h/48h bps"] = R.groupby("trq").agg(b12=("f12rev", lambda x: x.mean()*1e4), t12=("f12z", tt), b48=("f48rev", lambda x: x.mean()*1e4), t48=("f48z", tt))
    H = R[R.trq == 4].copy()
    H["mq"] = H.groupby("coin")["r24"].transform(lambda x: pd.qcut(x.abs(), 3, labels=False))
    out["top trailing-vol: by |r24| tercile x side"] = H.assign(side=np.where(H.r24 < 0, "fall", "rise")).groupby(["mq","side"]).agg(bps=("f24rev", lambda x: x.mean()*1e4), strength=("f24z","mean"), t=("f24z", tt), n=("f24z","count"))
    # graded signal: z24 * vol-rank, forecast-weighted case measure
    R["z24"] = -R["r24"]/(R["v168"]*np.sqrt(24))
    R["sig"] = R["z24"]*R["trank"]
    R["sq"] = R.groupby("coin")["sig"].transform(lambda x: pd.qcut(x, 10, labels=False))
    out["24h excess by decile of -z24 x trailing vol rank"] = R.groupby("sq").agg(bps=("f24ex", lambda x: x.mean()*1e4), t=("f24ex", tt), n=("f24ex","count"))
    out["top trailing-vol rev by year"] = H.groupby("yr").agg(bps=("f24rev", lambda x: x.mean()*1e4), t=("f24z", tt), n=("f24z","count"))
    out["top trailing-vol rev by coin"] = H.groupby("coin").agg(bps=("f24rev", lambda x: x.mean()*1e4), t=("f24z", tt), n=("f24z","count"))
    return out
