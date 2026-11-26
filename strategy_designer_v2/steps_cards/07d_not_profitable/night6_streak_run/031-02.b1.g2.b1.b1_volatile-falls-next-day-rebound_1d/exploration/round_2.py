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
    F = pd.concat(recs, ignore_index=True)
    drift = F.dropna(subset=["next"]).groupby("coin")["next"].mean()
    F["ex"] = F["next"] - F["coin"].map(drift)
    F["sig"] = F["fc"] > 0
    G = F.dropna(subset=["next", "volratio"])
    # condition alone vs with signal: volratio quintiles on no-signal (down and up days)
    edges = G.loc[G.sig, "volratio"].quantile([0.2, 0.4, 0.6, 0.8]).values
    G = G.copy(); G["vrb"] = np.digitize(G["volratio"], edges)
    def tt(x): return x.mean() / x.std() * np.sqrt(len(x))
    out["volratio_sig_vs_nosig"] = G.groupby(["vrb", "sig"]).agg(n=("ex", "size"), ex=("ex", "mean"), t=("ex", tt)).unstack()
    # down days without strong signal? interaction: volratio x fall depth on signal bars
    S = G[G.sig].copy()
    S["r0b"] = pd.qcut(S["r0"], 3, labels=["deep", "mid", "shallow"])
    S["vr2"] = np.where(S["volratio"] >= 1.0, "rising", "falling")
    out["sig_r0_x_volratio"] = S.groupby(["r0b", "vr2"]).agg(n=("ex", "size"), ex=("ex", "mean"), t=("ex", tt)).unstack()
    # non-overlapping is trivial at h=1. Variant books.
    F = F.sort_values(["coin", "wn", "pos"])
    cost = 0.0011
    def book(cond):
        p = np.where(cond, F["alloc"], 0.0)
        p = pd.Series(p, index=F.index)
        prev = p.groupby([F["coin"], F["wn"]]).shift(1).fillna(0)
        ret = p * F["next"].fillna(0) - cost * (p - prev).abs()
        d = pd.DataFrame({"wn": F["wn"], "day": F["day"], "r": ret, "inpos": (p != 0)})
        Bk = d.groupby(["wn", "day"]).agg(r=("r", "mean"), ip=("inpos", "mean")).reset_index().sort_values(["wn", "day"])
        v = (1 + Bk["r"]).cumprod()
        mdd = float((v / v.cummax() - 1).min())
        yr = v.iloc[-1] ** (365 / len(Bk)) - 1
        sh = Bk["r"].mean() / Bk["r"].std() * np.sqrt(365)
        return pd.Series({"sharpe": sh, "yearly": yr, "maxdd": mdd, "calmar": yr / -mdd, "mean_d": Bk["r"].mean(), "inpos": Bk["ip"].mean(),
                          "mean_d_inpos": Bk["r"].mean() / max(Bk["ip"].mean(), 1e-9)})
    vr = F["volratio"]; fc = F["fc"]; r0 = F["r0"]
    V = {"base": F["alloc"] != 0,
         "fc>=11": fc >= 11, "fc>=18.7": fc >= 18.7,
         "r0<=-3%": r0 <= -0.031, "r0<=-5%": r0 <= -0.053,
         "vr>=0.73": vr >= 0.734, "vr>=0.89": vr >= 0.887, "vr>=1.0": vr >= 1.0,
         "fc>=11&vr>=0.89": (fc >= 11) & (vr >= 0.887), "fc>=18.7&vr>=1": (fc >= 18.7) & (vr >= 1.0)}
    out["variant_books"] = pd.DataFrame({k: book(v.fillna(False).values) for k, v in V.items()}).T
    # worst book days of base: state of held bars
    held = F[F["alloc"] > 0].dropna(subset=["next"]).copy()
    held["g"] = held["alloc"] * held["next"]
    dg = held.groupby(["wn", "day"])["g"].sum()
    worst = dg.nsmallest(40).index
    W = held.set_index(["wn", "day"]).loc[worst]
    out["worst40_held_state"] = pd.Series({"mean_volratio": W["volratio"].mean(), "share_vr_lt_0.89": (W["volratio"] < 0.887).mean(),
                                           "mean_r0": W["r0"].mean(), "mean_fc": W["fc"].mean(), "mean_alloc": W["alloc"].mean(),
                                           "all_held_mean_vr": held["volratio"].mean(), "all_held_mean_r0": held["r0"].mean()})
    return out
