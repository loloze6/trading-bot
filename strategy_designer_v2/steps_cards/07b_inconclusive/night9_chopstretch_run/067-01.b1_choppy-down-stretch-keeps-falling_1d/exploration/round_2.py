import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sma = c.rolling(20).mean()
            sd = r.rolling(20).std()
            st = (c - sma) / sma / sd
            vol30 = r.rolling(30).std()
            fc = b["forecast"].astype(float)
            ch = (b["regime"] == "unknown")
            h = 5
            fwd = c.shift(-h) / c - 1
            for i in np.arange(0, len(b), h):
                rows.append((coin, w, i, st.iloc[i], fc.iloc[i], ch.iloc[i], fwd.iloc[i], vol30.iloc[i], r.iloc[max(i-4,0):i+1].sum() if i>=4 else np.nan))
    df = pd.DataFrame(rows, columns=["coin","w","i","st","fc","chop","fwd","vol30","r5"])
    drift = df.groupby("coin")["fwd"].mean().rename("drift")
    df = df.join(drift, on="coin")
    df["ex"] = df["fwd"] - df["drift"]
    df = df.dropna(subset=["st","ex"])
    out = {}
    def reg(d, x="st"):
        d = d.dropna(subset=[x])
        if len(d) < 10: return pd.Series({"n":len(d),"slope":np.nan,"t":np.nan,"spearman":np.nan,"mean_ex":d["ex"].mean() if len(d) else np.nan})
        s = stats.linregress(d[x], d["ex"])
        rho = stats.spearmanr(d[x], d["ex"]).correlation
        return pd.Series({"n":len(d),"slope":s.slope,"t":s.slope/s.stderr,"spearman":rho,"mean_ex":d["ex"].mean()})
    ch = df[df.chop]
    below = ch[ch.st<0]
    fneg = ch[ch.fc<0]
    res = {}
    res["raw_st_below"] = reg(below,"st")
    res["fc_on_fc<0"] = reg(fneg,"fc")
    res["raw_st_on_fc<0"] = reg(fneg,"st")
    w = below.copy(); w["ex"] = w["ex"].clip(w["ex"].quantile(.05), w["ex"].quantile(.95))
    res["raw_st_below_winsor"] = reg(w,"st")
    w2 = below[below.st > -3]
    res["raw_st_below_excl_st<-3"] = reg(w2,"st")
    res["chop_all_mean_ex_both"] = pd.Series({"n":len(ch),"mean_ex":ch["ex"].mean()})
    out["regs"] = pd.DataFrame(res).T
    out["fc_vs_st_corr_below"] = pd.Series({"corr":fneg[["fc","st"]].corr().iloc[0,1],"share_st<0_with_fc<0":(below.fc<0).mean(),"share_fc<0_with_st<0":(fneg.st<0).mean()})
    below = below.assign(bin=pd.cut(below.st,[-99,-3,-2,-1,-0.5,0]))
    out["below_bins"] = below.groupby("bin").agg(n=("ex","size"),ex=("ex","mean"),med=("ex","median"),t=("ex",lambda x: x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    med = df.groupby("coin")["vol30"].transform("median")
    below["agit"] = below["vol30"] > med.loc[below.index]
    out["below_by_agitation"] = below.groupby("agit").apply(reg)
    yr = {}
    for coin, ws in bars.items():
        for wn, b in ws.items():
            yr[(coin,wn)] = pd.to_datetime(b["timestamp"].iloc[0]).year
    below["yr"] = [yr[(c,ww)] for c,ww in zip(below.coin, below.w)]
    out["below_by_year"] = below.groupby("yr").apply(reg)
    return out
