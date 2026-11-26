def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    allret = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"].values
            r1 = np.r_[cl[1:]/cl[:-1]-1, np.nan]
            allret.append(pd.Series(r1).dropna())
            prev = np.r_[np.nan, cl[1:]/cl[:-1]-1]
            lr = np.log(cl)
            sd30 = pd.Series(prev).rolling(30, min_periods=20).std().values
            rng = (b["high"]-b["low"]).values/cl
            r3p = np.r_[[np.nan]*3, cl[3:]/cl[:-3]-1]
            r2f = np.r_[cl[2:]/cl[:-2]-1, [np.nan]*2]
            r3f = np.r_[cl[3:]/cl[:-3]-1, [np.nan]*3]
            # count consecutive up days
            up = (prev > 0).astype(int)
            streak = np.zeros(len(b)); s=0
            for i in range(len(b)):
                s = s+1 if up[i] else 0; streak[i]=s
            clpos = (cl - b["low"].values)/(b["high"].values-b["low"].values+1e-12)
            df = pd.DataFrame({"coin":c,"w":w,"i":np.arange(len(b)),"day":b["timestamp"].astype(str).str[:10],
                "regime":b["regime"].values,"fc":b["forecast"].values,"alloc":b["postRebalance_current_allocation"].values,
                "r1":r1,"r2f":r2f,"r3f":r3f,"prev":prev,"rng_sd":rng/sd30,"move_sd":prev/sd30,"r3p_sd":r3p/sd30,
                "streak":streak,"clpos":clpos,"sd30":sd30})
            rows.append(df)
    D = pd.concat(rows)
    mu = D.groupby("coin")["r1"].mean()
    D["mu"] = D["coin"].map(mu)
    D["u1"] = -(D["r1"]-D["mu"])
    D["u2"] = -(D["r2f"]-2*D["mu"]); D["u3"] = -(D["r3f"]-3*D["mu"])
    cases = D[(D.fc<0)&D.r1.notna()].copy()
    inprof = D[D.regime!="chop"]
    out = {}
    out["regime_counts"] = D.regime.value_counts()
    def summ(g, col="u1"):
        x=g[col].dropna(); 
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,"hit":(x>0).mean()})
    out["cases_by_window"] = cases.groupby("w").apply(summ)
    out["cases_by_coin"] = cases.groupby("coin").apply(summ)
    cases["rngq"] = pd.qcut(cases.rng_sd, 5, labels=False, duplicates="drop")
    out["by_range_quint"] = cases.groupby("rngq").apply(summ)
    cases["moveq"] = pd.qcut(cases.move_sd, 5, labels=False, duplicates="drop")
    out["by_daymove_quint"] = cases.groupby("moveq").apply(summ)
    cases["r3q"] = pd.qcut(cases.r3p_sd, 5, labels=False, duplicates="drop")
    out["by_3dpast_quint"] = cases.groupby("r3q").apply(summ)
    out["by_streak"] = cases.assign(s=cases.streak.clip(upper=4)).groupby("s").apply(summ)
    cases["clq"] = pd.qcut(cases.clpos, 4, labels=False, duplicates="drop")
    out["by_closepos_q"] = cases.groupby("clq").apply(summ)
    out["horizons"] = pd.DataFrame({h:summ(cases,h) for h in ["u1","u2","u3"]})
    # control: in-profile down days next-day (short sign)
    dn = inprof[(inprof.regime=="unknown")&inprof.r1.notna()]
    out["control_down_days_inprofile_short"] = summ(dn)
    # book daily
    bd=[]
    for c in days:
        for w,d in days[c].items():
            bd.append(pd.DataFrame({"w":w,"day":d["day"].astype(str).values,"br":d["book_return"].values,"cr":d["coin_return"].values}))
    B=pd.concat(bd).dropna()
    BB=B.groupby(["w","day"]).agg(br=("br","mean"),cr=("cr","mean")).reset_index().sort_values(["w","day"])
    BB["wn"]=BB.w.str[1:].astype(int); BB=BB.sort_values(["wn","day"])
    eq=(1+BB.br).cumprod().values; dd=eq/np.maximum.accumulate(eq)-1
    BB["dd"]=dd
    out["book_by_window"]=BB.groupby("wn").agg(mean_bp=("br",lambda x:1e4*x.mean()),sum_pct=("br",lambda x:100*x.sum()),coin_sum=("cr",lambda x:100*x.sum()),mindd=("dd","min"))
    # worst 15 days of book: which window, coin return
    worst=BB.nsmallest(15,"br")[["wn","br","cr"]].assign(br=lambda x:100*x.br,cr=lambda x:100*x.cr)
    out["worst15_days"]=worst.reset_index(drop=True)
    # loss tail of cases
    out["case_loss_tail"]=pd.Series({"share_u1<-5%":(cases.u1<-0.05).mean(),"sum_of_those%":100*cases.u1[cases.u1<-0.05].sum(),"sum_all%":100*cases.u1.sum(),"mean_alloc":cases.alloc.mean()})
    return out
