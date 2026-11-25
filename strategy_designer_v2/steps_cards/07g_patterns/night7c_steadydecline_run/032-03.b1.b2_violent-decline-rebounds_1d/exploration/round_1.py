def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]
            d=pd.DataFrame({"coin":coin,"win":w})
            d=pd.DataFrame(index=b.index)
            d["coin"]=coin; d["win"]=w; d["pos"]=np.arange(len(b))
            d["r28"]=c/c.shift(28)-1
            d["r5p"]=c/c.shift(5)-1
            d["r1"]=c.pct_change()
            rng=(b["high"]-b["low"])/c
            d["rngratio"]=rng.rolling(5).mean()/rng.rolling(28).mean()
            d["rng28rel"]=rng.rolling(28).mean()/rng.expanding(28).mean()
            d["volratio"]=b["volume"].rolling(5).mean()/b["volume"].rolling(28).mean()
            d["fwd5"]=c.shift(-5)/c-1
            d["fwd1"]=c.shift(-1)/c-1
            d["regime"]=b["regime"].values
            d["fc"]=b["forecast"].values
            d["wd"]=pd.to_datetime(b["timestamp"]).dt.weekday
            d["year"]=pd.to_datetime(b["timestamp"]).dt.year
            d["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    G=A[(A.pos%5==0)&A.fwd5.notna()].copy()
    G["ex"]=G.fwd5-G.groupby("coin").fwd5.transform("mean")
    out={}
    def tab(df,col,q=5):
        x=df.dropna(subset=[col,"ex"]).copy()
        x["b"]=pd.qcut(x[col],q,labels=False,duplicates="drop")
        g=x.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=("ex","size"),mean_ex=("ex","mean"),sd=("ex","std"))
        g["t"]=g.mean_ex/(g.sd/np.sqrt(g.n))
        r=stats.linregress(x[col],x.ex)
        g.loc["slope_t"]=[np.nan,np.nan,len(x),r.slope,np.nan,r.slope/r.stderr]
        return g
    out["r28_all"]=tab(G,"r28")
    out["r5p_all"]=tab(G,"r5p")
    out["r1_all"]=tab(G,"r1")
    out["rngratio_all"]=tab(G,"rngratio")
    out["rng28rel_all"]=tab(G,"rng28rel")
    out["volratio_all"]=tab(G,"volratio")
    neg=G[G.r28<0]
    out["r28neg_rng28rel"]=tab(neg,"rng28rel",3)
    out["r28neg_rngratio"]=tab(neg,"rngratio",3)
    out["by_regime"]=G.groupby("regime").ex.agg(["size","mean","std"]).assign(t=lambda g:g["mean"]/(g["std"]/np.sqrt(g["size"])))
    out["by_year"]=G.groupby("year").ex.agg(["size","mean"])
    A["ex1"]=A.fwd1-A.groupby("coin").fwd1.transform("mean")
    out["wd_fwd1"]=A.groupby("wd").ex1.agg(["size","mean","std"]).assign(t=lambda g:g["mean"]/(g["std"]/np.sqrt(g["size"])))
    out["r1_fwd1"]=tab(A.assign(ex=A.ex1),"r1")
    # book
    D=[]
    for coin,wins in data["days"].items():
        for w,dd in wins.items():
            x=dd.copy(); x["coin"]=coin; x["win"]=w; D.append(x)
    D=pd.concat(D)
    bk=D.groupby(["win","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).dropna()
    out["book_by_win"]=bk.groupby(level=0).agg(n=("br","size"),book=("br","mean"),coins=("cr","mean"))
    top=bk.br.nlargest(15); bot=bk.br.nsmallest(15)
    out["book_extremes_coin"]=pd.DataFrame({"top_book":[top.mean()],"top_coin":[bk.loc[top.index,"cr"].mean()],"bot_book":[bot.mean()],"bot_coin":[bk.loc[bot.index,"cr"].mean()],"corr":[bk.br.corr(bk.cr)]})
    T=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): T.append(t.assign(coin=coin))
    T=pd.concat(T)
    T["fq"]=pd.qcut(T.entry_forecast,4,labels=False,duplicates="drop")
    out["trades_by_fc"]=T.groupby("fq").agg(n=("net_profit_loss_percent","size"),fc=("entry_forecast","mean"),pl=("net_profit_loss_percent","mean"),dur_d=("duration_minutes",lambda s:s.mean()/1440))
    return out
