def explore(data):
    import numpy as np, pandas as pd
    bars=data["bars"]; days=data["days"]
    coins=list(bars.keys())
    wins=sorted({w for c in coins for w in bars[c].keys()}, key=lambda s:int(s[1:]))
    # book daily
    book=[]
    for w in wins:
        fr=[]
        for c in coins:
            if w in days[c]:
                d=days[c][w][["day","book_return"]].set_index("day")["book_return"].rename(c); fr.append(d)
        m=pd.concat(fr,axis=1).mean(axis=1).dropna()
        book.append(pd.DataFrame({"w":w,"r":m.values,"day":m.index}))
    book=pd.concat(book,ignore_index=True)
    v=(1+book.r).cumprod(); peak=v.cummax(); dd=v/peak-1
    book["dd"]=dd.values
    i_tr=int(dd.values.argmin()); i_pk=int(v.iloc[:i_tr+1].values.argmax())
    res={}
    res["deepest fall"]=pd.Series({"dd":dd.min(),"peak_w":book.w[i_pk],"trough_w":book.w[i_tr],"days":i_tr-i_pk})
    # dd per window
    res["by window"]=book.groupby("w").agg(mean=("r","mean"),sd=("r","std"),n=("r","size"),minr=("r","min")).reindex(wins)
    # per coin-bar
    rows=[]
    for c in coins:
        for w in bars[c]:
            b=bars[c][w].reset_index(drop=True)
            cl=b.close; ret1=cl.shift(-1)/cl-1
            a=b.postRebalance_current_allocation.fillna(0)
            r20=cl/cl.shift(20)-1; r60=cl/cl.shift(60)-1
            lr=np.log(cl).diff(); s30=lr.rolling(30).std(); s90=lr.rolling(90).std()
            r5p=cl/cl.shift(5)-1
            vr=b.get("debug_info.components.vol_growth.last_history_value")
            df=pd.DataFrame({"c":c,"w":w,"a":a,"g":a*ret1,"r1":ret1,"r20":r20,"r60":r60,"vratio":s30/s90,"r5p":r5p,"fc":b.forecast,
                             "f5":cl.shift(-5)/cl-1,"pos":np.arange(len(b))})
            df["day_in_book"]=book.loc[book.w==w].shape[0]
            rows.append(df)
    X=pd.concat(rows,ignore_index=True)
    X=X.dropna(subset=["r1"])
    X["side"]=np.sign(X.a)
    X["dd_flag"]=False
    # mark coin-days in deepest fall window range
    fallw=set(book.w.iloc[i_pk:i_tr+1])
    held=X[X.side!=0]
    res["gain by side"]=held.groupby("side").g.agg(["mean","sum","count","std"])
    held=held.copy()
    held["r20b"]=pd.cut(held.r20,[-1,-0.15,-0.1,-0.05,0,5])
    held["vrb"]=pd.cut(held.vratio,[0,0.8,1.0,1.2,5])
    res["gain side x r20"]=held.groupby(["side","r20b"]).g.agg(["mean","sum","count"])
    res["gain side x volratio(30/90)"]=held.groupby(["side","vrb"]).g.agg(["mean","sum","count"])
    held["fcb"]=pd.cut(held.fc.abs(),[0,5,10,15,21])
    res["gain side x |fc|"]=held.groupby(["side","fcb"]).g.agg(["mean","sum","count"])
    res["gain by window x side"]=held.groupby(["w","side"]).g.sum().unstack()
    # the fall: which coins/sides lost
    inf=held[held.w.isin(fallw)]
    res["fall windows coin x side sum"]=inf.groupby(["c","side"]).g.sum().unstack()
    # grid 5-day forecast cases: forward 5-day return by sign of forecast and r20 bucket
    G=X[(X.pos%5==0)&(X.fc!=0)].dropna(subset=["f5"]).copy()
    G["s"]=np.sign(G.fc); G["dirret"]=G.s*G.f5
    G["r20b"]=pd.cut(G.r20,[-1,-0.15,-0.1,-0.05,0,5]); G["vrb"]=pd.cut(G.vratio,[0,0.8,1.0,1.2,5])
    f=lambda x: pd.Series({"mean":x.mean(),"n":len(x),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    res["grid dir ret by side"]=G.groupby("s").dirret.apply(f).unstack()
    res["grid dir ret side x r20"]=G.groupby(["s","r20b"]).dirret.apply(f).unstack()
    res["grid dir ret side x volratio"]=G.groupby(["s","vrb"]).dirret.apply(f).unstack()
    return res
