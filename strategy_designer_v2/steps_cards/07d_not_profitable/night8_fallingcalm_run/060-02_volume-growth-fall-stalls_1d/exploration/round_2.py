def explore(data):
    import numpy as np, pandas as pd
    bars=data["bars"]
    out={}
    rows=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values; n=len(b)
            pos=b["postRebalance_current_allocation"].fillna(0).values
            r1=np.r_[cl[1:]/cl[:-1]-1,np.nan]
            raw=b.get("debug_info.components.vol_growth.last_history_value")
            raw=raw.values if raw is not None else np.full(n,np.nan)
            act=(b["regime"]=="unknown").values
            s=pd.Series(cl)
            ret20=s.pct_change(20).values
            vol30=s.pct_change().rolling(30).std().values
            f5=np.full(n,np.nan); f5[:-5]=cl[5:]/cl[:-5]-1
            for i in range(n):
                rows.append((c,w,i,i%5==0,pos[i],r1[i],act[i],raw[i],ret20[i],vol30[i],f5[i]))
    R=pd.DataFrame(rows,columns=["c","w","i","grid","pos","r1","act","raw","ret20","vol30","f5"])
    R["hv"]=R.groupby("c")["vol30"].transform(lambda x: x>x.median())
    drift=R[R.grid].groupby("c")["f5"].mean(); R["ex"]=R.f5-R.c.map(drift)
    G=R[R.grid&R.act].dropna(subset=["f5"])
    # condition alone: falling profile, by agitation and by 20d-ret tercile, regardless of raw
    G=G.copy(); G["r20q"]=pd.qcut(G.ret20,3,labels=False)
    out["falling grid by hv (all raw)"]=G.groupby("hv").agg(n=("ex","size"),ex=("ex","mean"),tot=("f5","mean"))
    out["falling grid by r20 tercile (all raw)"]=G.groupby("r20q").agg(n=("ex","size"),r20=("ret20","mean"),ex=("ex","mean"),tot=("f5","mean"))
    G["sg"]=np.sign(G.raw)
    G["direx"]=G.sg*G.ex
    out["direction-signed excess by hv x side"]=G.groupby(["hv","sg"]).agg(n=("direx","size"),direx=("direx","mean"),t=("direx",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
    # variants of the book, approximate daily: pos*r1 minus cost on change
    R=R.dropna(subset=["r1"]).copy()
    R=R.sort_values(["c","w","i"])
    def book(mask_fn,name):
        p=R.pos.where(mask_fn(R),0.0)
        dp=p.groupby([R.c,R.w]).diff().fillna(p).abs()
        g=p*R.r1-dp*0.00095
        bk=pd.DataFrame({"w":R.w,"i":R.i,"g":g,"h":R.r1}).groupby(["w","i"]).mean().reset_index()
        bk["wo"]=bk.w.str[1:].astype(int); bk=bk.sort_values(["wo","i"])
        v=(1+bk.g).cumprod().values; dd=(v/np.maximum.accumulate(v)-1).min()
        yr=v[-1]**(365/len(v))-1
        return pd.Series({"sharpe":bk.g.mean()/bk.g.std()*np.sqrt(365),"hold":bk.h.mean()/bk.h.std()*np.sqrt(365),"yr":yr,"maxdd":dd,"calmar":yr/-dd,"inpos":(p!=0).mean()})
    V={}
    V["as tested"]=book(lambda d: d.pos==d.pos,"")
    V["long only"]=book(lambda d: d.pos>0,"")
    V["short only"]=book(lambda d: d.pos<0,"")
    V["long only agitated"]=book(lambda d: (d.pos>0)&d.hv,"")
    V["agitated both"]=book(lambda d: d.hv,"")
    V["calm both"]=book(lambda d: ~d.hv,"")
    V["long + short when r20 between -20%,0"]=book(lambda d: (d.pos>0)|((d.pos<0)&(d.ret20>-0.2)&(d.ret20<0)),"")
    V["long; short only calm"]=book(lambda d: (d.pos>0)|((d.pos<0)&~d.hv),"")
    out["variants"]=pd.DataFrame(V).T
    # deepest falls: per window, gain by side during the window's worst 30 days
    R["g"]=R.pos*R.r1
    out["gain by side x hv"]=R[R.pos!=0].assign(sd=np.sign(R.pos)).groupby(["sd","hv"])["g"].agg(["count","mean","sum"])
    out["gain by side x r20 sign"]=R[R.pos!=0].assign(sd=np.sign(R.pos),r20p=R.ret20>0).groupby(["sd","r20p"])["g"].agg(["count","mean","sum"])
    return out
