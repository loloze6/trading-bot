def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    def rsi(c, n=14):
        d = c.diff()
        up = d.clip(lower=0).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
        dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
        return 100 - 100/(1+up/dn)
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            c = df["close"].reset_index(drop=True)
            r = rsi(c)
            fc = df["forecast"].reset_index(drop=True)
            r60 = c / c.shift(60) - 1
            ma = c.rolling(50, min_periods=30).mean()
            for h in [5, 10]:
                idx = np.arange(0, len(c) - h, h)
                fr = (c.shift(-h) / c - 1).iloc[idx]
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "rsi": r.iloc[idx].values,
                                          "fc": fc.iloc[idx].values, "fr": fr.values,
                                          "r60": r60.iloc[idx].values,
                                          "abovema": (c > ma).iloc[idx].values & ma.iloc[idx].notna().values}))
    D = pd.concat(rows)
    D["ex"] = D["fr"] - D.groupby(["coin", "h"])["fr"].transform("mean")
    D = D.dropna(subset=["rsi", "ex", "r60"])
    D["reg"] = np.where(D["r60"] > 0, "up60", "down60")
    D["b"] = pd.cut(D["rsi"], [0, 30, 40, 50, 60, 70, 100])
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["h_reg_bucket"] = D.groupby(["h", "reg", "b"])["ex"].apply(tt).unstack()
    cor = []
    for (h, reg), g in D.groupby(["h", "reg"]):
        rho, p = stats.spearmanr(g["rsi"], g["ex"])
        cor.append({"h": h, "reg": reg, "rho": rho, "p": p, "n": len(g)})
    out["spearman_by_reg"] = pd.DataFrame(cor)
    D5 = D[D.h == 5]
    ext = D5[D5.fc <= -5]
    out["ext_reg_coin_mean"] = ext.groupby(["coin", "reg"])["ex"].mean().unstack()
    out["ext_reg"] = ext.groupby("reg")["ex"].apply(tt).unstack()
    hi = D5[D5.rsi > 60]
    cc = []
    for coin, g in hi.groupby("coin"):
        g2 = g.copy(); g2["s"] = g2["rsi"] * np.sign(g2["r60"])
        rho, p = stats.spearmanr(g2["r60"], g2["ex"])
        cc.append({"coin": coin, "rho_r60_ex_whenRSI>60": rho, "n": len(g2)})
    out["hi_rsi_r60_corr"] = pd.DataFrame(cc)
    # book decomposition
    br, gm = [], []
    for coin, ws in data["days"].items():
        allc = pd.concat([d["coin_return"] for d in ws.values()]).mean()
        for w, d in ws.items():
            b = bars[coin][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            dd = d.set_index(pd.to_datetime(d["day"]))
            br.append(pd.DataFrame({"br": dd["book_return"].values, "drift": (pos.reindex(dd.index).values * allc)}))
    B = pd.concat(br).dropna()
    out["book"] = pd.Series({"mean_book": B.br.mean(), "drift_part": B.drift.mean(), "timing_part": B.br.mean() - B.drift.mean()})
    return out
