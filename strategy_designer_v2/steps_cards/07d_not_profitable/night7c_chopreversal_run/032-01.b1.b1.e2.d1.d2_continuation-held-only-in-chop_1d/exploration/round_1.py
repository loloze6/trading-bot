def explore(data):
    import numpy as np, pandas as pd
    out = {}
    H = 7
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            net = (c - c.shift(30)).abs()
            path = c.diff().abs().rolling(30).sum()
            er = net / path
            sd30 = r1.rolling(30).std()
            r7 = c / c.shift(7) - 1
            r30 = c / c.shift(30) - 1
            sd90 = r1.rolling(90, min_periods=60).std()
            volratio = sd30 / sd90
            fc = b["forecast"].astype(float)
            pos = b["postRebalance_current_allocation"].astype(float)
            fwd = c.shift(-H) / c - 1
            for i in range(0, len(b) - H, H):
                rows.append(dict(coin=coin, w=w, fc=fc[i], fwd=fwd[i], er=er[i], z=r7[i] / (sd30[i] * np.sqrt(7)) if sd30[i] > 0 else np.nan,
                                 r30=r30[i], vr=volratio[i], sd30=sd30[i], pos=pos[i]))
            g = pos.shift(1) * r1
            ts = pd.to_datetime(b["timestamp"])
            daily.append(pd.DataFrame(dict(coin=coin, w=w, day=ts.dt.floor("D"), g=g, pos=pos.shift(1), r1=r1,
                                           year=ts.dt.year)))
    G = pd.DataFrame(rows)
    mu = G.groupby("coin")["fwd"].mean()
    G["dm"] = G["fwd"] - G["coin"].map(mu)
    A = G[G.fc != 0].dropna(subset=["fwd"]).copy()
    A["s"] = np.sign(A.fc)
    A["sr"] = A.s * A.fwd
    A["sdm"] = A.s * A.dm
    def summ(df, key):
        t = df.groupby(key, observed=True).agg(n=("sr", "size"), total=("sr", "mean"), unusual=("sdm", "mean"),
                                 sd=("sr", "std"))
        t["t"] = t.unusual / (t.sd / np.sqrt(t.n))
        return t.round(4)
    A["absfc_q"] = pd.qcut(A.fc.abs(), 4, labels=False)
    out["by |forecast| quartile"] = summ(A, "absfc_q")
    A["absz_q"] = pd.qcut(A.z.abs(), 4, labels=False)
    out["by |raw scaled z| quartile"] = summ(A, "absz_q")
    A["side"] = np.where(A.s > 0, "long", "short")
    out["by side"] = summ(A, "side")
    A["er_b"] = pd.cut(A.er, [0, 0.1, 0.2, 0.3, 1])
    out["by ER bucket"] = summ(A, "er_b")
    A["vr_q"] = pd.qcut(A.vr, 3, labels=False)
    out["by vol ratio 30/90 tercile"] = summ(A, "vr_q")
    A["agree30"] = np.where(np.sign(A.r30) == A.s, "with30", "against30")
    out["by side vs 30d move"] = summ(A, "agree30")
    out["by window"] = summ(A, "w")
    out["by coin"] = summ(A, "coin")
    # sign agreement fc vs z
    out["share fc sign == z sign"] = float((np.sign(A.fc) == np.sign(A.z)).mean())
    # non-chop bars: same z continuation?
    N = G[(G.er > 0.3)].dropna(subset=["fwd", "z"]).copy()
    N["s"] = np.sign(N.z); N["sdm"] = N.s * N.dm
    out["nonchop z-continuation unusual mean, n"] = f"{N.sdm.mean():.4f}, {len(N)}"
    # book daily
    D = pd.concat(daily).dropna(subset=["g"])
    bd = D.groupby(["w", "day"]).agg(g=("g", "mean"), r=("r1", "mean")).reset_index()
    bd["wn"] = bd.w.str[1:].astype(int)
    bd = bd.sort_values(["wn", "day"])
    eq = (1 + bd.g).cumprod()
    dd = eq / eq.cummax() - 1
    bd["dd"] = dd.values
    out["deepest fall (gross, chained)"] = float(dd.min())
    # deepest-fall per window
    out["per window: gross mean, sd, min dd within, coin mean"] = bd.groupby("wn").apply(
        lambda x: pd.Series(dict(g=x.g.mean(), sd=x.g.std(), r=x.r.mean(),
                                 dd=((1 + x.g).cumprod() / (1 + x.g).cumprod().cummax() - 1).min()))).round(4)
    D["side"] = np.where(D.pos > 0, "long", np.where(D.pos < 0, "short", "flat"))
    out["daily gross by side"] = D.groupby("side").agg(n=("g", "size"), mean=("g", "mean"), sd=("g", "std")).round(5)
    out["mean |pos|"] = float(D.pos.abs().mean())
    return out
