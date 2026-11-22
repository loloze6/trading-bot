import pandas as pd, numpy as np

def explore(data):
    out = {}
    # book: gross gain vs fees, per day, via bars
    g = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ret = b.close.shift(-1)/b.close - 1
            gross = (b.postRebalance_current_allocation*ret).sum()
            fee = (b.total_portfolio_value - b.postRebalance_total_value).sum()/b.total_portfolio_value.mean()
            turn = (b.postRebalance_current_allocation - b.previous_allocation).abs().sum()
            days = len(b)/24
            active = (b.postRebalance_current_allocation.abs()>1e-6).mean()
            g.append(dict(coin=c, w=w, gross_per_day=gross/days, fee_per_day=fee/days, turnover_per_day=turn/days, active=active))
    g = pd.DataFrame(g)
    out["book_gross_fee"] = g.groupby("coin")[["gross_per_day","fee_per_day","turnover_per_day","active"]].mean()*[100,100,1,1]
    # product score cases, by score bin, horizons 1,2,4, plus vol regime
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b.close.reset_index(drop=True); v = b.volume.reset_index(drop=True)
            r = cl.pct_change()
            sd = r.rolling(720, min_periods=240).std()
            sdl = sd / sd.rolling(2160, min_periods=480).mean()
            vm = v.rolling(720, min_periods=240).mean()
            z = r/sd; vr = v/vm
            n = len(cl)
            for h in [1,2,4]:
                fr = cl.shift(-h)/cl - 1
                idx = np.arange(0, n, h)
                rows.append(pd.DataFrame({"coin":c,"w":w,"h":h,"z":z.values[idx],"vr":vr.values[idx],
                    "sdl":sdl.values[idx],"fr":fr.values[idx]}))
    a = pd.concat(rows).dropna()
    a["ab"] = a.fr - a.groupby(["coin","h"]).fr.transform("mean")
    a["score"] = -a.z.clip(upper=0)*a.vr
    def agg(s):
        return pd.Series({"n":len(s),"mean_ab_%":s.ab.mean()*100,"total_%":s.fr.mean()*100,
                          "t":s.ab.mean()/(s.ab.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    a["sb"] = pd.cut(a.score, [-0.01,1,3,6,10,20,40,1e9])
    for h in [1,2,4]:
        out[f"h{h}_by_score"] = a[a.h==h].groupby("sb", observed=True).apply(agg)
    s = a[(a.h==2)&(a.score>10)].copy()
    s["vol_state"] = pd.qcut(s.sdl, 3, labels=["calm","mid","hot"])
    out["h2_score>10_by_volstate"] = s.groupby("vol_state", observed=True).apply(agg)
    s["year"] = 0
    out["h2_score>10_by_coin"] = s.groupby("coin").apply(agg)
    wpos = s.groupby("w").ab.mean()
    out["h2_score>10_windows_positive_share"] = float((wpos>0).mean())
    return out
