def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; bar_rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r=c.pct_change()
            um=r.abs().rolling(180,min_periods=60).mean()
            sgn=np.sign(r).fillna(0).values
            L=np.zeros(len(b)); 
            for i in range(1,len(b)):
                if sgn[i]!=0 and sgn[i]==sgn[i-1]: L[i]=L[i-1]+sgn[i]
                else: L[i]=sgn[i]
            Ls=pd.Series(L)
            # streak gain relative to start
            st=[]; 
            for i in range(len(b)):
                k=int(abs(L[i])); st.append(c.iloc[i]/c.iloc[i-k]-1 if k>0 and i-k>=0 else 0.0)
            sg=pd.Series(st)/um
            # volume fade: last 2 bars volume vs streak-bars volume mean (log)
            vf=np.log(v.rolling(2).mean()/v.rolling(6).mean())
            r6=(c/c.shift(6)-1)/(um*np.sqrt(6)); r18=(c/c.shift(18)-1)/(um*np.sqrt(18))
            r42=(c/c.shift(42)-1)/(um*np.sqrt(42))
            volr=um/r.abs().rolling(1080,min_periods=200).mean()
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,len(b)-18,18):
                rows.append(dict(coin=coin,w=w,f18=c.iloc[i+18]/c.iloc[i]-1,f6=c.iloc[i+6]/c.iloc[i]-1 if i+6<len(b) else np.nan,
                    L=L[i],sg=sg.iloc[i],vf=vf.iloc[i],r6=r6.iloc[i],r18=r18.iloc[i],r42=r42.iloc[i],volr=volr.iloc[i],
                    fc=b["forecast"].iloc[i],um=um.iloc[i]))
            bar_rows.append(pd.DataFrame(dict(coin=coin,r_next=r.shift(-1),hour=ts.dt.hour,wd=ts.dt.weekday,
                    r1s=r/um, L=L)))
    G=pd.DataFrame(rows); B=pd.concat(bar_rows)
    G["drift"]=G.groupby("coin")["f18"].transform("mean")
    G["ex"]=G["f18"]-G["drift"]; G["exz"]=G["ex"]/G.groupby("coin")["f18"].transform("std")
    out={}
    def tab(col,q=5):
        d=G.dropna(subset=[col,"exz"]).copy()
        d["b"]=d.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"),q,labels=False))
        t=d.groupby("b")["exz"].agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
        top=d[d.b==q-1]; bot=d[d.b==0]
        pc=d[d.b==q-1].groupby("coin")["exz"].mean()-d[d.b==0].groupby("coin")["exz"].mean()
        t.loc["top-bot","mean"]=top.exz.mean()-bot.exz.mean(); t.loc["top-bot","t"]=stats.ttest_ind(top.exz,bot.exz,equal_var=False)[0]
        t.loc["coins_pos","mean"]=(pc>0).sum()
        return t[["mean","count","t"]].round(3)
    for col in ["sg","L","r6","r18","r42","volr","vf","fc"]: out["q_"+col]=tab(col)
    # streak size x volume fade (both sides): signed gain * fade
    d=G.dropna(subset=["sg","vf"]).copy(); d=d[d.L.abs()>=2]
    d["side"]=np.sign(d.L); d["exs"]=d.exz*d.side
    d["vfh"]=d.groupby("side")["vf"].transform(lambda x:(x<x.median()).astype(int))
    out["streak2plus_side_by_fade"]=d.groupby(["side","vfh"])["exs"].agg(["mean","count"]).round(3)
    # hour/weekday on 1-bar next returns (scaled)
    B["rn"]=B.groupby("coin")["r_next"].transform(lambda x:(x-x.mean())/x.std())
    for k in ["hour","wd"]:
        t=B.groupby(k)["rn"].agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"])); out[k]=t[["mean","t"]].round(3)
    # reversal after large single bar
    B["bq"]=pd.cut(B.r1s,[-99,-3,-2,-1,1,2,3,99])
    t=B.groupby("bq")["rn"].agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"])); out["after_1bar_move"]=t[["mean","count","t"]].round(3)
    # book days
    D=[]
    for coin,wins in data["days"].items():
        for w,dd in wins.items():
            dd=dd.copy(); dd["coin"]=coin; dd["cprev3"]=dd["close"]/dd["close"].shift(3)-1; D.append(dd)
    D=pd.concat(D).dropna(subset=["book_return"])
    D["q"]=D.groupby("coin")["book_return"].transform(lambda x:pd.qcut(x.rank(method="first"),10,labels=False))
    out["book_by_decile"]=D.groupby("q")[["book_return","coin_return","cprev3"]].mean().round(4)
    return out
