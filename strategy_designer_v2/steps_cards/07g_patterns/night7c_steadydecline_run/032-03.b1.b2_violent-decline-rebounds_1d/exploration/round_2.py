def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            d=pd.DataFrame(index=b.index)
            d["coin"]=coin; d["win"]=w; d["pos"]=np.arange(len(b))
            d["r28"]=c/c.shift(28)-1
            d["r14"]=c/c.shift(14)-1
            d["r5p"]=c/c.shift(5)-1
            d["r1"]=c.pct_change()
            rng=(b["high"]-b["low"])/c
            d["rngratio"]=rng.rolling(5).mean()/rng.rolling(28).mean()
            d["rng28rel"]=rng.rolling(28).mean()/rng.expanding(28).mean()
            vol=c.pct_change().rolling(28).std()
            d["vol28"]=vol
            d["volratio"]=b["volume"].rolling(5).mean()/b["volume"].rolling(28).mean()
            d["fwd5"]=c.shift(-5)/c-1
            d["fwd1"]=c.shift(-1)/c-1
            d["regime"]=b["regime"].values
            d["fc"]=b["forecast"].values
            ts=pd.to_datetime(b["timestamp"])
            d["wd"]=ts.dt.weekday.values
            d["year"]=ts.dt.year.values
            rows.append(d)
    A=pd.concat(rows,ignore_index=True)
    A["vol28z"]=A.vol28/A.groupby("coin").vol28.transform("mean")
    G=A[(A.pos%5==0)&A.fwd5.notna()].copy()
    G["ex"]=G.fwd5-G.groupby("coin").fwd5.transform("mean")
    def tab(df,col,q=5,y="ex"):
        x=df.dropna(subset=[col,y]).copy()
        x["b"]=pd.qcut(x[col],q,labels=False,duplicates="drop")
        g=x.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=(y,"size"),mean_ex=(y,"mean"),sd=(y,"std"))
        g["t"]=g.mean_ex/(g.sd/np.sqrt(g.n))
        r=stats.linregress(x[col],x[y])
        g.loc["slope_t"]=[np.nan,np.nan,len(x),r.slope,np.nan,r.slope/r.stderr]
        return g
    def safe(name,f):
        try: out[name]=f()
        except Exception as e: out[name]=str(e)[:200]
    safe("r28_all",lambda:tab(G,"r28"))
    safe("r14_all",lambda:tab(G,"r14"))
    safe("r5p_all",lambda:tab(G,"r5p"))
    safe("rngratio_all",lambda:tab(G,"rngratio"))
    safe("rng28rel_all",lambda:tab(G,"rng28rel"))
    safe("vol28z_all",lambda:tab(G,"vol28z"))
    safe("volratio_all",lambda:tab(G,"volratio"))
    neg=G[G.r28<0]
    safe("r28neg_calm_r28",lambda:tab(neg[neg.rng28rel<1],"r28",3))
    safe("r28neg_wide_r28",lambda:tab(neg[neg.rng28rel>=1],"r28",3))
    safe("r28pos_r28",lambda:tab(G[G.r28>=0],"r28",3))
    safe("inregime_r28",lambda:tab(G[G.regime=="mean_reversion"],"r28",3))
    safe("by_regime",lambda:G.groupby("regime").ex.agg(["size","mean","std"]).assign(t=lambda g:g["mean"]/(g["std"]/np.sqrt(g["size"]))))
    safe("by_year",lambda:G.groupby("year").ex.agg(["size","mean","std"]).assign(t=lambda g:g["mean"]/(g["std"]/np.sqrt(g["size"]))))
    A["ex1"]=A.fwd1-A.groupby("coin").fwd1.transform("mean")
    safe("wd_fwd1",lambda:A.groupby("wd").ex1.agg(["size","mean","std"]).assign(t=lambda g:g["mean"]/(g["std"]/np.sqrt(g["size"]))))
    safe("r1_fwd1",lambda:tab(A,"r1",5,"ex1"))
    def book():
        D=[]
        for coin,wins in data["days"].items():
            for w,dd in wins.items():
                x=dd.copy(); x["coin"]=coin; x["win"]=w; D.append(x)
        D=pd.concat(D)
        bk=D.groupby(["win","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).dropna()
        top=bk.br.nlargest(15); bot=bk.br.nsmallest(15)
        return bk.groupby(level=0).agg(n=("br","size"),book=("br","mean"),coins=("cr","mean")), pd.DataFrame({"top_book":[top.mean()],"top_coin":[bk.loc[top.index,"cr"].mean()],"bot_book":[bot.mean()],"bot_coin":[bk.loc[bot.index,"cr"].mean()],"corr":[bk.br.corr(bk.cr)]})
    try:
        a,b2=book(); out["book_by_win"]=a; out["book_extremes"]=b2
    except Exception as e: out["book"]=str(e)[:200]
    def trades():
        T=[]
        for coin,wins in data["trades"].items():
            for w,t in wins.items():
                if len(t): T.append(t.assign(coin=coin))
        T=pd.concat(T)
        T["fq"]=pd.qcut(T.entry_forecast,4,labels=False,duplicates="drop")
        return T.groupby("fq").agg(n=("net_profit_loss_percent","size"),fc=("entry_forecast","mean"),pl=("net_profit_loss_percent","mean"),dur_d=("duration_minutes",lambda s:s.mean()/1440))
    safe("trades_by_fc",trades)
    return out
