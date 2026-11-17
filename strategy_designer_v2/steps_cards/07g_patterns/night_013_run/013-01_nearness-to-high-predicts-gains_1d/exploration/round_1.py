def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(b)
            raw = b.get("debug_info.components.closeness.last_history_value")
            post = b.get("debug_info.components.closeness.post_pipeline_value")
            r1 = pd.Series(cl).pct_change()
            vol20 = r1.rolling(20).std()
            r7p = pd.Series(cl).pct_change(7)
            r30p = pd.Series(cl).pct_change(30)
            # within-window 30-bar high distance
            hi30 = pd.Series(cl).rolling(30).max()
            d30 = pd.Series(cl)/hi30 - 1
            for h in (7, 30):
                for t in range(0, n - h, h):
                    rows.append(dict(c=c, w=w, h=h, t=t, fwd=cl[t+h]/cl[t]-1,
                                     fc=b["forecast"].iloc[t],
                                     raw=raw.iloc[t] if raw is not None else np.nan,
                                     post=post.iloc[t] if post is not None else np.nan,
                                     pos=b["postRebalance_current_allocation"].iloc[t],
                                     r1=r1.iloc[t], r7p=r7p.iloc[t], r30p=r30p.iloc[t],
                                     vol=vol20.iloc[t], d30=d30.iloc[t]))
    S = pd.DataFrame(rows)
    S["ex"] = S["fwd"] - S.groupby(["c","h"])["fwd"].transform("mean")
    out["raw_descr"] = S[S.h==30][["raw","post","fc","pos"]].describe().round(3)
    def slope(df, x):
        d = df[[x,"ex"]].dropna()
        if len(d) < 20: return (np.nan, np.nan, len(d))
        r = stats.linregress(d[x], d["ex"])
        return (round(r.slope,5), round(r.slope/r.stderr,2), len(d))
    res = {}
    for h in (7,30):
        for x in ["fc","raw","pos","r1","r7p","r30p","vol","d30"]:
            res[f"h{h}_{x}"] = slope(S[S.h==h], x)
    out["slopes(slope,t,n)"] = pd.DataFrame(res, index=["slope","t","n"]).T
    # per coin slope of 30d on forecast and on past 30d return
    pc = {}
    for c, g in S[S.h==30].groupby("c"):
        pc[c] = slope(g,"fc") + slope(g,"r30p")
    out["percoin_fc_r30p"] = pd.DataFrame(pc, index=["s_fc","t_fc","n","s_r30","t_r30","n2"]).T
    # quintiles of forecast, 30d
    s30 = S[S.h==30].dropna(subset=["fc"]).copy()
    s30["q"] = pd.qcut(s30["fc"].rank(method="first"), 5, labels=False)
    out["fc_quintile_30d"] = s30.groupby("q").agg(fc=("fc","mean"), ex=("ex","mean"), n=("ex","size"), sd=("ex","std")).round(4)
    s7 = S[S.h==7].dropna(subset=["vol"]).copy()
    s7["vq"] = s7.groupby("c")["vol"].transform(lambda v: pd.qcut(v.rank(method="first"),5,labels=False))
    out["vol_quintile_7d"] = s7.groupby("vq").agg(ex=("ex","mean"), n=("ex","size"), sd=("ex","std")).round(4)
    s7 = s7.dropna(subset=["r7p"])
    s7["mq"] = s7.groupby("c")["r7p"].transform(lambda v: pd.qcut(v.rank(method="first"),5,labels=False))
    out["past7_quintile_7d"] = s7.groupby("mq").agg(r7p=("r7p","mean"), ex=("ex","mean"), n=("ex","size"), sd=("ex","std")).round(4)
    # daily: weekday effect, book
    D = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["c"]=c; d["w"]=w; D.append(d)
    D = pd.concat(D)
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    out["weekday_coin_ret"] = D.groupby("wd")["coin_return"].agg(["mean","std","count"]).assign(t=lambda x: x["mean"]/(x["std"]/np.sqrt(x["count"]))).round(4)
    bk = D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book_vs_hold"] = pd.DataFrame({"mean":bk.mean(),"std":bk.std(),"sharpe":bk.mean()/bk.std()*np.sqrt(365)}).round(4)
    bk["yr"] = pd.to_datetime(bk.index.get_level_values("day")).year
    out["book_by_year"] = bk.groupby("yr").agg(book=("book_return","mean"), hold=("coin_return","mean"), n=("book_return","size")).round(5)
    # mean position by window-year sign
    allb = []
    for c in bars:
        for w,b in bars[c].items():
            x = b[["timestamp","postRebalance_current_allocation","forecast"]].copy(); x["c"]=c; allb.append(x)
    A = pd.concat(allb)
    out["pos_share_long_short"] = pd.Series({"long":(A.iloc[:,1]>0).mean(),"short":(A.iloc[:,1]<0).mean(),"mean_pos":A.iloc[:,1].mean(),"mean_fc":A["forecast"].mean()}).round(3)
    return out
