def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    # ---------- book daily returns, deepest falls ----------
    rows = []
    for c in days:
        for w, d in days[c].items():
            t = d[["day","book_return","coin_return"]].copy(); t["coin"]=c; t["w"]=w
            b = bars[c][w]
            pos = b.groupby(pd.to_datetime(b["timestamp"]).dt.floor("D"))["postRebalance_current_allocation"].last()
            t["pos"] = pd.to_datetime(t["day"]).dt.floor("D").map(pos).values
            rows.append(t)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    bk = D.groupby(["wn","day"]).agg(br=("book_return","mean"), cr=("coin_return","mean")).dropna().reset_index().sort_values(["wn","day"])
    eq = (1+bk["br"]).cumprod(); dd = eq/eq.cummax()-1
    bk["dd"]=dd.values
    # deepest fall episode
    trough = dd.idxmin(); peak = eq.loc[:trough].idxmax()
    ep = bk.loc[peak:trough]
    out = {}
    out["deepest_fall"] = pd.Series({"depth":dd.min(),"days":len(ep),"windows":",".join(sorted(set("w"+ep.wn.astype(str)))),
                                     "coins_mean_ret_in_fall":(1+ep.cr).prod()-1,"book_in_fall":(1+ep.br).prod()-1})
    byw = bk.groupby("wn").agg(book=("br",lambda x:(1+x).prod()-1), coins=("cr",lambda x:(1+x).prod()-1), maxdd=("dd","min"))
    out["by_window"] = byw
    # ---------- signal cases with trend & forward returns ----------
    cases=[]; allg=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=(b.close-b.low)/(b.high-b.low)
            r5=b.close/b.close.shift(5)-1
            r60=b.close/b.close.shift(60)-1
            r20=b.close/b.close.shift(20)-1
            r1=b.close.pct_change()
            vol30=r1.rolling(30).std(); volmed=vol30.expanding(30).median()
            sig=(cl>=0.8)&(r5<0)
            for h in [1,2,5,10]:
                b[f"f{h}"]=b.close.shift(-h)/b.close-1
            n=len(b)
            for i in range(0,n-5,5):
                rec=dict(coin=c,w=w,r60=r60[i],r20=r20[i],r5=r5[i],cl=cl[i],sig=bool(sig[i]),
                         agi=bool(vol30[i]>volmed[i]) if pd.notna(vol30[i]) else np.nan,
                         f1=b.f1[i],f2=b.f2[i],f5=b.f5[i],f10=b.f10[i],pos=b.postRebalance_current_allocation[i])
                allg.append(rec)
            # signal bars, every one (for trades within grid use first sig per cell)
            for s in range(0,n-5,5):
                idx=[j for j in range(s,s+5) if sig[j]]
                if idx:
                    j=idx[0]
                    cases.append(dict(coin=c,w=w,r60=r60[j],r20=r20[j],r5=r5[j],cl=cl[j],
                                      f1=b.f1[j],f2=b.f2[j],f5=b.f5[j],f10=b.f10[j] if j+10<n else np.nan))
    G=pd.DataFrame(allg); C=pd.DataFrame(cases)
    drift=G.groupby("coin")["f5"].mean()
    C["u5"]=-(C.f5-C.coin.map(drift)); G["u5"]=-(G.f5-G.coin.map(drift))
    C["s5"]=-C.f5; G["s5"]=-G.f5
    def summ(df,col):
        x=df[col].dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    def tr(x):
        return np.where(x.isna(),"na",np.where(x>0.10,"rising",np.where(x<-0.10,"falling","choppy")))
    C["trend"]=tr(C.r60); G["trend"]=tr(G.r60)
    tab={}
    for k,g in C.groupby("trend"):
        a=summ(g,"s5"); tab[("sig",k,"short_total")]=a
        a=summ(g,"u5"); tab[("sig",k,"short_unusual")]=a
    for k,g in G[~G.sig].groupby("trend"):
        tab[("nosig",k,"short_total")]=summ(g,"s5")
    out["by_trend"]=pd.DataFrame(tab).T
    C["dq"]=pd.qcut(C.r5,5,labels=False)
    out["by_depth_quintile"]=C.groupby("dq").agg(r5=("r5","mean"),n=("s5","size"),short_total=("s5","mean"),unusual=("u5","mean"))
    G["r5q"]=pd.qcut(G.r5,5,labels=False)
    out["nosig_by_r5_quintile"]=G[~G.sig].groupby("r5q").agg(r5=("r5","mean"),n=("s5","size"),short_total=("s5","mean"))
    hz={}
    for h in [1,2,5,10]:
        x=-C[f"f{h}"].dropna(); hz[h]=pd.Series({"n":len(x),"short_total":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out["horizons_sig"]=pd.DataFrame(hz).T
    # 20d trend split within signal
    C["t20"]=np.where(C.r20< -0.10,"down20",np.where(C.r20>0.10,"up20","flat20"))
    G["t20"]=np.where(G.r20< -0.10,"down20",np.where(G.r20>0.10,"up20","flat20"))
    a=C.groupby("t20").agg(n=("s5","size"),short_total=("s5","mean"),unusual=("u5","mean"))
    b2=G[~G.sig].groupby("t20").agg(n_nosig=("s5","size"),nosig_short=("s5","mean"))
    out["by_20d"]=a.join(b2)
    # agitation (30d vol vs its in-window median)
    out["by_agit"]=C.assign(agi=None).pipe(lambda x:x).shape[0]
    return out
