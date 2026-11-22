def explore(data):
    import pandas as pd, numpy as np
    out = {}
    days = data["days"]; bars = data["bars"]
    wins = sorted({w for c in days for w in days[c]}, key=lambda s:int(s[1:]))
    # book daily chain
    rows=[]
    for w in wins:
        frames=[days[c][w].set_index("day")["book_return"].rename(c) for c in days if w in days[c]]
        d=pd.concat(frames,axis=1)
        m=d.mean(axis=1).dropna()
        for i,v in enumerate(m.values): rows.append((w,i,v))
    b=pd.DataFrame(rows,columns=["w","i","r"])
    eq=(1+b.r).cumprod(); dd=eq/eq.cummax()-1
    b["dd"]=dd.values
    out["worst_dd"]=float(dd.min())
    yr=eq.iloc[-1]**(365/len(b))-1
    out["yearly"]=float(yr)
    # drawdown depth per window: min dd within window and window return
    g=b.groupby("w").agg(ret=("r",lambda x:(1+x).prod()-1),mindd=("dd","min"),n=("r","size"))
    g["wdd"]=b.groupby("w")["r"].apply(lambda x:((1+x).cumprod()/(1+x).cumprod().cummax()-1).min())
    out["by_window"]=g.loc[wins].round(4)
    # per bar pnl with features
    recs=[]
    for c in bars:
        for w,df in bars[c].items():
            df=df.reset_index(drop=True)
            cl=df.close; pos=df.postRebalance_current_allocation.fillna(0)
            nr=cl.shift(-1)/cl-1
            r30=cl/cl.shift(30)-1
            rng=df.high.rolling(30).max()-df.low.rolling(30).min()
            nmr=(cl-cl.shift(30)).abs()/rng
            r5=cl/cl.shift(5)-1
            vol=cl.pct_change().rolling(20).std(); vol60=cl.pct_change().rolling(60,min_periods=20).std()
            hi=df.high.rolling(30).max(); lo=df.low.rolling(30).min()
            posr=(cl-lo)/(hi-lo)
            t=pd.DataFrame({"c":c,"w":w,"pos":pos,"pnl":pos*nr,"side":np.sign(pos),
              "f":df.forecast,"bir":df["debug_info.bars_in_regime"],"nmr":nmr,
              "r5dir":np.sign(pos)*r5,"r30dir":np.sign(pos)*r30,"vr":vol/vol60,"posr":posr,"ts":df.timestamp})
            recs.append(t)
    a=pd.concat(recs); a=a[a.pos!=0].dropna(subset=["pnl"])
    def grp(col,q=4):
        x=a.dropna(subset=[col]).copy(); x["b"]=pd.qcut(x[col],q,duplicates="drop")
        r=x.groupby("b",observed=True)["pnl"].agg(["mean","std","count"])
        r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"])); r["sum"]=x.groupby("b",observed=True)["pnl"].sum()
        return r.round(5)
    out["side"]=a.groupby("side")["pnl"].agg(["mean","count","sum"]).round(5)
    for col in ["bir","nmr","r5dir","r30dir","vr","f"]:
        out["by_"+col]=grp(col)
    a["year"]=pd.to_datetime(a.ts).dt.year
    out["year_side"]=a.groupby(["year","side"])["pnl"].agg(["mean","count","sum"]).round(5)
    out["tail_share_worst5pct"]=float(a.pnl[a.pnl<a.pnl.quantile(0.05)].sum()/a.pnl.sum())
    return out
