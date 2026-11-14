def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df.copy()
            d["ts"] = pd.to_datetime(d["timestamp"])
            d["r"] = d["close"].pct_change()
            d["nr"] = d["r"].shift(-1)
            d["nr3"] = d["close"].shift(-3)/d["close"] - 1
            d["r20"] = d["close"].pct_change(20)
            d["r60"] = d["close"].pct_change(60)
            d["absm"] = d["r"].abs().rolling(60, min_periods=20).mean()
            d["z"] = d["r"] / d["absm"]
            d["zp"] = d["z"].shift(1)
            d["vol20"] = d["r"].rolling(20).std()
            d["vr"] = d["vol20"] / d["r"].rolling(60, min_periods=40).std()
            d["dd60"] = d["close"]/d["close"].rolling(60, min_periods=20).max() - 1
            d["vz"] = d["volume"]/d["volume"].rolling(20, min_periods=10).mean()
            d["coin"] = coin; d["win"] = w
            d["wd"] = d["ts"].dt.weekday; d["yr"] = d["ts"].dt.year
            d["trend"] = (d["regime"] == "trending")
            d["i"] = np.arange(len(d))
            d["bv"] = d["postRebalance_total_value"]
            d["br_next"] = d["bv"].shift(-1)/d["bv"] - 1
            rows.append(d)
    A = pd.concat(rows).dropna(subset=["nr","z"])
    A["ex"] = A["nr"] - A.groupby("coin")["nr"].transform("mean")
    A["ex3"] = A["nr3"] - 3*A.groupby("coin")["nr"].transform("mean")
    def agg(g, col="ex"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan,
                          "hit": (x>0).mean()})
    out = {}
    A["vq"] = A.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    hv = A[(A.z < -1) & (~A.trend) & (A.vq == 2)]
    out["hvdip_nontrend_by_coin"] = hv.groupby("coin").apply(agg)
    out["hvdip_nontrend_by_year"] = hv.groupby("yr").apply(agg)
    # drawdown depth for big drops outside trend
    A["ddb"] = pd.cut(A["dd60"], [-1,-0.4,-0.25,-0.1,0.01])
    out["bigdrop_by_dd60"] = A[A.z < -1].groupby(["trend","ddb"]).apply(agg)
    # big up days outside trend (fade?)
    out["bigup_nontrend_vq"] = A[(A.z > 1) & (~A.trend)].groupby("vq").apply(agg)
    # volume on big drops
    A["vzb"] = pd.cut(A["vz"], [0,1,1.5,2.5,99])
    out["bigdrop_by_volume"] = A[A.z < -1].groupby(["trend","vzb"]).apply(agg)
    # two consecutive drops
    A["two"] = (A.z < -0.5) & (A.zp < -0.5)
    out["consec_drop"] = A.groupby(["trend","two"]).apply(agg)
    # weekday robustness: Monday/Wednesday vs rest by year half
    A["wdg"] = A["wd"].map({0:"Mon",2:"Wed",4:"Fri"}).fillna("other")
    out["wd_by_trend"] = A.groupby(["trend","wdg"]).apply(agg)
    out["wd_by_coin_MonWed"] = A[A.wd.isin([0,2])].groupby("coin").apply(agg)
    # 3-day non-overlapping after big drops, non-trend
    sub = A[(A.i % 3 == 0)]
    out["3d_nonoverlap_bigdrop"] = sub[sub.z < -1].groupby(["trend","vq"]).apply(lambda g: agg(g,"ex3"))
    # book: largest next-day book gains/losses — preceding context
    B = A.dropna(subset=["br_next"])
    B = B[B["postRebalance_current_allocation"].abs() > 0]
    q = B["br_next"].quantile([0.05,0.95])
    B["tail"] = np.where(B.br_next<=q.iloc[0],"loss5", np.where(B.br_next>=q.iloc[1],"gain5","mid"))
    out["book_tails_context"] = B.groupby("tail")[["z","vr","dd60","vz","forecast","r20"]].mean()
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    T["dur_d"] = T["duration_minutes"]/1440
    T["db"] = pd.cut(T["dur_d"], [0,1.5,3.5,7.5,999])
    out["trades_by_dur"] = T.groupby("db")["net_profit_loss_percent"].agg(["count","mean","median"])
    return out
