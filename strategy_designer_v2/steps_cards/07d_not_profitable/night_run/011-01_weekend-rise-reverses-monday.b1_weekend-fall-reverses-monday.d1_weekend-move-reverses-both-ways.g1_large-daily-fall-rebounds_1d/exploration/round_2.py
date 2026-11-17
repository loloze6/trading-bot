def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            nxt = c.shift(-1)/c - 1
            pos = b["postRebalance_current_allocation"].fillna(0)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            z = r1/vol20
            volrat = vol20/r1.rolling(60).std()
            vol5rat = r1.rolling(5).std()/vol20
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            df = pd.DataFrame({"coin":coin,"w":w,"pos":pos,"nxt":nxt,"z":z,"volrat":volrat,"vol5rat":vol5rat,
                               "fee":fee,"fc":b["forecast"],"day":pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    cm = d.groupby("coin")["nxt"].mean()
    d["ex"] = d["nxt"] - d["coin"].map(cm)
    d["g"] = d["pos"]*d["nxt"]
    act = d[d.pos>0].copy()
    act["fresh"] = act.fc>0
    out["fresh_vs_stale"] = act.groupby("fresh").agg(n=("ex","size"),mean_ex=("ex","mean"),gain=("g","sum"),fee=("fee","sum"),
        t=("ex",lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    a = act.dropna(subset=["volrat","z"]).copy()
    a["vq"] = pd.qcut(a.volrat,3,labels=False)
    a["zq"] = pd.qcut(a.z,3,labels=False)
    out["z_x_volrat_mean_ex"] = a.pivot_table(index="zq",columns="vq",values="ex",aggfunc="mean")
    out["z_x_volrat_n"] = a.pivot_table(index="zq",columns="vq",values="ex",aggfunc="size")
    a["v5"] = pd.qcut(a.vol5rat,5,labels=False)
    out["by_vol5rat"] = a.groupby("v5").agg(lo=("vol5rat","min"),hi=("vol5rat","max"),n=("ex","size"),mean_ex=("ex","mean"),
        gain=("g","sum"),t=("ex",lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    # gain by volrat tercile split: timing vs fee
    out["volrat_terc_fee"] = a.groupby("vq").agg(gain=("g","sum"),fee=("fee","sum"),mean_pos=("pos","mean"))
    # drawdown: worst book days and their volrat
    a2 = d.dropna(subset=["volrat"]).copy()
    a2["vq"] = pd.qcut(a2.volrat,3,labels=False)
    out["all_bars_g_by_vq"] = a2.groupby("vq").agg(gain=("g","sum"),fee=("fee","sum"),n_act=("pos",lambda x:(x>0).sum()))
    worst = d[d.pos>0].nsmallest(100,"g")
    out["worst100_bars"] = pd.Series({"mean_volrat":worst.volrat.mean(),"all_act_volrat":act.volrat.mean(),
        "mean_z":worst.z.mean(),"share_stale":(worst.fc<=0).mean(),"sum_g":worst.g.sum()})
    return out
