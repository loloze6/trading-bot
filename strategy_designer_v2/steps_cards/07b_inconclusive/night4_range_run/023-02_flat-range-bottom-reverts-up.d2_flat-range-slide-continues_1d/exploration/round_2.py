import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; h = df["high"]; l = df["low"]
            hh = h.rolling(30).max(); ll = l.rolling(30).min()
            ratio = (c - c.shift(29)).abs() / (hh - ll)
            pos = (c - ll) / (hh - ll)
            ret10 = c.pct_change(10)
            z = (ret10 - ret10.rolling(60, min_periods=20).mean()) / ret10.rolling(60, min_periods=20).std()
            vol = c.pct_change().rolling(30).std()
            ret3 = c.pct_change(3)
            n = len(df)
            for H in (5, 10):
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, H=H, regime=df["regime"].iloc[i], fc=df["forecast"].iloc[i],
                                     ratio=ratio.iloc[i], pos=pos.iloc[i], ret10=ret10.iloc[i], z=z.iloc[i],
                                     vol=vol.iloc[i], ret3=ret3.iloc[i],
                                     fwd=c.iloc[i+H]/c.iloc[i]-1))
    g = pd.DataFrame(rows)
    g = g.join(g.groupby(["coin","H"])["fwd"].mean().rename("drift"), on=["coin","H"])
    g["ex"] = g.fwd - g.drift
    out = {}
    d5 = g[(g.H==5)&(g.regime=="mean_reversion")]
    out["fc_distribution"] = pd.Series({"share_fc_eq_-20": (d5.fc<=-19.99).mean(), "share_fc_lt_-8": (d5.fc<-8).mean(),
                                         "median_fc_neg": d5[d5.fc<0].fc.median(), "n": len(d5)})
    def tab(d, col, q=5):
        d = d.dropna(subset=[col,"ex"]).copy()
        d["b"] = pd.qcut(d[col], q, duplicates="drop")
        r = d.groupby("b").ex.agg(["mean","count","std"])
        r["t"] = r["mean"]/(r["std"]/np.sqrt(r["count"]))
        r["mean_col"] = d.groupby("b")[col].mean()
        return r
    out["regime5_by_raw_ret10_quint"] = tab(d5, "ret10")
    out["regime5_by_z_quint"] = tab(d5, "z")
    out["regime5_by_pos_quint"] = tab(d5, "pos")
    out["regime5_by_vol_tercile"] = tab(d5, "vol", 3)
    neg = d5[d5.fc<0].copy()
    neg["volb"] = pd.qcut(neg.vol, 3, labels=["lowvol","midvol","highvol"])
    res=[]
    for vb, x in neg.groupby("volb"):
        x = x.dropna(subset=["ret10","ex"])
        r = stats.linregress(x.ret10, x.ex); res.append(dict(vol=vb, slope=r.slope, t=r.slope/r.stderr, n=len(x), ex=x.ex.mean()))
    out["neg_slope_ret10_by_vol"] = pd.DataFrame(res)
    # flat & below, all bars from prices, by ratio tercile: slope of ex on ret10
    a = g[(g.H==5)].dropna(subset=["ratio","pos","ret10","ex"])
    a = a[a.pos<0.5].copy()
    a["rb"] = pd.cut(a.ratio, [0,0.15,0.3,0.5,0.75,1.01])
    res=[]
    for rb, x in a.groupby("rb"):
        r = stats.linregress(x.ret10, x.ex); res.append(dict(ratio=str(rb), slope=r.slope, t=r.slope/r.stderr, n=len(x)))
    out["below_slope_ret10_by_ratio_5d"] = pd.DataFrame(res)
    a10 = g[(g.H==10)].dropna(subset=["ratio","pos","ret10","ex"])
    a10 = a10[a10.pos<0.5].copy(); a10["rb"] = pd.cut(a10.ratio, [0,0.15,0.3,0.5,0.75,1.01])
    res=[]
    for rb, x in a10.groupby("rb"):
        r = stats.linregress(x.ret10, x.ex); res.append(dict(ratio=str(rb), slope=r.slope, t=r.slope/r.stderr, n=len(x)))
    out["below_slope_ret10_by_ratio_10d"] = pd.DataFrame(res)
    return out
