import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 26
    bars = data["bars"]; days = data["days"]
    # normal drift per coin
    drift = {}; usual = {}
    for c in bars:
        rs = []
        for w, b in bars[c].items():
            cl = b["close"].values
            for i in range(0, len(cl) - H, H):
                rs.append(cl[i+H]/cl[i]-1)
        drift[c] = np.mean(rs); usual[c] = np.std(rs)
    cases = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; f = b["forecast"].values
            n = len(cl)
            lr = np.log(cl)
            for i in range(0, n - H, H):
                if f[i] < 0:
                    tot = cl[i+H]/cl[i]-1
                    past = cl[i]/cl[i-H]-1 if i >= H else np.nan
                    past60 = cl[i]/cl[max(0,i-60)]-1 if i>=60 else np.nan
                    # recomputed cloud distance where possible
                    dist = np.nan
                    if i >= 77:
                        hi = b["high"].values; lo = b["low"].values
                        j = i - 26
                        ten = (hi[j-8:j+1].max()+lo[j-8:j+1].min())/2
                        kij = (hi[j-25:j+1].max()+lo[j-25:j+1].min())/2
                        sa = (ten+kij)/2
                        sb = (hi[j-51:j+1].max()+lo[j-51:j+1].min())/2
                        dist = cl[i]/min(sa,sb)-1
                    # max adverse within horizon
                    mx = cl[i:i+H+1].max()/cl[i]-1
                    cases.append(dict(coin=c, win=w, f=f[i], tot=-tot, unus=-(tot-drift[c]),
                                      past26=past, past60=past60, dist=dist, maxup=mx,
                                      year=pd.Timestamp(b["timestamp"].iloc[i]).year))
    d = pd.DataFrame(cases)
    out = {}
    out["n_cases"] = len(d)
    out["drift_by_coin"] = pd.Series(drift)
    out["by_coin"] = d.groupby("coin")[["tot","unus"]].agg(["mean","count"])
    out["by_year"] = d.groupby("year")[["tot","unus"]].agg(["mean","count"])
    for col in ["f","past26","past60","dist"]:
        dd = d.dropna(subset=[col])
        if len(dd) > 20:
            q = pd.qcut(dd[col].rank(method="first"), 4, labels=False)
            g = dd.groupby(q)[["tot","unus",col]].mean()
            g["n"] = dd.groupby(q).size()
            out["quart_"+col] = g
    out["maxup_quart_tot"] = d.groupby(pd.qcut(d["maxup"].rank(method="first"),4,labels=False))[["maxup","tot"]].mean()
    # book daily
    br = []
    for c in days:
        for w, dy in days[c].items():
            x = dy[["book_return","coin_return"]].copy(); x["win"]=w; x["coin"]=c
            br.append(x)
    br = pd.concat(br).dropna()
    out["book_by_win"] = br.groupby("win")[["book_return","coin_return"]].mean().mul(1e4).round(1)
    out["book_by_coin"] = br.groupby("coin")[["book_return","coin_return"]].mean().mul(1e4).round(1)
    # trades
    tr = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    out["trades"] = tr.groupby("coin")[["net_profit_loss_percent","profit_loss_percent"]].agg(["mean","count"])
    out["trade_winshare"] = float((tr["net_profit_loss_percent"]>0).mean())
    return out
