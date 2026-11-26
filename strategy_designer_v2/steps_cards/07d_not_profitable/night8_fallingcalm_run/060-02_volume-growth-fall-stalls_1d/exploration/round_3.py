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
            ret10=s.pct_change(10).values
            vol30=s.pct_change().rolling(30).std().values
            f5=np.full(n,np.nan); f5[:-5]=cl[5:]/cl[:-5]-1
            f10=np.full(n,np.nan); f10[:-10]=cl[10:]/cl[:-10]-1
            for i in range(n):
                rows.append((c,w,i,i%5==0,i%10==0,pos[i],r1[i],act[i],raw[i],ret20[i],ret10[i],vol30[i],f5[i],f10[i]))
    R=pd.DataFrame(rows,columns=["c","w","i","g5","g10","pos","r1","act","raw","ret20","ret10","vol30","f5","f10"])
    R["hv"]=R.groupby("c")["vol30"].transform(lambda x: x>x.median())
    d5=R[R.g5].groupby("c")["f5"].mean(); R["ex5"]=R.f5-R.c.map(d5)
    d10=R[R.g10].groupby("c")["f10"].mean(); R["ex10"]=R.f10-R.c.map(d10)
    R["sg"]=np.sign(R.raw)
    tt=lambda x: x.mean()/x.std()*np.sqrt(len(x))
    G=R[R.g5&R.act].dropna(subset=["f5","raw","ret20"]).copy()
    G["r20neg"]=G.ret20<0
    # condition alone: r20<0 vs >0 in falling, raw-free
    out["cond alone: falling grid by r20<0"]=G.groupby("r20neg").agg(n=("ex5","size"),ex=("ex5","mean"),t=("ex5",tt))
    G["direx"]=G.sg*G.ex5
    out["signed excess by r20<0 x side"]=G.groupby(["r20neg","sg"]).agg(n=("direx","size"),direx=("direx","mean"),t=("direx",tt))
    G["q"]=G.groupby("r20neg")["raw"].transform(lambda x: pd.qcut(x,4,labels=False))
    out["ex by r20<0 x raw quartile"]=G.groupby(["r20neg","q"]).agg(n=("ex5","size"),raw=("raw","mean"),ex=("ex5","mean"))
    def slope(df,y):
        x=df.raw.values; yy=df[y].values; x=x-x.mean()
        b=(x*(yy-yy.mean())).sum()/(x*x).sum(); res=yy-yy.mean()-b*x
        se=np.sqrt((res**2).sum()/(len(x)-2)/(x*x).sum()); return pd.Series({"n":len(x),"slope":b,"t":b/se})
    out["slope on raw: all / r20<0 / r20>0"]=pd.DataFrame({"all":slope(G,"ex5"),"r20<0":slope(G[G.r20neg],"ex5"),"r20>0":slope(G[~G.r20neg],"ex5")}).T
    G10=R[R.g10&R.act].dropna(subset=["f10","raw","ret20"])
    out["slope 10d: all / r20<0"]=pd.DataFrame({"all":slope(G10,"ex10"),"r20<0":slope(G10[G10.ret20<0],"ex10")}).T
    R=R.dropna(subset=["r1"]).sort_values(["c","w","i"]).copy()
    def book(m):
        p=R.pos.where(m,0.0)
        dp=p.groupby([R.c,R.w]).diff().fillna(p).abs()
        g=p*R.r1-dp*0.00095
        bk=pd.DataFrame({"w":R.w,"i":R.i,"g":g}).groupby(["w","i"]).mean().reset_index()
        bk["wo"]=bk.w.str[1:].astype(int); bk=bk.sort_values(["wo","i"])
        v=(1+bk.g).cumprod().values; dd=(v/np.maximum.accumulate(v)-1).min()
        yr=v[-1]**(365/len(v))-1
        wl=min(bk[bk.w!=w].g.mean()/bk[bk.w!=w].g.std()*np.sqrt(365) for w in bk.w.unique())
        return pd.Series({"sharpe":bk.g.mean()/bk.g.std()*np.sqrt(365),"yr":yr,"maxdd":dd,"calmar":yr/-dd,"inpos":(p!=0).mean(),"loo_min":wl})
    V={}
    V["as tested"]=book(R.pos==R.pos)
    V["only r20<0"]=book(R.ret20<0)
    V["only r10<0"]=book(R.ret10<0)
    V["only r20<0 & agitated"]=book((R.ret20<0)&R.hv)
    V["r20<0, long only agitated"]=book((R.ret20<0)&((R.pos<0)|R.hv))
    out["variants"]=pd.DataFrame(V).T
    return out
