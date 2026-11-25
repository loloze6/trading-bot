import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allr = []
        for w, b in wins.items():
            allr.append(b["close"].pct_change())
        drift = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c, h, l = b["close"], b["high"], b["low"]
            d = pd.DataFrame({"coin": coin, "win": w, "ts": b["timestamp"]})
            d["fwd1"] = c.shift(-1)/c - 1 - drift
            d["fwd3"] = c.shift(-3)/c - 1 - 3*drift
            d["ret30"] = c/c.shift(30) - 1
            d["ret1"] = c/c.shift(1) - 1
            rng = (h - l)/c
            d["rngratio_today"] = rng/rng.shift(1).rolling(30).mean()
            d["rng30_vs_win"] = rng.rolling(30).mean()/rng.expanding(60).mean()
            for p in (10, 20, 30, 60):
                pl = l.shift(1).rolling(p).min()
                d[f"dist{p}"] = c/pl - 1
            d["mr"] = (b["regime"] == "mean_reversion")
            d["case"] = d["mr"] & (b["forecast"] > 0)
            d["pos"] = b["postRebalance_current_allocation"].abs() > 1e-9
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
    v = {}
    v["recorded cases"] = D["case"]
    v["regime mr"] = D["mr"]
    v["all bars"] = D["fwd1"].notna()
    v["below30"] = D["dist30"] < 0
    v["below30 & ret30<0"] = (D["dist30"] < 0) & (D["ret30"] < 0)
    v["below30 & rng30 wide(win)"] = (D["dist30"] < 0) & (D["rng30_vs_win"] > 1)
    v["below30 & ret30<0 & rngwide"] = (D["dist30"] < 0) & (D["ret30"] < 0) & (D["rng30_vs_win"] > 1)
    v["below20 & ret30<0"] = (D["dist20"] < 0) & (D["ret30"] < 0)
    v["below10 & ret30<0"] = (D["dist10"] < 0) & (D["ret30"] < 0)
    v["below60 & ret30<0"] = (D["dist60"] < 0) & (D["ret30"] < 0)
    v["below30 & ret30<0 & today range>1.5x"] = (D["dist30"] < 0) & (D["ret30"] < 0) & (D["rngratio_today"] > 1.5)
    v["below30 deep<-3%"] = D["dist30"] < -0.03
    v["below30 shallow 0..-3%"] = (D["dist30"] < 0) & (D["dist30"] >= -0.03)
    v["ret30<0 & rngwide, NOT below30"] = (D["dist30"] >= 0) & (D["ret30"] < 0) & (D["rng30_vs_win"] > 1)
    v["ret1<-5% not below30"] = (D["ret1"] < -0.05) & (D["dist30"] >= 0)
    v["ret1<-5% & below30"] = (D["ret1"] < -0.05) & (D["dist30"] < 0)
    out["next-day excess by situation"] = pd.DataFrame({k: stat(m) for k, m in v.items()}).T
    out["3-day excess by situation"] = pd.DataFrame({k: stat(m, "fwd3") for k in ["recorded cases", "below30", "below30 & ret30<0", "below20 & ret30<0"] for m in [v[k]]}).T
    # depth grading among ret30<0 & below10
    sub = D[(D["dist10"] < 0) & (D["ret30"] < 0) & D["fwd1"].notna()].copy()
    sub["q"] = pd.qcut(sub["dist10"], 4, labels=False)
    out["below10&ret30<0 by depth quartile"] = sub.groupby("q").agg(n=("fwd1", "size"), mean_pct=("fwd1", lambda x: 100*x.mean()), mind=("dist10", "min"), maxd=("dist10", "max"))
    out["cases by coin"] = D[D["case"]].groupby("coin").size()
    out["cases by window"] = D[D["case"]].groupby("win").size()
    out["mr bars vs cases"] = pd.Series({"mr": int(D["mr"].sum()), "cases": int(D["case"].sum()), "pos bars": int(D["pos"].sum()), "below30&ret30<0": int(v["below30 & ret30<0"].sum())})
    return out
