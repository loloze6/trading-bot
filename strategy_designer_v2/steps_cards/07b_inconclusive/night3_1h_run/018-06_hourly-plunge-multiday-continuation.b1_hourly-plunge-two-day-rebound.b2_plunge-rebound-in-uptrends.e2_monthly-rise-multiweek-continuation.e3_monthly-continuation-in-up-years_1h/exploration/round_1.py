def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    H = [24, 72, 168, 336, 720]
    drift = {}
    for coin, ws in bars.items():
        for h in H:
            rets = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rets.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = (np.mean(rets), np.std(rets))
        for w, df in ws.items():
            c = df["close"].values
            f = df["forecast"].values
            reg = df["regime"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            r30 = df["debug_info.components.ret_30d.last_history_value"].values if "debug_info.components.ret_30d.last_history_value" in df else np.full(len(c), np.nan)
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                for i in idx:
                    r = c[i + h] / c[i] - 1
                    m, s = drift[(coin, h)]
                    rows.append(dict(coin=coin, w=w, h=h, f=f[i], trend=reg[i] == "trending",
                                     yr=yr[i], r30=r30[i], u=r - m, z=(r - m) / s))
    d = pd.DataFrame(rows)

    def summ(g):
        n = len(g)
        m = g["u"].mean()
        sd = g["u"].std()
        return pd.Series(dict(n=n, mean_u=m, t=m / (sd / np.sqrt(n)) if n > 1 else np.nan, strength=g["z"].mean()))

    out = {}
    act = d[d.f > 0]
    out["by_horizon_active"] = act.groupby("h").apply(summ)
    out["by_horizon_trend_flat"] = d[(d.trend) & (d.f <= 0)].groupby("h").apply(summ)
    out["by_horizon_nontrend"] = d[~d.trend].groupby("h").apply(summ)
    a168 = act[act.h == 168].copy()
    out["168_by_coin"] = a168.groupby("coin").apply(summ)
    out["168_by_year"] = a168.groupby("yr").apply(summ)
    a168["q"] = pd.qcut(a168["f"].rank(method="first"), 4, labels=False)
    out["168_by_fq"] = a168.groupby("q").apply(summ)
    out["168_f_quart_mean"] = a168.groupby("q")["f"].mean()
    a720 = act[act.h == 720].copy()
    a720["q"] = pd.qcut(a720["f"].rank(method="first"), 4, labels=False)
    out["720_by_fq"] = a720.groupby("q").apply(summ)
    out["720_by_coin"] = a720.groupby("coin").apply(summ)
    out["336_by_coin"] = act[act.h == 336].groupby("coin").apply(summ)
    return out
