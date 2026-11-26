import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in (1,3,5,10)}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            r = pd.Series(c).pct_change()
            sd30 = r.rolling(30).std()
            z = r / sd30
            hi20 = pd.Series(c).rolling(20).max()
            dist = c / hi20 - 1
            tr60 = pd.Series(c).pct_change(60) * 100
            n = len(c)
            for h in allr:
                for i in range(0, n - h, h):
                    allr[h].append(c[i+h]/c[i]-1)
            for i in range(n):
                f = {}
                for h in (1,3,5,10):
                    f[h] = c[i+h]/c[i]-1 if i+h < n else np.nan
                rows.append(dict(coin=coin, win=w, i=i, grid5=(i//5), z=z.iloc[i], dist=dist.iloc[i],
                                 tr60=tr60.iloc[i], regime=df["regime"].iloc[i],
                                 fc=df["forecast"].iloc[i], year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                 day=str(df["timestamp"].iloc[i])[:10],
                                 f1=f[1], f3=f[3], f5=f[5], f10=f[10]))
        drift[coin] = {h: np.mean(v) for h, v in allr.items()}
    d = pd.DataFrame(rows)
    for h in (1,3,5,10):
        d[f"x{h}"] = d[f"f{h}"] - d["coin"].map(lambda k: drift[k][h])
    d["inprof"] = d["regime"] != "chop"
    d["athigh"] = d["dist"] >= -1e-12
    up = d[(d["z"] > 0)]
    # one per coin/window/grid cell, take the largest z
    def onepercell(s):
        return s.sort_values("z", ascending=False).groupby(["coin","win","grid5"]).head(1)
    out = {}
    def summ(s, h=5):
        s = s.dropna(subset=[f"x{h}"])
        if len(s) < 5: return pd.Series({"n": len(s)})
        sl = stats.linregress(s["z"], s[f"x{h}"])
        return pd.Series({"n": len(s), "mean_x%": s[f"x{h}"].mean()*100,
                          "t_mean": s[f"x{h}"].mean()/(s[f"x{h}"].std()/np.sqrt(len(s))),
                          "slope%": sl.slope*100, "t_slope": sl.slope/sl.stderr})
    groups = {
        "prof_high": up[up.inprof & up.athigh],
        "prof_nothigh": up[up.inprof & ~up.athigh],
        "prof_far": up[up.inprof & (up.dist <= -0.05)],
        "chop_high": up[~up.inprof & up.athigh],
        "prof_down_all": d[d.inprof & (d.z < 0)],
    }
    tab = {}
    for k, s in groups.items():
        s1 = onepercell(s)
        for h in (1,3,5,10):
            tab[(k,h)] = summ(s1, h)
    out["groups_by_horizon"] = pd.DataFrame(tab).T
    ph = onepercell(groups["prof_high"]).dropna(subset=["x5"])
    ph["zq"] = pd.qcut(ph["z"], 4, labels=False, duplicates="drop")
    out["prof_high_by_zq"] = ph.groupby("zq").agg(n=("x5","size"), zmean=("z","mean"), x5=("x5", lambda v: v.mean()*100), x10=("x10", lambda v: v.mean()*100))
    out["prof_high_by_coin"] = ph.groupby("coin").apply(summ)
    out["prof_high_by_year"] = ph.groupby("year").apply(summ)
    ph["trs"] = np.where(ph.tr60 > 0, "tr60>0", "tr60<=0")
    out["prof_high_by_trsign"] = ph.groupby("trs").apply(summ)
    # downside mirror: in profile, close at 20d low, falling day: continuation short?
    dn = d[d.inprof & (d.z < 0)].copy()
    lo = []
    out["n_rows"] = len(d)
    return out
