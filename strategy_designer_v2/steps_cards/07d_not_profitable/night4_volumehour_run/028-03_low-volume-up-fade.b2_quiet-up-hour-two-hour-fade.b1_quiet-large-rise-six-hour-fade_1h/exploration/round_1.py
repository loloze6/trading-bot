def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily
    dd = []
    for c in data["days"]:
        for w, d in data["days"][c].items():
            x = d[["day","book_return","coin_return"]].copy(); x["coin"]=c; x["w"]=w; dd.append(x)
    dd = pd.concat(dd)
    g = dd.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book_daily"] = pd.Series({"mean":g.book_return.mean(),"sd":g.book_return.std(),"n":len(g),
                                   "coin_mean":g.coin_return.mean()})
    # trades gross vs net
    tr = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            if len(t): x=t.copy(); x["coin"]=c; x["w"]=w; tr.append(x)
    tr = pd.concat(tr)
    out["trades"] = tr.groupby("coin").agg(n=("side","size"), gross=("profit_loss_percent","mean"),
        net=("net_profit_loss_percent","mean"), dur_h=("duration_minutes", lambda s: s.mean()/60),
        win_gross=("profit_loss_percent", lambda s:(s>0).mean()))
    # event study recomputed from prices: scaled hourly move, volume ratio, forward returns 1,2,6h
    rows = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            r = b.close.pct_change()
            mad = r.abs().rolling(720, min_periods=200).mean().shift(1)
            z = r / mad
            vr = b.volume / b.volume.rolling(720, min_periods=200).mean()
            df = pd.DataFrame({"z":z,"vr":vr,"coin":c,"w":w,
                               "atr": mad})
            for h in (1,2,6,12):
                df[f"f{h}"] = b.close.shift(-h)/b.close - 1
            df["pos"]=b["postRebalance_current_allocation"]
            df["gain"]=b["postRebalance_current_allocation"]*(b.close.shift(-1)/b.close-1)
            df["idx"]=np.arange(len(b))
            rows.append(df)
    A = pd.concat(rows).dropna(subset=["z","vr","f6"])
    drift = A[A.idx%6==0].groupby("coin").f6.mean()
    A["u6"] = A.f6 - A.coin.map(drift)
    G = A[A.idx%6==0].copy()
    G["zb"] = pd.cut(G.z, [-np.inf,-4,-2.5,-1.5,-0.5,0.5,1.5,2.5,4,np.inf])
    G["vb"] = pd.cut(G.vr, [0,0.5,1.5,3,np.inf], labels=["<0.5","0.5-1.5","1.5-3",">3"])
    def tt(s): return pd.Series({"n":len(s),"mean_bp":s.mean()*1e4,"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out["u6_by_zbin_vol"] = G.groupby(["zb","vb"], observed=True).u6.apply(tt).unstack()
    # momentum continuation at 1,2h for big moves by vol
    big = A[A.z.abs()>2.5].copy(); big["s"]=np.sign(big.z)
    big["vb"]=pd.cut(big.vr,[0,1.5,3,np.inf],labels=["<1.5","1.5-3",">3"])
    res={}
    for h in (1,2,6,12):
        big[f"sf{h}"]=big.s*big[f"f{h}"]
    out["big_moves_signed_fwd_bp"] = big.groupby("vb",observed=True)[["sf1","sf2","sf6","sf12"]].mean()*1e4
    out["big_moves_n"] = big.groupby("vb",observed=True).size()
    # book gain by position sign and year
    A["short"]=A.pos<0
    A["year"]=pd.concat([pd.to_datetime(data["bars"][c][w].timestamp).dt.year for c in data["bars"] for w in data["bars"][c]]).reindex(A.index) if False else np.nan
    out["exposure"] = pd.Series({"share_bars_short":(A.pos<0).mean(),"mean_pos_when_short":A.pos[A.pos<0].mean(),
                                 "gain_bp_per_bar_short":A.gain[A.pos<0].mean()*1e4})
    return out
