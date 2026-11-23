def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    cost = 0.0019
    F = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            rng = (b.high - b.low).replace(0, np.nan)
            b["cl"] = (b.high - b.close) / rng
            b["vr"] = b.volume / b.volume.shift(1).rolling(20).mean()
            b["r1"] = b.close.shift(-1) / b.close - 1
            b["dayret"] = b.close / b.close.shift(1) - 1
            b["ret20"] = b.close / b.close.shift(20) - 1
            b["ma50"] = b.close.rolling(50, min_periods=50).mean()
            b["below50"] = np.where(b.ma50.isna(), np.nan, (b.close < b.ma50).astype(float))
            b["vol20"] = b.dayret.rolling(20).std()
            b["dayz"] = b.dayret / b.vol20.shift(1)
            b["alloc"] = b.postRebalance_current_allocation
            b["prevfc"] = b.forecast.shift(1)
            b["day"] = pd.to_datetime(b.timestamp).dt.floor("D")
            b["coin"] = c; b["wi"] = int(w[1:])
            F.append(b)
    F = pd.concat(F, ignore_index=True)
    mu = F.groupby("coin").r1.mean()
    F["ex"] = F.r1 - F.coin.map(mu)
    F = F.dropna(subset=["r1"])
    F["gain"] = F.alloc * F.r1
    # book drawdown windows: worst days
    Bk = F.groupby(["wi", "day"]).agg(g=("gain", "mean"), a=("alloc", "mean"), cr=("r1", "mean")).reset_index().sort_values(["wi", "day"])
    v = (1 + Bk.g).cumprod(); Bk["dd"] = (v / v.cummax() - 1).values
    Bk["indd"] = (Bk.dd < -0.15).astype(int)
    out["dd_state"] = Bk.groupby("indd").agg(g=("g", "mean"), a=("a", "mean"), cr=("cr", "mean"), n=("g", "size"))
    F = F.merge(Bk[["wi", "day", "indd"]], on=["wi", "day"], how="left")
    S = F[F.forecast > 10]
    out["sig_in_dd"] = S.groupby("indd").agg(ex=("ex", "mean"), gain=("gain", "mean"), dayz=("dayz", "mean"), ret20=("ret20", "mean"), below50=("below50", "mean"), vol20=("vol20", "mean"), n=("ex", "size"))
    # signal day's own return (z) : crash days vs flat days
    S2 = F.dropna(subset=["dayz"]).copy()
    S2["zq"] = pd.cut(S2.dayz, [-99, -2, -1, -0.3, 0.3, 1, 99])
    S2["sig"] = (S2.forecast > 10).astype(int)
    out["dayz_x_sig"] = S2.groupby(["zq", "sig"]).agg(ex=("ex", "mean"), sdex=("ex", "std"), gain=("gain", "mean"), sdgain=("gain", "std"), n=("ex", "size"))
    # repeated signals (previous day also signal)
    S3 = F[F.forecast > 10].copy()
    S3["rep"] = (S3.prevfc > 10).astype(int)
    out["repeat"] = S3.groupby("rep").agg(ex=("ex", "mean"), sdex=("ex", "std"), gain=("gain", "mean"), n=("ex", "size"))
    # simulated variants
    def sim(mask, name, scale=None):
        G = F.copy()
        a = G.alloc.where(mask(G), 0.0) if mask is not None else G.alloc
        if scale is not None: a = a * scale(G)
        G["a"] = a.fillna(0)
        G["ch"] = G.groupby(["coin", "wi"]).a.diff().abs().fillna(G.a.abs())
        G["net"] = G.a * G.r1 - G.ch * cost / 2
        Bv = G.groupby(["wi", "day"]).net.mean().reset_index().sort_values(["wi", "day"])
        r = Bv.net
        vv = (1 + r).cumprod(); mdd = (vv / vv.cummax() - 1).min()
        yr = vv.iloc[-1] ** (365 / len(r)) - 1
        return [r.mean() / r.std() * np.sqrt(365), yr, mdd, yr / -mdd, (G.a > 0).mean()]
    res = {}
    res["base"] = sim(None, "base")
    res["below50_only"] = sim(lambda G: G.below50 == 1, "b")
    res["not_above50"] = sim(lambda G: G.below50 != 0, "b")
    res["dayz>-2"] = sim(lambda G: G.dayz > -2, "z")
    res["dayz>-1"] = sim(lambda G: G.dayz > -1, "z")
    res["dayz_abs<1"] = sim(lambda G: G.dayz.abs() < 1, "z")
    res["fc>10"] = sim(lambda G: G.forecast > 10, "f")
    res["half_size"] = sim(None, "h", scale=lambda G: 0.5)
    out["variants"] = pd.DataFrame(res, index=["sharpe", "yearly", "mdd", "calmar", "share_in"]).T
    # condition alone check for below50 and dayz
    out["cond_alone_below50"] = F.dropna(subset=["below50"]).assign(sig=lambda x: (x.forecast > 10).astype(int)).groupby(["below50", "sig"]).agg(ex=("ex", "mean"), n=("ex", "size"))
    return out
