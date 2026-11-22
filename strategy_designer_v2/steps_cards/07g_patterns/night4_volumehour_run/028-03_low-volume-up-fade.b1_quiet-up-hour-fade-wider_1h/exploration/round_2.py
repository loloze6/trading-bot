def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    G = []; H = []
    for coin, wins in bars.items():
        tmp = []; htmp = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            mar = r1.abs().rolling(720, min_periods=120).mean()
            r24 = c / c.shift(24) - 1
            s24 = r24 / (mar * np.sqrt(24))
            volreg = r1.abs().rolling(24).mean() / mar
            ts = pd.to_datetime(df["timestamp"])
            g = pd.DataFrame({"coin": coin, "w": w, "year": ts.dt.year, "s24": s24, "volreg": volreg,
                              "f24": c.shift(-24) / c - 1, "f12": c.shift(-12) / c - 1,
                              "f48": c.shift(-48) / c - 1, "pos": np.arange(len(df))})
            tmp.append(g)
            htmp.append(pd.DataFrame({"coin": coin, "year": ts.dt.year, "hour": ts.dt.hour,
                                      "f1": c.shift(-1) / c - 1}))
        g = pd.concat(tmp)
        for h, col in [(12, "f12"), (24, "f24"), (48, "f48")]:
            gg = g[g["pos"] % h == 0].dropna(subset=[col])
            d = gg[col].mean()
            gg = gg.assign(h=h, raw=gg[col], unus=gg[col] - d, sd=gg[col].std())
            G.append(gg[["coin", "w", "year", "s24", "volreg", "h", "raw", "unus", "sd"]])
        hh = pd.concat(htmp).dropna(subset=["f1"])
        H.append(hh.assign(u=hh["f1"] - hh["f1"].mean()))
    G = pd.concat(G); H = pd.concat(H)
    def summ(df, col, by):
        x = df.dropna(subset=[col] + by)
        a = x.groupby(by, observed=True)[col].agg(["mean", "std", "count"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        a["mean"] = a["mean"] * 100
        return a.drop(columns="std").round(4)
    G = G.dropna(subset=["s24", "volreg"])
    G["s24b"] = pd.cut(G["s24"], [-np.inf, -3, -1.5, -0.5, 0.5, 1.5, 3, np.inf])
    G["hv"] = np.where(G["volreg"] > 1.189, "hi", "lo")
    out = {}
    out["unusual % by s24 and horizon, high vol"] = summ(G[G.hv == "hi"], "unus", ["h", "s24b"])
    out["raw % by s24, h24, all"] = summ(G[G.h == 24], "raw", ["s24b"])
    F = G[(G.h == 24) & (G.s24 < -1.5)]
    out["falls<-1.5 h24 unusual % by year"] = summ(F, "unus", ["year"])
    out["falls<-1.5 h24 unusual % by coin"] = summ(F, "unus", ["coin"])
    out["falls<-1.5 h24 unusual % by vol"] = summ(F, "unus", ["hv"])
    x = G[G.h == 24]
    out["corr s24 vs unus/sd, hi vs lo vol"] = x.groupby("hv").apply(
        lambda a: pd.Series({"corr": np.corrcoef(a["s24"], a["unus"] / a["sd"])[0, 1], "n": len(a)})).round(4)
    out["h20-21 unusual 1h % by year"] = summ(H[H.hour.isin([20, 21])], "u", ["year"])
    out["h20-21 unusual 1h % by coin"] = summ(H[H.hour.isin([20, 21])], "u", ["coin"])
    out["h13 unusual 1h % by year"] = summ(H[H.hour == 13], "u", ["year"])
    return out
