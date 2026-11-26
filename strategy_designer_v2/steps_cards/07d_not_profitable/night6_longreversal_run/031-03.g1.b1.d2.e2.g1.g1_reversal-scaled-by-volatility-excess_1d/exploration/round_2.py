def explore(data):
    import numpy as np, pandas as pd
    coin = list(data["bars"].keys())[0]
    W = list(data["bars"][coin].keys())
    order = sorted(W, key=lambda s: int(s[1:]))
    rows = []
    for w in order:
        b = data["bars"][coin][w].copy().reset_index(drop=True)
        b["w"] = w
        b["ret1"] = b["close"].shift(-1)/b["close"] - 1
        b["ret3"] = b["close"].shift(-3)/b["close"] - 1
        r = b["close"].pct_change()
        b["r0"] = r
        b["vol30"] = r.rolling(30, min_periods=20).std()
        b["volratio"] = b["vol30"]/b["vol30"].rolling(180, min_periods=45).mean()
        b["z"] = r/b["vol30"]
        b["alloc"] = b["postRebalance_current_allocation"]
        b["turnrec"] = (b["alloc"]-b["previous_allocation"]).abs()
        b["bret"] = b["postRebalance_total_value"].shift(-1)/b["postRebalance_total_value"] - 1
        b["pos"] = np.arange(len(b))
        rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    cost = (B["alloc"]*B["ret1"] - B["bret"]).sum()/B["turnrec"].sum()
    mu = B["ret1"].mean()
    out = {"cost_per_unit_turn": cost, "mu": mu}
    B["absf"] = B["forecast"].abs()
    def sim(mask, hold=1):
        res = []
        allnet = []
        for w in order:
            b = B[B.w==w]
            p = b["alloc"].where(mask.loc[b.index], 0.0).fillna(0)
            turn = (p - p.shift(1).fillna(0)).abs()
            net = (p*b["ret1"]).fillna(0) - cost*turn
            allnet.append(net)
        n = pd.concat(allnet)
        v = (1+n).cumprod()
        dd = (v/v.cummax()-1).min()
        yr = v.iloc[-1]**(365/len(n))-1
        return pd.Series({"mean": n.mean(), "sharpe": n.mean()/n.std()*np.sqrt(365),
                          "yearly": yr, "maxdd": dd, "calmar": yr/abs(dd),
                          "share_in": (mask & B.alloc.ne(0)).mean()})
    T = pd.Series(True, index=B.index)
    vr = B["volratio"]
    sims = {"all": sim(T)}
    for k in [5, 8, 10, 12, 15]:
        sims[f"absf>={k}"] = sim(B.absf>=k)
        sims[f"long_absf>={k}"] = sim((B.absf>=k)&(B.forecast>0))
    sims["long_only"] = sim(B.forecast>0)
    sims["vr>1"] = sim(vr>1)
    sims["vr>1_absf>=8"] = sim((vr>1)&(B.absf>=8))
    sims["vr>1_long_absf>=8"] = sim((vr>1)&(B.absf>=8)&(B.forecast>0))
    out["sims"] = pd.DataFrame(sims).T.round(4)
    # condition alone check: coin next-day return by volratio tercile x signal strength/side
    B["vq"] = pd.qcut(vr, 3, labels=["lo","mid","hi"])
    B["fside"] = np.where(B.forecast>=8, "strong_long", np.where(B.forecast<=-8, "strong_short", "weak"))
    out["ret1_vq_side"] = B.pivot_table(index="fside", columns="vq", values="ret1", aggfunc="mean", observed=True).round(5)
    out["n_vq_side"] = B.pivot_table(index="fside", columns="vq", values="ret1", aggfunc="count", observed=True)
    # longer horizon: 3-day forward on non-overlapping grid by side
    G = B[B.pos % 3 == 0]
    out["ret3_side_grid"] = G.groupby("fside")["ret3"].agg(["mean","count",lambda x: x.mean()/(x.std()/np.sqrt(x.count()))])
    out["ret1_side_all"] = B.groupby("fside")["ret1"].agg(["mean","count",lambda x: x.mean()/(x.std()/np.sqrt(x.count()))])
    # weak bars: turnover share and fee share
    B["fee"] = cost*B["turnrec"]
    out["fee_by_fside"] = B.groupby("fside")[["fee"]].sum().assign(gross=B.groupby("fside").apply(lambda x:(x.alloc*x.ret1).sum()))
    return out
