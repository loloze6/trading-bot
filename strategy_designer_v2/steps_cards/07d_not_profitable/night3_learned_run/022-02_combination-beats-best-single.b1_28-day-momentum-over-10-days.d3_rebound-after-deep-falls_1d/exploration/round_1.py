import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin in bars:
        allw = []
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            for i in range(0, n - 10, 10):
                r = c[i+10]/c[i]-1
                r5 = c[i+5]/c[i]-1 if i+5 < n else np.nan
                past28 = c[i]/c[i-28]-1 if i >= 28 else np.nan
                past10 = c[i]/c[i-10]-1 if i >= 10 else np.nan
                past60 = c[i]/c[i-60]-1 if i >= 60 else np.nan
                rows.append(dict(coin=coin, w=w, i=i, r=r,
                    f=b["forecast"].iloc[i],
                    alloc=b["postRebalance_current_allocation"].iloc[i],
                    fall28=b.get("debug_info.components.fall28.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                    low60=b.get("debug_info.components.near_low60.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                    p28=past28, p10=past10, p60=past60,
                    vol=pd.Series(c[:i+1]).pct_change().tail(20).std() if i >= 20 else np.nan))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby("coin")["r"].transform("mean")
    df["ex"] = df["r"] - df["drift"]
    out = {}
    def tab(col, q=5):
        d = df.dropna(subset=[col]).copy()
        d["bin"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        g = d.groupby("bin").agg(n=("ex","size"), mean_x=(col,"mean"), ex=("ex","mean"), tot=("r","mean"), sd=("ex","std"))
        g["t"] = g["ex"]/(g["sd"]/np.sqrt(g["n"]))
        return g
    out["by_p28"] = tab("p28"); out["by_p10"] = tab("p10"); out["by_p60"] = tab("p60")
    out["by_low60_raw"] = tab("low60"); out["by_vol"] = tab("vol")
    df["fpos"] = df["f"] > 0
    out["by_forecast_on"] = df.groupby("fpos").agg(n=("ex","size"), ex=("ex","mean"), tot=("r","mean"), alloc=("alloc","mean"))
    # interaction: p28 sign x p60 sign
    d = df.dropna(subset=["p28","p60"])
    out["p28neg_by_p60sign"] = d[d.p28<0].groupby(d.p60>0).agg(n=("ex","size"), ex=("ex","mean"), tot=("r","mean"))
    out["by_year_on"] = df.assign(y=lambda x: x.coin).groupby(["coin","fpos"]).agg(n=("ex","size"), ex=("ex","mean")).unstack()
    # book daily: drift vs timing, deepest fall
    br = []
    for coin in days:
        for w, dd in days[coin].items():
            dd = dd.copy(); dd["coin"]=coin; dd["w"]=w; br.append(dd)
    D = pd.concat(br)
    out["book_vs_coin"] = pd.Series({"book_mean": D.book_return.mean(), "coin_mean": D.coin_return.mean(),
        "corr": D[["book_return","coin_return"]].corr().iloc[0,1]})
    out["book_by_window"] = D.groupby("w").agg(book=("book_return","mean"), coin=("coin_return","mean"))
    out["ranges_low60_fall28"] = df[["fall28","low60","p28"]].describe()
    return out
