def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    G = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; ts = pd.to_datetime(df["timestamp"])
            r = c.pct_change()
            vol20 = r.rolling(20).std()
            x = pd.DataFrame(dict(coin=coin, win=w, ts=ts, yr=ts.dt.year, wd=ts.dt.dayofweek,
                                  r1s=r / vol20, r5s=(c / c.shift(5) - 1) / (vol20 * np.sqrt(5)),
                                  fwd5=c.shift(-5) / c - 1, f=df["forecast"]))
            G.append(x.iloc[::5])
    G = pd.concat(G, ignore_index=True)
    G["ex5"] = G["fwd5"] - G.groupby("coin")["fwd5"].transform("mean")
    G = G.dropna(subset=["r1s", "r5s", "ex5"])
    G["a1"] = G["r1s"].abs()
    for col in ["r1s", "r5s", "a1"]:
        G[col + "_z"] = G.groupby("coin")[col].transform(lambda s: (s - s.mean()) / s.std())
    res = {}
    for col in ["r1s_z", "r5s_z", "a1_z"]:
        P = (G[col] * G["ex5"]).groupby(G["ts"]).mean()
        res[col] = pd.Series({"mean_prod": P.mean(), "t_dates": P.mean() / (P.std() / np.sqrt(len(P))), "n_dates": len(P), "n_cells": len(G)})
    out["date-clustered signal x excess5"] = pd.DataFrame(res).T.round(5)
    # by year for the three
    yrs = {}
    for col in ["r1s_z", "r5s_z", "a1_z"]:
        P = (G[col] * G["ex5"]).groupby([G["yr"], G["ts"]]).mean()
        yrs[col] = P.groupby(level=0).apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
    out["date-clustered t by year"] = pd.DataFrame(yrs).round(3)
    # quintiles of abs r1, date-clustered means
    G["aq"] = G.groupby("coin")["a1"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    Q = G.groupby(["aq", "ts"])["ex5"].mean().groupby(level=0).agg(["count", "mean", "std"])
    Q["t"] = Q["mean"] / (Q["std"] / np.sqrt(Q["count"]))
    out["excess5 by |r1|/vol quintile, date-clustered"] = Q.round(4)
    # weekday 5-day excess, date-clustered
    W = G.groupby(["wd", "ts"])["ex5"].mean().groupby(level=0).agg(["count", "mean", "std"])
    W["t"] = W["mean"] / (W["std"] / np.sqrt(W["count"]))
    out["excess5 by weekday, date-clustered"] = W.round(4)
    return out
