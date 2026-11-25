import numpy as np, pandas as pd
from scipy.stats import spearmanr

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        drift = pd.concat([b["close"].pct_change() for b in wins.values()]).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c, h, l = b["close"], b["high"], b["low"]
            d = pd.DataFrame({"coin": coin, "win": w, "ts": b["timestamp"]})
            d["fwd1"] = c.shift(-1)/c - 1 - drift
            d["fwd2"] = c.shift(-2)/c - 1 - 2*drift
            d["ret30"] = c/c.shift(30) - 1
            d["ret10"] = c/c.shift(10) - 1
            rng = (h - l)/c
            d["rng30"] = rng.shift(1).rolling(30).mean()
            d["rngwide"] = rng.rolling(30).mean()/rng.expanding(60).mean()
            for p in (5, 10, 30):
                d[f"dist{p}"] = c/l.shift(1).rolling(p).min() - 1
                d[f"zd{p}"] = d[f"dist{p}"]/d["rng30"]
            d["case"] = (b["regime"] == "mean_reversion") & (b["forecast"] > 0)
            d["alloc"] = b["postRebalance_current_allocation"]
            d["fc"] = b["forecast"]
            d["sizing_target"] = b["sizing_target_allocation"]
            d["approved"] = b["approved_rebalance"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)

    def stat(mask, col="fwd1"):
        s = D.loc[mask & D[col].notna(), [col, "ts"]]
        n = len(s)
        if n < 3:
            return pd.Series({"n": n})
        m = s[col].mean()
        dev = (s[col] - m).groupby(s["ts"]).sum()
        nd = len(dev)
        se = np.sqrt((dev**2).sum()*nd/(nd-1))/n
        return pd.Series({"n": n, "days": nd, "mean%": 100*m, "t": m/se})

    out = {}
    cs = D[D["case"]]
    out["case bars: forecast, alloc"] = pd.Series({
        "cases": len(cs), "alloc>0": int((cs["alloc"].abs() > 1e-9).sum()),
        "mean fc": cs["fc"].mean(), "median fc": cs["fc"].median(),
        "mean alloc": cs["alloc"].mean(), "mean sizing_target": pd.to_numeric(cs["sizing_target"], errors="coerce").mean(),
        "approved share": pd.to_numeric(cs["approved"], errors="coerce").mean(),
        "fwd1 alloc>0 %": 100*cs.loc[cs["alloc"].abs() > 1e-9, "fwd1"].mean(),
        "fwd1 alloc==0 %": 100*cs.loc[cs["alloc"].abs() <= 1e-9, "fwd1"].mean()})
    out["trades per coin"] = pd.Series({k: sum(len(t) for t in v.values()) for k, v in data["trades"].items()})

    v = {}
    fall = D["ret30"] < 0
    for p in (5, 10, 30):
        below = D[f"dist{p}"] < 0
        v[f"below{p}&fall"] = below & fall
        v[f"below{p}&fall&wide"] = below & fall & (D["rngwide"] > 1)
        v[f"below{p}&fall zd<-0.5"] = below & fall & (D[f"zd{p}"] < -0.5)
        v[f"below{p}&fall&wide zd<-0.5"] = below & fall & (D["rngwide"] > 1) & (D[f"zd{p}"] < -0.5)
        v[f"below{p}&fall zd>=-0.5"] = below & fall & (D[f"zd{p}"] >= -0.5)
    v["wide&fall, not below10"] = fall & (D["rngwide"] > 1) & (D["dist10"] >= 0)
    v["wide&fall&ret10<-10%, not below10"] = fall & (D["rngwide"] > 1) & (D["dist10"] >= 0) & (D["ret10"] < -0.10)
    v["rising(ret30>0)&below10"] = (D["ret30"] >= 0) & (D["dist10"] < 0)
    out["next-day excess"] = pd.DataFrame({k: stat(m) for k, m in v.items()}).T
    out["2-day excess"] = pd.DataFrame({k: stat(v[k], "fwd2") for k in ["below10&fall", "below10&fall zd<-0.5", "below10&fall&wide zd<-0.5"]}).T

    sub = D[(D["dist10"] < 0) & fall & D["fwd1"].notna()]
    rho, p = spearmanr(-sub["zd10"], sub["fwd1"], nan_policy="omit")
    q = pd.qcut(sub["zd10"], 4, labels=False)
    out["below10&fall by zd10 quartile"] = sub.groupby(q).agg(n=("fwd1", "size"), mean_pct=("fwd1", lambda x: 100*x.mean()), zmin=("zd10", "min"), zmax=("zd10", "max"))
    out["spearman -zd10 vs fwd1 (below10&fall)"] = pd.Series({"rho": rho, "p": p, "n": len(sub)})
    sub2 = sub[sub["rngwide"] > 1]
    rho2, p2 = spearmanr(-sub2["zd10"], sub2["fwd1"], nan_policy="omit")
    out["spearman, wide only"] = pd.Series({"rho": rho2, "p": p2, "n": len(sub2)})
    out["below10&fall by window count"] = sub.groupby("win").size()
    out["below10&fall by year: mean%"] = sub.groupby(sub["ts"].dt.year)["fwd1"].agg(["size", lambda x: 100*x.mean()])
    return out
