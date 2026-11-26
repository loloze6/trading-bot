import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(b)
            r28 = pd.Series(c).pct_change(28).values
            raw = b.get("debug_info.components.calm.last_history_value")
            pp = b.get("debug_info.components.calm.post_pipeline_value")
            rng = ((b["high"] - b["low"]) / b["close"])
            rr = (rng / rng.rolling(28).mean()).values  # not used for grading; info
            for h in (5, 10, 20):
                for t in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, ret=c[t+h]/c[t]-1,
                                     regime=b["regime"].iat[t], r28=r28[t],
                                     raw=(raw.iat[t] if raw is not None else np.nan),
                                     absf=(abs(pp.iat[t]) if pp is not None else np.nan),
                                     day=str(b["timestamp"].iat[t])[:10]))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby(["coin", "h"])["ret"].transform("mean")
    df["adj"] = df["ret"] - df["drift"]
    tr = df[(df.regime == "trending")].dropna(subset=["absf", "raw"]).copy()
    out = {}
    res = []
    for h in (5, 10, 20):
        s = tr[tr.h == h]
        for var in ["absf", "raw", "r28"]:
            ss = s.dropna(subset=[var])
            sl = stats.linregress(ss[var], ss["adj"])
            res.append(dict(h=h, var=var, n=len(ss), slope=sl.slope, t=sl.slope/sl.stderr))
        s2 = s.copy()
        s2["q"] = pd.qcut(s2["absf"], 5, labels=False, duplicates="drop")
        out[f"by absf quintile h{h}"] = s2.groupby("q")["adj"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
        s3 = s.dropna(subset=["r28"]).copy()
        s3["qr"] = pd.qcut(s3["r28"], 5, labels=False)
        out[f"by r28 quintile h{h}"] = s3.groupby("qr").agg(count=("adj", "count"), mean=("adj", "mean"),
                                                             r28=("r28", "mean"))
        # within shallow vs deep halves, absf slope
        med = s3.r28.median()
        g = []
        for name, part in [("deep", s3[s3.r28 < med]), ("shallow", s3[s3.r28 >= med])]:
            sl = stats.linregress(part["absf"], part["adj"])
            g.append(dict(part=name, n=len(part), mean=part.adj.mean(), slope=sl.slope, t=sl.slope/sl.stderr))
        out[f"absf slope by depth half h{h}"] = pd.DataFrame(g)
    out["slopes (recorded)"] = pd.DataFrame(res)
    s5 = tr[tr.h == 5]
    g = []
    for k, s in s5.groupby("win"):
        if len(s) > 15:
            sl = stats.linregress(s["absf"], s["adj"]); g.append(dict(win=k, n=len(s), mean=s.adj.mean(), slope=sl.slope, t=sl.slope/sl.stderr))
    out["by window h5 absf"] = pd.DataFrame(g)
    g = []
    for k, s in s5.groupby("coin"):
        sl = stats.linregress(s["absf"], s["adj"]); g.append(dict(coin=k, n=len(s), mean=s.adj.mean(), slope=sl.slope, t=sl.slope/sl.stderr))
    out["by coin h5 absf"] = pd.DataFrame(g)
    # day-clustered t of mean adj at each h, and of r28 slope residual sign
    g = []
    for h in (5, 10, 20):
        s = tr[tr.h == h]
        d = s.groupby("day")["adj"].sum()
        g.append(dict(h=h, cases=len(s), days=len(d), mean=s.adj.mean(),
                      t_day=d.sum()/len(s) / (d.std()*np.sqrt(len(d))/len(s))))
    out["mean adj, day-clustered"] = pd.DataFrame(g)
    return out
