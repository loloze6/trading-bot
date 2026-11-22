def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # book daily, pooled over coins
    rows = []
    for c in data["days"]:
        for w, d in data["days"][c].items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows)
    P = D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    P["wn"] = P["w"].str[1:].astype(int)
    P = P.sort_values(["wn","day"]).dropna()
    def stats(r):
        eq = (1+r).cumprod(); dd = eq/eq.cummax()-1
        yr = eq.iloc[-1]**(365/len(r))-1
        return pd.Series({"mean":r.mean(),"sharpe":r.mean()/r.std()*np.sqrt(365),"yearly":yr,"maxdd":dd.min(),"calmar":yr/-dd.min()})
    out["book_vs_hold"] = pd.DataFrame({"book":stats(P.book_return.reset_index(drop=True)),"hold":stats(P.coin_return.reset_index(drop=True))})
    # per window
    pw = P.groupby("wn").agg(book=("book_return","sum"),hold=("coin_return","sum"),
                             bookmin=("book_return","min"))
    out["per_window_sum"] = pw
    # bars-level: exposure, gain by allocation, context
    recs=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.copy()
            r1 = b.close.pct_change()
            b["nxt"] = b.close.shift(-1)/b.close-1
            b["alloc"]=b.postRebalance_current_allocation
            b["ret168"]=b.close/b.close.shift(168)-1
            b["ret720"]=b.close/b.close.shift(720)-1
            sd=r1.rolling(720,min_periods=200).std()
            b["z"]=r1/sd
            b["vr"]=b.volume/b.volume.rolling(720,min_periods=200).mean()
            b["fwd24"]=b.close.shift(-24)/b.close-1
            b["pos"]=np.arange(len(b)); b["coin"]=c; b["w"]=w
            b["hour"]=pd.to_datetime(b.timestamp).dt.hour
            b["sd720"]=sd
            recs.append(b[["coin","w","pos","forecast","alloc","nxt","ret168","ret720","z","vr","fwd24","hour","sd720"]])
    B=pd.concat(recs)
    drift = B[B.pos%24==0].fwd24.mean()
    out["drift24"]=drift
    out["share_bars_in"]=(B.alloc.abs()>1e-6).mean()
    out["mean_alloc_when_in"]=B.loc[B.alloc.abs()>1e-6,"alloc"].mean()
    B["gain"]=B.alloc*B.nxt
    # entries: forecast>0 and previous ==0
    B["fprev"]=B.groupby(["coin","w"]).forecast.shift(1)
    E=B[(B.forecast>0)&(B.fprev<=0)].dropna(subset=["fwd24"]).copy()
    E["cell"]=E.pos//24
    E=E.groupby(["coin","w","cell"]).head(1)
    E["u"]=E.fwd24-drift
    def tt(x): return pd.Series({"n":len(x),"mean_u":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x))})
    E["tr7"]=pd.qcut(E.ret168,5,labels=False)
    E["tr30"]=pd.qcut(E.ret720,5,labels=False)
    E["fq"]=pd.qcut(E.forecast.rank(method="first"),5,labels=False)
    E["vq"]=pd.qcut(E.vr.rank(method="first"),5,labels=False)
    E["zq"]=pd.qcut(E.z.rank(method="first"),5,labels=False)
    E["sdq"]=pd.qcut(E.sd720.rank(method="first"),5,labels=False)
    out["entries_all"]=tt(E.u)
    out["by_prior7d_quintile"]=E.groupby("tr7").u.apply(tt).unstack()
    out["by_prior30d_quintile"]=E.groupby("tr30").u.apply(tt).unstack()
    out["by_forecast_quintile"]=E.groupby("fq").u.apply(tt).unstack()
    out["by_volratio_quintile"]=E.groupby("vq").u.apply(tt).unstack()
    out["by_z_quintile"]=E.groupby("zq").u.apply(tt).unstack()
    out["by_vol720_quintile"]=E.groupby("sdq").u.apply(tt).unstack()
    out["by_coin"]=E.groupby("coin").u.apply(tt).unstack()
    # book gain bars-level by prior 30d trend sign when in
    I=B[B.alloc.abs()>1e-6].dropna(subset=["ret720","nxt"])
    I["tr30s"]=np.sign(I.ret720)
    out["inpos_gain_by_30d_sign"]=I.groupby("tr30s").agg(n=("gain","size"),mean_gain=("gain","mean"),mean_nxt=("nxt","mean"))
    # trades
    T=pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    out["trades"]=pd.Series({"n":len(T),"mean_gross":T.profit_loss_percent.mean(),"mean_net":T.net_profit_loss_percent.mean(),"mean_dur_h":T.duration_minutes.mean()/60,"win":(T.net_profit_loss_percent>0).mean()})
    return out
