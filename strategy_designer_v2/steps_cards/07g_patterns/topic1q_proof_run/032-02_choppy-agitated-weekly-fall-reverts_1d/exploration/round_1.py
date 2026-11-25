import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            n = len(c)
            inprof = (b["regime"].astype(str) == "unknown").values
            ts = pd.to_datetime(b["timestamp"])
            # daily
            r1 = np.full(n, np.nan); r1[1:] = c[1:]/c[:-1]-1
            nx1 = np.full(n, np.nan); nx1[:-1] = c[1:]/c[:-1]-1
            rng = (b["high"]-b["low"]).values/c
            for i in range(n):
                daily.append((coin, w, i, inprof[i], r1[i], nx1[i], rng[i], ts.iloc[i].weekday()))
            for i in range(0, n, 7):
                if i+7 < n and i-7 >= 0:
                    p7 = c[i]/c[i-7]-1; f7 = c[i+7]/c[i]-1
                    p30 = c[i]/c[i-30]-1 if i-30 >= 0 else np.nan
                    vol = np.std(np.diff(np.log(c[max(0,i-30):i+1])))
                    rows.append((coin, w, ts.iloc[i].normalize(), inprof[i], p7, f7, p30, vol, b["forecast"].iloc[i]))
    g = pd.DataFrame(rows, columns=["coin","w","day","prof","p7","f7","p30","vol","fc"])
    g["drift"] = g.groupby("coin")["f7"].transform("mean")
    g["ex"] = g["f7"] - g["drift"]
    g["usual"] = g.groupby("coin")["f7"].transform("std")
    g["z"] = g["p7"]/g["usual"]
    out["share in profile (grid)"] = g["prof"].mean()
    def tab(sub):
        sub = sub.copy()
        sub["q"] = pd.qcut(sub["z"], 5, labels=False, duplicates="drop")
        t = sub.groupby("q").agg(n=("ex","size"), p7=("p7","mean"), ex=("ex","mean"), f7=("f7","mean"))
        t["t"] = sub.groupby("q")["ex"].apply(lambda x: x.mean()/(x.std()/np.sqrt(len(x))))
        return t
    out["quintile past7 -> excess next7, in profile"] = tab(g[g.prof])
    out["quintile past7 -> excess next7, out of profile"] = tab(g[~g.prof])
    for name, sub in [("all", g), ("prof", g[g.prof]), ("noprof", g[~g.prof])]:
        r = stats.linregress(sub["z"], sub["ex"]/sub["usual"])
        out[f"slope z->ex/usual {name}"] = f"slope {r.slope:.3f} t {r.slope/r.stderr:.2f} n {len(sub)}"
    # 30d past return quintiles
    s = g.dropna(subset=["p30"]).copy()
    s["q"] = pd.qcut(s["p30"], 5, labels=False)
    out["quintile past30 -> excess next7 (all)"] = s.groupby("q").agg(n=("ex","size"), p30=("p30","mean"), ex=("ex","mean"), tt=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    s["vq"] = s.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["vol tercile -> excess next7"] = s.groupby("vq").agg(n=("ex","size"), ex=("ex","mean"), tt=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    d = pd.DataFrame(daily, columns=["coin","w","i","prof","r1","nx1","rng","wd"]).dropna()
    d["z1"] = d["r1"]/d.groupby("coin")["r1"].transform("std")
    d["nz"] = d["nx1"]/d.groupby("coin")["r1"].transform("std")
    d["q"] = d.groupby("coin")["z1"].transform(lambda x: pd.qcut(x, 10, labels=False))
    out["decile daily ret -> next day z"] = d.groupby("q").agg(n=("nz","size"), z1=("z1","mean"), nz=("nz","mean"), tt=("nz", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    out["weekday -> next day z"] = d.groupby("wd").agg(n=("nz","size"), nz=("nz","mean"), tt=("nz", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    d["rq"] = d.groupby("coin")["rng"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["range quintile x sign -> next day z"] = d.groupby(["rq", d["r1"]>0]).agg(n=("nz","size"), nz=("nz","mean"), tt=("nz", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    # book
    days = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            days.append(dd.assign(coin=coin, w=w))
    D = pd.concat(days)
    B = D.groupby(["w","day"])["book_return"].mean().dropna()
    out["book mean daily, t"] = f"{B.mean():.5f} t {B.mean()/(B.std()/np.sqrt(len(B))):.2f} n {len(B)}"
    out["book by window"] = D.groupby("w")["book_return"].mean()
    return out
