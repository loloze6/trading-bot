import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    H = 40
    drift = {}; usual = {}
    for coin, ws in bars.items():
        r = []
        for w, df in ws.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                r.append(c[i+H]/c[i]-1)
        drift[coin] = np.mean(r); usual[coin] = np.std(r, ddof=1)
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            lr = np.log(df["close"]).diff()
            vol20 = lr.rolling(20).std() * np.sqrt(365)
            ret20 = df["close"].pct_change(20)
            idx = np.where((df["regime"] == "trending").values)[0]
            for i in idx:
                rec = {"coin": coin, "window": w, "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                       "forecast": df["forecast"].iloc[i], "vol20": vol20.iloc[i], "ret20": ret20.iloc[i],
                       "pos": i}
                for h in (10, 20, 40, 60):
                    if i + h < len(c):
                        rec[f"adj{h}"] = (c[i+h]/c[i]-1) - drift[coin]*h/H
                rows.append(rec)
    d = pd.DataFrame(rows)
    d40 = d.dropna(subset=["adj40"])
    def summ(g):
        x = g["adj40"]
        return pd.Series({"n": len(x), "mean": x.mean(), "median": x.median(),
                          "t": x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "share_up": (x > 0).mean()})
    out = {}
    out["all"] = summ(d40)
    out["by_coin"] = d40.groupby("coin").apply(summ)
    out["by_year"] = d40.groupby("year").apply(summ)
    d40 = d40.copy()
    d40["fc_q"] = pd.qcut(d40["forecast"].rank(method="first"), 3, labels=["low_fc", "mid", "high_fc"])
    out["by_forecast_tercile"] = d40.groupby("fc_q").apply(summ)
    dv = d40.dropna(subset=["vol20"]).copy()
    dv["vol_q"] = pd.qcut(dv["vol20"].rank(method="first"), 3, labels=["calm", "mid", "violent"])
    out["by_vol20_tercile"] = dv.groupby("vol_q").apply(summ)
    dr = d40.dropna(subset=["ret20"]).copy()
    dr["r_q"] = pd.qcut(dr["ret20"].rank(method="first"), 3, labels=["low_ret20", "mid", "high_ret20"])
    out["by_ret20_tercile"] = dr.groupby("r_q").apply(summ)
    cors = {}
    for col in ["forecast", "vol20", "ret20"]:
        z = d40.dropna(subset=[col])
        s = stats.spearmanr(z[col], z["adj40"])
        cors[col] = s.correlation
        cors[col + "_p"] = s.pvalue
    out["spearman_with_adj40"] = pd.Series(cors)
    hz = {}
    for h in (10, 20, 40, 60):
        x = d[f"adj{h}"].dropna()
        hz[f"h{h}_n"] = len(x); hz[f"h{h}_mean"] = x.mean(); hz[f"h{h}_t"] = x.mean()/(x.std(ddof=1)/np.sqrt(len(x)))
    out["horizons"] = pd.Series(hz)
    out["vol_by_coin_corr"] = dv.groupby("coin").apply(lambda g: stats.spearmanr(g["vol20"], g["adj40"]).correlation if len(g) > 4 else np.nan)
    out["position_in_window"] = pd.Series({"median_pos": d["pos"].median(), "n_all": len(d), "n_with40": len(d40)})
    return out
