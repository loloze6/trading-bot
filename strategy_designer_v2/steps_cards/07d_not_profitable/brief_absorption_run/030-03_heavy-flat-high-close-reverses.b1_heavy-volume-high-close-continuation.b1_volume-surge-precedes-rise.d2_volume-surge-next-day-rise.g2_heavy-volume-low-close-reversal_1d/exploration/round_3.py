def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    cost = 0.0019
    F = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            b["r1"] = b.close.shift(-1) / b.close - 1
            b["dayret"] = b.close / b.close.shift(1) - 1
            b["vol20"] = b.dayret.rolling(20).std()
            b["dayz"] = b.dayret / b.vol20.shift(1)
            b["ret60"] = b.close / b.close.shift(60) - 1
            b["ret5"] = b.close / b.close.shift(5) - 1
            b["vr"] = b.volume / b.volume.shift(1).rolling(20).mean()
            b["volrank"] = b.vol20.rolling(120, min_periods=60).rank(pct=True)
            b["alloc"] = b.postRebalance_current_allocation
            b["day"] = pd.to_datetime(b.timestamp).dt.floor("D")
            b["coin"] = c; b["wi"] = int(w[1:])
            F.append(b)
    F = pd.concat(F, ignore_index=True)
    mu = F.groupby("coin").r1.mean()
    F["ex"] = F.r1 - F.coin.map(mu)
    F = F.dropna(subset=["r1"])
    def sim(mask, scale=None):
        G = F.copy()
        a = G.alloc.where(mask(G), 0.0) if mask is not None else G.alloc
        if scale is not None: a = a * scale(G)
        G["a"] = a.fillna(0).clip(upper=2)
        G["ch"] = G.groupby(["coin", "wi"]).a.diff().abs().fillna(G.a.abs())
        G["net"] = G.a * G.r1 - G.ch * cost / 2
        r = G.groupby(["wi", "day"]).net.mean().reset_index().sort_values(["wi", "day"]).net
        vv = (1 + r).cumprod(); mdd = (vv / vv.cummax() - 1).min()
        yr = vv.iloc[-1] ** (365 / len(r)) - 1
        return [r.mean() / r.std() * np.sqrt(365), yr, mdd, yr / -mdd, (G.a > 0).mean()]
    res = {}
    res["base"] = sim(None)
    res["fc>10"] = sim(lambda G: G.forecast > 10)
    res["fc>10_dayz<0"] = sim(lambda G: (G.forecast > 10) & (G.dayz < 0))
    res["fc>10_dayz<-1"] = sim(lambda G: (G.forecast > 10) & (G.dayz < -1))
    res["fc>10_ret5<0"] = sim(lambda G: (G.forecast > 10) & (G.ret5 < 0))
    res["fc>10_ret60>0"] = sim(lambda G: (G.forecast > 10) & (G.ret60 > 0))
    res["fc>10_ret60<0"] = sim(lambda G: (G.forecast > 10) & (G.ret60 < 0))
    res["fc>10_volrank>.5"] = sim(lambda G: (G.forecast > 10) & (G.volrank > 0.5))
    res["fc>15"] = sim(lambda G: G.forecast > 15)
    res["fc>10_vr>1.5"] = sim(lambda G: (G.forecast > 10) & (G.vr > 1.5))
    out["variants"] = pd.DataFrame(res, index=["sharpe", "yearly", "mdd", "calmar", "share_in"]).T
    # condition alone: down day, no signal vs signal
    T = F.dropna(subset=["dayz"]).copy()
    T["down"] = (T.dayz < -1).astype(int); T["sig"] = (T.forecast > 10).astype(int)
    out["down_x_sig"] = T.groupby(["down", "sig"]).agg(ex=("ex", "mean"), r1=("r1", "mean"), n=("ex", "size"))
    T2 = F.dropna(subset=["vr", "dayz"]).copy()
    T2 = T2[T2.forecast > 10]
    T2["vrq"] = pd.qcut(T2.vr, 4, labels=False)
    out["vr_in_signals"] = T2.groupby("vrq").agg(vr=("vr", "mean"), ex=("ex", "mean"), sdex=("ex", "std"), n=("ex", "size"))
    T3 = F.dropna(subset=["ret60"]).copy(); T3["sig"] = (T3.forecast > 10).astype(int); T3["up60"] = (T3.ret60 > 0).astype(int)
    out["ret60_x_sig"] = T3.groupby(["up60", "sig"]).agg(ex=("ex", "mean"), n=("ex", "size"))
    # 2-day horizon on signals, non-overlap approx: r2
    return out
