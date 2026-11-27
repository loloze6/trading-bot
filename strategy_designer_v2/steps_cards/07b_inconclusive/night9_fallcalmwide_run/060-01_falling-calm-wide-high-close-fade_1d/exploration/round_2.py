import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        rets = np.concatenate([df["close"].values[1:]/df["close"].values[:-1]-1 for df in wins.values()])
        mu = np.nanmean(rets); sd = np.nanstd(rets)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; h = df["high"].values; l = df["low"].values; o = df["open"].values
            r = pd.Series(c).pct_change()
            vol = r.rolling(30).std().values
            width = ((h-l)/c)/vol
            loc = np.where(h>l, (c-l)/(h-l), np.nan)
            body = np.where(h>l, (c-o)/(h-l), np.nan)
            fc = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            ret5 = pd.Series(c).pct_change(5).values
            n = len(df)
            for t in range(n-1):
                if not (fc[t] < 0): continue
                u1 = -(c[t+1]/c[t]-1-mu)
                rows.append(dict(coin=coin, w=w, day=ts.iloc[t].normalize(), u1=u1, u1s=u1/sd,
                                 width=width[t], loc=loc[t], body=body[t], f=-fc[t],
                                 ret1=r.iloc[t]/vol[t], ret5=ret5[t]))
    C = pd.DataFrame(rows).dropna(subset=["u1","width","loc"])
    def tday(x, col="u1"):
        if len(x) < 3: return (np.nan, np.nan, len(x))
        m = x[col].mean(); d = (x[col]-m).groupby(x["day"]).sum()
        se = np.sqrt((d**2).sum())/len(x)
        return (m, m/se, len(x))
    out = {}
    def sl(xc):
        s = stats.linregress(C[xc], C["u1"]); return f"slope {s.slope:.5f} t {s.slope/s.stderr:.2f} n {len(C)}"
    out["slope_on_loc"] = sl("loc")
    out["slope_on_width"] = sl("width")
    out["slope_on_body"] = sl("body")
    out["slope_on_ret1_in_sd"] = sl("ret1")
    out["slope_on_ret5"] = sl("ret5")
    out["by_window"] = pd.DataFrame({k: tday(g) for k,g in C.groupby("w")}, index=["mean","t","n"]).T
    C["bq"] = pd.qcut(C["body"], 3, labels=["low","mid","high"])
    out["by_body"] = pd.DataFrame({str(k): tday(g) for k,g in C.groupby("bq")}, index=["mean","t","n"]).T
    C["r5"] = pd.qcut(C["ret5"], 3, labels=["low","mid","high"])
    out["by_ret5"] = pd.DataFrame({str(k): tday(g) for k,g in C.groupby("r5")}, index=["mean","t","n"]).T
    out["share_positive"] = float((C.u1>0).mean())
    out["median_u1"] = float(C.u1.median())
    out["strength"] = float(C.u1s.mean())
    return out
