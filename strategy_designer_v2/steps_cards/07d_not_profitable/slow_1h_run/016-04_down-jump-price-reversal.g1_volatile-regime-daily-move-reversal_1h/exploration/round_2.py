def explore(data):
    import numpy as np, pandas as pd
    out = {}
    H = []
    G = []
    for coin, wins in data["bars"].items():
        # coin mean hourly return over all windows
        allr = pd.concat([ (b["close"].shift(-1)/b["close"]-1) for b in wins.values()])
        mu1 = allr.mean()
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            pos = b["postRebalance_current_allocation"].astype(float)
            r1 = c.shift(-1)/c - 1
            lr = np.log(c).diff()
            s = lr.rolling(168, min_periods=100).std()
            vr = s / s.rolling(720, min_periods=200).mean()
            f = b["forecast"].astype(float)
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            H.append(pd.DataFrame({"coin": coin, "gross": pos*r1, "drift": pos*mu1, "fee": fee,
                                   "absf": f.abs(), "vr": vr, "side": np.sign(pos)}))
            # slow version: forecast at grid bars held 24h
            idx = np.arange(0, len(b)-24, 24)
            r24 = c.shift(-24)/c - 1
            fs = f.iloc[idx].values/10
            fs_prev = np.r_[0, fs[:-1]]
            G.append(pd.DataFrame({"coin": coin, "w": w, "g24": fs*r24.iloc[idx].values,
                                   "turn24": np.abs(fs-fs_prev), "absf": np.abs(fs)*10,
                                   "vr": vr.iloc[idx].values, "r24": r24.iloc[idx].values,
                                   "fsgn": np.sign(fs)}))
    Hd = pd.concat(H).dropna(subset=["gross"])
    out["hourly_gross_drift_fee_mean"] = Hd[["gross","drift","fee"]].mean()*24
    Hd["fq"] = Hd.groupby("coin")["absf"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["hourly_by_absf_q_x24"] = Hd.groupby("fq")[["gross","fee"]].mean()*24
    Hd2 = Hd.dropna(subset=["vr"]).copy()
    Hd2["vq"] = pd.qcut(Hd2["vr"], 3, labels=False)
    out["hourly_by_volratio_t_x24"] = Hd2.groupby("vq")[["gross","fee"]].mean()*24
    out["hourly_by_side_x24"] = Hd.groupby("side")[["gross","fee"]].mean()*24
    Gd = pd.concat(G).dropna(subset=["g24"])
    out["slow24_mean_g_turn"] = pd.Series({"g24_mean": Gd["g24"].mean(),
        "t": Gd["g24"].mean()/(Gd["g24"].std()/np.sqrt(len(Gd))), "n": len(Gd),
        "turn_per_day": Gd["turn24"].mean(), "fee_at_0.001": Gd["turn24"].mean()*0.001})
    Gd["fq"] = Gd.groupby("coin")["absf"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["slow24_by_absf_q"] = Gd.groupby("fq").agg(g=("g24","mean"), n=("g24","size"), turn=("turn24","mean"))
    G2 = Gd.dropna(subset=["vr"]).copy(); G2["vq"] = pd.qcut(G2["vr"], 3, labels=False)
    out["slow24_by_vr"] = G2.groupby("vq").agg(g=("g24","mean"), n=("g24","size"),
                         sgn_ret=("r24", lambda x: 0))
    G2["sr"] = G2["fsgn"]*G2["r24"]
    out["slow24_signed_ret_by_vr_side"] = G2.groupby(["vq","fsgn"])["sr"].agg(["mean","count"])
    return out
