def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; n=len(c)
            r30=c.pct_change(30); dr=c.pct_change()
            sd30=dr.rolling(30).std()
            sdm=sd30.rolling(365,min_periods=60).median()
            pos=b["postRebalance_current_allocation"].fillna(0)
            gain=pos*(c.shift(-1)/c-1)
            f7=c.shift(-7)/c-1
            raw=b["debug_info.components.month_fall.last_history_value"]
            df=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(n),"r30":r30,"raw":raw,"fc":b["forecast"],"reg":b["regime"],
                             "pos":pos,"gain":gain,"f7":f7,"agit":sd30>sdm,"agit_w":sd30>sd30.median(),
                             "day":b["timestamp"].astype(str).str[:10],"chg":b["allocation_change"].abs() if "allocation_change" in b else np.nan})
            rows.append(df)
    df=pd.concat(rows)
    out={}
    act=df[df.pos!=0].copy()
    act["r30pos"]=act.r30>0
    out["held_bars_by_r30_sign"]=act.groupby("r30pos").agg(n=("gain","size"),mean_gain_bp=("gain",lambda s:1e4*s.mean()),mean_pos=("pos","mean"))
    act["q"]=pd.cut(act.r30,[-9,-0.3,-0.2,-0.1,-0.05,0,0.05,0.1,0.2,9])
    out["held_bars_by_r30_bin"]=act.groupby("q").agg(n=("gain","size"),gain_bp=("gain",lambda s:1e4*s.mean()),t=("gain",lambda s:s.mean()/s.std()*np.sqrt(len(s)) if len(s)>2 else np.nan),pos=("pos","mean"))
    out["held_bars_by_agit"]=act.groupby("agit_w").agg(n=("gain","size"),gain_bp=("gain",lambda s:1e4*s.mean()),pos=("pos","mean"))
    # condition alone check on grid of 7: choppy bars, agitated, by r30 sign and depth
    g=df[(df.reg=="unknown")&(df.i%7==0)&df.f7.notna()&df.r30.notna()].copy()
    drift=df[(df.i%7==0)&df.f7.notna()].groupby("coin").f7.mean()
    g["x7"]=g.f7-g.coin.map(drift)
    g["dep"]=pd.cut(g.r30,[-9,-0.15,0,0.15,9])
    def s(x):
        return pd.Series({"n":len(x),"days":x.day.nunique(),"raw%":100*x.f7.mean(),"exc%":100*x.x7.mean(),"t_raw":stats.ttest_1samp(x.f7,0).statistic if len(x)>2 else np.nan})
    out["choppy_grid_by_depth_and_agit_w"]=g.groupby(["agit_w","dep"]).apply(s)
    out["choppy_grid_by_depth_and_agit_prof"]=g.dropna(subset=["agit"]).groupby(["agit","dep"]).apply(s)
    # turnover: number of rebalances by held bars
    out["rebalances"]=pd.Series({"held_bars":len(act),"rebalance_bars":int((df.chg.fillna(0)>1e-9).sum()),"mean_abs_change":df.chg[df.chg>1e-9].mean()})
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items() if len(t)])
    tr["dur_d"]=tr.duration_minutes/1440
    out["trades_dur"]=tr.groupby(pd.cut(tr.dur_d,[0,3,7,14,30,999])).agg(n=("net_profit_loss_percent","size"),net=("net_profit_loss_percent","mean"),gross=("profit_loss_percent","mean"))
    tr["ef"]=pd.cut(tr.entry_forecast,[-21,-10,-5,-2,0])
    out["trades_by_entry_fc"]=tr.groupby("ef").agg(n=("net_profit_loss_percent","size"),net=("net_profit_loss_percent","mean"),gross=("profit_loss_percent","mean"))
    return out
