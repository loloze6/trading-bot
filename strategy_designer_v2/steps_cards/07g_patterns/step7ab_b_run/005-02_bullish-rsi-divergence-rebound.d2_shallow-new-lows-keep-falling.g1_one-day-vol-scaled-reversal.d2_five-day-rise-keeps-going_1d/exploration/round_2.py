import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "wn": int(w[1:]), "pos": np.arange(len(b)),
                "vsr5": (c / c.shift(5) - 1) / (vol20 * np.sqrt(5)),
                "vsr1": r1 / vol20,
                "vsr2": (c / c.shift(2) - 1) / (vol20 * np.sqrt(2)),
                "vol20": vol20, "vratio": vol20 / vol60,
                "rng": ((b["high"] - b["low"]) / c).astype(float) / vol20,
                "r60": c / c.shift(60) - 1,
                "fc": b["forecast"].astype(float),
            })
            for h in (1, 2, 3, 5, 7):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for h in (1, 2, 3, 5, 7):
        g = d[d["pos"] % h == 0]
        m = g.groupby("coin")[f"f{h}"].mean(); sd = g.groupby("coin")[f"f{h}"].std()
        d[f"u{h}"] = d[f"f{h}"] - d["coin"].map(m)
        d[f"s{h}"] = d[f"u{h}"] / d["coin"].map(sd)
    # within-coin vol tercile using coin's own median
    d["lowvol"] = d["vol20"] <= d.groupby("coin")["vol20"].transform("median")
    d["lowratio"] = d["vratio"] <= d.groupby("coin")["vratio"].transform("median")
    d["up60"] = d["r60"] > 0

    def slope(col, h, mask=None):
        g = d[d["pos"] % h == 0].dropna(subset=[col, f"s{h}"])
        if mask is not None:
            g = g[mask(g)]
        s = stats.linregress(g[col], g[f"s{h}"])
        return pd.Series({"n": len(g), "slope_std": s.slope, "t": s.slope / s.stderr})

    res = {}
    for col in ("vsr1", "vsr2", "vsr5", "rng"):
        for h in (1, 2, 3, 5, 7):
            res[f"{col}_h{h}"] = slope(col, h)
    out["slopes_all"] = pd.DataFrame(res).T

    res = {}
    for col, h in (("vsr1", 1), ("vsr5", 3), ("vsr5", 5), ("vsr5", 7)):
        for nm, mk in (("lowvol", lambda g: g.lowvol), ("highvol", lambda g: ~g.lowvol),
                       ("lowratio", lambda g: g.lowratio), ("highratio", lambda g: ~g.lowratio),
                       ("up60", lambda g: g.up60), ("down60", lambda g: ~g.up60),
                       ("BTC", lambda g: g.coin == "BTCUSD"), ("ETH", lambda g: g.coin == "ETHUSD"),
                       ("w1-12", lambda g: g.wn <= 12), ("w13-24", lambda g: g.wn > 12)):
            res[f"{col}_h{h}_{nm}"] = slope(col, h, mk)
    out["slopes_split"] = pd.DataFrame(res).T

    # interaction test: vsr5 x lowvol at h3
    g = d[d.pos % 3 == 0].dropna(subset=["vsr5", "s3", "vol20"]).copy()
    g["lv"] = g["lowvol"].astype(float)
    X = np.column_stack([np.ones(len(g)), g.vsr5, g.lv, g.vsr5 * g.lv])
    beta, *_ = np.linalg.lstsq(X, g.s3.values, rcond=None)
    resid = g.s3.values - X @ beta
    s2 = resid @ resid / (len(g) - 4)
    cov = s2 * np.linalg.inv(X.T @ X)
    out["interaction_vsr5_lowvol_h3"] = pd.Series({"b_vsr5": beta[1], "b_inter": beta[3], "t_inter": beta[3] / np.sqrt(cov[3, 3]), "n": len(g)})

    # size of 1-day reversal: top quintile of vsr1, unusual move short side, strength
    g = d[d.pos % 1 == 0].dropna(subset=["vsr1", "u1"]).copy()
    g["q"] = g.groupby("coin")["vsr1"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["vsr1_quint_h1"] = g.groupby("q").agg(n=("u1", "size"), mean_u=("u1", "mean"), mean_raw=("f1", "mean"), mean_s=("s1", "mean"))
    g = d[d.pos % 5 == 0].dropna(subset=["vsr5", "u5"]).copy()
    g["q"] = g.groupby("coin")["vsr5"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["vsr5_quint_h5_lowvol"] = g[g.lowvol].groupby("q").agg(n=("u5", "size"), mean_u=("u5", "mean"), mean_s=("s5", "mean"))
    out["vsr5_quint_h5_highvol"] = g[~g.lowvol].groupby("q").agg(n=("u5", "size"), mean_u=("u5", "mean"), mean_s=("s5", "mean"))
    return out
