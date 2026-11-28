def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            up = (r1 > 0).astype(float); dn = (r1 < 0).astype(float)
            share = (v*up).rolling(20).sum() / v.rolling(20).sum()
            # down-day volume per down day vs up-day volume per up day (20d)
            dvol = (v*dn).rolling(20).sum() / dn.rolling(20).sum().replace(0, np.nan)
            uvol = (v*up).rolling(20).sum() / up.rolling(20).sum().replace(0, np.nan)
            ratio = np.log(uvol / dvol)
            # down-day volume trend: last 10d down-day vol vs prior 10d
            dv10 = (v*dn).rolling(10).sum() / dn.rolling(10).sum().replace(0, np.nan)
            dtrend = np.log(dv10 / dv10.shift(10))
            vtrend = np.log(v.rolling(10).mean() / v.rolling(60).mean())
            r20 = c / c.shift(20) - 1
            inprof = (b["regime"] == "unknown")
            fc = b["forecast"].astype(float)
            sc = b.get("debug_info.components.up_vol_share.last_history_value")
            n = len(b)
            for h in (3, 5, 10):
                for off in range(h):
                    for i in range(off, n - h, h):
                        rows.append(dict(coin=coin, win=w, h=h, off=off, inprof=bool(inprof[i]),
                                         share=share[i], ratio=ratio[i], dtrend=dtrend[i], vtrend=vtrend[i],
                                         r20=r20[i], fc=fc[i], ret=c[i+h]/c[i]-1))
    df = pd.DataFrame(rows)
    df["ret_adj"] = df["ret"] - df[df.off == 0].groupby(["coin", "h"])["ret"].mean().reindex(
        pd.MultiIndex.from_frame(df[["coin", "h"]])).values
    out = {}
    ip = df[df.inprof]
    out["in-profile mean adj return by h (grid 0)"] = ip[ip.off == 0].groupby("h")["ret_adj"].agg(
        ["size", "mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    res = []
    for var in ["share", "ratio", "dtrend", "vtrend", "r20", "fc"]:
        for h in (3, 5, 10):
            g0 = ip[(ip.h == h) & (ip.off == 0)].dropna(subset=[var, "ret_adj"])
            s = stats.linregress(g0[var], g0["ret_adj"])
            ts = []
            for off in range(h):
                g = ip[(ip.h == h) & (ip.off == off)].dropna(subset=[var, "ret_adj"])
                if len(g) > 10:
                    ss = stats.linregress(g[var], g["ret_adj"]); ts.append(ss.slope/ss.stderr)
            res.append(dict(var=var, h=h, n0=len(g0), t0=s.slope/s.stderr, corr0=s.rvalue,
                            t_mean_offsets=np.mean(ts), t_min=np.min(ts), t_max=np.max(ts)))
    out["in-profile slopes, all grid offsets"] = pd.DataFrame(res)
    # forecast>0 vs =0 at h5, all offsets pooled (overlapping, descriptive)
    g = ip[ip.h == 5].dropna(subset=["fc"])
    out["h5 fc>0 vs 0 (pooled offsets)"] = g.groupby(g.fc > 0)["ret_adj"].agg(["size", "mean"])
    g = ip[ip.h == 5].dropna(subset=["dtrend"]).copy()
    g["q"] = pd.qcut(g["dtrend"], 4, labels=False)
    out["h5 by down-day vol trend quartile (pooled)"] = g.groupby("q").agg(n=("ret_adj", "size"),
        dtrend=("dtrend", "mean"), mean=("ret_adj", "mean"))
    g = ip[ip.h == 5].dropna(subset=["ratio"]).copy()
    g["q"] = pd.qcut(g["ratio"], 4, labels=False)
    out["h5 by up/down vol ratio quartile (pooled)"] = g.groupby("q").agg(n=("ret_adj", "size"),
        ratio=("ratio", "mean"), mean=("ret_adj", "mean"))
    # out-of-profile comparison for share at h5
    oo = df[(~df.inprof) & (df.h == 5) & (df.off == 0)].dropna(subset=["share"])
    s = stats.linregress(oo["share"], oo["ret_adj"])
    out["out-of-profile h5 share slope"] = pd.Series(dict(n=len(oo), t=s.slope/s.stderr))
    return out
