def explore(data):
    import numpy as np, pandas as pd
    out = {}
    days = data["days"]; bars = data["bars"]
    # book daily returns: mean over coins per (window, day)
    rows = []
    for c in days:
        for w, d in days[c].items():
            t = d[["day","book_return","coin_return"]].copy()
            t["coin"] = c; t["w"] = w
            rows.append(t)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"]).agg(br=("book_return","mean"), cr=("coin_return","mean")).reset_index().sort_values(["wn","day"])
    B = B.dropna(subset=["br"])
    eq = (1+B["br"]).cumprod().values
    dd = eq/np.maximum.accumulate(eq)-1
    B["dd"] = dd
    out["dd_by_window"] = B.groupby("wn").agg(min_dd=("dd","min"), book_sum=("br","sum"), coin_sum=("cr","sum"), n=("br","size"))
    # per-window own drawdown
    def wdd(s):
        e=(1+s).cumprod(); return (e/e.cummax()-1).min()
    out["own_dd_by_window"] = B.groupby("wn")["br"].apply(wdd).sort_values().head(8)
    # per coin calmar-like
    pc = {}
    for c in days:
        s = pd.concat([days[c][w]["book_return"].dropna() for w in sorted(days[c], key=lambda x:int(x[1:]))])
        e=(1+s).cumprod(); mdd=(e/e.cummax()-1).min()
        yr = e.iloc[-1]**(365/len(s))-1
        pc[c]=(yr, mdd, s.mean()/s.std()*np.sqrt(365))
    out["per_coin_yr_mdd_sharpe"] = pd.DataFrame(pc, index=["yr","mdd","sharpe"]).T
    # grid-cell state analysis over 168 bars
    H=168; recs=[]
    for c in bars:
        for w, b in bars[c].items():
            cl=b["close"].values; n=len(cl)
            r7 = pd.Series(cl).pct_change(168).values
            r30 = pd.Series(cl).pct_change(720).values
            lr = np.log(pd.Series(cl)).diff()
            vol = lr.rolling(168).std().values
            volL = lr.rolling(720).std().values
            hi30 = pd.Series(cl).rolling(720).max().values
            f = b["forecast"].values; al=b["postRebalance_current_allocation"].values
            for i in range(0, n-H, H):
                recs.append((c,w,f[i],al[i],cl[i+H]/cl[i]-1,r7[i],r30[i],vol[i]/volL[i] if volL[i]>0 else np.nan,cl[i]/hi30[i]-1,
                             np.min(cl[i:i+H+1])/cl[i]-1))
    G=pd.DataFrame(recs,columns=["c","w","f","al","fwd","r7","r30","volr","dhi","minpath"])
    G["drift"]=G.groupby("c")["fwd"].transform("mean")
    G["un"]=G["fwd"]-G["drift"]
    A=G[G["f"]>0.5].copy()
    out["n_active_cells"]=len(A)
    def tab(col):
        A["q"]=pd.qcut(A[col],4,labels=False,duplicates="drop")
        g=A.groupby("q").agg(lo=(col,"min"),hi=(col,"max"),un=("un","mean"),fwd=("fwd","mean"),minpath=("minpath","mean"),n=("un","size"),
                             tt=("un",lambda x:x.mean()/x.std()*np.sqrt(len(x))))
        return g
    for col in ["r30","volr","dhi","r7","f"]:
        out["active_by_"+col]=tab(col)
    # r30 minus r7 (trend before the week)
    A["r23"]=(1+A["r30"])/(1+A["r7"])-1
    out["active_by_prior23d"]=tab("r23")
    # deepest falls: days in worst 5% of book returns: share of coins long and their coin return
    worst=B.nsmallest(15,"br")[["wn","br","cr","dd"]]
    out["worst15_days"]=worst.reset_index(drop=True)
    return out
