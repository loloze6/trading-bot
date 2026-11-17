def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; drows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            ts=pd.to_datetime(b["timestamp"],utc=True)
            b["wd"]=ts.dt.weekday; b["year"]=ts.dt.year
            c=b["close"].values
            b["r0"]=b["close"].pct_change()
            b["r1"]=pd.Series(c).shift(-1)/c-1
            b["r2"]=pd.Series(c).shift(-2)/c-1
            b["r2b"]=pd.Series(c).shift(-2)/pd.Series(c).shift(-1)-1
            b["ret20"]=pd.Series(c)/pd.Series(c).shift(20)-1
            b["vol20"]=b["r0"].rolling(20).std()
            b["absmean60"]=b["r0"].abs().shift(1).rolling(60,min_periods=20).mean()
            b["volrel"]=b["volume"]/b["volume"].shift(1).rolling(30,min_periods=10).mean()
            b["alloc"]=b["postRebalance_current_allocation"]
            b["coin"]=coin; b["w"]=w
            rows.append(b)
        for w,d in data["days"][coin].items():
            d=d.copy(); d["coin"]=coin; d["w"]=w
            d["wd"]=pd.to_datetime(d["day"]).dt.weekday
            drows.append(d)
    B=pd.concat(rows,ignore_index=True); D=pd.concat(drows,ignore_index=True)
    out={}
    # book daily
    port=D.groupby(["w","day"]).agg(book=("book_return","mean"),hold=("coin_return","mean")).dropna().reset_index()
    port["wd"]=pd.to_datetime(port["day"]).dt.weekday
    out["book_by_weekday"]=port.groupby("wd").agg(n=("book","size"),book_mean=("book","mean"),book_sd=("book","std"),hold_mean=("hold","mean"))
    out["book_overall"]=pd.Series({"mean":port.book.mean(),"sd":port.book.std(),"hold_mean":port.hold.mean(),"hold_sd":port.hold.std(),"share_days_nonzero":(port.book.abs()>1e-9).mean()})
    # active sundays
    S=B[(B.wd==6)&(B.forecast!=0)&B.r1.notna()].copy()
    S["pos_gain"]=S.alloc*S.r1
    S["side"]=np.where(S.forecast>0,"long_after_fall","short_after_rise")
    S["signed_r1"]=np.sign(S.forecast)*S.r1; S["signed_r2b"]=np.sign(S.forecast)*S.r2b
    g=S.groupby("side").agg(n=("r1","size"),mean_alloc=("alloc","mean"),pos_gain=("pos_gain","mean"),signed_mon=("signed_r1","mean"),signed_tue=("signed_r2b","mean"))
    out["by_side"]=g
    S["fterc"]=pd.qcut(S.forecast.abs().rank(method="first"),3,labels=["lo","mid","hi"])
    out["by_size_terc"]=S.groupby("fterc").agg(n=("r1","size"),abs_alloc=("alloc",lambda x:x.abs().mean()),pos_gain=("pos_gain","mean"),signed_mon=("signed_r1","mean"),signed_tue=("signed_r2b","mean"),abs_r0=("r0",lambda x:x.abs().mean()))
    S["trend"]=pd.qcut(S.ret20.rank(method="first"),3,labels=["down","mid","up"])
    out["by_trend20_side"]=S.groupby(["trend","side"]).agg(n=("r1","size"),pos_gain=("pos_gain","mean"),signed_mon=("signed_r1","mean"),signed_tue=("signed_r2b","mean"))
    S["vr"]=pd.qcut(S.volrel.rank(method="first"),3,labels=["lowvol","mid","highvol"])
    out["by_sunday_volume"]=S.groupby("vr").agg(n=("r1","size"),pos_gain=("pos_gain","mean"),signed_mon=("signed_r1","mean"),signed_tue=("signed_r2b","mean"))
    out["by_year"]=S.groupby("year").agg(n=("r1","size"),pos_gain=("pos_gain","mean"),signed_mon=("signed_r1","mean"),signed_tue=("signed_r2b","mean"))
    # fees
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()],ignore_index=True)
    out["trades"]=pd.Series({"n":len(T),"gross_mean":T.profit_loss_percent.mean(),"net_mean":T.net_profit_loss_percent.mean(),"dur_h_mean":T.duration_minutes.mean()/60,"mean_alloc_abs_all_bars":B.alloc.abs().mean()})
    # other weekdays: does day-move reverse next day too?
    B["sr"]=-np.sign(B.r0)*B.r1
    out["reversal_by_weekday_all"]=B.dropna(subset=["sr"]).groupby("wd").agg(n=("sr","size"),mean_rev=("sr","mean"))
    # drawdown
    port=port.sort_values(["w","day"]); eq=(1+port.book).cumprod(); dd=eq/eq.cummax()-1
    out["maxdd"]=float(dd.min())
    return out
