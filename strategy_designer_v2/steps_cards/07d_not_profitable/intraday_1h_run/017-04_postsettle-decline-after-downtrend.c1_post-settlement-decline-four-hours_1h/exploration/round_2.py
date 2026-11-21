def explore(data):
    import numpy as np, pandas as pd
    out = {}
    eps = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True).copy()
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"]
            lr = np.log(cl).diff()
            vol = lr.rolling(168, min_periods=48).std()
            f72 = cl / cl.shift(72) - 1
            idx = np.where(ts.dt.hour.isin([23, 7, 15]))[0]
            for i in idx:
                r = {"coin": c, "w": w, "hour": int(ts.iloc[i].hour), "fc": b["forecast"].iloc[i + 1] if i + 1 < len(b) else np.nan,
                     "f72": f72.iloc[i], "vol": vol.iloc[i], "pos": b["postRebalance_current_allocation"].iloc[i]}
                for h in [1, 2, 4, 8, 16, 24]:
                    j = i + h
                    if j < len(b) and (ts.iloc[j] - ts.iloc[i]) == pd.Timedelta(hours=h):
                        r[f"r{h}"] = cl.iloc[j] / cl.iloc[i] - 1
                    else:
                        r[f"r{h}"] = np.nan
                eps.append(r)
    E = pd.DataFrame(eps)
    E = E[E["f72"].notna()]
    dn = E[E["f72"] < 0].copy()
    dn["dec"] = pd.qcut(dn["f72"].rank(method="first"), 5, labels=["q1_bigfall", "q2", "q3", "q4", "q5_smallfall"])
    g = dn.groupby("dec")
    res = g[[f"r{h}" for h in [1, 2, 4, 8, 16, 24]]].mean()
    res["n"] = g.size(); res["f72"] = g["f72"].mean(); res["vol"] = g["vol"].mean()
    out["down_by_fall_quintile"] = res
    up = E[E["f72"] >= 0]
    out["up_mean"] = up[[f"r{h}" for h in [1, 2, 4, 8, 16, 24]]].mean()
    out["all_mean"] = E[[f"r{h}" for h in [1, 2, 4, 8, 16, 24]]].mean()
    # by vol tercile within big falls
    big = dn[dn["dec"].isin(["q1_bigfall", "q2"])].copy()
    big["vt"] = pd.qcut(big["vol"].rank(method="first"), 3, labels=["lowvol", "mid", "highvol"])
    gb = big.groupby("vt")
    vv = gb[["r4", "r24"]].mean(); vv["n"] = gb.size(); vv["t_r4"] = gb["r4"].mean() / gb["r4"].std() * np.sqrt(gb.size())
    out["bigfall_by_vol"] = vv
    out["down_by_hour"] = dn.groupby("hour")[["r4", "r24"]].mean()
    # fee per episode in return units
    tr = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            tr.append(t)
    T = pd.concat(tr)
    out["comm_vs_pl"] = pd.Series({"median_comm": T["total_commission"].median(), "median_gross": T["profit_loss_percent"].median(), "mean_net_minus_gross": (T["net_profit_loss_percent"] - T["profit_loss_percent"]).mean()})
    return out
