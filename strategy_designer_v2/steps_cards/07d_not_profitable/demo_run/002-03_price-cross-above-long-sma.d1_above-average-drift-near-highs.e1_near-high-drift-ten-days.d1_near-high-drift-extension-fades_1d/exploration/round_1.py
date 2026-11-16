def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    fr = []
    for coin, wins in data["bars"].items():
        # coin mean daily return over all windows
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            allr.append(c[1:]/c[:-1]-1)
        mu = np.nanmean(np.concatenate(allr))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            r1 = np.append(c[1:]/c[:-1]-1, np.nan)
            pos = b["postRebalance_current_allocation"].values
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"]).values/b["total_portfolio_value"].values
            d = pd.DataFrame({"coin":coin,"w":w,"pos":pos,"g":pos*r1,"mkt":pos*mu,"fee":fee,
                              "fc":b["forecast"].values,"reg":b["regime"].values,"r1":r1})
            # forward 10-day, non overlapping
            f10 = np.full(len(c), np.nan)
            f10[:-10] = c[10:]/c[:-10]-1
            d["f10"]=f10
            d["grid"]=(np.arange(len(c))%10==0)
            # 30d return and range pos
            s=pd.Series(c)
            d["ret30"]=s.pct_change(30).values
            hi=s.rolling(20).max(); lo=s.rolling(20).min()
            d["rng"]=((s-lo)/(hi-lo)).values
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["side"]=np.sign(D["pos"]).map({1:"long",-1:"short",0:"flat"})
    out["by_side"]=D.groupby("side").agg(n=("g","size"),gain=("g","mean"),mkt=("mkt","mean"),fee=("fee","mean"),r1=("r1","mean"),meanpos=("pos","mean"))
    out["totals"]=pd.Series({"gain_mean":D["g"].mean(),"mkt_mean":D["mkt"].mean(),"fee_mean":D["fee"].mean(),"share_short":(D.pos<0).mean(),"share_long":(D.pos>0).mean()})
    G=D[D.grid & D.f10.notna() & (D.reg=="trending")].copy()
    G["fcb"]=pd.cut(G.fc,[-20.1,-5,-2,-0.01,0.01,2,5,20.1])
    out["fc_bucket_f10"]=G.groupby("fcb").agg(n=("f10","size"),f10=("f10","mean"),med=("f10","median"),hit=("f10",lambda x:(x>0).mean()))
    G["rb"]=pd.qcut(G.rng,5,duplicates="drop")
    out["range_f10"]=G.groupby("rb").agg(n=("f10","size"),f10=("f10","mean"))
    G["r30b"]=pd.qcut(G.ret30,5)
    out["ret30_f10"]=G.groupby("r30b").agg(n=("f10","size"),f10=("f10","mean"))
    A=D[D.grid & D.f10.notna()]
    out["regime_f10"]=A.groupby("reg").agg(n=("f10","size"),f10=("f10","mean"))
    out["coin_gain"]=D.groupby("coin").agg(gain=("g","mean"),fee=("fee","mean"),short=("pos",lambda x:(x<0).mean()))
    return out
