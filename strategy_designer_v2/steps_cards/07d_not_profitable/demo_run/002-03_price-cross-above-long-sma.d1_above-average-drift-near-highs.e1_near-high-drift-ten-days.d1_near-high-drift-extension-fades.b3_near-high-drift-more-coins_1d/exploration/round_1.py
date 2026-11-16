def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # coin mean daily return over all windows
    rows=[]; grid=[]; dayrows=[]
    for c in bars:
        cm = pd.concat([days[c][w]["coin_return"] for w in days[c]]).mean()
        for w, b in bars[c].items():
            b = b.copy()
            r1 = b["close"].shift(-1)/b["close"]-1
            pos = b["postRebalance_current_allocation"]
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            df = pd.DataFrame({"coin":c,"w":w,"pos":pos,"r1":r1,"gain":pos*r1,"mkt":pos*cm,
                               "fee":fee,"fc":b["forecast"],"regime":b["regime"],
                               "rng":b.get("debug_info.components.range20.post_pipeline_value"),
                               "ext":b.get("debug_info.components.ext30.post_pipeline_value"),
                               "ret30":b.get("debug_info.components.ext30.last_history_value"),
                               "rngraw":b.get("debug_info.components.range20.last_history_value")})
            rows.append(df)
            g = b.iloc[::10].copy()
            idx = np.arange(0,len(b),10)
            f10 = b["close"].shift(-10)/b["close"]-1
            gg = df.iloc[idx].copy(); gg["f10"]=f10.iloc[idx].values
            grid.append(gg)
        for w,d in days[c].items():
            dd=d[["book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w; dayrows.append(dd)
    A = pd.concat(rows); G = pd.concat(grid); D = pd.concat(dayrows)
    G["ex10"] = G["f10"] - G.groupby("coin")["f10"].transform("mean")
    A["side"] = np.sign(A["pos"]).map({1:"long",-1:"short",0:"flat"})
    s = A.groupby("side").agg(n=("gain","size"),mean_gain=("gain","mean"),mean_mkt=("mkt","mean"),mean_r1=("r1","mean"),mean_pos=("pos","mean"),fee=("fee","mean"))
    out["by side (bar gains)"]=s
    out["totals"]=pd.Series({"bar gain mean":A["gain"].mean(),"mkt part":A["mkt"].mean(),"timing":A["gain"].mean()-A["mkt"].mean(),"fee per bar":A["fee"].mean(),
        "book daily mean":D["book_return"].mean(),"coin daily mean":D["coin_return"].mean(),"share trending":(A["regime"]=="trending").mean()})
    T = A[A["regime"]=="trending"].copy()
    T["fcb"]=pd.qcut(T["fc"].rank(method="first"),5,labels=False)
    out["trending by forecast quintile"]=T.groupby("fcb").agg(fc=("fc","mean"),pos=("pos","mean"),r1=("r1","mean"),gain=("gain","mean"),fee=("fee","mean"),n=("gain","size"))
    GT = G[G["regime"]=="trending"].dropna(subset=["ex10"]).copy()
    GT["rq"]=pd.qcut(GT["rng"].rank(method="first"),5,labels=False)
    out["grid ex10 by range20 post quintile"]=GT.groupby("rq").agg(rng=("rng","mean"),rngraw=("rngraw","mean"),ex10=("ex10","mean"),f10=("f10","mean"),n=("ex10","size"))
    GT["eq"]=pd.cut(GT["ext"],[-1e9,-5,-1,-0.01,0.01],labels=["<=-5","-5..-1","-1..0","0"])
    out["grid ex10 by ext30 post"]=GT.groupby("eq").agg(ret30=("ret30","mean"),ex10=("ex10","mean"),fc=("fc","mean"),n=("ex10","size"))
    GT["r30q"]=pd.qcut(GT["ret30"].rank(method="first"),5,labels=False)
    out["grid ex10 by raw ret30 quintile"]=GT.groupby("r30q").agg(ret30=("ret30","mean"),ex10=("ex10","mean"),fc=("fc","mean"),n=("ex10","size"))
    GN = G[G["regime"]!="trending"].dropna(subset=["ex10"])
    out["grid ex10 trending vs not"]=pd.Series({"trend mean":GT["ex10"].mean(),"trend n":len(GT),"other mean":GN["ex10"].mean(),"other n":len(GN),"welch t":stats.ttest_ind(GT["ex10"],GN["ex10"],equal_var=False).statistic})
    out["by coin"]=A.groupby("coin").agg(gain=("gain","mean"),mkt=("mkt","mean"),fee=("fee","mean"),long=("pos",lambda x:(x>0).mean()),short=("pos",lambda x:(x<0).mean()))
    return out
