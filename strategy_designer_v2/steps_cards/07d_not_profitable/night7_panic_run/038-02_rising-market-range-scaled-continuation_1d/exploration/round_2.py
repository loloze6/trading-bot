def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["bars"].keys())
    COL = "debug_info.components.scaled_rise.last_history_value"
    rows = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r = cl.pct_change()
            a = b["postRebalance_current_allocation"].fillna(0)
            f = b["forecast"].fillna(0)
            rng = (b["high"] - b["low"]) / b["close"]
            vol10 = r.rolling(10).std(); vol60 = r.rolling(60).std()
            inprof = (b["regime"].astype(str) == "unknown")
            bv = b["postRebalance_total_value"]
            dfc = pd.DataFrame(dict(
                coin=c, w=w, pos=np.arange(len(b)), a=a, f=f,
                gain=a * (cl.shift(-1) / cl - 1),
                bret=bv / bv.shift(1) - 1,
                vr=vol10 / vol60, r1=r, r3=cl / cl.shift(3) - 1,
                r10=cl / cl.shift(10) - 1,
                hi20=cl / cl.rolling(20).max() - 1,
                rngr=rng / rng.rolling(30).mean(),
                fwd3=cl.shift(-3) / cl - 1, inprof=inprof,
                y=pd.to_datetime(b["timestamp"]).dt.year))
            rows.append(dfc)
    B = pd.concat(rows, ignore_index=True)
    out["share in profile / held"] = pd.Series({"inprof": B.inprof.mean(), "held": (B.a > 0).mean()})

    def calmar(ret_col):
        ch = []
        for w in sorted(B.w.unique(), key=lambda s: int(s[1:])):
            s = B[B.w == w].groupby("pos")[ret_col].mean().dropna()
            ch.append(s)
        s = pd.concat(ch, ignore_index=True)
        v = (1 + s).cumprod()
        dd = (v / v.cummax() - 1).min()
        yr = v.iloc[-1] ** (365 / len(s)) - 1
        sh = s.mean() / s.std() * np.sqrt(365)
        return pd.Series({"yearly": yr, "maxdd": dd, "calmar": yr / -dd, "sharpe": sh})

    # filtered books: zero the next bar's return when the previous bar's condition holds
    B["prev_vr"] = B.groupby(["coin", "w"])["vr"].shift(1)
    B["prev_hi20"] = B.groupby(["coin", "w"])["hi20"].shift(1)
    B["prev_r1"] = B.groupby(["coin", "w"])["r1"].shift(1)
    B["prev_rngr"] = B.groupby(["coin", "w"])["rngr"].shift(1)
    B["prev_f"] = B.groupby(["coin", "w"])["f"].shift(1)
    res = {"base": calmar("bret")}
    vq = B.loc[B.a > 0, "vr"].quantile([0.5, 0.75])
    for name, cond in {
        "out when vr>q75": B.prev_vr > vq[0.75],
        "out when vr>q50": B.prev_vr > vq[0.5],
        "out when rngr>1.5": B.prev_rngr > 1.5,
        "out when r1<-0.03": B.prev_r1 < -0.03,
        "out when f>15": B.prev_f > 15,
    }.items():
        B["tmp"] = np.where(cond.fillna(False), 0.0, B.bret)
        B.loc[B.bret.isna(), "tmp"] = np.nan
        res[name] = calmar("tmp")
    B["half"] = np.where(B.prev_vr > vq[0.5], 0.5 * B.bret, B.bret)
    res["half size when vr>q50"] = calmar("half")
    out["filtered books"] = pd.DataFrame(res).T

    held = B[B.a > 0].copy()
    for k in ["vr", "rngr", "r3", "f", "hi20"]:
        held["q"] = pd.qcut(held[k], 4, labels=False, duplicates="drop")
        g = held.groupby("q")["gain"]
        out["held gain by " + k + " quartile"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "std": g.std(),
                                                             "p5": g.quantile(0.05), "lo": held.groupby("q")[k].min()})
    out["held gain by year"] = held.groupby("y")["gain"].agg(["size", "mean", "std", "min"])

    # grid: signal vs condition alone (in profile)
    G = B[(B.pos % 3 == 0)].copy()
    drift = G.groupby("coin")["fwd3"].mean()
    G["ex"] = G.fwd3 - G.coin.map(drift)
    Gp = G[G.inprof].copy()
    Gp["sig"] = Gp.f > 0
    Gp["hvr"] = Gp.vr > vq[0.5]
    g = Gp.groupby(["hvr", "sig"])["ex"]
    out["grid ex3: high vr x signal"] = pd.DataFrame({"n": g.size(), "mean": g.mean(),
                                                      "t": g.mean() / (g.std() / np.sqrt(g.size())), "std": g.std()})
    Gs = Gp[Gp.sig].copy()
    Gs["fq"] = pd.qcut(Gs.f, 4, labels=False, duplicates="drop")
    g = Gs.groupby("fq")["ex"]
    out["grid ex3 by forecast quartile"] = pd.DataFrame({"n": g.size(), "mean": g.mean(), "std": g.std(),
                                                         "t": g.mean() / (g.std() / np.sqrt(g.size()))})
    return out
