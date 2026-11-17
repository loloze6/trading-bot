def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            df=pd.DataFrame({
                "coin":coin,"win":w,
                "fwd7":c.shift(-7)/c-1,
                "fwd1":c.shift(-1)/c-1,
                "ret1":r1,
                "ret7":c/c.shift(7)-1,
                "ret30":c/c.shift(30)-1,
                "vol20":r1.rolling(20).std(),
                "vrat":b["volume"]/b["volume"].rolling(20).mean(),
                "fc":b["forecast"],
                "rp":b.get("debug_info.components.range_pos.last_history_value"),
                "m30":b.get("debug_info.components.mom30.last_history_value"),
                "reg":b["regime"],
                "alloc":b["postRebalance_current_allocation"],
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "pos":np.arange(len(b)),
                "hi_gap":c/c.rolling(60,min_periods=20).max()-1,
            })
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    A["cm7"]=A.groupby("coin")["fwd7"].transform(lambda s: s[A.loc[s.index,"pos"]%7==0].mean())
    G=A[(A.pos%7==0)&A.fwd7.notna()].copy()
    G["ex"]=G.fwd7-G.cm7
    def tab(df,col,q=5):
        d=df.dropna(subset=[col,"ex"]).copy()
        d["b"]=d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),q,labels=False) if len(s)>=q else np.nan)
        g=d.groupby("b")["ex"].agg(["mean","count","std"])
        g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        g["mid"]=d.groupby("b")[col].median()
        return g.drop(columns="std")
    out={}
    act=G[G.fc>0]; ina=G[~(G.fc>0)]
    out["active_vs_inactive"]=pd.DataFrame({"mean":[act.ex.mean(),ina.ex.mean()],"n":[len(act),len(ina)],
        "t":[stats.ttest_1samp(act.ex,0).statistic,stats.ttest_1samp(ina.ex,0).statistic]},index=["active","inactive"])
    out["fc_q_active"]=tab(act,"fc")
    out["rp_q_active"]=tab(act,"rp")
    out["m30_q_active"]=tab(act,"m30")
    out["ret30_q_inactive"]=tab(ina,"ret30")
    out["higap60_q_inactive"]=tab(ina,"hi_gap")
    out["higap60_q_all"]=tab(G,"hi_gap")
    out["ret7_q_all"]=tab(G,"ret7")
    out["ret1_q_all"]=tab(G,"ret1")
    out["vol20_q_all"]=tab(G,"vol20")
    out["vrat_q_active"]=tab(act,"vrat")
    out["vrat_q_all"]=tab(G,"vrat")
    # weekday on daily 1-bar returns (non-overlapping by nature)
    A["ex1"]=A.fwd1-A.groupby("coin")["fwd1"].transform("mean")
    g=A.groupby("wd")["ex1"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["weekday_next1"]=g.drop(columns="std")
    # book
    D=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["win"]=w; D.append(d)
    D=pd.concat(D)
    bd=D.groupby("day")[["book_return","coin_return"]].mean().dropna()
    out["book_summary"]=pd.Series({"book_mean":bd.book_return.mean(),"hold_mean":bd.coin_return.mean(),
        "book_sh":bd.book_return.mean()/bd.book_return.std()*np.sqrt(365),"hold_sh":bd.coin_return.mean()/bd.coin_return.std()*np.sqrt(365),
        "corr":bd.corr().iloc[0,1],"n_days":len(bd)})
    bd["yr"]=pd.to_datetime(bd.index).year
    out["book_by_year"]=bd.groupby("yr").agg(book=("book_return","mean"),hold=("coin_return","mean"),n=("book_return","count"))
    tr=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): tr.append(t)
    T=pd.concat(tr)
    T["dur_d"]=T.duration_minutes/1440
    T["db"]=pd.qcut(T.dur_d.rank(method="first"),5,labels=False)
    out["trades_by_duration"]=T.groupby("db").agg(n=("dur_d","size"),dur=("dur_d","median"),pnl=("net_profit_loss_percent","mean"),win=("net_profit_loss_percent",lambda s:(s>0).mean()))
    return out
