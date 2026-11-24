def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rows = {7: [], 30: []}
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            v = df["volume"].astype(float).values
            n = len(c)
            lr = np.r_[np.nan, np.diff(np.log(c))]
            fc = df["forecast"].astype(float).values
            al = df["postRebalance_current_allocation"].astype(float).values
            hi = df["high"].astype(float).values; lo = df["low"].astype(float).values
            for h in (7, 30):
                for t in range(0, n - h, h):
                    r = dict(coin=coin, win=w, ts=pd.Timestamp(df["timestamp"].iloc[t]).floor("D"),
                             fwd=c[t+h]/c[t]-1, fc=fc[t], al=al[t])
                    for L in (7, 14, 30, 60, 90):
                        r[f"past{L}"] = c[t]/c[t-L]-1 if t >= L else np.nan
                    r["vol20"] = np.nanstd(lr[t-19:t+1]) if t >= 20 else np.nan
                    r["volratio"] = (np.nanstd(lr[t-6:t+1]) / np.nanstd(lr[t-29:t+1])) if t >= 30 else np.nan
                    r["vlm"] = (v[t-6:t+1].mean() / v[t-29:t+1].mean()) if t >= 30 else np.nan
                    r["dd30"] = c[t]/c[t-29:t+1].max()-1 if t >= 29 else np.nan
                    r["rng30"] = ((c[t]-lo[t-29:t+1].min())/(hi[t-29:t+1].max()-lo[t-29:t+1].min())) if t >= 29 else np.nan
                    r["ret1"] = c[t]/c[t-1]-1 if t >= 1 else np.nan
                    rows[h].append(r)
    def tclust(d):
        s = d.groupby("ts")["ex"].sum()
        G = len(s)
        if G < 3: return np.nan
        m = d["ex"].mean(); N = len(d)
        se = np.sqrt((s - d.groupby("ts").size()*m).pow(2).sum() * G/(G-1)) / N
        return m/se if se > 0 else np.nan
    for h in (7, 30):
        D = pd.DataFrame(rows[h])
        D["ex"] = D["fwd"] - D.groupby("coin")["fwd"].transform("mean")
        D["exz"] = D["ex"] / D.groupby("coin")["fwd"].transform("std")
        feats = ["past7","past14","past30","past60","past90","vol20","volratio","vlm","dd30","rng30","ret1"]
        res = []
        for f in feats:
            d = D.dropna(subset=[f]).copy()
            d["q"] = d.groupby("coin")[f].rank(pct=True)
            d["Q"] = np.ceil(d["q"]*5).clip(1,5)
            rho, p = stats.spearmanr(d["q"], d["exz"])
            top = d[d.Q==5]; bot = d[d.Q==1]
            res.append(dict(feat=f, n=len(d), rho=round(rho,3), p=round(p,4),
                            q1=round(bot.ex.mean(),4), q5=round(top.ex.mean(),4),
                            t_q1=round(tclust(bot),2), t_q5=round(tclust(top),2),
                            t_diff=round(stats.ttest_ind(top.ex, bot.ex, equal_var=False)[0],2)))
        out[f"h{h} feature quintiles"] = pd.DataFrame(res)
        g = D.assign(inpos=D.fc > 0).groupby("inpos")["ex"].agg(["count","mean"])
        out[f"h{h} forecast>0 vs 0"] = g
    # weekday daily returns
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df[["day","coin_return","book_return"]].copy(); x["coin"]=coin; dd.append(x)
    DD = pd.concat(dd).dropna(subset=["coin_return"])
    DD["wd"] = pd.to_datetime(DD["day"]).dt.weekday
    DD["ex"] = DD["coin_return"] - DD.groupby("coin")["coin_return"].transform("mean")
    out["weekday"] = DD.groupby("wd")["ex"].agg(["count","mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["year coin mean"] = DD.assign(y=pd.to_datetime(DD["day"]).dt.year).groupby("y")["coin_return"].agg(["count","mean"])
    return out
