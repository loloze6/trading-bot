import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    rows = []
    H = [6, 24, 72]
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(24).std()
            z = r1 / sd
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r24p = c / c.shift(24) - 1
            vol = b["volume"].astype(float)
            vrel = vol / vol.rolling(24 * 7).median()
            sd72 = r1.rolling(72).std()
            for h in H:
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(b), h)
                d = pd.DataFrame({
                    "coin": coin, "w": w, "h": h,
                    "z": z.iloc[idx].values, "f": b["forecast"].iloc[idx].values,
                    "fwd": fwd.iloc[idx].values, "hour": ts.dt.hour.iloc[idx].values,
                    "year": ts.dt.year.iloc[idx].values,
                    "r24p": (r24p / (sd * np.sqrt(24))).iloc[idx].values,
                    "vrel": vrel.iloc[idx].values,
                    "volreg": (sd / sd72).iloc[idx].values,
                    "usual": np.nan})
                rows.append(d)
    g = pd.concat(rows).dropna(subset=["z", "fwd"])
    # drift and usual move per coin and h
    st = g.groupby(["coin", "h"])["fwd"].agg(["mean", "std"]).rename(columns={"mean": "drift", "std": "usual"})
    g = g.drop(columns="usual").join(st, on=["coin", "h"])
    g["dirn"] = -np.sign(g["z"])
    g["tot"] = g["dirn"] * g["fwd"]
    g["unus"] = g["dirn"] * (g["fwd"] - g["drift"])
    g["absz"] = g["z"].abs()
    out = {}
    def summ(df, by):
        a = df.groupby(by, observed=True).agg(n=("tot", "size"), total=("tot", "mean"), unusual=("unus", "mean"),
                                              sdv=("unus", "std"))
        a["t"] = a["unusual"] / (a["sdv"] / np.sqrt(a["n"]))
        a[["total", "unusual"]] *= 100
        return a.drop(columns="sdv").round(3)
    g["zbin"] = pd.cut(g["absz"], [0, 0.5, 1, 1.5, 2, 3, 4, 100])
    out["by |z| bin and h (% move in signal dir)"] = summ(g, ["h", "zbin"])
    g24 = g[g.h == 24].copy()
    g24["side"] = np.where(g24["dirn"] > 0, "long", "short")
    g24["big"] = g24["absz"] > 2
    out["h24 by side x big"] = summ(g24, ["side", "big"])
    # trend alignment: move against prior 24h trend vs with
    g24["against_trend"] = np.sign(g24["z"]) != np.sign(g24["r24p"])
    out["h24 big moves: shock against prior 24h trend?"] = summ(g24[g24.big], ["against_trend"])
    g24["vrb"] = pd.qcut(g24["vrel"], 3, labels=["lowvol", "midvol", "highvol"])
    out["h24 big moves by relative volume"] = summ(g24[g24.big], ["vrb"])
    g24["settle"] = g24["hour"].isin([0, 8, 16]) | g24["hour"].isin([23, 7, 15])
    out["h24 big by settlement hour"] = summ(g24[g24.big], ["settle"])
    out["h24 by year (all)"] = summ(g24, ["year"])
    out["h24 big by coin"] = summ(g24[g24.big], ["coin"])
    # trades
    T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values()])
    T["absf"] = T["entry_forecast"].abs()
    T["fb"] = pd.cut(T["absf"], [0, 2, 5, 10, 15, 21])
    out["trades by |entry forecast|"] = T.groupby(["fb"], observed=True).agg(
        n=("net_profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"), dur_h=("duration_minutes", lambda x: x.mean() / 60)).round(3)
    out["trades by side"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean")).round(3)
    # allocation turnover
    tu = []
    for coin in bars:
        for w, b in bars[coin].items():
            ch = (b["postRebalance_current_allocation"] - b["previous_allocation"]).abs()
            tu.append([ch.sum() / (len(b) / 24), (ch > 0).mean(), b["postRebalance_current_allocation"].abs().mean()])
    tu = np.array(tu)
    out["turnover per day, share bars traded, mean |alloc|"] = pd.Series(tu.mean(0), index=["turn_per_day", "share_traded", "abs_alloc"]).round(4)
    # book by window
    D = pd.concat([d.assign(coin=c, w=w) for c in days for w, d in days[c].items()])
    bw = D.groupby("w").agg(book=("book_return", "mean"), hold=("coin_return", "mean"))
    out["book vs hold mean daily % by window"] = (bw * 100).round(3)
    return out
