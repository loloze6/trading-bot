import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    Hs = [1,2,3,5,10]
    rows = []
    for coin, wins in bars.items():
        cm = {}
        for H in Hs:
            allr = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c)-H, H):
                    allr.append(c[i+H]/c[i]-1)
            cm[H] = np.mean(allr)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(c)
            r = np.r_[np.nan, c[1:]/c[:-1]-1]
            sd = pd.Series(r).rolling(30).std().shift(1).values
            streak = np.zeros(n)
            for i in range(1,n):
                streak[i] = streak[i-1]+1 if r[i] < 0 else 0
            fc = df["forecast"].values
            for i in range(1,n):
                up = r[i] > 0
                k = int(streak[i-1]) if up else 0
                depth = np.nan
                if k>0 and i-k-1>=0 and not np.isnan(sd[i]):
                    depth = (1-c[i-1]/c[i-1-k])/sd[i]
                d = dict(coin=coin, w=w, i=i, prof=df["regime"].iloc[i]!="chop", up=up, k=k,
                         depth=depth, r1=r[i], r1z=r[i]/sd[i] if not np.isnan(sd[i]) else np.nan,
                         fc=fc[i], year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                         day=str(df["timestamp"].iloc[i])[:10])
                for H in Hs:
                    d[f"f{H}"] = c[i+H]/c[i]-1-cm[H] if i+H<n else np.nan
                    d[f"c{H}"] = i//H
                rows.append(d)
    D = pd.DataFrame(rows)
    P = D[D.prof]
    def cases(sub, H):
        s = sub.dropna(subset=[f"f{H}"])
        return s.sort_values("i").groupby(["coin","w",f"c{H}"]).head(1)
    def summ(s, H, col=None):
        col = col or f"f{H}"
        if len(s)<3: return dict(n=len(s), mean=np.nan, t=np.nan)
        g = s.groupby("day")[col].sum()
        return dict(n=len(s), days=len(g), mean=s[col].mean(), t=g.mean()/(g.std(ddof=1)/np.sqrt(len(g))))
    def slope(s, x, H):
        s = s.dropna(subset=[x, f"f{H}"])
        if len(s)<5: return np.nan, np.nan
        res = stats.linregress(s[x], s[f"f{H}"])
        return res.slope, res.slope/res.stderr
    out = {}
    sits = {"break_ge2": P[P.up&(P.k>=2)], "break_ge3": P[P.up&(P.k>=3)],
            "break_eq1": P[P.up&(P.k==1)], "all_prof": P, "fc_pos": P[P.fc>0],
            "upday_top_z": P[P.r1z>1.5], "downday_z": P[P.r1z<-1.5]}
    tab=[]
    for nm, g in sits.items():
        for H in Hs:
            s = cases(g,H); d = summ(s,H); d["grp"]=nm; d["H"]=H
            sl, st = slope(s,"depth",H); d["depth_slope_t"]=st
            sl2, st2 = slope(s,"r1z",H); d["r1z_slope_t"]=st2
            tab.append(d)
    out["sit_H"] = pd.DataFrame(tab).set_index(["grp","H"]).round(4)
    B = cases(P[P.up&(P.k>=2)],5).dropna(subset=["depth"]).copy()
    B["dq"] = pd.qcut(B.depth,4,labels=False,duplicates="drop")
    out["b5_depthq"] = B.groupby("dq").agg(n=("f5","size"),depth=("depth","mean"),f5=("f5","mean"),f2=("f2","mean")).round(4)
    out["b5_runlen"] = B.groupby(B.k.clip(upper=5)).agg(n=("f5","size"),f5=("f5","mean")).round(4)
    out["b5_coin"] = B.groupby("coin").agg(n=("f5","size"),f5=("f5","mean")).round(4)
    out["b5_year"] = B.groupby("year").agg(n=("f5","size"),f5=("f5","mean")).round(4)
    B["uq"] = pd.qcut(B.r1z,3,labels=False,duplicates="drop")
    out["b5_upday_z"] = B.groupby("uq").agg(n=("f5","size"),r1z=("r1z","mean"),f5=("f5","mean")).round(4)
    A = cases(P,5).dropna(subset=["r1z"]).copy()
    A["q"] = pd.qcut(A.r1z,5,labels=False)
    out["prof_r1z_q_f5"] = A.groupby("q").agg(n=("f5","size"),r1z=("r1z","mean"),f5=("f5","mean")).round(4)
    A3 = cases(P,3).dropna(subset=["r1z"]).copy(); A3["q"]=pd.qcut(A3.r1z,5,labels=False)
    out["prof_r1z_q_f3"] = A3.groupby("q").agg(n=("f3","size"),f3=("f3","mean")).round(4)
    return out
