import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    # trades: gross vs net
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t): tr.append(t.assign(coin=c))
    tr = pd.concat(tr)
    out["trades"] = pd.DataFrame({
        "n": [len(tr)],
        "gross_mean_%": [tr.profit_loss_percent.mean()],
        "net_mean_%": [tr.net_profit_loss_percent.mean()],
        "dur_h_median": [tr.duration_minutes.median()/60],
        "dur_h_mean": [tr.duration_minutes.mean()/60],
        "win_gross": [(tr.profit_loss_percent>0).mean()]})
    # book daily
    d = []
    for c, ws in data["days"].items():
        for w, t in ws.items():
            d.append(t.assign(coin=c, w=w))
    d = pd.concat(d)
    out["book_by_coin"] = d.groupby("coin")[["book_return","coin_return"]].mean()
    # recompute situation, forward returns at several horizons, by fall sigma x volume ratio
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b.close.reset_index(drop=True); v = b.volume.reset_index(drop=True)
            r = cl.pct_change()
            sd = r.rolling(720, min_periods=240).std()
            vm = v.rolling(720, min_periods=240).mean()
            z = r/sd; vr = v/vm
            f = b.forecast.reset_index(drop=True)
            n = len(cl)
            for h in [2,6,12,24]:
                fr = cl.shift(-h)/cl - 1
                idx = np.arange(0, n, h)
                rows.append(pd.DataFrame({"coin":c,"w":w,"h":h,"z":z.values[idx],"vr":vr.values[idx],
                                          "fr":fr.values[idx],"fc":f.values[idx]}))
    a = pd.concat(rows).dropna()
    drift = a.groupby(["coin","h"]).fr.transform("mean")
    a["ab"] = a.fr - drift
    a["zb"] = pd.cut(a.z, [-99,-4,-3,-2,-1,1,2,3,4,99])
    a["vb"] = pd.cut(a.vr, [0,1,2,3,5,999])
    def agg(g):
        return pd.Series({"n":len(g),"mean_ab_%":g.ab.mean()*100,"t":g.ab.mean()/(g.ab.std()/np.sqrt(len(g))) if len(g)>2 else np.nan})
    for h in [2,6,24]:
        s = a[a.h==h]
        out[f"h{h}_by_zbin"] = s.groupby("zb", observed=True).apply(agg)
        ss = s[s.z<-2]
        out[f"h{h}_falls_by_vol"] = ss.groupby("vb", observed=True).apply(agg)
        su = s[s.z>2]
        out[f"h{h}_rises_by_vol"] = su.groupby("vb", observed=True).apply(agg)
    # forecast active share and by forecast level, h2
    s = a[a.h==2]
    s["fb"] = pd.cut(s.fc, [-0.01,0.01,1,5,20.1])
    out["h2_by_forecast"] = s.groupby("fb", observed=True).apply(agg)
    return out
