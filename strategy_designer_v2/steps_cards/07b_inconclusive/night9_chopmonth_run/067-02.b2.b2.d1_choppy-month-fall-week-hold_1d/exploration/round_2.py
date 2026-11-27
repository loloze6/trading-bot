def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    hold = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(df)
            lr = np.log(c[1:] / c[:-1])
            lr = np.r_[np.nan, lr]
            s = pd.Series(lr)
            sd30 = s.rolling(30, min_periods=20).std()
            # agitation proxy inside the window: 30d swing vs its expanding median (window-limited)
            med = sd30.expanding(min_periods=60).median()
            agit = (sd30 > med).values
            agit_known = med.notna().values
            raw = df["debug_info.components.month_fall.last_history_value"].values
            fc = df["forecast"].values
            reg = df["regime"].values
            alloc = df["postRebalance_current_allocation"].values
            nxt = np.r_[c[1:] / c[:-1] - 1, np.nan]
            for i in range(n - 1):
                if fc[i] == 0 and alloc[i] < 0:
                    above = (raw[i] >= 0) if not np.isnan(raw[i]) else np.nan
                    hold.append(dict(coin=coin, w=w, gain=alloc[i] * nxt[i], ret=nxt[i],
                                     chop=reg[i] == "unknown", above=above))
            for i in range(0, n - 7, 7):
                rows.append(dict(coin=coin, w=w, ret=c[i + 7] / c[i] - 1, raw=raw[i], fc=fc[i],
                                 chop=reg[i] == "unknown", agit=agit[i] if agit_known[i] else np.nan,
                                 ts=pd.Timestamp(df["timestamp"].iloc[i]).normalize()))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby("coin")["ret"].transform("mean")
    R["unus"] = R["ret"] - R["drift"]

    def summ(g, sign=-1, wcol=None):
        x = sign * g["unus"]
        wts = g[wcol].abs() if wcol else pd.Series(1.0, index=g.index)
        m = (x * wts).sum() / wts.sum()
        u = (wts * (x - m)).groupby(g["ts"]).sum()
        G = len(u)
        se = np.sqrt(G / (G - 1) * (u ** 2).sum()) / wts.sum() if G > 1 else np.nan
        return pd.Series(dict(n=len(x), days=G, mean=m, t=m / se if se else np.nan,
                              total=(sign * g["ret"] * wts).sum() / wts.sum()))
    out = {}
    F = R[R.chop & (R.fc < 0)]
    out["main measure B,C (fc<0, |fc| weighted)"] = summ(F, -1, "fc")
    out["main measure unweighted"] = summ(F, -1)
    out["by agitation (fc<0)"] = F.groupby("agit").apply(lambda g: summ(g, -1, "fc"))
    F = F.copy()
    F["fq"] = pd.qcut(F["fc"], 3, duplicates="drop")
    out["by forecast tercile"] = F.groupby("fq").apply(lambda g: summ(g, -1, "fc"))
    F["cq"] = F.groupby("coin")["drift"].transform("first") > R["drift"].median()
    out["by coin drift above median"] = F.groupby("cq").apply(lambda g: summ(g, -1, "fc"))
    H = pd.DataFrame(hold)
    out["held short, forecast 0"] = H.groupby(["chop", "above"], dropna=False)["gain"].agg(["count", "mean", "std"])
    out["held short, fc 0, by window"] = H.groupby("w")["gain"].agg(["count", "mean"])
    return out
