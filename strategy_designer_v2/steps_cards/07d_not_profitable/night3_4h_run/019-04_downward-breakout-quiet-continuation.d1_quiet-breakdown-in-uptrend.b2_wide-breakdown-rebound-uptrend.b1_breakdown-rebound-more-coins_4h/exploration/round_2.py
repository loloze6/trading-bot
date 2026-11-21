def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    recs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; lo = b["low"]
            r180 = cl / cl.shift(180) - 1
            ret1 = cl / cl.shift(1) - 1
            ret6 = cl / cl.shift(6) - 1
            vol = ret1.rolling(180).std()
            volr = ret1.rolling(36).std() / vol
            fwd18 = cl.shift(-18) / cl - 1
            dd18 = (cl.shift(-1).rolling(18).min().shift(-17)) / cl - 1
            df = pd.DataFrame({"sig": b["regime"] == "trending", "r180": r180, "ret6": ret6,
                               "vol": vol, "volr": volr, "fwd18": fwd18, "dd18": dd18})
            df["coin"] = c; df["w"] = int(w[1:])
            df["cell"] = np.arange(len(df)) // 18
            recs.append(df)
    B = pd.concat(recs, ignore_index=True)
    g = B.iloc[::1]
    drift = B[B.index.isin(B.index)].groupby("coin")["fwd18"].mean()
    S = B[B["sig"] & B["fwd18"].notna()].groupby(["coin", "w", "cell"]).first().reset_index()
    S["u"] = S["fwd18"] - S["coin"].map(drift)
    S["ret6n"] = S["ret6"] / S["vol"]
    S["r180n"] = S["r180"] / (S["vol"] * np.sqrt(180))
    S = S.dropna(subset=["u", "ret6n", "r180n", "volr"])
    S["qa"] = pd.qcut(S["ret6n"], 3, labels=["sharp", "mid", "mild"])
    S["qb"] = pd.qcut(S["r180n"], 3, labels=["weakup", "midup", "strongup"])
    out["ret6n_x_r180n_mean_u"] = S.pivot_table(index="qa", columns="qb", values="u", aggfunc="mean")
    out["ret6n_x_r180n_n"] = S.pivot_table(index="qa", columns="qb", values="u", aggfunc="size")
    S["qv"] = pd.qcut(S["volr"], 5, labels=False)
    out["q_volr"] = S.groupby("qv").agg(mid=("volr", "median"), mean_u=("u", "mean"),
                                       n=("u", "size"), dd18=("dd18", "mean"),
                                       worst=("fwd18", lambda x: x.quantile(0.05)))
    # by window coin trend sign: windows whose pooled coin mean negative vs positive
    wm = B.groupby("w")["fwd18"].mean()
    S["wneg"] = S["w"].map(wm) < 0
    out["by_window_sign"] = S.groupby("wneg").agg(mean_u=("u", "mean"), mean_tot=("fwd18", "mean"), n=("u", "size"),
                                                  dd18=("dd18", "mean"))
    a = S["u"][S["ret6n"] < S["ret6n"].median()]; bb = S["u"][S["ret6n"] >= S["ret6n"].median()]
    t = stats.ttest_ind(a, bb, equal_var=False)
    out["sharp_minus_mild"] = pd.Series({"diff": a.mean() - bb.mean(), "t": t.statistic, "n_a": len(a), "n_b": len(bb),
                                         "t_sharp": a.mean() / (a.std() / np.sqrt(len(a)))})
    hi = S["u"][S["r180n"] >= S["r180n"].median()]; lo_ = S["u"][S["r180n"] < S["r180n"].median()]
    t2 = stats.ttest_ind(hi, lo_, equal_var=False)
    out["strong_minus_weak_trend"] = pd.Series({"diff": hi.mean() - lo_.mean(), "t": t2.statistic,
                                                "mean_strong": hi.mean(), "mean_weak": lo_.mean()})
    return out
