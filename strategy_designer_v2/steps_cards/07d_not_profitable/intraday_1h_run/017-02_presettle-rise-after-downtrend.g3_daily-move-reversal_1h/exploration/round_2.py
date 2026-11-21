def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    G = []; fees = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            r1 = np.log(b.close).diff()
            vol = r1.rolling(168).std()
            vlong = r1.rolling(720).std()
            base = (b.close / b.close.shift(24) - 1) / (vol * np.sqrt(24))
            f = b.forecast
            fwd = b.close.shift(-24) / b.close - 1
            idx = np.arange(0, len(b) - 24, 24)
            G.append(pd.DataFrame({"c": c, "f": f.iloc[idx].values, "base": base.iloc[idx].values,
                                   "fwd": fwd.iloc[idx].values, "vr": (vol / vlong).iloc[idx].values,
                                   "vol": vol.iloc[idx].values}))
            turn = (b.postRebalance_current_allocation - b.previous_allocation).abs()
            fee = (b.total_portfolio_value - b.postRebalance_total_value) / b.total_portfolio_value
            fees.append(pd.DataFrame({"turn": turn, "fee": fee}))
    D = pd.concat(G).dropna()
    D["ex"] = D.fwd - D.groupby("c").fwd.transform("mean")
    D["exv"] = D.ex / (D.vol * np.sqrt(24))
    out = {}
    F = pd.concat(fees).dropna()
    out["fee per unit turnover"] = F.fee.sum() / F.turn.sum()
    D["bq"] = pd.qcut(D.base, 10, labels=False)
    out["24h excess fwd by raw base decile"] = D.groupby("bq").agg(base=("base", "mean"), ex=("ex", "mean"),
        exv=("exv", "mean"), n=("ex", "size"))
    D["fq"] = pd.qcut(D.f, 10, labels=False, duplicates="drop")
    out["24h excess fwd by forecast decile"] = D.groupby("fq").agg(f=("f", "mean"), ex=("ex", "mean"), n=("ex", "size"))
    res = []
    for nm, x in [("base", -D.base), ("forecast", D.f)]:
        s = stats.linregress(x, D.ex); res.append({"x": nm, "slope": s.slope, "t": s.slope / s.stderr, "r": s.rvalue})
    out["slope neg base vs forecast"] = pd.DataFrame(res)
    D["vq"] = pd.qcut(D.vr, 3, labels=["calm", "mid", "hot"])
    r2 = []
    for q, gp in D.groupby("vq"):
        s = stats.linregress(-gp.base, gp.ex)
        r2.append({"vq": q, "n": len(gp), "slope": s.slope, "t": s.slope / s.stderr,
                   "top_minus_bottom_decile": gp.ex[gp.base < gp.base.quantile(.1)].mean() - gp.ex[gp.base > gp.base.quantile(.9)].mean()})
    out["reversal by vol ratio (168h vol/720h vol)"] = pd.DataFrame(r2)
    r3 = []
    for c, gp in D.groupby("c"):
        s = stats.linregress(-gp.base, gp.ex); r3.append({"c": c, "slope": s.slope, "t": s.slope / s.stderr})
    out["per coin slope neg base"] = pd.DataFrame(r3)
    return out
