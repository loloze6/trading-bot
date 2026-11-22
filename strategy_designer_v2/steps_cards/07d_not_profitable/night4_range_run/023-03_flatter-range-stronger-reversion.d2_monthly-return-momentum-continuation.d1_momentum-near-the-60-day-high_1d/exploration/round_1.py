import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            b["ret1"] = c.shift(-1)/c - 1
            b["alloc"] = b["postRebalance_current_allocation"]
            b["pnl"] = b["alloc"]*b["ret1"]
            b["r30"] = c/c.shift(30)-1
            b["dist60"] = 1 - c/c.rolling(60, min_periods=30).max()
            b["vol20"] = c.pct_change().rolling(20).std()
            b["r5past"] = c/c.shift(5)-1
            b["coin"] = coin; b["win"] = w
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[["coin","win","day","year","alloc","ret1","pnl","r30","dist60","vol20","r5past","forecast"]])
    B = pd.concat(rows)
    B = B.dropna(subset=["pnl"])
    B["side"] = np.where(B["alloc"]>0.01,"long",np.where(B["alloc"]<-0.01,"short","flat"))
    g = B.groupby("side")["pnl"]
    out["pnl by side"] = pd.DataFrame({"n":g.size(),"mean":g.mean(),"sum":g.sum(),"std":g.std(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    act = B[B.side!="flat"].copy()
    for col in ["r30","dist60","vol20","r5past"]:
        act[col+"_q"] = act.groupby("side")[col].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        gg = act.groupby(["side",col+"_q"])
        out["pnl by side x "+col+" quintile"] = pd.DataFrame({"n":gg.size(),"mean pnl":gg["pnl"].mean(),"sum pnl":gg["pnl"].sum(),"mean "+col:gg[col].mean(),"mean |alloc|":gg["alloc"].apply(lambda s: s.abs().mean())})
    # book daily
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d.copy(); dd["coin"]=coin; dd["win"]=w; D.append(dd)
    D = pd.concat(D)
    D["wn"] = D["win"].str[1:].astype(int)
    port = D.groupby(["wn","day"]).agg(br=("book_return","mean"), cr=("coin_return","mean")).dropna().reset_index().sort_values(["wn","day"])
    port["eq"] = (1+port.br).cumprod()
    port["peak"] = port.eq.cummax()
    port["dd"] = port.eq/port.peak-1
    # episodes
    port["pk_id"] = (port.eq>=port.peak).cumsum()
    ep = port.groupby("pk_id").agg(depth=("dd","min"), days=("dd","size"), wn_first=("wn","first"), wn_last=("wn","last"))
    ep = ep.sort_values("depth").head(6)
    info = []
    for pid, r in ep.iterrows():
        seg = port[port.pk_id==pid]
        trough = seg.dd.idxmin()
        s2 = seg.loc[:trough]
        info.append({"depth":r.depth,"days to trough":len(s2),"windows":f"w{r.wn_first}-w{r.wn_last}",
                     "book chained":(1+s2.br).prod()-1,"coins chained":(1+s2.cr).prod()-1,
                     "year":pd.to_datetime(s2.day.iloc[0]).year})
    out["deepest falls"] = pd.DataFrame(info)
    # what held during the worst fall: join day sets
    worst = ep.index[0]
    seg = port[port.pk_id==worst]; seg = seg.loc[:seg.dd.idxmin()]
    keys = set(zip(seg.wn, seg.day))
    B["wn"] = B["win"].str[1:].astype(int)
    m = B[[ (a,b) in keys for a,b in zip(B.wn,B.day)]]
    gm = m.groupby(["coin","side"])
    out["worst fall by coin side"] = pd.DataFrame({"n":gm.size(),"sum pnl":gm.pnl.sum(),"mean r30":gm.r30.mean(),"mean dist60":gm.dist60.mean(),"mean vol20":gm.vol20.mean()})
    # all drawdown days (dd< -0.1) vs others
    port["indd"] = port.dd < -0.10
    kk = set(zip(port[port.indd].wn, port[port.indd].day))
    B["indd"] = [ (a,b) in kk for a,b in zip(B.wn,B.day)]
    gd = B[B.side!="flat"].groupby(["indd","side"])
    out["deep-dd days vs others"] = pd.DataFrame({"n":gd.size(),"sum pnl":gd.pnl.sum(),"mean pnl":gd.pnl.mean(),"mean r30":gd.r30.mean(),"mean dist60":gd.dist60.mean(),"mean vol20":gd.vol20.mean()})
    gy = B[B.side!="flat"].groupby(["year","side"])
    out["pnl by year side"] = pd.DataFrame({"n":gy.size(),"sum":gy.pnl.sum(),"mean":gy.pnl.mean()})
    out["max dd"] = port.dd.min()
    return out
