import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    grid = []
    daily = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.shift(-1)/c - 1
            a = b["postRebalance_current_allocation"].fillna(0).astype(float)
            gross = a*r1
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            turn = (a - b["previous_allocation"].fillna(0)).abs()
            f = b["forecast"].fillna(0)
            df = pd.DataFrame({"coin":coin,"w":w,"gross":gross,"fee":fee,"turn":turn,"a":a,"f":f,"r1":r1,
                               "f72":b.get("debug_info.components.fall72.post_pipeline_value"),
                               "f24":b.get("debug_info.components.fall24.post_pipeline_value")})
            df["ret72"] = c/c.shift(72)-1
            df["ret24"] = c/c.shift(24)-1
            df["fwd72"] = c.shift(-72)/c-1
            df["fwd24"] = c.shift(-24)/c-1
            rows.append(df)
            grid.append(df.iloc[::72])
    B = pd.concat(rows)
    G = pd.concat(grid)
    out["bar_totals"] = pd.Series({"mean_gross_per_bar":B["gross"].mean(),"mean_fee_per_bar":B["fee"].mean(),
        "gross_per_day":B["gross"].mean()*24,"fee_per_day":B["fee"].mean()*24,
        "share_bars_long":(B["a"]>0).mean(),"mean_alloc_when_long":B.loc[B.a>0,"a"].mean(),
        "turnover_per_day":B["turn"].mean()*24})
    # market part vs timing
    mu = B.groupby("coin")["r1"].mean()
    B["mkt"] = B["a"]*B["coin"].map(mu)
    out["mkt_vs_timing_per_day"] = pd.Series({"market_part":B["mkt"].mean()*24,"timing":(B["gross"]-B["mkt"]).mean()*24})
    # gross gain by forecast bucket
    L = B[B.f>0].copy()
    L["fq"] = pd.qcut(L["f"],5,labels=False,duplicates="drop")
    out["by_forecast_q"] = L.groupby("fq").agg(n=("f","size"),f=("f","mean"),gross=("gross","mean"),fee=("fee","mean"),turn=("turn","mean"),r1=("r1","mean"))
    # grid forward returns by component, active bars
    Ga = G[(G.ret72<=0)].copy()
    mu72 = G.groupby("coin")["fwd72"].mean()
    mu24 = G.groupby("coin")["fwd24"].mean()
    Ga["x72"] = Ga["fwd72"]-Ga["coin"].map(mu72)
    Ga["x24"] = Ga["fwd24"]-Ga["coin"].map(mu24)
    Ga["q72"] = pd.qcut(Ga["ret72"],5,labels=False)
    Ga["q24"] = pd.qcut(Ga["ret24"],5,labels=False)
    out["grid_by_ret72_q"] = Ga.groupby("q72").agg(n=("x72","size"),ret72=("ret72","mean"),x72=("x72","mean"),x24=("x24","mean"))
    out["grid_by_ret24_q"] = Ga.groupby("q24").agg(n=("x72","size"),ret24=("ret24","mean"),x72=("x72","mean"),x24=("x24","mean"))
    # forecast persistence: how long forecast stays >0
    runs=[]
    for (cn,w),d in B.groupby(["coin","w"]):
        on=(d.f>0).astype(int).values
        cnt=0
        for v in on:
            if v: cnt+=1
            elif cnt: runs.append(cnt); cnt=0
    out["active_run_hours"] = pd.Series(runs).describe()
    # windows
    out["by_window"] = B.groupby("w").agg(gross=("gross","mean"),fee=("fee","mean"),r1=("r1","mean")).mul(24)
    return out
