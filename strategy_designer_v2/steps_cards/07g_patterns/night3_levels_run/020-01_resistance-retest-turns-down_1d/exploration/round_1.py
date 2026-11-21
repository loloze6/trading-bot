import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        # drift
        allr=[]
        for w,b in ws.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H)
            allr+=list(c[idx+H]/c[idx]-1)
        drift=np.mean(allr); sd=np.std(allr)
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; hi=b["high"]; lo=b["low"]
            r1=c.pct_change()
            f=pd.DataFrame({
                "ret5":c/c.shift(5)-1,
                "ret20":c/c.shift(20)-1,
                "vol20":r1.rolling(20).std(),
                "near20hi":c/hi.rolling(20).max()-1,
                "brk20":c/hi.shift(1).rolling(20).max()-1,
                "brk20lo":c/lo.shift(1).rolling(20).min()-1,
                "range1":(hi-lo)/c,
                "ret1":r1,
                "raw":b["debug_info.components.resistance.last_history_value"],
                "fc":b["forecast"],
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr":pd.to_datetime(b["timestamp"]).dt.year,
            })
            f["fwd"]=(c.shift(-H)/c-1-drift)/sd
            f["fwdraw"]=c.shift(-H)/c-1-drift
            f=f.iloc[::H]
            f["coin"]=coin; f["w"]=w
            rows.append(f)
    d=pd.concat(rows).dropna(subset=["fwd"])
    out={}
    def q(col,n=5):
        x=d.dropna(subset=[col]).copy()
        x["q"]=x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),n,labels=False))
        g=x.groupby("q")["fwdraw"].agg(["mean","count","std"])
        g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        sl=stats.linregress(x["q"],x["fwd"])
        g.loc["slope_t","mean"]=sl.slope/sl.stderr
        return g
    for col in ["ret5","ret20","vol20","near20hi","brk20","brk20lo","range1","ret1","raw"]:
        out[col]=q(col)
    g=d.groupby("wd")["fwdraw"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"])); out["weekday"]=g
    g=d.groupby("yr")["fwdraw"].agg(["mean","count"]); out["year"]=g
    return out
