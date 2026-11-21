import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            d = df[["timestamp","close","postRebalance_current_allocation"]].copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.reset_index(drop=True)
            c = d["close"]
            d["r1"] = c.shift(-1)/c - 1
            d["r2"] = c.shift(-2)/c - 1
            d["p24"] = c/c.shift(24) - 1
            lr = np.log(c).diff()
            d["vol24"] = lr.rolling(24).std()
            d["z24"] = d["p24"]/(d["vol24"]*np.sqrt(24))
            d["z1"] = lr/d["vol24"]
            d["vol_lvl"] = d["vol24"]/d["vol24"].rolling(720, min_periods=200).median()
            d["hour"] = d["ts"].dt.hour; d["year"] = d["ts"].dt.year
            d["coin"] = coin; d["win"] = w
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["ex1"] = A["r1"] - A.groupby("coin")["r1"].transform("mean")
    A["ex2"] = A["r2"] - A.groupby("coin")["r2"].transform("mean")
    out = {}
    def tstat(s): return s.mean()/(s.std()/np.sqrt(s.count()))
    H = A[A["hour"]==21].dropna(subset=["ex2","z24"])
    # 21:00 bar 2h excess by coin and year
    out["h21_ex2_by_coin"] = H.groupby("coin")["ex2"].agg(lambda s: pd.Series({"bp":s.mean()*1e4})).to_frame("bp").join(H.groupby("coin")["ex2"].apply(tstat).rename("t"))
    out["h21_ex2_by_year"] = H.groupby("year")["ex2"].apply(lambda s: s.mean()*1e4).to_frame("bp").join(H.groupby("year")["ex2"].apply(tstat).rename("t")).join(H.groupby("year").size().rename("n"))
    # 21:00 slope on z24 by coin and year
    def slp(s):
        r = stats.linregress(s["z24"], s["ex2"]); return pd.Series({"slope_bp":r.slope*1e4,"t":r.slope/r.stderr,"n":len(s)})
    out["h21_slope_by_coin"] = H.groupby("coin").apply(slp)
    out["h21_slope_by_year"] = H.groupby("year").apply(slp)
    # 21:00 ex2 by z24 quintile
    H = H.copy(); H["q"] = pd.qcut(H["z24"],5,labels=False)
    out["h21_ex2_by_z24_q"] = H.groupby("q")["ex2"].apply(lambda s: s.mean()*1e4).to_frame("bp").join(H.groupby("q")["ex2"].apply(tstat).rename("t"))
    # 14:00 slope by year (US open continuation)
    H14 = A[A["hour"]==14].dropna(subset=["ex2","z24"])
    out["h14_slope_by_year"] = H14.groupby("year").apply(slp)
    out["h14_slope_by_coin"] = H14.groupby("coin").apply(slp)
    # 1h reversal: slope of ex1 on z1 by vol level tercile and by coin
    B = A.dropna(subset=["ex1","z1","vol_lvl"]).copy()
    B["vq"] = pd.qcut(B["vol_lvl"],3,labels=False)
    def slp1(s):
        r = stats.linregress(s["z1"], s["ex1"]); return pd.Series({"slope_bp":r.slope*1e4,"t":r.slope/r.stderr,"n":len(s)})
    out["rev1h_by_vol_tercile"] = B.groupby("vq").apply(slp1)
    out["rev1h_by_coin"] = B.groupby("coin").apply(slp1)
    out["rev1h_by_year"] = B.groupby("year").apply(slp1)
    # hours 20-21 1h excess by year
    C = A[A["hour"].isin([20,21])].dropna(subset=["ex1"])
    out["h20_21_ex1_by_year"] = C.groupby("year")["ex1"].apply(lambda s: s.mean()*1e4).to_frame("bp").join(C.groupby("year")["ex1"].apply(tstat).rename("t"))
    return out
