def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            a = b["postRebalance_current_allocation"].fillna(0)
            r1 = cl.shift(-1)/cl - 1
            g = a*r1
            p20 = cl/cl.shift(20)-1
            p60 = cl/cl.shift(60)-1
            dd60 = cl/cl.rolling(60, min_periods=1).max()-1
            vol20 = (cl/cl.shift(1)-1).rolling(20).std()
            vol100 = (cl/cl.shift(1)-1).rolling(100).std()
            raw = b["debug_info.components.above_ma.last_history_value"]
            dfo = b["forecast"] - b["forecast"].shift(5)
            rows.append(pd.DataFrame(dict(coin=c, wn=int(w[1:]), a=a, g=g, r1=r1, p20=p20, p60=p60,
                                          dd60=dd60, vr=vol20/vol100, raw=raw, f=b["forecast"], dfo=dfo)))
    d = pd.concat(rows).dropna(subset=["g"])
    act = d[d.a > 0].copy()
    out = {}
    def summ(x):
        return pd.Series(dict(n=len(x), mean_g=x.g.mean(), sum_g=x.g.sum(), t=x.g.mean()/x.g.std()*np.sqrt(len(x)), mean_r1=x.r1.mean()))
    for col in ["p20", "p60", "dd60", "vr", "raw", "dfo"]:
        q = pd.qcut(act[col], 4, labels=False, duplicates="drop")
        out[f"active position gain by {col} quartile"] = act.groupby(q).apply(summ).join(act.groupby(q)[col].mean().rename("mid"))
    bad = act[act.wn.isin([12, 13, 16, 18])]
    good = act[~act.wn.isin([12, 13, 16, 18])]
    out["bad windows vs rest: medians"] = pd.DataFrame({"bad": bad[["p20", "p60", "dd60", "vr", "raw", "f", "a"]].median(),
                                                     "rest": good[["p20", "p60", "dd60", "vr", "raw", "f", "a"]].median()})
    out["bad windows active gain by p20 sign"] = bad.groupby(bad.p20 > 0).apply(summ)
    # joint: p20 sign x dd60 deep
    act["state"] = np.where(act.p20 > 0, "p20+", "p20-") + np.where(act.dd60 < -0.1, "_deep", "_near")
    out["active gain by p20 sign x near high"] = act.groupby("state").apply(summ)
    out["share of days active"] = float((d.a > 0).mean())
    out["flat days mean coin r1"] = float(d[d.a == 0].r1.mean())
    return out
