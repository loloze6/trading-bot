import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    H = [5, 10, 20]
    coin_mean = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            coin_mean[(coin, h)] = np.mean(rs) if rs else np.nan
    out = {}
    for G in [5, 10, 20]:
        rows = []
        for coin, wins in bars.items():
            for w, df in wins.items():
                df = df.reset_index(drop=True)
                c = df["close"].values; f = df["forecast"].values; reg = df["regime"].values
                r1 = pd.Series(c).pct_change()
                vol = r1.rolling(30).std().values
                vol_rel = (r1.rolling(30).std() / r1.rolling(90, min_periods=60).std()).values
                ts = pd.to_datetime(df["timestamp"]); n = len(c)
                for i in range(0, n - G, G):
                    if reg[i] != "unknown" or not np.isfinite(f[i]) or f[i] == 0:
                        continue
                    x = c[i + G] / c[i] - 1 - coin_mean[(coin, G)]
                    rows.append({"coin": coin, "win": w, "f": f[i], "day": ts.iloc[i].floor("D"),
                                 "year": ts.iloc[i].year, "vol30": vol[i], "vrel": vol_rel[i], "x": x})
        X = pd.DataFrame(rows)
        X["s"] = X.f / 10 * X.x
        X["d"] = np.sign(X.f) * X.x
        lo, hi = X.x.quantile([0.025, 0.975])
        X["sw"] = X.f / 10 * X.x.clip(lo, hi)

        def ct(sub, col):
            s = sub.dropna(subset=[col])
            if len(s) < 5:
                return pd.Series({"n": len(s), "days": np.nan, "mean": np.nan, "t": np.nan})
            m = s[col].mean()
            dev = (s[col] - m).groupby(s["day"]).sum(); D = len(dev)
            se = np.sqrt((dev**2).sum() * D / (D - 1)) / len(s)
            return pd.Series({"n": len(s), "days": D, "mean": m, "t": m / se})
        res = {"all_s": ct(X, "s"), "all_winsor": ct(X, "sw"), "noDOGE_s": ct(X[X.coin != "DOGEUSD"], "s"),
               "long_s": ct(X[X.f > 0], "s"), "short_s": ct(X[X.f < 0], "s"),
               "core6_s": ct(X[X.coin.isin(["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"])], "s"),
               "vrel_low_s": ct(X[X.vrel <= 1], "s"), "vrel_high_s": ct(X[X.vrel > 1], "s"),
               "vrel_low_winsor": ct(X[X.vrel <= 1], "sw"), "vrel_high_winsor": ct(X[X.vrel > 1], "sw")}
        out[f"h{G}_grid"] = pd.DataFrame(res).T
        out[f"h{G}_year"] = X.groupby("year").apply(lambda s: ct(s, "sw"))
        X["fq"] = pd.qcut(X.f.abs(), 3, labels=["lo", "mid", "hi"])
        out[f"h{G}_absf_winsor_dir"] = X.assign(dw=np.sign(X.f) * X.x.clip(lo, hi)).groupby("fq").apply(lambda s: ct(s, "dw"))
    return out
