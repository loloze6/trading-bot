import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    out = {}
    def grid_rows(h, lb):
        rows = []
        for coin, ws in bars.items():
            # coin mean h-return over all windows (grid)
            allr = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c)-h, h):
                    allr.append(c[i+h]/c[i]-1)
            mu = np.mean(allr); sd = np.std(allr, ddof=1)
            for w, df in ws.items():
                c = df["close"].reset_index(drop=True)
                lr = np.log(c).diff()
                mx = c.shift(1).rolling(lb, min_periods=lb).max()
                mn = c.shift(1).rolling(lb, min_periods=lb).min()
                r5 = c/c.shift(5)-1; r20 = c/c.shift(20)-1; r1 = c/c.shift(1)-1
                vol20 = lr.rolling(20).std()
                vol60 = lr.rolling(60).std()
                rng = np.log(mx/mn)
                for i in range(0, len(c)-h, h):
                    rows.append(dict(coin=coin, w=w, fwd=c[i+h]/c[i]-1, ex=(c[i+h]/c[i]-1-mu)/sd,
                        exraw=c[i+h]/c[i]-1-mu,
                        dhi=np.log(c[i]/mx[i]) if pd.notna(mx[i]) else np.nan,
                        dlo=np.log(c[i]/mn[i]) if pd.notna(mn[i]) else np.nan,
                        rng=rng[i], r1=r1[i], r5=r5[i], r20=r20[i],
                        vr=vol20[i]/vol60[i] if pd.notna(vol60[i]) else np.nan, vol20=vol20[i]))
        return pd.DataFrame(rows)
    def qtab(df, col, y="ex", q=5):
        d = df.dropna(subset=[col, y]).copy()
        d["q"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        g = d.groupby("q")[y].agg(["mean","count","std"])
        g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
        g["xmean"] = d.groupby("q")[col].mean()
        r, p = stats.spearmanr(d[col], d[y])
        g.loc["rho"] = [r, len(d), p, np.nan, np.nan]
        return g.round(4)
    g20 = grid_rows(20, 60); g5 = grid_rows(5, 60); g5b = grid_rows(5, 20)
    out["h20 by dist to 60d high (ex in usual moves)"] = qtab(g20, "dhi")
    out["h20 by 60d range width"] = qtab(g20, "rng")
    out["h20 by prior 20d return"] = qtab(g20, "r20")
    out["h5 by prior 5d return"] = qtab(g5b, "r5")
    out["h5 by prior 1d return"] = qtab(g5b, "r1")
    out["h5 by vol ratio 20/60"] = qtab(g5, "vr")
    out["h5 by dist to 60d high"] = qtab(g5, "dhi")
    out["h5 by dist to 60d low"] = qtab(g5, "dlo")
    out["h5 by vol20 level"] = qtab(g5b, "vol20")
    # weekday & per-year daily
    dl = []
    for coin, ws in days.items():
        for w, df in ws.items():
            d = df.dropna(subset=["coin_return"]).copy()
            d["wd"] = pd.to_datetime(d["day"]).dt.dayofweek; d["yr"] = pd.to_datetime(d["day"]).dt.year
            d["coin"] = coin; d["w"] = w; dl.append(d)
    D = pd.concat(dl)
    wd = D.groupby("wd")["coin_return"].agg(["mean","count","std"]); wd["t"] = wd["mean"]/(wd["std"]/np.sqrt(wd["count"]))
    out["weekday daily coin return"] = wd.round(5)
    # book by window
    bw = D.groupby("w").agg(book=("book_return","mean"), coin=("coin_return","mean"), n=("coin_return","count"))
    out["book vs coin mean daily by window"] = bw.round(5)
    # trades
    tl = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t): t = t.copy(); t["coin"] = coin; tl.append(t)
    T = pd.concat(tl)
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean","count","median"]).round(3)
    T["fq"] = pd.qcut(T["entry_forecast"], 3, labels=False, duplicates="drop")
    out["trades by entry forecast tercile"] = T.groupby("fq").agg(f=("entry_forecast","mean"), pnl=("net_profit_loss_percent","mean"), n=("net_profit_loss_percent","count")).round(3)
    return out
