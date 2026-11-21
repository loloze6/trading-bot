import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    out = {}
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            c = b["close"].values.astype(float); n = len(c)
            hi = b["high"].values.astype(float); lo = b["low"].values.astype(float)
            lr = np.r_[np.nan, np.diff(np.log(c))]
            for H in (7, 26):
                for t in range(0, n - H, H):
                    r = c[t+H]/c[t]-1
                    past26 = c[t]/c[t-26]-1 if t >= 26 else np.nan
                    past7 = c[t]/c[t-7]-1 if t >= 7 else np.nan
                    vol = np.nanstd(lr[max(1,t-25):t+1]) if t >= 26 else np.nan
                    hh = hi[max(0,t-25):t+1].max(); ll = lo[max(0,t-25):t+1].min()
                    rng_pos = (c[t]-ll)/(hh-ll) if t >= 26 and hh > ll else np.nan
                    rows.append(dict(coin=coin, w=w, H=H, r=r, past26=past26, past7=past7,
                                     vol=vol, rngpos=rng_pos, fc=b["forecast"].iloc[t],
                                     reg=b["regime"].iloc[t]))
    df = pd.DataFrame(rows)
    df["ex"] = df["r"] - df.groupby(["coin","H"])["r"].transform("mean")
    df["exz"] = df["ex"] / df.groupby(["coin","H"])["r"].transform("std")
    res = []
    for H in (7, 26):
        d = df[df.H == H]
        res.append(dict(H=H, grp="all", n=len(d), mean_r=d.r.mean()))
        for g, dd in d.groupby("reg"):
            res.append(dict(H=H, grp="reg_"+str(g), n=len(dd), mean_ex=dd.ex.mean(), t=stats.ttest_1samp(dd.ex, 0).statistic))
        for f in ["past26", "past7", "vol", "rngpos"]:
            dd = d.dropna(subset=[f]).copy()
            dd["q"] = dd.groupby("coin")[f].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
            for q, g in dd.groupby("q"):
                res.append(dict(H=H, grp=f"{f}_q{q}", n=len(g), mean_ex=g.ex.mean(), mean_exz=g.exz.mean(),
                                t=stats.ttest_1samp(g.ex, 0).statistic))
            sp = stats.spearmanr(dd[f], dd.exz)
            res.append(dict(H=H, grp=f"{f}_spearman", n=len(dd), mean_exz=sp.correlation, t=sp.pvalue))
    out["grid"] = pd.DataFrame(res)
    # per-coin spearman for past26 at H=26 and H=7
    pc = []
    for (coin, H), g in df.dropna(subset=["past26","rngpos"]).groupby(["coin","H"]):
        pc.append(dict(coin=coin, H=H, n=len(g), rho_past26=stats.spearmanr(g.past26, g.ex).correlation,
                       rho_rngpos=stats.spearmanr(g.rngpos, g.ex).correlation,
                       rho_vol=stats.spearmanr(g.vol, g.ex).correlation))
    out["percoin"] = pd.DataFrame(pc)
    # daily: weekday, after big moves
    dl = []
    for coin, ws in days.items():
        for w, d in ws.items():
            d = d.copy(); d["coin"]=coin; d["w"]=w
            d["wd"] = pd.to_datetime(d["day"]).dt.weekday
            d["next"] = d["coin_return"].shift(-1)
            d["next5"] = d["close"].shift(-5)/d["close"]-1
            dl.append(d)
    D = pd.concat(dl)
    D["z"] = D["coin_return"]/D.groupby("coin")["coin_return"].transform("std")
    wd = D.groupby("wd")["coin_return"].agg(["count","mean"])
    wd["t"] = D.groupby("wd")["coin_return"].apply(lambda x: stats.ttest_1samp(x.dropna(),0).statistic)
    out["weekday"] = wd
    D["zb"] = pd.cut(D["z"], [-99,-2,-1,1,2,99])
    out["after_move"] = D.groupby("zb", observed=True).agg(n=("next","count"), next1=("next","mean"), next5=("next5","mean"))
    bk = D.dropna(subset=["book_return"])
    bk["bq"] = pd.qcut(bk["book_return"].rank(method="first"), [0,.01,.05,.95,.99,1], labels=False)
    out["book_extremes"] = bk.groupby("bq").agg(n=("book_return","count"), book=("book_return","mean"), coin=("coin_return","mean"), next_coin=("next","mean"))
    return out
