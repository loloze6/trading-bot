import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); h = b["high"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20).std()
            hh20 = h.rolling(20).max()
            depth = (c - hh20) / hh20 / sd20
            tr60 = c / c.shift(60) - 1
            n = len(b)
            for H in (1, 5):
                fwd = c.shift(-H) / c - 1
                for i in range(0, n - H, H):
                    rows.append(dict(coin=coin, w=w, H=H, i=i, r1=r1[i], depth=depth[i], fwd=fwd[i],
                                     regime=b["regime"][i], tr60=tr60[i],
                                     wd=pd.Timestamp(b["timestamp"][i]).dayofweek,
                                     ret5p=(c[i]/c[i-5]-1) if i>=5 else np.nan,
                                     sd20=sd20[i]))
    d = pd.DataFrame(rows)
    # drift per coin and H over all windows
    d["drift"] = d.groupby(["coin","H"])["fwd"].transform("mean")
    d["un"] = d["fwd"] - d["drift"]
    out = {}
    def tab(g):
        return pd.Series(dict(n=len(g), mean_un=g["un"].mean(), t=g["un"].mean()/(g["un"].std()/np.sqrt(len(g))) if len(g)>2 else np.nan,
                              mean_tot=g["fwd"].mean()))
    for H in (1,5):
        x = d[(d.H==H)].dropna(subset=["depth","un"]).copy()
        x["dq"] = pd.qcut(x["depth"], 5, labels=False)
        x["up"] = x["r1"]>0
        x["prof"] = np.where(x["regime"]=="chop","trend", "choppy")
        out[f"H{H} by profile x up x depth quintile"] = x.groupby(["prof","up","dq"]).apply(tab)
        out[f"H{H} by weekday"] = x.groupby("wd").apply(tab)
        x["vq"] = x.groupby("coin")["sd20"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
        out[f"H{H} by vol tercile x up"] = x.groupby(["vq","up"]).apply(tab)
        x["mq"] = pd.qcut(x["r1"]/x["sd20"], 5, labels=False)
        out[f"H{H} by 1d move/sd quintile"] = x.groupby(["prof","mq"]).apply(tab)
        x["tq"] = pd.qcut(x["tr60"], 5, labels=False)
        out[f"H{H} by 60d trend quintile"] = x.groupby("tq").apply(tab)
    # book
    dd=[]
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            dd.append(t.assign(coin=coin, w=w))
    dd = pd.concat(dd)
    br = dd.groupby(["w","day"])["book_return"].mean().dropna()
    out["book by window"] = br.groupby(level=0).agg(["count","mean","std"])
    return out
