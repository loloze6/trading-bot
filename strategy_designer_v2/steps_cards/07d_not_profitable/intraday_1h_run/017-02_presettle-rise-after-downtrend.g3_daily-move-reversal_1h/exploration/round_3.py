def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    G = []; Bd = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            r1 = np.log(b.close).diff()
            vol = r1.rolling(168).std(); vlong = r1.rolling(720).std()
            vr = vol / vlong
            base = (b.close / b.close.shift(24) - 1) / (vol * np.sqrt(24))
            pos = b.postRebalance_current_allocation
            gross = pos * (b.close.shift(-1) / b.close - 1)
            fee = (b.total_portfolio_value - b.postRebalance_total_value) / b.total_portfolio_value
            turn = (pos - b.previous_allocation).abs()
            Bd.append(pd.DataFrame({"vr": vr, "gross": gross, "fee": fee, "turn": turn, "ap": pos.abs()}))
            for h in [12, 24, 48]:
                fwd = b.close.shift(-h) / b.close - 1
                idx = np.arange(0, len(b) - h, h)
                G.append(pd.DataFrame({"h": h, "c": c, "base": base.iloc[idx].values, "fwd": fwd.iloc[idx].values,
                                       "vr": vr.iloc[idx].values}))
    out = {}
    B = pd.concat(Bd).dropna()
    B["vq"] = pd.qcut(B.vr, 3, labels=["calm", "mid", "hot"])
    out["per bar x24 by vol state"] = B.groupby("vq")[["gross", "fee", "turn", "ap"]].mean() * 24
    D = pd.concat(G).dropna()
    D["ex"] = D.fwd - D.groupby(["h", "c"]).fwd.transform("mean")
    D["vq"] = pd.qcut(D.vr, 3, labels=["calm", "mid", "hot"])
    r = []
    for (h, q), gp in D.groupby(["h", "vq"]):
        s = stats.linregress(-gp.base, gp.ex)
        r.append({"h": h, "vq": q, "n": len(gp), "slope": s.slope, "t": s.slope / s.stderr})
    out["slope by horizon and vol state"] = pd.DataFrame(r)
    H = D[(D.h == 24)].copy()
    H["vq5"] = pd.qcut(H.vr, 5, labels=False)
    r = []
    for q, gp in H.groupby("vq5"):
        s = stats.linregress(-gp.base, gp.ex)
        r.append({"vq5": q, "vr": gp.vr.mean(), "n": len(gp), "slope": s.slope, "t": s.slope / s.stderr})
    out["24h slope by vol ratio quintile"] = pd.DataFrame(r)
    return out
