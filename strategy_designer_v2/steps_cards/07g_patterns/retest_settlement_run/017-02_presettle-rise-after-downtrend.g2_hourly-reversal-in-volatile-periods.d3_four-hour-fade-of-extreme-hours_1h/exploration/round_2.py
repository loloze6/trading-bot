def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, df in ws.items():
            d = df[["timestamp","close"]].copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d["coin"] = coin; d["w"] = w; d["pos"] = np.arange(len(d))
            c = d["close"]
            d["r1"] = c.pct_change()
            d["f24"] = c.shift(-24)/c - 1
            d["f12"] = c.shift(-12)/c - 1
            d["p24"] = c/c.shift(24) - 1
            d["p12"] = c/c.shift(12) - 1
            d["p48"] = c/c.shift(48) - 1
            d["vol24"] = d["r1"].rolling(24).std()
            d["vol720"] = d["r1"].rolling(720, min_periods=240).std()
            d["vratio"] = d["vol24"]/d["vol720"]
            d["p24z"] = d["p24"]/(d["vol720"]*np.sqrt(24))
            d["hour"] = d["ts"].dt.hour; d["year"] = d["ts"].dt.year
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    S = A[A["pos"] % 24 == 0].copy()
    S["ex"] = S["f24"] - S.groupby("coin")["f24"].transform("mean")
    S = S.dropna(subset=["ex","p24z","vratio"])
    out["usual_24h_move_pct"] = round(S["f24"].std()*100, 3)
    out["n_cases_24h"] = len(S)
    # quintiles of p24z: mean ex, signed reversal
    S["q"] = pd.qcut(S["p24z"], 10, labels=False)
    g = S.groupby("q")
    out["p24z_deciles"] = pd.DataFrame({"p24z_mean": g["p24z"].mean(), "ex_bp": g["ex"].mean()*1e4,
        "t": g["ex"].mean()/(g["ex"].std()/np.sqrt(g["ex"].count())), "n": g["ex"].count()}).round(3)
    # by coin and by year: slope of ex on p24z
    def sl(s, x="p24z"):
        lr = stats.linregress(s[x], s["ex"]); 
        top = s[s[x].abs() >= s[x].abs().quantile(0.8)]
        sg = -np.sign(top[x])*top["ex"]
        return pd.Series({"slope_bp": lr.slope*1e4, "t": lr.slope/lr.stderr, "top20_fade_bp": sg.mean()*1e4, "n": len(s)})
    out["p24z_by_coin"] = S.groupby("coin").apply(sl).round(3)
    out["p24z_by_year"] = S.groupby("year").apply(sl).round(3)
    # vol regime: by vratio tercile
    S["vt"] = pd.qcut(S["vratio"], 3, labels=["low","mid","high"])
    out["p24z_by_volratio"] = S.groupby("vt").apply(sl).round(3)
    # interaction product
    S["px"] = S["p24z"]*S["vratio"]
    out["p24z_x_vratio"] = sl(S, "px").round(3)
    # hours 21-22 effect by year and coin
    H = A.dropna(subset=["r1"]).copy()
    H["h2122"] = H["hour"].isin([21,22])
    def hd(s):
        a = s.loc[s["h2122"],"r1"]; b = s.loc[~s["h2122"],"r1"]
        t = stats.ttest_ind(a,b,equal_var=False)
        return pd.Series({"diff_bp": (a.mean()-b.mean())*1e4, "t": t.statistic, "n21_22": len(a)})
    out["h2122_by_year"] = H.groupby("year").apply(hd).round(3)
    out["h2122_by_coin"] = H.groupby("coin").apply(hd).round(3)
    # trades: mean pl before fees and after
    tr = pd.concat([df for ws in data["trades"].values() for df in ws.values()], ignore_index=True)
    out["trades"] = pd.Series({"n": len(tr), "mean_pl_pct": tr["profit_loss_percent"].mean(),
        "mean_net_pct": tr["net_profit_loss_percent"].mean(), "mean_dur_h": tr["duration_minutes"].mean()/60}).round(4)
    return out
