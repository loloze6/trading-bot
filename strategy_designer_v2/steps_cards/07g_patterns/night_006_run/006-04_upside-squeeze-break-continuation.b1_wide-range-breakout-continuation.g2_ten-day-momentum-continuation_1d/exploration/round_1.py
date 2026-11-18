import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    H = 10
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; h = df["high"].values; l = df["low"].values; v = df["volume"].values
            n = len(df)
            s = pd.Series(c)
            ret10 = s.pct_change(10).values
            ret1 = s.pct_change(1).values
            hh20 = pd.Series(h).rolling(20).max().shift(1).values
            ll20 = pd.Series(l).rolling(20).min().shift(1).values
            width20 = (hh20 - ll20) / c
            pos20 = (c - ll20) / (hh20 - ll20)
            vol20 = pd.Series(np.log(c)).diff().rolling(20).std().values
            vol60 = pd.Series(np.log(c)).diff().rolling(60).std().values
            vr = pd.Series(v).rolling(10).mean().values / pd.Series(v).rolling(60).mean().values
            for i in range(0, n - H, H):
                fr = c[i + H] / c[i] - 1
                rows.append(dict(coin=coin, w=w, fc=df["forecast"].iloc[i],
                                 alloc=df["postRebalance_current_allocation"].iloc[i],
                                 ret10=ret10[i], ret1=ret1[i], pos20=pos20[i], width20=width20[i],
                                 vol20=vol20[i], volratio=vol20[i] / vol60[i] if vol60[i] else np.nan,
                                 vr=vr[i], wd=pd.Timestamp(df["timestamp"].iloc[i]).weekday(),
                                 year=pd.Timestamp(df["timestamp"].iloc[i]).year, fr=fr))
    g = pd.DataFrame(rows)
    g["ex"] = g["fr"] - g.groupby("coin")["fr"].transform("mean")
    g["absfr"] = g["fr"].abs()
    out = {}
    def qtab(col, target="ex", q=5):
        d = g.dropna(subset=[col, target]).copy()
        d["q"] = pd.qcut(d[col].rank(method="first"), q, labels=False)
        t = d.groupby("q")[target].agg(["mean", "count"])
        t["t"] = d.groupby("q")[target].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
        return t
    out["fc_quint_ex"] = qtab("fc")
    out["ret10_quint_ex"] = qtab("ret10")
    out["pos20_quint_ex"] = qtab("pos20")
    out["ret1_quint_ex"] = qtab("ret1")
    out["volratio_quint_ex"] = qtab("volratio")
    out["volratio_quint_abs"] = qtab("volratio", "absfr")
    out["width_quint_abs"] = qtab("width20", "absfr")
    out["vr_quint_abs"] = qtab("vr", "absfr")
    out["vol20_quint_ex"] = qtab("vol20")
    # per-coin slope t of ex on fc
    pc = {}
    for coin, d in g.dropna(subset=["fc"]).groupby("coin"):
        r = stats.linregress(d["fc"], d["ex"]); pc[coin] = (r.slope, r.slope / r.stderr, len(d))
    out["percoin_fc_slope"] = pd.DataFrame(pc, index=["slope", "t", "n"]).T
    pcy = {}
    for y, d in g.dropna(subset=["fc"]).groupby("year"):
        r = stats.linregress(d["fc"], d["ex"]); pcy[y] = (r.slope / r.stderr, len(d))
    out["year_fc_slope_t"] = pd.DataFrame(pcy, index=["t", "n"]).T
    # book: daily
    dr = []
    for coin, wins in days.items():
        for w, d in wins.items():
            b = bars[coin][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            a = b.groupby("day")["postRebalance_current_allocation"].last()
            dd = d.copy(); dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd["pos_prev"] = dd["day"].map(a).shift(1).values
            dd["coin"] = coin; dd["w"] = w
            dr.append(dd)
    D = pd.concat(dr).dropna(subset=["book_return", "coin_return"])
    D["cm"] = D.groupby("coin")["coin_return"].transform("mean")
    out["book_mean_daily"] = D["book_return"].mean()
    out["book_market_part"] = (D["pos_prev"] * D["cm"]).mean()
    out["mean_pos"] = D["pos_prev"].mean()
    out["share_long_days"] = (D["pos_prev"] > 0).mean()
    D["posq"] = pd.qcut(D["pos_prev"].rank(method="first"), 5, labels=False)
    out["book_by_posq"] = D.groupby("posq").agg(pos=("pos_prev", "mean"), coin=("coin_return", "mean"), book=("book_return", "mean"))
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    wt = D.groupby("wd")["coin_return"].agg(["mean", "count", "std"]); wt["t"] = wt["mean"] / (wt["std"] / np.sqrt(wt["count"]))
    out["coin_by_weekday"] = wt
    out["book_by_coin"] = D.groupby("coin")[["book_return", "coin_return"]].mean()
    return out
