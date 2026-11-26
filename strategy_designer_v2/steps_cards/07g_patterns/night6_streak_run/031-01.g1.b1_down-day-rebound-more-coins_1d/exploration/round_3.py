import pandas as pd, numpy as np

def explore(data):
    H = 3
    rows = []
    for coin, wins in data["bars"].items():
        g_all = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            g_all.append(c[idx + H] / c[idx] - 1)
        g_all = np.concatenate(g_all)
        if len(g_all) < 10:
            continue
        drift, usual = g_all.mean(), g_all.std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(60, min_periods=20).std()
            rng = (b["high"] - b["low"]) / c
            rng_s = rng / rng.rolling(60, min_periods=20).mean()
            volu = b["volume"].astype(float)
            volu_s = volu / volu.rolling(60, min_periods=20).mean()
            lowtail = (c - b["low"]) / c / rng.rolling(60, min_periods=20).mean()
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in np.arange(0, len(c) - H, H):
                rows.append(dict(coin=coin, win=w, wn=int(w[1:]), day=ts.iloc[i].normalize(), year=ts.iloc[i].year,
                                 sr=r.iloc[i] / vol.iloc[i] if vol.iloc[i] > 0 else np.nan,
                                 rng_s=rng_s.iloc[i], volu_s=volu_s.iloc[i], lowtail=lowtail.iloc[i],
                                 u=fwd.iloc[i] - drift, z=(fwd.iloc[i] - drift) / usual,
                                 u1=fwd1.iloc[i]))
    d = pd.DataFrame(rows).dropna(subset=["u", "rng_s", "sr", "volu_s"])
    d = d[d.sr < 0].copy()
    d["lrng"] = np.log(d["rng_s"].clip(lower=0.05))
    d["lvol"] = np.log(d["volu_s"].clip(lower=0.05))
    d["lfall"] = -d["sr"]
    d["ltail"] = d["lowtail"]

    def multi(x, cols, y="z"):
        X = np.column_stack([np.ones(len(x))] + [x[c].values for c in cols])
        Y = x[y].values
        XtXi = np.linalg.inv(X.T @ X)
        bb = XtXi @ X.T @ Y
        e = Y - X @ bb
        S = pd.DataFrame(X * e[:, None]).groupby(x["day"].values).sum().values
        V = XtXi @ (S.T @ S) @ XtXi
        G = x["day"].nunique(); V *= G / (G - 1)
        return pd.DataFrame({"coef": bb[1:], "t": bb[1:] / np.sqrt(np.diag(V))[1:]}, index=cols)

    res = {}
    res["down_rng_and_fall"] = multi(d, ["lrng", "lfall"])
    res["down_rng_vol_fall"] = multi(d, ["lrng", "lvol", "lfall"])
    res["down_tail_given_rng"] = multi(d.dropna(subset=["ltail"]), ["lrng", "ltail"])
    res["down_rng_first_half_windows"] = multi(d[d.wn <= 12], ["lrng"])
    res["down_rng_second_half_windows"] = multi(d[d.wn > 12], ["lrng"])
    res["down_rng_1day_horizon"] = multi(d.dropna(subset=["u1"]).assign(z1=lambda x: x.u1), ["lrng"], y="z1")
    x = d.copy(); x["q"] = pd.qcut(x["rng_s"], 5, labels=False)
    x["f"] = pd.qcut(x["lfall"], 2, labels=["small_fall", "large_fall"])
    res["down_mean_u_pct_rng_q_by_fall"] = x.groupby(["q", "f"], observed=True)["u"].mean().unstack() * 100
    return res
