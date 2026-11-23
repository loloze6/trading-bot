def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    out = {}
    rows = []
    drift = {}
    for coin in bars:
        r24 = []
        for w, df in bars[coin].items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 24, 24)
            r24 += list(c[idx + 24] / c[idx] - 1)
        drift[coin] = np.mean(r24); 
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"]
            ts = pd.to_datetime(df["timestamp"])
            closehour = ((ts + pd.Timedelta(hours=1)).dt.hour).values
            hr = np.log(c).diff()
            vol7 = hr.rolling(168).std()
            vr = (vol7 / vol7.rolling(720, min_periods=200).mean()).values
            r2 = (c / c.shift(2) - 1).values
            r30d = (c / c.shift(720) - 1).values
            n = len(df)
            for h in (24, 72):
                fwd = np.full(n, np.nan)
                fwd[:n - h] = c.values[h:] / c.values[:n - h] - 1
                cell = np.arange(n) // h
                sett = np.isin(closehour, [0, 16])
                d = pd.DataFrame({"cell": cell, "sett": sett, "f": df["forecast"].values,
                                  "fwd": fwd, "vr": vr, "r2": r2, "r30": r30d, "hour": closehour})
                for kind in ("sett", "other"):
                    m = d["sett"] if kind == "sett" else (~d["sett"])
                    s = d[m].groupby("cell").first().dropna(subset=["fwd"])
                    s = s.assign(coin=coin, window=w, h=h, kind=kind)
                    rows.append(s)
    R = pd.concat(rows)
    R["ex"] = R.apply(lambda x: x["fwd"] - drift[x["coin"]] * x["h"] / 24, axis=1)
    def summ(g):
        return pd.Series({"n": len(g), "mean_total%": 100 * g["fwd"].mean(), "mean_ex%": 100 * g["ex"].mean(),
                          "t_ex": g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g)))})
    S = R[(R.kind == "sett")]
    S24 = S[S.h == 24].copy()
    S24["fb"] = pd.cut(S24["f"], [-0.01, 0.0001, 1, 2, 3, 5, 30])
    out["sett24 by forecast bucket"] = S24.groupby("fb").apply(summ)
    S72 = S[S.h == 72].copy()
    S72["fb"] = pd.cut(S72["f"], [-0.01, 0.0001, 1, 2, 3, 5, 30])
    out["sett72 by forecast bucket"] = S72.groupby("fb").apply(summ)
    # fall size in usual moves alone vs vol ratio
    S24["vrb"] = pd.qcut(S24["vr"], 4)
    S24["fall"] = S24["f"] >= 2
    out["sett24 by volratio x strongfall"] = S24.groupby(["vrb", "fall"]).apply(summ)
    S24["trend"] = pd.qcut(S24["r30"], 3)
    out["sett24 by 30d trend x strongfall"] = S24.groupby(["trend", "fall"]).apply(summ)
    # other hours with a 2h fall of similar size: broader case
    O = R[(R.kind == "other") & (R.h == 24)].copy()
    O["r2b"] = pd.qcut(O["r2"], 5)
    out["other hours 24h by 2h ret quintile"] = O.groupby("r2b").apply(summ)
    S24["r2b"] = pd.qcut(S24["r2"], 5)
    out["sett hours 24h by 2h ret quintile"] = S24.groupby("r2b").apply(summ)
    # book
    br = []
    for coin in days:
        for w, d in days[coin].items():
            br.append(d.assign(coin=coin, window=w))
    D = pd.concat(br)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["book vs coin by year"] = D.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    # allocation summary
    al = []
    for coin in bars:
        for w, df in bars[coin].items():
            a = df["postRebalance_current_allocation"]
            al.append(pd.Series({"mean_alloc": a.mean(), "share_in": (a.abs() > 1e-6).mean(), "share_forecast_pos": (df["forecast"] > 0).mean()}))
    out["allocation"] = pd.DataFrame(al).mean()
    T = pd.concat([t.assign(coin=c) for c in trades for w, t in trades[c].items()])
    T["fb"] = pd.cut(T["entry_forecast"], [-0.01, 1, 2, 3, 5, 30])
    out["trades by entry forecast"] = T.groupby("fb").agg(n=("profit_loss_percent", "count"), gross=("profit_loss_percent", "mean"),
                                                           net=("net_profit_loss_percent", "mean"), dur_h=("duration_minutes", lambda x: x.mean() / 60))
    return out
