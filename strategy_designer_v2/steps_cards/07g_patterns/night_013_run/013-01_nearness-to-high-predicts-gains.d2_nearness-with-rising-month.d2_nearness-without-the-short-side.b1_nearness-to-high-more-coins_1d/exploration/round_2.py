def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({
                "coin":coin,"win":w,"wn":int(w[1:]),
                "fwd7":c.shift(-7)/c-1,"fwd1":c.shift(-1)/c-1,
                "ret7":c/c.shift(7)-1,"ret30":c/c.shift(30)-1,
                "vrat":b["volume"]/b["volume"].rolling(20).mean(),
                "vrat5":b["volume"].rolling(5).mean()/b["volume"].rolling(30).mean(),
                "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],
                "wd":ts.dt.weekday,"yr":ts.dt.year,"day":ts.dt.floor("D"),
                "pos":np.arange(len(b)),
                "hi_gap":c/c.rolling(60,min_periods=20).max()-1,
            })
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    A["cm7"]=A.groupby("coin")["fwd7"].transform(lambda s: s[A.loc[s.index,"pos"]%7==0].mean())
    A["cm1"]=A.groupby("coin")["fwd1"].transform("mean")
    G=A[(A.pos%7==0)&A.fwd7.notna()].copy()
    G["ex"]=G.fwd7-G.cm7
    G["late"]=(G.wn>=13).astype(int)
    out={}
    # weekday clustered: one obs per day = mean across coins of excess next-day return
    A["ex1"]=A.fwd1-A.cm1
    dd=A.dropna(subset=["ex1"]).groupby(["day"]).agg(ex1=("ex1","mean"),wd=("wd","first"),yr=("yr","first"))
    def tt(s): return pd.Series({"mean":s.mean(),"n":s.count(),"t":s.mean()/(s.std()/np.sqrt(s.count()))})
    out["weekday_dayclustered"]=dd.groupby("wd")["ex1"].apply(tt).unstack()
    dd["half"]=(dd.yr>=2022).astype(int)
    out["weekday_by_half_t"]=dd.groupby(["half","wd"])["ex1"].apply(lambda s:s.mean()/(s.std()/np.sqrt(len(s)))).unstack()
    # clustered quintile tables: average ex per (win,pos) date-cell within quintile
    def ctab(df,col,q=5,by=None):
        d=df.dropna(subset=[col,"ex"]).copy()
        d["b"]=d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),q,labels=False))
        keys=["b"]+([by] if by else [])
        cl=d.groupby(keys+["win","pos"])["ex"].mean().reset_index()
        g=cl.groupby(keys)["ex"].apply(tt).unstack()
        return g
    ina=G[G.ret30<=0]; act=G[G.ret30>0]
    out["ret30neg_q_clustered"]=ctab(ina,"ret30")
    out["ret30neg_q_by_late"]=ctab(ina,"ret30",by="late")
    out["higap_all_clustered_by_late"]=ctab(G,"hi_gap",by="late")
    out["vrat_all_clustered_by_late"]=ctab(G,"vrat",by="late")
    out["vrat5_all_clustered"]=ctab(G,"vrat5")
    out["vrat_inactive_clustered"]=ctab(ina,"vrat")
    out["ret7_active_clustered"]=ctab(act,"ret7")
    out["ret7_inactive_clustered"]=ctab(ina,"ret7")
    # regressions per regime, slope t pooled
    for nm,d in [("ret30neg",ina),("ret30pos",act)]:
        dd2=d.dropna(subset=["ret30","ex"])
        r=stats.linregress(dd2.ret30,dd2.ex)
        out["slope_ret30_"+nm]=pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":len(dd2)})
    # book: largest gain/loss days; coin returns before/after
    D=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["win"]=w; D.append(d)
    D=pd.concat(D)
    bd=D.groupby("day")[["book_return","coin_return"]].mean().dropna().reset_index(drop=True)
    for k in [1,2,3,5]:
        bd[f"hold_next{k}"]=bd.coin_return[::-1].rolling(k).sum()[::-1].shift(-1)
        bd[f"hold_prev{k}"]=bd.coin_return.rolling(k).sum().shift(1)
    bd["q"]=pd.qcut(bd.book_return.rank(method="first"),10,labels=False)
    out["book_decile_context"]=bd.groupby("q")[["book_return","hold_prev5","hold_next1","hold_next5"]].mean()
    out["book_autocorr"]=pd.Series({f"lag{l}":bd.book_return.autocorr(l) for l in [1,2,3,5,7]})
    return out
