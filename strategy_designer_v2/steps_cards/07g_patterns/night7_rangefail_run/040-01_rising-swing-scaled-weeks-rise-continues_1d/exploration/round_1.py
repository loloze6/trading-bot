import numpy as np
import pandas as pd
from scipy import stats

def _ct(x, day):
    x = np.asarray(x, float); m = x.mean(); n = len(x)
    d = pd.Series(x - m).groupby(np.asarray(day)).sum().values
    se = np.sqrt((d**2).sum()) / n
    return m / se if se > 0 else np.nan

def _cases(data, h):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            r1 = pd.Series(c).pct_change()
            ret20 = pd.Series(c).pct_change(20)
            ret5 = pd.Series(c).pct_change(5)
            sd20 = r1.rolling(20).std()
            sd60 = r1.rolling(60).std()
            z = ret20 / (sd20 * np.sqrt(20))
            z5 = ret5 / (sd20 * np.sqrt(5))
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for i in range(0, n - h, h):
                rows.append(dict(coin=coin, w=w, day=str(ts[i].date()), wd=ts[i].dayofweek, yr=ts[i].year,
                                 reg=b["regime"].iloc[i], fc=b["forecast"].iloc[i],
                                 r1=r1.iloc[i], z=z.iloc[i], z5=z5.iloc[i], ret20=ret20.iloc[i],
                                 volrel=(sd20 / sd60).iloc[i], sd20=sd20.iloc[i],
                                 fwd=c[i + h] / c[i] - 1))
    df = pd.DataFrame(rows)
    df["ex"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    return df

def _tab(df, col, q=5, y="ex"):
    d = df.dropna(subset=[col, y]).copy()
    d["bin"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
    out = d.groupby("bin").agg(n=(y, "size"), xmean=(col, "mean"), mean=(y, "mean"))
    out["t_day"] = [ _ct(g[y], g["day"]) for _, g in d.groupby("bin")]
    return out

def explore(data):
    res = {}
    d14 = _cases(data, 14)
    d14["rising"] = d14["reg"] == "unknown"
    ris = d14[d14["rising"]]; nr = d14[~d14["rising"]]
    res["14d rising: fwd excess by z quintile"] = _tab(ris, "z")
    res["14d not rising: fwd excess by z quintile"] = _tab(nr, "z")
    res["14d rising: by short 5d z quintile"] = _tab(ris, "z5")
    res["14d rising: by vol ratio sd20/sd60"] = _tab(ris, "volrel")
    res["14d all: by vol ratio"] = _tab(d14, "volrel")
    res["14d rising z>0: excess by year"] = ris[ris.z > 0].groupby("yr")["ex"].agg(["size", "mean"])
    d3 = _cases(data, 3)
    d3["rising"] = d3["reg"] == "unknown"
    res["3d all: fwd excess by 1d return decile"] = _tab(d3, "r1", 10)
    res["3d rising: by 1d return quintile"] = _tab(d3[d3.rising], "r1")
    res["3d not rising: by 1d return quintile"] = _tab(d3[~d3.rising], "r1")
    d1 = _cases(data, 1)
    g = d1.groupby("wd")["fwd"]
    res["1d next-day return by weekday"] = pd.DataFrame({"n": g.size(), "mean": g.mean(),
        "t": g.mean() / (g.std() / np.sqrt(g.size()))})
    # book daily
    days = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["w"] = w; days.append(x)
    D = pd.concat(days)
    bk = D.dropna(subset=["book_return"]).groupby(["w", "day"])[["book_return", "coin_return"]].mean()
    res["book by window: mean, sd, n"] = bk.groupby("w")["book_return"].agg(["mean", "std", "size"])
    q = bk["book_return"].quantile([0.02, 0.98]).values
    res["book worst 2% / best 2% days: mean coin ret"] = pd.DataFrame({
        "worst": [bk[bk.book_return <= q[0]]["book_return"].mean(), bk[bk.book_return <= q[0]]["coin_return"].mean()],
        "best": [bk[bk.book_return >= q[1]]["book_return"].mean(), bk[bk.book_return >= q[1]]["coin_return"].mean()]},
        index=["book", "coins"])
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): x = t.copy(); x["coin"] = coin; T.append(x)
    T = pd.concat(T)
    T["dur_d"] = T["duration_minutes"] / 1440
    T["fbin"] = pd.qcut(T["entry_forecast"], 4, labels=False, duplicates="drop")
    res["trades by entry forecast quartile"] = T.groupby("fbin").agg(n=("coin", "size"), f=("entry_forecast", "mean"),
        pnl=("net_profit_loss_percent", "mean"), dur=("dur_d", "mean"), win=("net_profit_loss_percent", lambda s: (s > 0).mean()))
    T["dbin"] = pd.qcut(T["dur_d"], 4, labels=False, duplicates="drop")
    res["trades by duration quartile"] = T.groupby("dbin").agg(n=("coin", "size"), dur=("dur_d", "mean"),
        pnl=("net_profit_loss_percent", "mean"))
    return res
