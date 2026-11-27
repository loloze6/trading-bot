def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    H=[7,14,21]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(c)
            r30=pd.Series(c).pct_change(30).values
            r7=pd.Series(c).pct_change(7).values
            dr=pd.Series(c).pct_change()
            sd30=dr.rolling(30).std().values
            reg=b["regime"].values; fc=b["forecast"].values
            for i in range(0,n):
                d={"coin":coin,"w":w,"i":i,"r30":r30[i],"r7":r7[i],"sd30":sd30[i],"reg":reg[i],"fc":fc[i],"day":str(b["timestamp"].iloc[i])[:10],"year":str(b["timestamp"].iloc[i])[:4]}
                for h in H:
                    d[f"f{h}"]=c[i+h]/c[i]-1 if i+h<n else np.nan
                    d[f"g{h}"]=(i%h==0)
                rows.append(d)
    df=pd.DataFrame(rows)
    for h in H:
        drift=df[df[f"g{h}"]].groupby("coin")[f"f{h}"].mean()
        df[f"x{h}"]=df[f"f{h}"]-df["coin"].map(drift)
    df["agit"]=df["sd30"]>df.groupby("coin")["sd30"].transform("median")
    out={}
    def summ(s,h):
        g=s.dropna(subset=[f"f{h}"])
        if len(g)<3: return pd.Series({"n":len(g)})
        return pd.Series({"n":len(g),"days":g["day"].nunique(),"raw%":100*g[f"f{h}"].mean(),"exc%":100*g[f"x{h}"].mean(),
                          "t_raw":stats.ttest_1samp(g[f"f{h}"],0).statistic,"t_exc":stats.ttest_1samp(g[f"x{h}"],0).statistic})
    ch=df[(df.reg=="unknown")&df.r30.notna()]
    for h in H:
        g=ch[ch[f"g{h}"]].copy()
        g["q"]=pd.cut(g.r30,[-9,-0.3,-0.2,-0.1,-0.05,0,0.05,0.1,0.2,0.3,9])
        out[f"depth_bins_h{h}"]=g.groupby("q").apply(lambda s:summ(s,h))
    g=ch[ch["g7"]&(ch.r30<0)].copy()
    out["fall_by_agit_h7"]=g.groupby("agit").apply(lambda s:summ(s,7))
    out["fall_by_year_h7"]=g.groupby("year").apply(lambda s:summ(s,7))
    g["r7s"]=np.sign(g.r7)
    out["fall_by_lastweek_sign"]=g.groupby("r7s").apply(lambda s:summ(s,7))
    g2=ch[ch["g7"]&(ch.r30>=0)].copy()
    out["rise_by_agit_h7"]=g2.groupby("agit").apply(lambda s:summ(s,7))
    # book by window
    bk=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            bk.append(pd.DataFrame({"w":w,"br":d["book_return"],"cr":d["coin_return"],"day":d["day"].astype(str)}))
    bk=pd.concat(bk).dropna()
    daily=bk.groupby(["w","day"])[["br","cr"]].mean().reset_index()
    out["book_by_window"]=daily.groupby("w").agg(book_sum=("br","sum"),coin_sum=("cr","sum"),ndays=("br","size"))
    # trades
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items() if len(t)])
    out["trades"]=tr.groupby("side")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out
