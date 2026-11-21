def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]
            nxt=c.shift(-1)/c-1
            a=b["postRebalance_current_allocation"].fillna(0)
            short=a<0
            start=short&~short.shift(1,fill_value=False)
            tid=start.cumsum().where(short)
            age=short.groupby(tid).cumcount().where(short)
            ret30=c/c.shift(30)-1
            entry_ret30=ret30.where(start).groupby(tid).transform("first") if short.any() else ret30*np.nan
            r10=c.shift(-10)/c-1
            rows.append(pd.DataFrame({"coin":coin,"w":w,"g":a*nxt,"a":a,"short":short,"age":age,
                "reg":b["regime"],"ret30":ret30,"eret30":entry_ret30,"start":start,"r10":r10,
                "fresh":b["debug_info.components.break.last_history_value"].fillna(0)>0}))
    d=pd.concat(rows); s=d[d.short]
    out={}
    s=s.assign(agebin=pd.cut(s.age,[-1,4,9,14,19,29,1000]))
    out["gain_by_age_regime"]=s.groupby(["agebin","reg"]).agg(bars=("g","size"),mean_g=("g","mean"),sum_g=("g","sum"))
    st=d[d.start].copy()
    st["eq"]=pd.qcut(st.ret30,4)
    out["entry_by_ret30_q"]=st.groupby("eq").agg(n=("r10","size"),mean_r10=("r10","mean"),
        share_up=("r10",lambda x:(x>0).mean()))
    s2=s.copy(); s2["eq"]=pd.qcut(s2.eret30,4)
    out["holding_gain_by_entry_ret30_q"]=s2.groupby(["eq","reg"]).agg(bars=("g","size"),sum_g=("g","sum"))
    s3=s.copy(); s3["rq"]=pd.cut(s3.ret30,[-1,-0.3,-0.15,-0.05,0,0.1,0.3,10])
    out["holding_gain_by_current_ret30"]=s3.groupby("rq").agg(bars=("g","size"),mean_g=("g","mean"),sum_g=("g","sum"))
    out["by_window_sum"]=s.groupby("w").g.sum().sort_values().head(8)
    out["fresh_while_short_share"]=float(s.fresh.mean())
    out["n_positions"]=int(d.start.sum())
    return out
