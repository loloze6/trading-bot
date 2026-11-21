import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rawcol = "debug_info.components.cloud_pos.last_history_value"
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            ts = pd.to_datetime(df["timestamp"])
            hi = df["high"]; lo = df["low"]
            ten = (hi.rolling(9).max()+lo.rolling(9).min())/2
            kij = (hi.rolling(26).max()+lo.rolling(26).min())/2
            sa = ((ten+kij)/2).shift(26); sb = ((hi.rolling(52).max()+lo.rolling(52).min())/2).shift(26)
            top = np.maximum(sa, sb); bot = np.minimum(sa, sb)
            dist = (df["close"]/top - 1)*100
            thick = (top-bot)/df["close"]*100
            ma = df["close"].rolling(52).mean()
            madist = (df["close"]/ma-1)*100
            for h in [5, 10, 26, 52]:
                for i in range(0, n-h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=ts[i].year,
                        fc=df["forecast"].iloc[i],
                        raw=df[rawcol].iloc[i] if rawcol in df else np.nan,
                        dist=dist.iloc[i], thick=thick.iloc[i], madist=madist.iloc[i],
                        ret=c[i+h]/c[i]-1))
    R = pd.DataFrame(rows)
    R["ex"] = R["ret"] - R.groupby(["coin","h"])["ret"].transform("mean")
    def slope_t(d, x="fc"):
        d = d[[x,"ex"]].dropna()
        if len(d) < 10 or d[x].std() == 0: return pd.Series({"n":len(d),"t":np.nan,"slope":np.nan})
        r = stats.linregress(d[x], d["ex"])
        return pd.Series({"n":len(d),"t":r.slope/r.stderr,"slope":r.slope})
    out = {}
    out["by_h_fc"] = R.groupby("h").apply(slope_t)
    out["by_h_rawcol"] = R.groupby("h").apply(lambda d: slope_t(d,"raw"))
    out["by_h_dist_recomputed"] = R.groupby("h").apply(lambda d: slope_t(d,"dist"))
    out["by_h_madist"] = R.groupby("h").apply(lambda d: slope_t(d,"madist"))
    R26 = R[R.h==26]
    out["coin_26"] = R26.groupby("coin").apply(slope_t)
    out["year_26"] = R26.groupby("year").apply(slope_t)
    R26 = R26.copy()
    R26["side"] = np.sign(R26["fc"])
    out["side_26_mean_ex"] = R26.groupby("side")["ex"].agg(["count","mean","std"])
    out["side_26_slope"] = R26.groupby("side").apply(slope_t)
    R26["q"] = pd.qcut(R26["fc"].rank(method="first"), 5, labels=False)
    out["quint_26"] = R26.groupby("q").agg(n=("ex","size"), fc=("fc","mean"), ex=("ex","mean"), ret=("ret","mean"))
    R26["thq"] = pd.qcut(R26["thick"].rank(method="first"), 3, labels=False)
    out["thick_tercile_26"] = R26.groupby("thq").apply(slope_t)
    out["corr_fc_raw_dist_ma"] = R26[["fc","raw","dist","madist"]].corr()
    R52 = R[R.h==52].copy(); R52["side"]=np.sign(R52["fc"])
    out["side_52_mean_ex"] = R52.groupby("side")["ex"].agg(["count","mean","std"])
    out["coin_52"] = R52.groupby("coin").apply(slope_t)
    return out
