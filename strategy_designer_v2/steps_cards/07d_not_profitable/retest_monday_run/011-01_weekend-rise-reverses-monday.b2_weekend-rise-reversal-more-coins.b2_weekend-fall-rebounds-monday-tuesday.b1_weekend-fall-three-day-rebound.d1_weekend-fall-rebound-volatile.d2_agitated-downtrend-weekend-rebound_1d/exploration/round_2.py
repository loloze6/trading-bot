def explore(data):
    import pandas as pd, numpy as np
    out = {}
    cs=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            ts=pd.to_datetime(b["timestamp"],utc=True)
            lo=b["low"]
            dfc=pd.DataFrame({"coin":c,"w":w,"sun":ts.dt.dayofweek==6,"r":r,
                              "vr":r.rolling(20).std()/r.rolling(60).std(),
                              "ret20":cl/cl.shift(20)-1,"ret60":cl/cl.shift(60)-1,
                              "f1":cl.shift(-1)/cl-1,"f2":cl.shift(-2)/cl-1,"fwd":cl.shift(-3)/cl-1,
                              "minlow":pd.concat([lo.shift(-k) for k in (1,2,3)],axis=1).min(axis=1)/cl-1,
                              "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],
                              "vol20":r.rolling(20).std(),"r2":cl/cl.shift(2)-1})
            cs.append(dfc[dfc["sun"]])
    C=pd.concat(cs).dropna(subset=["fwd","ret20"])
    C["wn"]=C["w"].str[1:].astype(int)
    act=C[C["fc"]>0].copy()
    act["contrib"]=act["alloc"]*act["fwd"]
    # worst contributions
    worst=act.sort_values("contrib").head(25)
    out["worst25_profile"]=pd.Series({"contrib_sum":worst["contrib"].sum(),"all_contrib_sum":act["contrib"].sum(),
        "mean_alloc":worst["alloc"].mean(),"mean_r":worst["r"].mean(),"mean_ret20":worst["ret20"].mean(),
        "mean_vr":worst["vr"].mean(),"mean_vol20":worst["vol20"].mean(),"mean_fc":worst["fc"].mean(),
        "mean_r2":worst["r2"].mean(),"share_w2":(worst["wn"]==2).mean()})
    out["act_overall_profile"]=act[["alloc","r","ret20","vr","vol20","fc","r2"]].mean()
    w2=act[act["wn"].isin([2])]
    out["w2_by_coin"]=w2.groupby("coin").agg(n=("fwd","count"),fwd=("fwd","mean"),contrib=("contrib","sum"),alloc=("alloc","mean"),vr=("vr","mean"),r=("r","mean")).round(4)
    # how many coins signal on the same sunday: crowding
    act["n_same"]=act.groupby(["wn",act.index.map(lambda x:0)]).transform("size") if False else 0
    # horizons by vr quintile and forecast quintile
    def hz(df,col):
        g=pd.qcut(df[col],5,duplicates="drop")
        t=df.groupby(g,observed=True).agg(n=("fwd","count"),f1=("f1","mean"),f2=("f2","mean"),f3=("fwd","mean"),
            minlow=("minlow","mean"),contrib=("contrib","sum"),worst=("fwd","min"),sd=("fwd","std"))
        t["t3"]=t["f3"]/(t["sd"]/np.sqrt(t["n"]))
        return t.round(4).reset_index(drop=True)
    out["hz_by_vr"]=hz(act,"vr")
    out["hz_by_fc"]=hz(act,"fc")
    out["hz_by_r"]=hz(act,"r")
    # two-day fall vs sunday-only
    out["hz_by_r2"]=hz(act,"r2")
    # combination: vr>1 and r below median
    act["vrhi"]=act["vr"]>1; act["rlo"]=act["r"]<act["r"]["r"].median() if False else act["r"]<act["r"].median()
    g=act.groupby(["vrhi","rlo"]).agg(n=("fwd","count"),f3=("fwd","mean"),sd=("fwd","std"),contrib=("contrib","sum"),worst=("fwd","min"),minlow=("minlow","mean"))
    g["t"]=g["f3"]/(g["sd"]/np.sqrt(g["n"]))
    out["vrhi_x_rlo"]=g.round(4)
    # condition alone: Sundays with ret20<0, vr>1, r>=0 (no signal)
    nos=C[(C["ret20"]<0)&(C["r"]>=0)]
    g2=nos.groupby(nos["vr"]>1)["fwd"].agg(["count","mean","std"])
    g2["t"]=g2["mean"]/(g2["std"]/np.sqrt(g2["count"]))
    out["nosig_by_vrhi"]=g2.round(4)
    # Sundays any trend, vr>1, falls (outside ret20<0)
    pos=C[(C["ret20"]>=0)&(C["r"]<0)]
    g3=pos.groupby(pos["vr"]>1)["fwd"].agg(["count","mean","std"])
    g3["t"]=g3["mean"]/(g3["std"]/np.sqrt(g3["count"]))
    out["uptrend_fall_by_vrhi"]=g3.round(4)
    # book-level effect of dropping vr<=1 cases: sum contrib per window
    pw=act.groupby("wn").apply(lambda x: pd.Series({"all":x["contrib"].sum(),"vr_gt1":x.loc[x["vr"]>1,"contrib"].sum(),"vr_le1":x.loc[x["vr"]<=1,"contrib"].sum()}))
    out["contrib_by_window_vr"]=pw.round(4)
    return out
