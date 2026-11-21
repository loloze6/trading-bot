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
            ts = pd.to_datetime(df["timestamp"])
            yr = ts.dt.year.values; hr = ts.dt.hour.values
            for t in range(0, n, 24):
                if t < 720 or t + 24 >= n: continue
                seg = lr[t-71:t+1]; sa = np.nansum(np.abs(seg))
                if sa <= 0: continue
                v24 = np.nanstd(lr[t-23:t+1]); v168 = np.nanstd(lr[t-167:t+1]); v720 = np.nanstd(lr[t-719:t+1])
                rows.append(dict(coin=coin, win=w, yr=yr[t], hour=hr[t],
                    r24=c[t]/c[t-24]-1, r72=c[t]/c[t-72]-1,
                    eff=abs(np.nansum(seg))/sa, v168=v168, v720=v720, vr=v168/v720,
                    fwd=c[t+24]/c[t]-1))
    R = pd.DataFrame(rows).dropna()
    R["drift"] = R.groupby("coin")["fwd"].transform("mean")
    R["sd"] = R.groupby("coin")["fwd"].transform("std")
    R["exr"] = R["fwd"] - R["drift"]
    R["ex"] = R["exr"]/R["sd"]
    R["rev"] = -np.sign(R["r24"])*R["ex"]
    R["revraw"] = -np.sign(R["r24"])*R["exr"]
    R["totrev"] = -np.sign(R["r24"])*R["fwd"]
    R["volq"] = R.groupby("coin")["v168"].transform(lambda x: pd.qcut(x, 5, labels=False))
    R["vrq"] = R.groupby("coin")["vr"].transform(lambda x: pd.qcut(x, 5, labels=False))
    R["side"] = np.where(R["r24"] < 0, "fall", "rise")
    def tt(x): return x.mean()/x.std()*np.sqrt(len(x))
    agg = lambda g: R.groupby(g).agg(strength=("rev","mean"), t=("rev", tt), ex_bps=("revraw", lambda x: x.mean()*1e4), tot_bps=("totrev", lambda x: x.mean()*1e4), n=("rev","count"))
    out["rev by vol168 quintile (30d-trailing sample)"] = agg("volq")
    out["rev by vol ratio 7d/30d quintile"] = agg("vrq")
    out["rev by volq x side"] = agg(["volq","side"])
    H = R[R.volq == 4].copy()
    out["top-vol rev by coin"] = H.groupby("coin").agg(strength=("rev","mean"), t=("rev", tt), ex_bps=("revraw", lambda x: x.mean()*1e4), n=("rev","count"))
    out["top-vol rev by year"] = H.groupby("yr").agg(strength=("rev","mean"), t=("rev", tt), ex_bps=("revraw", lambda x: x.mean()*1e4), n=("rev","count"))
    H["mq"] = H.groupby("coin")["r24"].transform(lambda x: pd.qcut(x.abs(), 3, labels=False))
    out["top-vol rev by |r24| tercile"] = H.groupby("mq").agg(strength=("rev","mean"), t=("rev", tt), ex_bps=("revraw", lambda x: x.mean()*1e4), n=("rev","count"))
    # graded: regress ex on r24 scaled by v168, interacted with vol rank
    R["z24"] = R["r24"]/(R["v168"]*np.sqrt(24))
    R["vrank"] = R.groupby("coin")["v168"].rank(pct=True)
    X = np.c_[np.ones(len(R)), R["z24"], R["z24"]*R["vrank"], R["vrank"]]
    y = R["ex"].values
    b, *_ = np.linalg.lstsq(X, y, rcond=None); res = y - X@b
    se = np.sqrt(np.diag(res@res/(len(y)-4)*np.linalg.inv(X.T@X)))
    out["reg ex ~ z24, z24*vrank, vrank"] = pd.DataFrame({"b": b, "t": b/se}, index=["const","z24","z24xvrank","vrank"])
    # leave-one-window-out stability of top-vol reversal
    lw = []
    for w in sorted(H["win"].unique()):
        s = H[H.win != w]["rev"]; lw.append(tt(s))
    out["top-vol rev t, min/max one window left out"] = f"{min(lw):.2f} / {max(lw):.2f}"
    out["top-vol rev, share of windows positive"] = float((H.groupby("win")["rev"].mean() > 0).mean())
    # grind continuation: eff given size, in bps, cont on 72h direction
    R["cont"] = np.sign(R["r72"])*R["ex"]; R["contraw"] = np.sign(R["r72"])*R["exr"]
    R["sq"] = R.groupby("coin")["r72"].transform(lambda x: pd.qcut(x.abs(), 3, labels=False))
    R["eq"] = R.groupby(["coin","sq"])["eff"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out["cont by size tercile x eff tercile"] = R.groupby(["sq","eq"]).agg(strength=("cont","mean"), t=("cont", tt), bps=("contraw", lambda x: x.mean()*1e4), n=("cont","count"))
    return out
