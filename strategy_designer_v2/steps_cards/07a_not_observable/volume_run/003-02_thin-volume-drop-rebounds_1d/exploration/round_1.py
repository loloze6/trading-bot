import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    ev = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float); v = df["volume"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20).std()
            z = r / vol.shift(1)
            z2 = r / vol
            vr = v / v.rolling(30).mean()
            fwd = c.shift(-5) / c - 1
            yr = pd.to_datetime(df["timestamp"]).dt.year
            fc = df["forecast"].astype(float)
            for i in range(len(df)):
                rows.append((coin, w, yr.iloc[i], z.iloc[i], z2.iloc[i], vr.iloc[i], fwd.iloc[i], fc.iloc[i]))
    d = pd.DataFrame(rows, columns=["coin","w","year","z","z2","vr","fwd","fc"])
    d = d.dropna(subset=["z2","vr"])
    d["fall"] = d["z2"] <= -2
    d["thin"] = d["vr"] <= 0.5
    d["both"] = d["fall"] & d["thin"]
    d["fc_on"] = d["fc"] > 0
    out = {}
    out["totals"] = pd.Series({"bars": len(d), "fall<=-2": d.fall.sum(), "vr<=0.5": d.thin.sum(),
                               "both": d.both.sum(), "forecast>0": d.fc_on.sum(),
                               "share_fall": d.fall.mean(), "share_thin": d.thin.mean(),
                               "share_thin_given_fall": d.loc[d.fall,"thin"].mean(),
                               "corr_z_vr": d[["z2","vr"]].corr().iloc[0,1]})
    out["per_coin"] = d.groupby("coin")[["fall","thin","both","fc_on"]].sum()
    out["per_year"] = d.groupby("year")[["fall","thin","both","fc_on"]].sum()
    out["vr_on_falls_quantiles"] = d.loc[d.fall,"vr"].quantile([0.05,0.1,0.25,0.5,0.75,0.9])
    out["vr_all_quantiles"] = d["vr"].quantile([0.01,0.05,0.1,0.25,0.5])
    # 5-day outcome dispersion after sharp falls
    m5 = d["fwd"].mean()
    f = d.loc[d.fall,"fwd"].dropna() - m5
    out["falls_fwd5_excess"] = pd.Series({"n": len(f), "mean": f.mean(), "sd": f.std(),
                                          "t": f.mean()/(f.std()/np.sqrt(len(f)))})
    # falls split by volume ratio tercile below/above median
    ff = d.loc[d.fall].dropna(subset=["fwd"]).copy()
    ff["vr_bin"] = pd.cut(ff["vr"], [0,0.5,0.75,1.0,1.5,100])
    out["falls_by_vr_bin"] = ff.groupby("vr_bin")["fwd"].agg(["count","mean","std"])
    return out
