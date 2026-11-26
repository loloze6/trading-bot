def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]; trades=data["trades"]
    out={}
    rows=[]; grid=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True).copy()
            cl=b["close"].values
            pos=b["postRebalance_current_allocation"].fillna(0).values
            r1=np.r_[cl[1:]/cl[:-1]-1,np.nan]
            raw=b.get("debug_info.components.vol_growth.last_history_value")
            raw=raw.values if raw is not None else np.full(len(b),np.nan)
            act=(b["regime"]=="unknown").values
            # 20-day trailing return and 30-day vol inside window
            ret20=pd.Series(cl).pct_change(20).values
            vol30=pd.Series(cl).pct_change().rolling(30).std().values
            f5=np.full(len(b),np.nan)
            f5[:-5]=cl[5:]/cl[:-5]-1
            for i in range(len(b)):
                rows.append((c,w,pos[i],r1[i],act[i],raw[i],b["forecast"].iloc[i]))
            for i in range(0,len(b)-5,5):
                grid.append((c,w,f5[i],act[i],raw[i],b["forecast"].iloc[i],ret20[i],vol30[i],pos[i]))
    R=pd.DataFrame(rows,columns=["c","w","pos","r1","act","raw","fc"]).dropna(subset=["r1"])
    R["g"]=R.pos*R.r1
    R["side"]=np.sign(R.pos)
    out["bar gain by side"]=R.groupby("side")["g"].agg(["count","mean","sum"])
    out["bar gain by side,window sum"]=R.pivot_table(index="w",columns="side",values="g",aggfunc="sum")
    G=pd.DataFrame(grid,columns=["c","w","f5","act","raw","fc","ret20","vol30","pos"]).dropna(subset=["f5"])
    drift=G.groupby("c")["f5"].mean(); G["ex"]=G.f5-G.c.map(drift)
    A=G[G.act & (G.fc!=0)].copy()
    A["q"]=pd.qcut(A.raw,5,labels=False,duplicates="drop")
    out["active grid by raw quintile"]=A.groupby("q").agg(n=("ex","size"),raw=("raw","mean"),ex=("ex","mean"),tot=("f5","mean"))
    A["sideexp"]=np.sign(A.raw)
    out["active by sign of raw"]=A.groupby("sideexp").agg(n=("ex","size"),ex=("ex","mean"),tot=("f5","mean"),t=("ex",lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    # all grid by raw quintile regardless of profile
    Gn=G.dropna(subset=["raw"]).copy()
    out["inactive grid count with raw"]=len(G[~G.act])
    # vol state split
    A["hv"]=A.groupby("c")["vol30"].transform(lambda x: x>x.median())
    out["active by raw sign x high vol"]=A.groupby(["sideexp","hv"]).agg(n=("ex","size"),ex=("ex","mean"),tot=("f5","mean"))
    A["r20q"]=pd.qcut(A.ret20,3,labels=False)
    out["active by raw sign x 20d ret tercile"]=A.groupby(["sideexp","r20q"]).agg(n=("ex","size"),r20=("ret20","mean"),ex=("ex","mean"),tot=("f5","mean"))
    # book daily
    D=[]
    for c in days:
        for w,d in days[c].items():
            d=d.copy(); d["c"]=c; d["w"]=w; d["i"]=range(len(d)); D.append(d)
    D=pd.concat(D)
    bk=D.groupby(["w","i"]).agg(b=("book_return","mean"),h=("coin_return","mean")).dropna().reset_index()
    order=sorted(bk.w.unique(),key=lambda s:int(s[1:]))
    bk["wo"]=bk.w.map({w:k for k,w in enumerate(order)}); bk=bk.sort_values(["wo","i"])
    v=(1+bk.b).cumprod().values; dd=v/np.maximum.accumulate(v)-1
    out["book sharpe/hold sharpe"]=pd.Series({"book":bk.b.mean()/bk.b.std()*np.sqrt(365),"hold":bk.h.mean()/bk.h.std()*np.sqrt(365),"maxdd":dd.min(),"corr":bk.b.corr(bk.h)})
    bk["dd"]=dd
    out["book by window"]=bk.groupby("w").agg(b=("b","sum"),h=("h","sum"),mindd=("dd","min"))
    T=pd.concat([t.assign(c=c) for c in trades for t in trades[c].values() if len(t)])
    out["trades by side"]=T.groupby("side").agg(n=("net_profit_loss_percent","size"),net=("net_profit_loss_percent","mean"),gross=("profit_loss_percent","mean"),dur=("duration_minutes",lambda x:x.mean()/1440))
    return out
