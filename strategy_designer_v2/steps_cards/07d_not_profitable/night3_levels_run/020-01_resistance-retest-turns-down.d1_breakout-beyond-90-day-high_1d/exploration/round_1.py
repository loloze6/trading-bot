def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; tr_rows = []; dd_rows = []; post_rows = []; exp_rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            pos = b["postRebalance_current_allocation"].fillna(0).values
            c = b["close"].values
            r1 = np.append(c[1:]/c[:-1]-1, np.nan)
            g = pos*r1
            exp_rows.append({"coin":coin,"win":w,"in_share":(np.abs(pos)>1e-6).mean(),
                             "mean_pos":np.mean(pos),"gain_sum":np.nansum(g),"coin_ret":c[-1]/c[0]-1})
            raw = b.get("debug_info.components.breakout_dist.last_history_value")
            f = b["forecast"].fillna(0).values
            # forward returns at 5,10,20 days from bars with forecast>0 (non-overlap 5 grid)
            n=len(c)
            for i in range(0,n,5):
                if f[i]>0:
                    d={"coin":coin,"win":w,"f":f[i]}
                    for h in (5,10,20,40):
                        d[f"r{h}"]=c[i+h]/c[i]-1 if i+h<n else np.nan
                    # prior 20-day return
                    d["prior20"]=c[i]/c[i-20]-1 if i>=20 else np.nan
                    post_rows.append(d)
        dd = data["days"][coin]
        for w, d in dd.items():
            v=d["book_value"].values
            peak=np.maximum.accumulate(v); ddv=v/peak-1
            dd_rows.append({"coin":coin,"win":w,"maxdd":ddv.min(),"book_ret":v[-1]/v[0]-1,
                            "coin_ret":d["close"].values[-1]/d["close"].values[0]-1})
        for w,t in data["trades"][coin].items():
            if len(t):
                t=t.copy(); t["coin"]=coin; t["win"]=w; tr_rows.append(t)
    E=pd.DataFrame(exp_rows); P=pd.DataFrame(post_rows); D=pd.DataFrame(dd_rows)
    T=pd.concat(tr_rows)
    out["exposure_by_coin"]=E.groupby("coin")[["in_share","mean_pos","gain_sum"]].mean()
    out["exposure_overall"]=E[["in_share","mean_pos"]].mean()
    # drift per coin over horizons: mean over all grid returns
    drift={}
    for coin, wins in data["bars"].items():
        for h in (5,10,20,40):
            rs=[]
            for w,b in wins.items():
                c=b["close"].values
                rs+= [c[i+h]/c[i]-1 for i in range(0,len(c)-h,h)]
            drift[(coin,h)]=np.mean(rs)
    for h in (5,10,20,40):
        P[f"u{h}"]=P[f"r{h}"]-P["coin"].map(lambda x: drift[(x,h)])
    s=[]
    for h in (5,10,20,40):
        x=P[f"u{h}"].dropna()
        s.append({"h":h,"n":len(x),"mean_unusual":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))),
                  "mean_total":P[f"r{h}"].dropna().mean()})
    out["breakout_forward_by_horizon"]=pd.DataFrame(s)
    P["fq"]=pd.qcut(P["f"].rank(method="first"),4,labels=False)
    out["by_forecast_quartile"]=P.groupby("fq")[["f","u5","u10","u20"]].agg(["mean","count"])
    P["pq"]=pd.qcut(P["prior20"].rank(method="first"),4,labels=False)
    out["by_prior20_quartile"]=P.groupby("pq")[["prior20","u5","u10","u20"]].mean()
    out["dd_worst"]=D.sort_values("maxdd").head(12)[["coin","win","maxdd","book_ret","coin_ret"]]
    T["dur_d"]=T["duration_minutes"]/1440
    T["dq"]=pd.cut(T["dur_d"],[0,5.5,10,20,40,1000])
    out["trades_by_duration"]=T.groupby("dq")["net_profit_loss_percent"].agg(["mean","count","sum"])
    out["trades_summary"]=pd.Series({"n":len(T),"mean_net":T["net_profit_loss_percent"].mean(),
        "median_dur":T["dur_d"].median(),"win_rate":(T["net_profit_loss_percent"]>0).mean(),
        "mean_fee":T["total_commission"].mean()})
    return out
