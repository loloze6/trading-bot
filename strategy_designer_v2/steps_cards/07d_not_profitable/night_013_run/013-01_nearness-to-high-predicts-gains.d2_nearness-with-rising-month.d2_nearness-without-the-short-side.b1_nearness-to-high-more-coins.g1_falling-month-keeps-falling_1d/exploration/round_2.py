import numpy as np, pandas as pd

def explore(data):
    bars=data["bars"]
    rows=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values; n=len(b)
            pos=b["postRebalance_current_allocation"].fillna(0).values
            r1=np.r_[cl[1:]/cl[:-1]-1,np.nan]
            gain=pos*r1
            ret30=pd.Series(cl).pct_change(30).values
            ret7=pd.Series(cl).pct_change(7).values
            hi60=pd.Series(cl).rolling(60,min_periods=1).max().values
            depth=cl/hi60-1
            r7=np.full(n,np.nan); r7[:-7]=cl[7:]/cl[:-7]-1
            fc=b["forecast"].values
            for i in range(n):
                rows.append((c,w,i,pos[i],gain[i],ret30[i],ret7[i],depth[i],r7[i],r1[i],fc[i]))
    df=pd.DataFrame(rows,columns="c w i pos gain ret30 ret7 depth r7 r1 fc".split())
    out={}
    act=df[(df.pos!=0)].dropna(subset=["gain"]).copy()
    def sh(s): return s.mean()/s.std()*np.sqrt(365) if len(s)>2 else np.nan
    # counterfactual: active bars only, keep moderate declines
    for name,m in {"all":act.depth<1,"depth>-0.45":act.depth>-0.45,"ret30>-0.30":act.ret30>-0.30,
                   "both":(act.depth>-0.45)&(act.ret30>-0.30),
                   "ret7<0":act.ret7<0,"ret7>=0":act.ret7>=0}.items():
        s=act[m]
        out.setdefault("subsets",[]).append(pd.Series({"name":name,"n":len(s),"gain":s.gain.mean(),"t":s.gain.mean()/(s.gain.std()/np.sqrt(len(s))),"sh_bar":sh(s.gain)}))
    out["subsets"]=pd.DataFrame(out["subsets"])
    # 7-day bounce: last 7-day return quintiles while active
    act["q7"]=pd.qcut(act.ret7,5,labels=False)
    out["by_ret7"]=act.groupby("q7").agg(ret7=("ret7","mean"),depth=("depth","mean"),gain=("gain","mean"),r1=("r1","mean"),n=("gain","size"))
    # grid excess in falling month by depth deciles, to see where it turns
    g=df[df.i%7==0].copy(); g["ex"]=g.r7-g.groupby("c")["r7"].transform("mean")
    g=g.dropna(subset=["ex","ret30"]); gf=g[g.ret30<0].copy()
    gf["dq"]=pd.qcut(gf.depth,10,labels=False)
    out["fall_depth_dec"]=gf.groupby("dq").agg(depth=("depth","mean"),r30=("ret30","mean"),ex=("ex","mean"),n=("ex","size"),t=("ex",lambda s:s.mean()/(s.std()/np.sqrt(len(s)))))
    # the deepest-fall bars of book: worst 5% gain days, what situation
    thr=act.gain.quantile(0.05)
    worst=act[act.gain<=thr]
    out["worst5pct_vs_all"]=pd.DataFrame({"worst":[worst.depth.mean(),worst.ret30.mean(),worst.ret7.mean(),worst.pos.mean(),worst.gain.sum()],
        "all":[act.depth.mean(),act.ret30.mean(),act.ret7.mean(),act.pos.mean(),act.gain.sum()]},index=["depth","ret30","ret7","pos","sum_gain"])
    return out
