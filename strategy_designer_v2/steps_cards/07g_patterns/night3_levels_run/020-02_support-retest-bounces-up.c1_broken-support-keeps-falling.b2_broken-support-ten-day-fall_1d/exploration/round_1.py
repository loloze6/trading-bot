def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=10
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            fwd=c.shift(-H)/c-1
            r1=c.pct_change()
            f=pd.DataFrame({
                "coin":coin,"w":w,"fwd":fwd,
                "fc":b["forecast"].astype(float),
                "raw":pd.to_numeric(b.get("debug_info.components.support_above.last_history_value"),errors="coerce"),
                "p1":r1,"p5":c/c.shift(5)-1,"p10":c/c.shift(10)-1,"p30":c/c.shift(30)-1,
                "vol20":r1.rolling(20).std(),
                "vol_ratio":r1.rolling(5).std()/r1.rolling(60).std(),
                "dlow90":c/b["low"].astype(float).rolling(90,min_periods=30).min()-1,
                "dhigh90":c/b["high"].astype(float).rolling(90,min_periods=30).max()-1,
                "rng":(b["high"]-b["low"]).astype(float)/c,
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
            })
            f=f.iloc[::H]
            rows.append(f)
    g=pd.concat(rows).dropna(subset=["fwd"])
    g["drift"]=g.groupby("coin")["fwd"].transform("mean")
    g["ex"]=g["fwd"]-g["drift"]
    out={}
    out["n_cases"]=len(g)
    def quint(col,q=5):
        d=g.dropna(subset=[col]).copy()
        d["q"]=d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),q,labels=False))
        t=d.groupby("q")["ex"].agg(["mean","count","std"])
        t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
        top=d[d.q==q-1]["ex"];bot=d[d.q==0]["ex"]
        t.loc["top-bot","mean"]=top.mean()-bot.mean()
        t.loc["top-bot","t"]=stats.ttest_ind(top,bot,equal_var=False).statistic
        # per-coin spearman
        sp=d.groupby("coin").apply(lambda x: stats.spearmanr(x[col],x["ex"]).correlation)
        t.loc["top-bot","count"]=(sp>0).sum()
        return t.round(4)
    for col in ["p1","p5","p10","p30","vol20","vol_ratio","dlow90","dhigh90","rng"]:
        out["q_"+col]=quint(col)
    a=g[g.fc<0].copy()
    a["q"]=pd.qcut(a["fc"].rank(method="first"),5,labels=False)
    t=a.groupby("q")["ex"].agg(["mean","count"]); out["fc_quint(0=most neg)"]=t.round(4)
    out["fc_zero_vs_neg"]=pd.DataFrame({"mean":[g[g.fc==0].ex.mean(),a.ex.mean()],"n":[(g.fc==0).sum(),len(a)]},index=["zero","neg"])
    out["by_wd"]=g.groupby("wd")["ex"].agg(["mean","count"]).round(4)
    out["by_coin_spearman_p30"]=g.dropna(subset=["p30"]).groupby("coin").apply(lambda x: pd.Series({"rho_p30":stats.spearmanr(x.p30,x.ex).correlation,"rho_dlow":stats.spearmanr(x.dlow90,x.ex,nan_policy="omit").correlation,"rho_dhigh":stats.spearmanr(x.dhigh90,x.ex,nan_policy="omit").correlation})).round(3)
    # book: daily
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; dd.append(d)
    D=pd.concat(dd)
    D["year"]=pd.to_datetime(D["day"]).dt.year
    out["book_by_year"]=D.groupby("year")[["book_return","coin_return"]].mean().round(5)
    return out
