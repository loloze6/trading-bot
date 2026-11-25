def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    drift = {}
    for coin, wins in bars.items():
        g = {h: [] for h in (5, 10, 20)}
        for w, df in wins.items():
            c = df["close"].values
            for h in g:
                for i in range(0, len(c) - h, h):
                    g[h].append(c[i + h] / c[i] - 1)
        drift[coin] = {h: (np.mean(v), np.std(v)) for h, v in g.items()}
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            lr = c.pct_change()
            vol20 = lr.rolling(20).std()
            z5 = (c / c.shift(5) - 1) / vol20
            r20 = c / c.shift(20) - 1
            z20 = r20 / (vol20 * np.sqrt(20))
            n = len(df)
            for i in range(n):
                d = dict(coin=coin, win=w, pos=i, day=pd.Timestamp(df["timestamp"].iloc[i]).floor("D"),
                         regime=df["regime"].iloc[i], fc=df["forecast"].iloc[i],
                         z5=z5.iloc[i], z20=z20.iloc[i], r20=r20.iloc[i])
                for h in (5, 10, 20):
                    d[f"f{h}"] = c.iloc[i + h] / c.iloc[i] - 1 if i + h < n else np.nan
                rows.append(d)
    R = pd.DataFrame(rows)

    def tday(d, col):
        d = d.dropna(subset=[col])
        if len(d) < 5:
            return pd.Series(dict(n=len(d), mean=d[col].mean(), med=d[col].median(), t=np.nan, days=d.day.nunique()))
        m = d[col].mean()
        s = (d[col] - m).groupby(d.day).sum()
        D = len(s)
        se = np.sqrt((s ** 2).sum() * D / (D - 1)) / len(d)
        return pd.Series(dict(n=len(d), mean=m, med=d[col].median(), t=m / se, days=D))

    out = {}
    for h in (5, 10, 20):
        G = R[(R.pos % h == 0) & R[f"f{h}"].notna() & R.z20.notna()].copy()
        G["u"] = -(G[f"f{h}"] - G.coin.map(lambda k: drift[k][h][0]))
        G["u_strength"] = G.u / G.coin.map(lambda k: drift[k][h][1])
        G["prof"] = np.where(G.regime == "chop", "out", "choppy")
        Gc = G[G.prof == "choppy"].copy()
        Gc["z20b"] = pd.cut(Gc.z20, [-99, -2, -1, -0.5, 0, 0.5, 1, 99])
        out[f"h{h}_choppy_by_z20bin"] = Gc.groupby("z20b").apply(lambda d: tday(d, "u"))
        Go = G[G.prof == "out"].copy()
        Go["z20b"] = pd.cut(Go.z20, [-99, -2, -1, -0.5, 0, 0.5, 1, 99])
        out[f"h{h}_outside_by_z20bin"] = Go.groupby("z20b").apply(lambda d: tday(d, "u"))
        Gf = Gc[Gc.r20 < 0]
        sl = np.polyfit(-Gf.z20, Gf.u, 1)[0] if len(Gf) > 5 else np.nan
        out[f"h{h}_choppy_r20neg"] = pd.concat([tday(Gf, "u"), pd.Series(dict(slope_on_fallsize=sl,
                strength=Gf.u_strength.mean()))])
        out[f"h{h}_choppy_r20neg_by_win"] = Gf.groupby("win").apply(lambda d: tday(d, "u"))
        out[f"h{h}_choppy_r20neg_no_w16"] = tday(Gf[Gf.win != "w16"], "u")
    return out
