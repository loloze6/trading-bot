def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily returns
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["window"].str[1:].astype(int)
    B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"])
    B = B.dropna()
    val = (1 + B["book_return"]).cumprod()
    peak = val.cummax(); dd = val / peak - 1
    B["dd"] = dd.values
    B["year"] = pd.to_datetime(B["day"]).dt.year
    out["book by window"] = B.groupby("wn").agg(ret=("book_return", lambda x: (1 + x).prod() - 1),
                                                 coin=("coin_return", lambda x: (1 + x).prod() - 1),
                                                 min_dd=("dd", "min"), n=("book_return", "size"))
    out["book by year"] = B.groupby("year").agg(ret=("book_return", lambda x: (1 + x).prod() - 1),
                                                coin=("coin_return", lambda x: (1 + x).prod() - 1),
                                                sd=("book_return", "std"))
    out["max dd"] = float(dd.min())
    # cases
    cases = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values; vol = b["volume"].values
            n = len(b)
            r1 = pd.Series(cl).pct_change().values
            r20 = pd.Series(cl).pct_change(20).values
            r60 = pd.Series(cl).pct_change(60).values
            vol20 = pd.Series(r1).rolling(20).std().values
            vol60 = pd.Series(r1).rolling(60).std().values
            vrel = (pd.Series(vol) / pd.Series(vol).rolling(28).mean()).values
            for i in range(n - 3):
                if ts[i].dayofweek != 6: continue
                f = b["forecast"].iloc[i]
                fw = (cl[i + 3] / cl[i] - 1)
                cases.append(dict(coin=c, wn=int(w[1:]), year=ts[i].year, fc=f, alloc=b["postRebalance_current_allocation"].iloc[i],
                                  r1=r1[i], r20=r20[i], r60=r60[i], v20=vol20[i], vrat=vol20[i] / vol60[i] if vol60[i] else np.nan,
                                  vrel=vrel[i], fwd=fw))
    C = pd.DataFrame(cases)
    # coin drift on 3-bar grid
    drift = {}
    for c, ws in data["bars"].items():
        rr = []
        for w, b in ws.items():
            cl = b["close"].values
            rr += list(cl[3::3] / cl[0:-3:3] - 1) if len(cl) > 3 else []
        drift[c] = np.mean(rr)
    C["ex"] = C["fwd"] - C["coin"].map(drift)
    A = C[C["fc"] > 0].copy()
    def summ(g):
        return pd.Series(dict(n=len(g), mean_fwd=g["fwd"].mean(), mean_ex=g["ex"].mean(),
                              t=g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                              p10=g["fwd"].quantile(0.1)))
    out["active all"] = summ(A)
    out["active by year"] = A.groupby("year").apply(summ)
    A["r60q"] = pd.qcut(A["r60"], 4, labels=False)
    out["active by 60d ret quartile"] = A.groupby("r60q").apply(summ)
    A["r20q"] = pd.qcut(A["r20"], 4, labels=False)
    out["active by 20d ret quartile"] = A.groupby("r20q").apply(summ)
    A["r1q"] = pd.qcut(A["r1"], 4, labels=False)
    out["active by sunday ret quartile"] = A.groupby("r1q").apply(summ)
    A["vratq"] = pd.qcut(A["vrat"], 4, labels=False)
    out["active by vol20/vol60 quartile"] = A.groupby("vratq").apply(summ)
    A["vrelq"] = pd.qcut(A["vrel"], 4, labels=False)
    out["active by volume rel quartile"] = A.groupby("vrelq").apply(summ)
    A["v20q"] = pd.qcut(A["v20"], 4, labels=False)
    out["active by vol20 quartile"] = A.groupby("v20q").apply(summ)
    # non-active Sundays with same conditions (r60 low)
    N = C[(C["fc"] <= 0) | C["fc"].isna()].copy()
    N["r60q"] = pd.cut(N["r60"], [-np.inf] + list(A["r60"].quantile([.25, .5, .75])) + [np.inf], labels=False)
    out["nonactive sundays by 60d quartile (active cuts)"] = N.groupby("r60q").apply(summ)
    # cases per active Sunday date count -> clustering
    return out
