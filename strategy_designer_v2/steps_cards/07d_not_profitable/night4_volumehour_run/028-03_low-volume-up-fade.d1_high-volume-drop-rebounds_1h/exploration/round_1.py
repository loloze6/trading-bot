import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    # 1. book gross vs fees
    g_list=[]; f_list=[]; n_bars=0; turn=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            r=b["close"].shift(-1)/b["close"]-1
            g=(b["postRebalance_current_allocation"]*r)
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            g_list.append(g.dropna()); f_list.append(fee.dropna())
            turn.append((b["postRebalance_current_allocation"]-b["previous_allocation"]).abs())
    G=pd.concat(g_list); F=pd.concat(f_list); T=pd.concat(turn)
    out["book_per_bar"]=pd.Series({"gross_mean_bp":G.mean()*1e4,"fee_mean_bp":F.mean()*1e4,
        "gross_t":G.mean()/G.std()*np.sqrt(len(G)),"turnover_mean":T.mean(),"bars":len(G),
        "share_bars_in":(pd.concat([b["postRebalance_current_allocation"].abs()>0 for c in bars for b in bars[c].values()])).mean()})
    # 2. signal buckets recomputed
    rows=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            ret=b["close"].pct_change()
            sd=ret.rolling(720,min_periods=200).std()
            vr=b["volume"]/b["volume"].rolling(720,min_periods=200).mean()
            z=ret/sd
            d=pd.DataFrame({"z":z,"vr":vr,"coin":c})
            for h in [1,2,4,6,12,24]:
                d[f"f{h}"]=b["close"].shift(-h)/b["close"]-1
            d["pos"]=np.arange(len(b))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift={h:D[D.pos%h==0].groupby("coin")[f"f{h}"].mean() for h in [1,2,4,6,12,24]}
    sdh={h:D[D.pos%h==0][f"f{h}"].std() for h in [1,2,4,6,12,24]}
    F_=D[(D.z<-2)].dropna(subset=["vr"]).copy()
    F_["zb"]=pd.cut(-F_.z,[2,3,4,6,100])
    F_["vb"]=pd.qcut(F_.vr,3,labels=["vlow","vmid","vhigh"])
    res=[]
    for (zb,vb),g in F_.groupby(["zb","vb"],observed=True):
        row={"zb":str(zb),"vb":vb,"n":len(g)}
        for h in [1,2,6,24]:
            u=g[f"f{h}"]-g.coin.map(drift[h])
            u=u.dropna()
            row[f"u{h}_bp"]=u.mean()*1e4; row[f"t{h}"]=u.mean()/u.std()*np.sqrt(len(u)) if len(u)>2 else np.nan
        res.append(row)
    out["falls_unusual_by_depth_volume"]=pd.DataFrame(res)
    # same for big rises (continuation?) sign as raw
    R_=D[(D.z>3)].dropna(subset=["vr"]).copy()
    R_["vb"]=pd.qcut(R_.vr,3,labels=["vlow","vmid","vhigh"])
    res=[]
    for vb,g in R_.groupby("vb",observed=True):
        row={"vb":vb,"n":len(g)}
        for h in [2,6,24]:
            u=(g[f"f{h}"]-g.coin.map(drift[h])).dropna()
            row[f"u{h}_bp"]=u.mean()*1e4; row[f"t{h}"]=u.mean()/u.std()*np.sqrt(len(u))
        res.append(row)
    out["rises_z3_unusual"]=pd.DataFrame(res)
    out["usual_move_bp"]=pd.Series({h:sdh[h]*1e4 for h in sdh})
    # 3. trades
    tr=pd.concat([t for c in data["trades"] for t in data["trades"][c].values()])
    tr["dur_h"]=tr.duration_minutes/60
    tr["db"]=pd.cut(tr.dur_h,[0,2,3,6,24,1e5])
    out["trades_by_duration"]=tr.groupby("db",observed=True).agg(n=("dur_h","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"))
    out["trades_all"]=pd.Series({"n":len(tr),"gross_mean":tr.profit_loss_percent.mean(),"net_mean":tr.net_profit_loss_percent.mean(),"dur_med_h":tr.dur_h.median()})
    return out
