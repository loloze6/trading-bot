def explore(data):
    import numpy as np, pandas as pd
    out = {}
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            nxt = c.shift(-1) / c - 1
            absm = r1.abs().rolling(60, min_periods=20).mean()
            z = -r1 / absm
            al = b["postRebalance_current_allocation"].fillna(0)
            df = pd.DataFrame({"coin": coin, "w": w, "wn": int(w[1:]),
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "r1": r1, "z": z, "nxt": nxt, "fc": b["forecast"].fillna(0),
                               "alloc": al, "dal": al.diff().abs().fillna(al.abs()),
                               "agit": b["regime"] != "chop",
                               "ret7": c / c.shift(7) - 1, "ret3": c.shift(1) / c.shift(4) - 1,
                               "prevsig": (b["forecast"].shift(1).fillna(0) > 0)})
            recs.append(df)
    X = pd.concat(recs).dropna(subset=["nxt", "r1", "z"])
    mu = X.groupby("coin")["nxt"].mean()
    X["ex"] = X["nxt"] - X["coin"].map(mu)
    S = X[X["fc"] > 0].copy()
    q = S["z"].quantile([0.5, 0.75]).values
    out["z_cut_median_q75"] = pd.Series(q, index=["median", "q75"])
    def summ(g):
        return pd.Series({"n": len(g), "ex_mean": g["ex"].mean(),
                          "t": g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))),
                          "gain_mean": (g["alloc"] * g["nxt"]).mean(), "alloc": g["alloc"].mean()})
    out["by_prevday_signal"] = S.groupby("prevsig").apply(summ)
    S["big"] = S["z"] > q[1]
    out["big_x_prevsig"] = S.groupby(["big", "prevsig"]).apply(summ)
    # condition alone: agitated, no signal, previous day a signal (i.e. up day after a fall)
    out["agit_by_prevsig_nosignal"] = X[(X["fc"] <= 0) & X["agit"]].groupby("prevsig").apply(summ)
    # variant books
    cost = 0.00095
    def book(alloc):
        g = alloc * X["nxt"] - alloc.groupby([X["coin"], X["w"]]).diff().abs().fillna(alloc.abs()) * cost
        B = pd.DataFrame({"wn": X["wn"], "day": X["day"], "g": g}).groupby(["wn", "day"])["g"].mean().sort_index()
        v = (1 + B).cumprod()
        dd = (v / v.cummax() - 1).min()
        yr = v.iloc[-1] ** (365 / len(B)) - 1
        return pd.Series({"yearly": yr, "deepest": dd, "calmar": yr / -dd,
                          "sharpe": B.mean() / B.std() * np.sqrt(365), "held_share": (alloc != 0).mean()})
    a = X["alloc"]
    sig = X["fc"] > 0
    zz = X["z"].clip(lower=0)
    v = {}
    v["original"] = book(a)
    v["only_above_median_fall"] = book(a.where(X["z"] > q[0], 0))
    v["only_top_quarter_fall"] = book(a.where(X["z"] > q[1], 0))
    v["alloc_x_z_over_median"] = book((a * zz / q[0]).clip(upper=2))
    v["skip_ret7_middle"] = book(a.where(~((X["ret7"] > S["ret7"].quantile(1/3)) & (X["ret7"] < S["ret7"].quantile(2/3))), 0))
    out["variant_books_approx"] = pd.DataFrame(v).T
    # drawdown episode anatomy for original
    g = a * X["nxt"]
    X["g"] = g
    B = X.groupby(["wn", "day"])["g"].mean().sort_index()
    vv = (1 + B).cumprod(); ddv = vv / vv.cummax() - 1
    worst_end = ddv.idxmin()
    peak = vv.loc[:worst_end].idxmax()
    ep = X.set_index(["wn", "day"]).sort_index().loc[peak:worst_end].reset_index()
    epS = ep[ep["alloc"] > 0]
    out["deepest_episode"] = pd.Series({"days": ep["day"].nunique(), "positions": len(epS),
                                        "mean_z": epS["z"].mean(), "mean_nxt": epS["nxt"].mean(),
                                        "share_prevsig": epS["prevsig"].mean(),
                                        "share_big": (epS["z"] > q[1]).mean(),
                                        "mean_ret7": epS["ret7"].mean(), "mean_alloc": epS["alloc"].mean()})
    # losing positions overall: by z quartile, share of loss
    S["zbin"] = pd.qcut(S["z"], 4, labels=False)
    out["loss_days_by_zbin"] = S.assign(l=(S["alloc"] * S["nxt"]).clip(upper=0)).groupby("zbin")["l"].sum()
    out["gain_days_by_zbin"] = S.assign(l=(S["alloc"] * S["nxt"]).clip(lower=0)).groupby("zbin")["l"].sum()
    return out
