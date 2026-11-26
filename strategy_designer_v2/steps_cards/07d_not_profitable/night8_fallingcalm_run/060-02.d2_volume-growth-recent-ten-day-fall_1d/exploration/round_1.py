def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    wins = sorted({w for c in coins for w in bars[c].keys()}, key=lambda s: int(s[1:]))
    # book daily
    book_rows = []
    side_rows = []
    case_rows = []
    for w in wins:
        dfs = []
        for c in coins:
            if w not in days[c]: continue
            d = days[c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c
            dfs.append(d)
            b = bars[c][w].copy()
            b["ret1"] = b["close"].shift(-1)/b["close"]-1
            b["pos"] = b["postRebalance_current_allocation"]
            b["g"] = b["pos"]*b["ret1"]
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["long_g"] = np.where(b["pos"]>0, b["g"], 0.0)
            b["short_g"] = np.where(b["pos"]<0, b["g"], 0.0)
            s = b.groupby("day")[["long_g","short_g"]].sum().reset_index(); s["coin"]=c; s["w"]=w
            side_rows.append(s)
            # cases on 5-bar grid
            b["r5"] = b["close"].shift(-5)/b["close"]-1
            b["r10"] = b["close"]/b["close"].shift(10)-1
            b["vol20"] = b["ret1"].shift(1).rolling(20).std()
            g = b.iloc[::5]
            g = g[(g["forecast"]!=0)&g["r5"].notna()]
            for _,r in g.iterrows():
                case_rows.append(dict(coin=c,w=w,f=r["forecast"],r5=r["r5"],r10=r["r10"],vol20=r["vol20"],pos=r["pos"]))
        D = pd.concat(dfs)
        bd = D.groupby("day").agg(book=("book_return","mean"), hold=("coin_return","mean")).reset_index()
        bd["w"]=w
        book_rows.append(bd)
    B = pd.concat(book_rows).dropna(subset=["book"]).reset_index(drop=True)
    S = pd.concat(side_rows)
    S = S.groupby(["w","day"])[["long_g","short_g"]].sum()/len(coins)
    S = S.reset_index()
    B = B.merge(S, on=["w","day"], how="left")
    v = (1+B["book"]).cumprod()
    peak = v.cummax(); dd = v/peak-1
    B["dd"]=dd
    i_tr = dd.idxmin(); i_pk = v.loc[:i_tr].idxmax()
    out["deepest_dd"] = pd.Series({"dd":dd.min(),"days_peak_to_trough":i_tr-i_pk,"window_trough":B.loc[i_tr,"w"],"window_peak":B.loc[i_pk,"w"]})
    seg = B.loc[i_pk+1:i_tr]
    out["dd_segment_sides"] = pd.Series({"sum_long_g":seg["long_g"].sum(),"sum_short_g":seg["short_g"].sum(),"sum_book":seg["book"].sum(),"sum_hold":seg["hold"].sum()})
    # per window
    pw = B.groupby("w").agg(book_sum=("book","sum"),long=("long_g","sum"),short=("short_g","sum"),hold=("hold","sum"),n=("book","size"))
    pw["maxdd_in_w"] = B.groupby("w")["book"].apply(lambda x: ((1+x).cumprod()/(1+x).cumprod().cummax()-1).min())
    out["per_window"] = pw.loc[wins]
    out["side_totals"] = pd.Series({"long_mean_daily":B["long_g"].mean(),"short_mean_daily":B["short_g"].mean(),
        "long_std":B["long_g"].std(),"short_std":B["short_g"].std()})
    # worst 15 days attribution
    worst = B.nsmallest(20,"book")
    out["worst20_days"] = pd.Series({"book":worst["book"].sum(),"long":worst["long_g"].sum(),"short":worst["short_g"].sum(),"hold":worst["hold"].sum()})
    C = pd.DataFrame(case_rows)
    C["side"]=np.sign(C["f"])
    C["dirret"]=C["side"]*C["r5"]
    def summ(g):
        return pd.Series({"n":len(g),"mean_r5":g["r5"].mean(),"mean_dir":g["dirret"].mean(),"t_dir":g["dirret"].mean()/(g["dirret"].std()/np.sqrt(len(g))) if len(g)>2 else np.nan})
    out["cases_by_side"] = C.groupby("side").apply(summ)
    C["fq"]=pd.qcut(C["f"],5,labels=False,duplicates="drop")
    out["cases_by_fq"] = C.groupby("fq").apply(summ)
    C["r10q"]=pd.qcut(C["r10"],3,labels=False,duplicates="drop")
    out["cases_side_r10q"] = C.groupby(["side","r10q"]).apply(summ)
    C["volq"]=pd.qcut(C["vol20"],3,labels=False,duplicates="drop")
    out["cases_side_volq"] = C.groupby(["side","volq"]).apply(summ)
    return out
