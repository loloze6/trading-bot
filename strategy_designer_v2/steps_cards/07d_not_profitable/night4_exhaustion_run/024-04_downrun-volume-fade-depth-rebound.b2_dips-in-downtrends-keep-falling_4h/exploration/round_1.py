def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H=18
    rows=[]
    for coin,wins in data["bars"].items():
        grid=[]
        for w,b in wins.items():
            c=b["close"].values
            for i in range(0,len(c)-H,H): grid.append(c[i+H]/c[i]-1)
        grid=np.array(grid); drift=grid.mean(); usual=grid.std()
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].fillna(0).values
            df=np.diff(f,prepend=f[0])
            ret30=pd.Series(c).pct_change(180).values
            sl=b.get("debug_info.components.streak_loss.last_history_value")
            sl=sl.values if sl is not None else np.full(len(c),np.nan)
            ret1=pd.Series(c).pct_change(6).values  # 1-day prior return
            vol=b["volume"].values
            vr=(pd.Series(vol).rolling(6).mean()/pd.Series(vol).rolling(180).mean()).values
            seen=set()
            for i in np.where(df<=-2)[0]:
                cell=i//H
                if cell in seen or i+H>=len(c): continue
                seen.add(cell)
                r=c[i+H]/c[i]-1
                un=-(r-drift)
                rows.append(dict(coin=coin,w=w,year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                    un=un,tot=-r,s=un/usual,ret30=ret30[i],f=f[i],sl=sl[i],r1=ret1[i],vr=vr[i]))
    d=pd.DataFrame(rows)
    def g(col,q=5):
        x=d.dropna(subset=[col]).copy(); x["b"]=pd.qcut(x[col],q,duplicates="drop")
        return x.groupby("b").agg(n=("s","size"),strength=("s","mean"),tot=("tot","mean"),un=("un","mean"),
            t=("s",lambda v: v.mean()/(v.std()/np.sqrt(len(v)))))
    out={"by_ret30":g("ret30"),"by_forecast":g("f"),"by_streakloss":g("sl"),"by_r1":g("r1"),"by_volratio":g("vr"),
         "by_coin":d.groupby("coin").agg(n=("s","size"),strength=("s","mean"),tot=("tot","mean")),
         "by_year":d.groupby("year").agg(n=("s","size"),strength=("s","mean"),tot=("tot","mean"))}
    # book
    br=[];tr=[]
    for coin,wins in data["days"].items():
        for w,dd in wins.items():
            x=dd[["day","book_return","coin_return"]].copy(); x["coin"]=coin; x["w"]=w; br.append(x)
    B=pd.concat(br); B["year"]=pd.to_datetime(B["day"]).dt.year
    out["book_by_year"]=B.groupby("year").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","size"))
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): tt=t.copy(); tt["coin"]=coin; tr.append(tt)
    T=pd.concat(tr)
    out["trades"]=T.groupby("side").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),
        net=("net_profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda v:(v>0).mean()),
        dur_h=("duration_minutes",lambda v:v.mean()/60))
    return out
