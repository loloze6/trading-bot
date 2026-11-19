def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # book daily
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            t = d[["day","book_return","coin_return"]].copy(); t["coin"]=c; t["w"]=w
            rows.append(t)
    D = pd.concat(rows)
    B = D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    B["wn"] = B["w"].str[1:].astype(int)
    B = B.sort_values(["wn","day"]).dropna()
    eq = (1+B["book_return"]).cumprod().values
    peak = np.maximum.accumulate(eq); dd = eq/peak-1
    B["dd"]=dd
    out["book"] = pd.Series({"mean":B.book_return.mean(),"sd":B.book_return.std(),"hold_mean":B.coin_return.mean(),
        "maxdd":dd.min(),"n":len(B)})
    # per-window book return and hold
    pw = B.groupby("wn").agg(book=("book_return",lambda x:(1+x).prod()-1), hold=("coin_return",lambda x:(1+x).prod()-1), mindd=("dd","min"))
    out["per_window"] = pw.round(4)
    # per coin
    pc = D.groupby("coin")[["book_return","coin_return"]].mean()
    out["per_coin_daily"]=pc
    # bar-level
    feats=[]; fee=[]; gainrows=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            cl=b.close.values; pos=b.postRebalance_current_allocation.fillna(0).values
            r1=np.r_[cl[1:]/cl[:-1]-1, np.nan]
            fee.append(pd.Series({"coin":c,"fee":((b.total_portfolio_value-b.postRebalance_total_value)/b.total_portfolio_value).sum(),"gross":np.nansum(pos*r1),"expo":pos.mean(),"meanr1":np.nanmean(r1)}))
            n=len(b)
            hi=pd.Series(b.high.values).rolling(720,min_periods=200).max().values
            ret30=pd.Series(cl).pct_change(720).values
            ret3=pd.Series(cl).pct_change(72).values
            ret1=pd.Series(cl).pct_change(24).values
            vol=pd.Series(r1).shift(1).rolling(168,min_periods=50).std().values
            idx=np.arange(0,n-72,72)
            f=pd.DataFrame({"coin":c,"w":w,"fc":b.forecast.values[idx],"pos":pos[idx],"fwd":cl[idx+72]/cl[idx]-1,
              "near":cl[idx]/hi[idx]-1,"ret30":ret30[idx],"ret3":ret3[idx],"ret1":ret1[idx],"vol":vol[idx],"reg":b.regime.values[idx],
              "hour":pd.to_datetime(b.timestamp.values[idx]).hour})
            feats.append(f)
    F=pd.concat(feats)
    fe=pd.DataFrame(fee)
    out["fees_gross_by_coin"]=fe.groupby("coin")[["fee","gross","expo"]].agg(["sum","mean"]).round(4)
    F["ex"]=F.fwd-F.groupby("coin").fwd.transform("mean")
    T=F[F.reg=="trending"].copy()
    out["share_trending"]=float((F.reg=="trending").mean())
    act=T[T.fc>0].copy()
    def tab(df,col,q=4):
        df=df.dropna(subset=[col,"ex"]).copy()
        df["b"]=pd.qcut(df[col],q,labels=False,duplicates="drop")
        g=df.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=("ex","size"),ex=("ex","mean"),fwd=("fwd","mean"),
           t=("ex",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
        return g.round(4)
    out["T_fc0_vs_pos"]=T.groupby(T.fc>0).agg(n=("ex","size"),ex=("ex","mean"),fwd=("fwd","mean")).round(4)
    out["act_by_fc"]=tab(act,"fc")
    out["act_by_near"]=tab(act,"near")
    out["act_by_ret30"]=tab(act,"ret30")
    out["act_by_ret3"]=tab(act,"ret3")
    out["act_by_ret1"]=tab(act,"ret1")
    out["act_by_vol"]=tab(act,"vol")
    out["T_by_near"]=tab(T,"near")
    out["T_by_ret3"]=tab(T,"ret3")
    return out
