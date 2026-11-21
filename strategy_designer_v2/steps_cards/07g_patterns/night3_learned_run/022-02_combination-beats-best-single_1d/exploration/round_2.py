def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []; daily = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            f = pd.DataFrame({"coin": coin, "win": w, "yr": ts.dt.year,
                "ret1z": r1 / r1.rolling(30).std(), "ret28": c / c.shift(28) - 1,
                "ret28z": (c / c.shift(28) - 1) / (r1.rolling(30).std() * np.sqrt(28)),
                "comb": b.get("debug_info.components.combined.post_pipeline_value"),
                "y": c.shift(-5) / c - 1})
            g = f.iloc[::5]; g = g[g["y"].notna()]; rows.append(g)
            daily.append(pd.DataFrame({"coin": coin, "win": w, "yr": ts.dt.year, "wd": ts.dt.weekday, "r": r1,
                                       "absprev": (r1.shift(1) / r1.rolling(30).std().shift(1))}))
    G = pd.concat(rows, ignore_index=True)
    G["y"] = G["y"] - G.groupby("coin")["y"].transform("mean")
    G["wnum"] = G["win"].str[1:].astype(int)
    G["half"] = np.where(G["wnum"] <= 12, "w1-12", "w13-24")
    out = {}
    def rk(d, s):
        return d.groupby("coin")[s].rank(pct=True) - 0.5
    for s in ["ret1z", "ret28z"]:
        d = G[[s, "y", "coin", "half", "yr"]].dropna().copy()
        d["rk"] = rk(d, s)
        d["sy"] = np.sign(d["rk"]) * d["y"]
        res = []
        for key in ["coin", "half", "yr"]:
            for k, e in d.groupby(key):
                r = e["rk"].corr(e["y"])
                t = e["sy"].mean() / (e["sy"].std() / np.sqrt(len(e)))
                res.append([key, str(k), len(e), round(r, 3), round(e["sy"].mean() * 100, 3), round(t, 2)])
        r = d["rk"].corr(d["y"]); t = d["sy"].mean() / (d["sy"].std() / np.sqrt(len(d)))
        res.append(["all", "all", len(d), round(r, 3), round(d["sy"].mean() * 100, 3), round(t, 2)])
        out["signed_rank_" + s] = pd.DataFrame(res, columns=["by", "k", "n", "rank_corr", "signed_y%", "t"])
        d["dec"] = d.groupby("coin")[s].transform(lambda x: pd.qcut(x.rank(method="first"), 10, labels=False))
        out["decile_" + s] = d.groupby("dec")["y"].agg(["count", "mean"]).assign(mean=lambda x: x["mean"] * 100)
    d = G[["ret1z", "comb", "y"]].dropna()
    out["corr_ret1z_comb"] = round(d["ret1z"].corr(d["comb"]), 3)
    D = pd.concat(daily).dropna(subset=["r"])
    D["r"] = D["r"] - D.groupby("coin")["r"].transform("mean")
    D["sat"] = D["wd"] == 5
    res = []
    for key in ["coin", "yr"]:
        for k, e in D.groupby(key):
            a = e[e.sat]["r"]; b2 = e[~e.sat]["r"]
            res.append([key, str(k), len(a), round(a.mean() * 100, 3), round(stats.ttest_ind(a, b2, equal_var=False).statistic, 2)])
    out["saturday_minus_rest"] = pd.DataFrame(res, columns=["by", "k", "n_sat", "sat_mean%", "t_vs_rest"])
    return out
