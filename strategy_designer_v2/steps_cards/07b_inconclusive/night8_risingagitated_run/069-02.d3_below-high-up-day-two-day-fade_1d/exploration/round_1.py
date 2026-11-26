def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(20).std()
            hh = h.rolling(20).max()
            depth = (c / hh - 1) / sd
            tr60 = c / c.shift(60) - 1
            sd30 = r1.rolling(30).std()
            vrel = sd30 / sd30.expanding(30).median()
            fc = b["forecast"].astype(float)
            n = len(b)
            for H in (1, 2, 3, 5):
                fwd = c.shift(-H) / c - 1
                idx = np.arange(0, n, H)
                for i in idx:
                    rows.append(dict(coin=coin, w=w, H=H, pos=i, fwd=fwd.iat[i], up=r1.iat[i] > 0,
                                     depth=depth.iat[i], tr=tr60.iat[i], vrel=vrel.iat[i], fc=fc.iat[i],
                                     r1=r1.iat[i], ts=b["timestamp"].iat[i]))
    df = pd.DataFrame(rows).dropna(subset=["fwd"])
    drift = df.groupby(["coin", "H"])["fwd"].mean().rename("drift")
    df = df.join(drift, on=["coin", "H"])
    df["ex_short"] = -(df["fwd"] - df["drift"])
    df["tot_short"] = -df["fwd"]
    up = df[df["up"] & df["depth"].notna()].copy()
    def tstat(s):
        s = s.dropna(); return pd.Series({"mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))), "n": len(s)})
    out = {}
    out["by_H_up_all"] = up.groupby("H")["ex_short"].apply(tstat).unstack()
    nonup = df[~df["up"]]
    out["by_H_notup"] = nonup.groupby("H")["ex_short"].apply(tstat).unstack()
    u2 = up[up.H == 2].copy()
    u2["dq"] = pd.qcut(u2["depth"], 5, labels=["deepest", "q2", "q3", "q4", "shallow"])
    out["H2_by_depth_q"] = u2.groupby("dq")["ex_short"].apply(tstat).unstack()
    for H in (1, 3, 5):
        uh = up[up.H == H].copy()
        uh["dq"] = pd.qcut(uh["depth"], 5, labels=["deepest", "q2", "q3", "q4", "shallow"])
        out[f"H{H}_by_depth_q"] = uh.groupby("dq")["ex_short"].apply(tstat).unstack()
    out["H2_by_coin"] = u2.groupby("coin")["ex_short"].apply(tstat).unstack()
    out["H2_by_window"] = u2.groupby("w")["ex_short"].apply(tstat).unstack()
    u2["trend"] = np.where(u2.tr > 0.10, "rising", np.where(u2.tr < -0.10, "falling", "choppy"))
    u2.loc[u2.tr.isna(), "trend"] = "na"
    out["H2_by_trend"] = u2.groupby("trend")["ex_short"].apply(tstat).unstack()
    out["H2_by_trend_deepest"] = u2[u2.dq.isin(["deepest", "q2"])].groupby("trend")["ex_short"].apply(tstat).unstack()
    u2["agit"] = np.where(u2.vrel > 1, "agitated_proxy", "calm_proxy")
    out["H2_by_agit_proxy"] = u2[u2.vrel.notna()].groupby("agit")["ex_short"].apply(tstat).unstack()
    u2["r1q"] = pd.qcut(u2["r1"], 3, labels=["small_up", "mid_up", "big_up"])
    out["H2_by_upsize"] = u2.groupby("r1q")["ex_short"].apply(tstat).unstack()
    out["H2_corr_depth_ex"] = float(np.corrcoef(u2["depth"], u2["ex_short"])[0, 1])
    u2["year"] = pd.to_datetime(u2["ts"]).dt.year
    out["H2_by_year"] = u2.groupby("year")["ex_short"].apply(tstat).unstack()
    out["H2_tot_by_trend"] = u2.groupby("trend")["tot_short"].apply(tstat).unstack()
    return out
