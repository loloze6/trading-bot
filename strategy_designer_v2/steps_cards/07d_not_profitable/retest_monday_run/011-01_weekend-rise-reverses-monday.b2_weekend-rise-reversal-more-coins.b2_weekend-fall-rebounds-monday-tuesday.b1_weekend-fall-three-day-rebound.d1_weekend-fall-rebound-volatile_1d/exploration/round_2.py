def explore(data):
    import numpy as np, pandas as pd
    out = {}
    cs = []
    ncoins_w = {}
    for c, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 3, 3)
            allr += list(cl[idx + 3] / cl[idx] - 1)
        mu = np.mean(allr)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"]; r1 = cl.pct_change()
            f3 = cl.shift(-3) / cl - 1
            r20 = cl / cl.shift(20) - 1
            vol20 = r1.rolling(20).std(); vol60 = r1.rolling(60).std()
            f1 = cl.shift(-1) / cl - 1
            alloc = b["postRebalance_current_allocation"]
            sun = (ts.dt.dayofweek == 6)
            for k, i in enumerate(np.where(sun & f3.notna())[0]):
                cs.append(dict(coin=c, wn=int(w[1:]), wk=f"{w}_{k}", fc=b["forecast"].iloc[i], r1=r1.iloc[i], f3=f3.iloc[i],
                               f1=f1.iloc[i], ex=f3.iloc[i] - mu, r20=r20.iloc[i],
                               vr=vol20.iloc[i] / vol60.iloc[i] if vol60.iloc[i] else np.nan, alloc=alloc.iloc[i]))
    C = pd.DataFrame(cs)
    S = C[C.fc > 0].copy(); S["pnl"] = S.alloc * S.f3
    N = C[C.fc <= 0].copy()
    # condition alone: no-signal Sundays by vol ratio
    def g(df, col, q=3):
        df = df.dropna(subset=[col]).copy()
        df["b"] = pd.qcut(df[col], q, labels=False, duplicates="drop")
        return df.groupby("b").agg(n=("ex", "size"), lo=(col, "min"), hi=(col, "max"), ex=("ex", "mean"),
                                   t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    out["no-signal Sundays by vol ratio"] = g(N, "vr")
    # fall period w2-w3
    F = S[S.wn.isin([2, 3])]
    out["w2-3 signal by vol ratio"] = g(F.assign(ex=F.ex), "vr")
    out["w2-3 signal by r20"] = g(F, "r20")
    out["w2-3 signal by forecast"] = g(F, "fc")
    # cross: r20 thirds x vr halves, all windows
    S2 = S.dropna(subset=["vr", "r20"]).copy()
    S2["r20b"] = pd.qcut(S2.r20, 3, labels=False); S2["vrb"] = (S2.vr > 1).astype(int)
    out["r20 third x vr>1"] = S2.groupby(["r20b", "vrb"]).agg(n=("ex", "size"), ex=("ex", "mean"),
        t=("ex", lambda x: x.mean() / x.std() * np.sqrt(len(x))), p5=("f3", lambda x: x.quantile(.05)))
    # weekly book approximations: per (window, week) sum of pnl over coins / coins present
    ncoin = C.groupby("wk").coin.nunique()
    def book(mask, name):
        p = S[mask].groupby("wk").pnl.sum().reindex(ncoin.index).fillna(0) / ncoin
        order = sorted(p.index, key=lambda s: (int(s.split("_")[0][1:]), int(s.split("_")[1])))
        p = p.loc[order]
        v = (1 + p).cumprod(); dd = (v / v.cummax() - 1).min()
        yrs = len(p) * 7 / 365
        yr = v.iloc[-1] ** (1 / yrs) - 1
        return pd.Series({"weeks_active": (p != 0).sum(), "mean_wk": p.mean(), "yearly": yr, "maxdd": dd, "calmar": yr / -dd,
                          "sharpe_wk": p.mean() / p.std() * np.sqrt(52)})
    vr = S.vr.fillna(1)
    out["approx weekly books"] = pd.DataFrame({
        "all": book(S.fc > 0, "all"),
        "fc top 2/3": book(S.fc > 2.84, ""),
        "vr>1": book(vr > 1, ""),
        "vr>0.86": book(vr > 0.86, ""),
        "r20<0.05": book(S.r20 < 0.053, ""),
        "vr>0.86 & fc>2.84": book((vr > 0.86) & (S.fc > 2.84), ""),
    }).T
    # holding: 1-day vs 3-day share of gain
    out["gain by day after Sunday"] = pd.Series({"f1_mean": S.f1.mean(), "f3_mean": S.f3.mean(),
                                                  "f1_top_vr": S[vr > 1.08].f1.mean(), "f3_top_vr": S[vr > 1.08].f3.mean()})
    return out
