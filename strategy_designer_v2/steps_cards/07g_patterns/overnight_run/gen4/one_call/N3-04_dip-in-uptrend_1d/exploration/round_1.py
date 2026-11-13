def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df.copy()
            d["ts"] = pd.to_datetime(d["timestamp"])
            d["r"] = d["close"].pct_change()
            d["nr"] = d["r"].shift(-1)
            d["r20"] = d["close"].pct_change(20)
            d["r60"] = d["close"].pct_change(60)
            d["absm"] = d["r"].abs().rolling(60, min_periods=20).mean()
            d["z"] = d["r"] / d["absm"]
            d["vol20"] = d["r"].rolling(20).std()
            d["rng"] = (d["high"] - d["low"]) / d["close"]
            d["clv"] = (d["close"] - d["low"]) / (d["high"] - d["low"]).replace(0, np.nan)
            d["coin"] = coin; d["win"] = w
            d["wd"] = d["ts"].dt.weekday; d["yr"] = d["ts"].dt.year
            d["trend"] = (d["regime"] == "trending")
            rows.append(d[["coin","win","r","nr","r20","r60","z","vol20","rng","clv","wd","yr","trend","forecast"]])
    A = pd.concat(rows).dropna(subset=["nr","z"])
    A["ex"] = A["nr"] - A.groupby("coin")["nr"].transform("mean")
    def agg(g):
        x = g["ex"]
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan,
                          "hit": (g["nr"]>0).mean()})
    out = {}
    A["zb"] = pd.cut(A["z"], [-99,-2,-1,-0.5,0,0.5,1,2,99])
    out["z_by_trend"] = A.groupby(["trend","zb"]).apply(agg)
    out["fc_pos_by_coin"] = A[A.forecast>0].groupby("coin").apply(agg)
    out["fc_pos_by_year"] = A[A.forecast>0].groupby("yr").apply(agg)
    out["wd_all"] = A.groupby("wd").apply(agg)
    A["vq"] = A.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["dip_by_vol_trend"] = A[A.z < -1].groupby(["trend","vq"]).apply(agg)
    A["cb"] = pd.cut(A["clv"], [0,0.2,0.5,0.8,1.0], include_lowest=True)
    out["dip_by_clv"] = A[(A.z < -0.5)].groupby(["trend","cb"]).apply(agg)
    out["trend_vs_not"] = A.groupby("trend").apply(agg)
    return out
