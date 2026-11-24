def explore(data):
    import pandas as pd, numpy as np
    out = {}
    bars = data["bars"]
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r = cl.pct_change()
            f = pd.DataFrame({"coin": c, "wn": int(w[1:]), "pos": np.arange(len(b)), "fc": b["forecast"],
                              "alloc": b["postRebalance_current_allocation"].fillna(0),
                              "r0": r, "next": cl.shift(-1) / cl - 1,
                              "vol20": r.rolling(20, min_periods=15).std(), "vol60": r.rolling(60, min_periods=40).std(),
                              "ma50": cl / cl.rolling(50, min_periods=30).mean() - 1})
            f["volratio"] = f["vol20"] / f["vol60"]
            f["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            recs.append(f)
    F = pd.concat(recs, ignore_index=True).sort_values(["coin", "wn", "pos"])
    drift = F.dropna(subset=["next"]).groupby("coin")["next"].mean()
    F["ex"] = F["next"] - F["coin"].map(drift)
    F["sig"] = F["fc"] > 0
    cost = 0.0011
    def book(cond):
        p = pd.Series(np.where(cond, F["alloc"], 0.0), index=F.index)
        prev = p.groupby([F["coin"], F["wn"]]).shift(1).fillna(0)
        ret = p * F["next"].fillna(0) - cost * (p - prev).abs()
        d = pd.DataFrame({"wn": F["wn"], "day": F["day"], "r": ret, "inpos": (p != 0)})
        Bk = d.groupby(["wn", "day"]).agg(r=("r", "mean"), ip=("inpos", "mean")).reset_index().sort_values(["wn", "day"])
        v = (1 + Bk["r"]).cumprod()
        mdd = float((v / v.cummax() - 1).min())
        yr = v.iloc[-1] ** (365 / len(Bk)) - 1
        sh = Bk["r"].mean() / Bk["r"].std() * np.sqrt(365)
        w16 = Bk[Bk.wn == 16]; v16 = (1 + w16["r"]).cumprod(); dd16 = float((v16 / v16.cummax() - 1).min())
        loo = min(Bk[Bk.wn != k]["r"].mean() / Bk[Bk.wn != k]["r"].std() * np.sqrt(365) for k in Bk.wn.unique())
        return pd.Series({"sharpe": sh, "yearly": yr, "maxdd": mdd, "calmar": yr / -mdd, "dd_w16": dd16, "loo_sharpe": loo,
                          "inpos": Bk["ip"].mean(), "mean_d_inpos": Bk["r"].mean() / max(Bk["ip"].mean(), 1e-9)})
    vr = F["volratio"]; r0 = F["r0"]; m = F["ma50"]
    ext = (m <= -0.167) | (m >= 0.006)
    V = {"base": F["alloc"] != 0,
         "r0<=-5%&vr>=1": (r0 <= -0.053) & (vr >= 1.0),
         "r0<=-3%&vr>=1": (r0 <= -0.031) & (vr >= 1.0),
         "r0<=-3%&vr>=0.89": (r0 <= -0.031) & (vr >= 0.887),
         "ma50_extreme": ext,
         "r0<=-3%&ma_ext": (r0 <= -0.031) & ext,
         "vr>=1&ma_ext": (vr >= 1.0) & ext}
    out["variant_books"] = pd.DataFrame({k: book(v.fillna(False).values) for k, v in V.items()}).T
    def tt(x): return x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan
    G = F.dropna(subset=["next", "volratio", "ma50"]).copy()
    G["deep"] = G["r0"] <= -0.031
    G["vrup"] = G["volratio"] >= 1.0
    out["deep_x_vrup_all_bars"] = G.groupby(["deep", "vrup"]).agg(n=("ex", "size"), ex=("ex", "mean"), t=("ex", tt))
    # in w16 episode: what deep&vrup bars did
    H = G[G.wn == 16]
    out["w16_deep_vrup"] = H.groupby(["deep", "vrup"]).agg(n=("ex", "size"), ex=("ex", "mean"), nxt=("next", "mean"))
    return out
