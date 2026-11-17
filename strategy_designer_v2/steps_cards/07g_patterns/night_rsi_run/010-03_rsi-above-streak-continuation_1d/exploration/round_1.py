import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 14
    rows = []
    days = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            age = b.get("debug_info.components.rsi_age.last_history_value")
            past14 = c / c.shift(14) - 1
            past3 = c / c.shift(3) - 1
            vol = r1.rolling(14).std()
            fwd = c.shift(-H) / c - 1
            # RSI recomputed (Wilder) inside window
            d = c.diff()
            up = d.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
            dn = (-d.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
            rsi = 100 - 100 / (1 + up / dn)
            rng = (b["high"] - b["low"]) / c
            for i in range(0, len(b), H):
                if pd.isna(fwd.iloc[i]):
                    continue
                rows.append(dict(coin=coin, w=w, fwd=fwd.iloc[i], age=age.iloc[i] if age is not None else np.nan,
                                 fc=b["forecast"].iloc[i], p14=past14.iloc[i], p3=past3.iloc[i],
                                 vol=vol.iloc[i], rsi=rsi.iloc[i] if i >= 14 else np.nan, rng=rng.iloc[i],
                                 wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday()))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")

    def bucket(col, q=5):
        x = g.dropna(subset=[col, "ex"]).copy()
        x["b"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        out = x.groupby("b").agg(n=("ex", "size"), mean_ex=("ex", "mean"), sd=("ex", "std"), xmean=(col, "mean"))
        out["t"] = out["mean_ex"] / (out["sd"] / np.sqrt(out["n"]))
        r, p = stats.spearmanr(x[col], x["ex"])
        out.loc["spearman", ["n", "mean_ex"]] = [len(x), r]
        out.loc["spearman", "t"] = p
        return out.round(4)

    res = {}
    res["n_grid_by_coin"] = g.groupby("coin").size()
    res["by_age_raw"] = bucket("age")
    res["by_past14"] = bucket("p14")
    res["by_past3"] = bucket("p3")
    res["by_vol"] = bucket("vol", 3)
    res["by_rsi"] = bucket("rsi")
    res["by_range"] = bucket("rng", 3)
    wd = g.groupby("wd")["ex"].agg(["size", "mean", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    res["by_weekday_start"] = wd.round(4)
    # book daily
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    D = pd.concat(dd).dropna(subset=["book_return", "coin_return"])
    D["cq"] = D.groupby("coin")["coin_return"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    res["book_by_coin_ret_quintile"] = D.groupby("cq").agg(n=("book_return", "size"), book=("book_return", "mean"),
                                                         coin=("coin_return", "mean")).round(5)
    res["book_by_coin"] = D.groupby("coin").agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
                                               bsd=("book_return", "std")).round(5)
    res["book_by_weekday"] = D.assign(wd=pd.to_datetime(D["day"]).dt.weekday).groupby("wd")[["book_return", "coin_return"]].mean().round(5)
    return res
