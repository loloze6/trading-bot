def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["bars"].keys())
    rows = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r = cl.pct_change()
            a = b["postRebalance_current_allocation"].fillna(0)
            f = b["forecast"].fillna(0)
            bv = b["postRebalance_total_value"]
            dfc = pd.DataFrame(dict(
                coin=c, w=w, pos=np.arange(len(b)), a=a, f=f,
                gain=a * (cl.shift(-1) / cl - 1),
                bret=bv / bv.shift(1) - 1, r1=r,
                hi20=cl / cl.rolling(20).max() - 1,
                r10=cl / cl.shift(10) - 1,
                fwd3=cl.shift(-3) / cl - 1,
                inprof=(b["regime"].astype(str) == "unknown"),
                y=pd.to_datetime(b["timestamp"]).dt.year))
            rows.append(dfc)
    B = pd.concat(rows, ignore_index=True)
    grp = B.groupby(["coin", "w"])
    for k in ["f", "hi20", "r1", "a"]:
        B["prev_" + k] = grp[k].shift(1)

    def calmar(col):
        ch = []
        for w in sorted(B.w.unique(), key=lambda s: int(s[1:])):
            ch.append(B[B.w == w].groupby("pos")[col].mean().dropna())
        s = pd.concat(ch, ignore_index=True)
        v = (1 + s).cumprod()
        dd = (v / v.cummax() - 1)
        yr = v.iloc[-1] ** (365 / len(s)) - 1
        return pd.Series({"yearly": yr, "maxdd": dd.min(), "calmar": yr / -dd.min(),
                          "sharpe": s.mean() / s.std() * np.sqrt(365)})

    res = {"base": calmar("bret")}
    held_f = B.loc[B.a > 0, "f"]
    fq = held_f.quantile([0.25, 0.5])
    conds = {
        "out when prev f < q25 held": (B.prev_f < fq[0.25]) & (B.prev_a > 0),
        "out when prev f < q50 held": (B.prev_f < fq[0.5]) & (B.prev_a > 0),
        "out when prev f == 0": (B.prev_f <= 0),
        "out when hi20 < -0.10": B.prev_hi20 < -0.10,
        "out when hi20 < -0.05": B.prev_hi20 < -0.05,
    }
    for name, cond in conds.items():
        B["tmp"] = np.where(cond.fillna(False), 0.0, B.bret)
        B.loc[B.bret.isna(), "tmp"] = np.nan
        res[name] = calmar("tmp")
    # double size weight on strong forecasts: scale by prev_f/10 relative
    out["filtered books"] = pd.DataFrame(res).T
    out["prev f quantiles of held"] = fq

    # grid check: hi20 condition with and without signal, in profile
    G = B[B.pos % 3 == 0].copy()
    drift = G.groupby("coin")["fwd3"].mean()
    G["ex"] = G.fwd3 - G.coin.map(drift)
    Gp = G[G.inprof].copy()
    Gp["sig"] = Gp.f > 0
    Gp["near_hi"] = Gp.hi20 >= -0.05
    g = Gp.groupby(["near_hi", "sig"])["ex"]
    out["grid ex3: near 20d high x signal"] = pd.DataFrame({"n": g.size(), "mean": g.mean(),
        "t": g.mean() / (g.std() / np.sqrt(g.size()))})
    # signal strength graded within near_hi
    Gs = Gp[Gp.sig].copy()
    Gs["fq"] = pd.qcut(Gs.f, 2, labels=False, duplicates="drop")
    g = Gs.groupby(["near_hi", "fq"])["ex"]
    out["grid ex3 signal: near_hi x forecast half"] = pd.DataFrame({"n": g.size(), "mean": g.mean(),
        "t": g.mean() / (g.std() / np.sqrt(g.size()))})
    # falls: daily book days in the worst 5% of book days - what was held
    held = B[B.a > 0].copy()
    held["weakf"] = held.f < fq[0.5]
    g = held.groupby("weakf")["gain"]
    out["held gain weak vs strong forecast"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "std": g.std(),
        "p5": g.quantile(0.05), "sum": g.sum()})
    g = held.groupby(["y", "weakf"])["gain"]
    out["held gain by year x weak"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "sum": g.sum()})
    return out
