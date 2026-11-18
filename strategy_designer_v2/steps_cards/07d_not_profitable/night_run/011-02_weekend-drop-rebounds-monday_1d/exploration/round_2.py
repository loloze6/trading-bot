def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            b["wd"] = ts.dt.weekday.values
            b["year"] = ts.dt.year.values
            b["r1"] = b["close"].pct_change()
            b["nxt"] = b["close"].shift(-1) / b["close"] - 1
            b["nxt2"] = b["close"].shift(-2) / b["close"].shift(-1) - 1
            b["z"] = b["r1"] / b["r1"].rolling(20).std()
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["coin"] = coin; b["win"] = w
            rows.append(b[["coin","win","wd","year","r1","nxt","nxt2","z","ret20","pos"]])
    B = pd.concat(rows, ignore_index=True)
    S = B[B.wd == 6].dropna(subset=["z","nxt","nxt2"]).copy()
    S["zb"] = pd.cut(S.z, [-99,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,99])
    def agg(df, key, col):
        r = df.groupby(key)[col].agg(["count","mean","std"])
        r["t"] = r["mean"]/(r["std"]/np.sqrt(r["count"]))
        return r
    out["sun_z_bins_monday_ret"] = agg(S, "zb", "nxt")
    out["sun_z_bins_tuesday_ret"] = agg(S, "zb", "nxt2")
    # deep drops by 20d trend
    S["trend"] = np.where(S.ret20 < 0, "down20", "up20")
    S["side"] = np.where(S.z < 0, "drop", "rise")
    out["sun_side_trend_monday"] = S.groupby(["side","trend"])["nxt"].agg(["count","mean"])
    # correlation of -z with monday return, by side
    out["corr_negz_mon"] = pd.Series({
        "drops": np.corrcoef(-S[S.z<0].z, S[S.z<0].nxt)[0,1],
        "rises": np.corrcoef(-S[S.z>=0].z, S[S.z>=0].nxt)[0,1],
        "all": np.corrcoef(-S.z, S.nxt)[0,1]})
    # book deepest falls: book daily returns averaged
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            d["wd"] = pd.to_datetime(d["day"]).dt.weekday
            D.append(d)
    D = pd.concat(D, ignore_index=True)
    bk = D.groupby(["win","day"]).agg(br=("book_return","mean"), cr=("coin_return","mean"), wd=("wd","first")).dropna().reset_index()
    out["book_by_weekday"] = bk.groupby("wd")[["br","cr"]].agg(["mean","sum"])
    eq = (1 + bk.br).cumprod()
    dd = eq / eq.cummax() - 1
    out["book_dd"] = pd.Series({"maxdd": dd.min(), "worst5pct_days_mean": bk.br.quantile(0.01)})
    # book loss by year
    bk["year"] = pd.to_datetime(bk.day).dt.year
    out["book_by_year"] = bk.groupby("year").br.agg(["mean","sum"])
    return out
