def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for c,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            allr.append((b.close.shift(-1)/b.close-1).dropna())
        mu=pd.concat(allr).mean()
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            d=pd.DataFrame()
            d["loc"]=(b.close-b.low)/(b.high-b.low)
            d["ret1"]=b.close.pct_change()
            d["r60"]=b.close/b.close.shift(60)-1
            d["r20"]=b.close/b.close.shift(20)-1
            v30=d.ret1.rolling(30,min_periods=20).std()
            d["agit"]=v30>v30.expanding(min_periods=30).median()
            d["fwd"]=b.close.shift(-1)/b.close-1
            d["fwd3"]=b.close.shift(-3)/b.close-1
            d["ex"]=d.fwd-mu
            d["alloc"]=b.postRebalance_current_allocation
            d["gain"]=d.alloc*d.fwd
            d["turn"]=(b.postRebalance_current_allocation-b.previous_allocation).abs()
            d["feeret"]=(b.total_portfolio_value-b.postRebalance_total_value)/b.total_portfolio_value
            d["coin"]=c; d["w"]=w; d["mu"]=mu
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["fwd","loc"])
    out={}
    out["costs"]=pd.Series({"mean_turn":D.turn.mean(),"mean_fee_per_bar%":D.feeret.mean()*100,
        "gain_before_fee%":D.gain.mean()*100,"n_bars_r60":D.r60.notna().sum()})
    E=D.dropna(subset=["r60"]).copy()
    E["tr"]=pd.cut(E.r60,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    E["hi"]=E["loc"]>=0.8
    def agg(g):
        return pd.Series({"n":len(g),"ex%":g.ex.mean()*100,"t":g.ex.mean()/g.ex.std()*np.sqrt(len(g)),
                          "fwd%":g.fwd.mean()*100,"slope":np.polyfit(g["loc"],g.ex,1)[0] if len(g)>30 else np.nan,
                          "gain%":g.gain.mean()*100})
    out["r60_trend_x_hi"]=E.groupby(["tr","hi"]).apply(agg)
    out["r60_trend_all"]=E.groupby("tr").apply(agg)
    out["fall_agit_x_hi"]=E[E.tr=="fall"].groupby(["agit","hi"]).apply(agg)
    # graded inside falling
    F=E[E.tr=="fall"].copy()
    F["q"]=pd.cut(F["loc"],[-.01,.2,.4,.6,.8,1.01],labels=["q1","q2","q3","q4","q5"])
    out["fall_by_q"]=F.groupby("q").apply(agg)
    # short-only-in-falling hypothetical: position = -loc, in falling only, per window
    F["pos"]=-F["loc"]
    out["fall_short_hyp"]=pd.Series({"mean_gain%":(F.pos*F.fwd).mean()*100,"t":(F.pos*F.fwd).mean()/(F.pos*F.fwd).std()*np.sqrt(len(F)),
        "fwd3_q5%":F[F.q=="q5"].fwd3.mean()*100,"fwd3_fall_all%":F.fwd3.mean()*100})
    # by window, falling q5 ex
    out["fall_hi_by_window"]=E[(E.tr=="fall")&E.hi].groupby("w").ex.agg(["count","mean"])
    # 20-day falling, years
    E["year"]=0
    return out
