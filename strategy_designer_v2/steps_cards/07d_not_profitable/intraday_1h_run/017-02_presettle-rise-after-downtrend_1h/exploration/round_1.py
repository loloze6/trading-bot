import numpy as np, pandas as pd
def explore(data):
    out = {}
    rows = []
    hrs = []
    trows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            r1 = b["close"].shift(-1)/b["close"]-1
            pos = b["postRebalance_current_allocation"].fillna(0)
            g = pos*r1
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["g"]=g; b["fee"]=fee; b["pos"]=pos; b["r1"]=r1; b["h"]=b["ts"].dt.hour
            rows.append(pd.DataFrame({"coin":coin,"gross":[g.sum()],"fees":[fee.sum()],"bars":[len(b)],
                                      "turnover":[b["postRebalance_current_allocation"].diff().abs().sum()]}))
            hrs.append(b[["h","r1","pos","g","fee"]])
        for w, t in data["trades"][coin].items():
            t=t.copy(); t["coin"]=coin; trows.append(t)
    R = pd.concat(rows)
    s = R.groupby("coin")[["gross","fees","bars","turnover"]].sum()
    s["gross_per_day"]=s["gross"]/(s["bars"]/24); s["fee_per_day"]=s["fees"]/(s["bars"]/24)
    s["fee_per_unit_turn"]=s["fees"]/s["turnover"]
    out["gross vs fees by coin"]=s
    H = pd.concat(hrs)
    hh = H.groupby("h").agg(mean_r1=("r1","mean"),mean_pos=("pos","mean"),gross=("g","mean"),fee=("fee","mean"),n=("r1","size"))
    hh["t_r1"]=H.groupby("h")["r1"].apply(lambda x: x.mean()/x.std()*np.sqrt(x.count()))
    out["by hour"]=hh
    T = pd.concat(trows)
    out["trades"]=T.groupby("coin").agg(n=("side","size"),mean_pl=("profit_loss_percent","mean"),
        mean_net=("net_profit_loss_percent","mean"),win=("profit_loss_percent",lambda x:(x>0).mean()),
        dur_h=("duration_minutes",lambda x:x.mean()/60))
    out["trade pl t"]=float(T["profit_loss_percent"].mean()/T["profit_loss_percent"].std()*np.sqrt(len(T)))
    return out
