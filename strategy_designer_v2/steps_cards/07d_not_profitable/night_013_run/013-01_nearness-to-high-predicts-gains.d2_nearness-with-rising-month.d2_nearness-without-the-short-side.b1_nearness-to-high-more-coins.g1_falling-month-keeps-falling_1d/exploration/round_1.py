import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars=data["bars"]; days=data["days"]
    rows=[]; drows=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values
            n=len(b)
            pos=b["postRebalance_current_allocation"].fillna(0).values
            gain=np.r_[pos[:-1]*(cl[1:]/cl[:-1]-1),np.nan]
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"]).values/b["total_portfolio_value"].values
            ret30=pd.Series(cl).pct_change(30).values
            hi60=pd.Series(cl).rolling(60,min_periods=1).max().values
            depth=cl/hi60-1
            r7=np.full(n,np.nan); r7[:-7]=cl[7:]/cl[:-7]-1
            r1=np.r_[cl[1:]/cl[:-1]-1,np.nan]
            # 7-day vol of past
            vol=pd.Series(np.r_[np.nan,cl[1:]/cl[:-1]-1]).rolling(20).std().values
            for i in range(n):
                rows.append((c,w,i,b["regime"].iloc[i],b["forecast"].iloc[i],pos[i],gain[i],fee[i],ret30[i],depth[i],r7[i],r1[i],vol[i],b["timestamp"].iloc[i]))
    df=pd.DataFrame(rows,columns="c w i reg fc pos gain fee ret30 depth r7 r1 vol ts".split())
    df["mr1"]=df.groupby("c")["r1"].transform("mean")
    df["mkt"]=df["pos"]*df["mr1"]
    df["tim"]=df["gain"]-df["mkt"]
    out={}
    out["overall"]=pd.Series({"gain":df.gain.mean(),"mkt":df.mkt.mean(),"timing":df.tim.mean(),"fee":df.fee.mean(),"mean_pos":df.pos.mean(),"share_active":(df.pos!=0).mean()})
    act=df[df.pos!=0].copy()
    act["dq"]=pd.qcut(act.depth,5,labels=False)
    out["by_depth_q"]=act.groupby("dq").agg(depth=("depth","mean"),pos=("pos","mean"),gain=("gain","mean"),tim=("tim","mean"),r1=("r1","mean"),n=("gain","size"))
    act["r30q"]=pd.qcut(act.ret30,5,labels=False)
    out["by_ret30_q"]=act.groupby("r30q").agg(r30=("ret30","mean"),pos=("pos","mean"),gain=("gain","mean"),tim=("tim","mean"),r1=("r1","mean"),n=("gain","size"))
    act["vq"]=pd.qcut(act.vol,4,labels=False)
    out["by_vol_q"]=act.groupby("vq").agg(vol=("vol","mean"),pos=("pos","mean"),gain=("gain","mean"),tim=("tim","mean"),n=("gain","size"))
    act["yr"]=pd.to_datetime(act.ts).dt.year
    out["by_year"]=act.groupby("yr").agg(gain=("gain","mean"),mkt=("mkt","mean"),tim=("tim","mean"),n=("gain","size"))
    # 7-day grid, all bars, depth within falling month vs rising month excess
    g=df[df.i%7==0].copy(); g["mr7"]=g.groupby("c")["r7"].transform("mean"); g["ex"]=g.r7-g.mr7
    g=g.dropna(subset=["ex","ret30"])
    g["fall"]=g.ret30<0
    g["dq"]=g.groupby("fall")["depth"].transform(lambda s:pd.qcut(s.rank(method="first"),5,labels=False))
    out["grid_excess"]=g.groupby(["fall","dq"]).agg(depth=("depth","mean"),ex=("ex","mean"),n=("ex","size"),t=("ex",lambda s:s.mean()/(s.std()/np.sqrt(len(s)))))
    gf=g[g.fall].copy(); gf["r30q"]=pd.qcut(gf.ret30,4,labels=False)
    out["grid_fall_by_r30"]=gf.groupby("r30q").agg(r30=("ret30","mean"),depth=("depth","mean"),ex=("ex","mean"),n=("ex","size"))
    # daily book
    dd=[]
    for c in days:
        for w,d in days[c].items():
            x=d.dropna(subset=["book_return"]); dd.append(x.assign(c=c,w=w))
    dd=pd.concat(dd)
    out["by_window_book"]=dd.groupby("w").agg(br=("book_return","mean"),cr=("coin_return","mean"),n=("book_return","size"))
    return out
