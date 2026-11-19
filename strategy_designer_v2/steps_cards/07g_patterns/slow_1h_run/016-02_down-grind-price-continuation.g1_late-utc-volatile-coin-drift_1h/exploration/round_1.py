def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    hr_rows = []; slot = []; grid = []; book = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values
            r1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            hr_rows.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour.values, "wd": ts.dt.weekday.values, "r": r1}))
            # book decomposition
            pos = b["postRebalance_current_allocation"].fillna(0).values
            gross = pos * r1
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]).values / b["total_portfolio_value"].values
            book.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour.values, "gross": gross, "fee": fee, "pos": pos}))
            # 24h grid
            lr = np.log(c)
            ret = pd.Series(c)
            vol = pd.Series(r1).shift(1).rolling(168).std().values
            past24 = np.full(len(c), np.nan); past24[24:] = c[24:]/c[:-24]-1
            fut24 = np.full(len(c), np.nan); fut24[:-24] = c[24:]/c[:-24]-1
            # path: share of the 24h move made by largest hour
            absr = pd.Series(np.r_[np.nan, c[1:]/c[:-1]-1]).abs()
            maxh = absr.rolling(24).max().values
            sumabs = absr.rolling(24).sum().values
            idx = np.arange(0, len(c), 24)
            grid.append(pd.DataFrame({"coin": coin, "win": w, "past": past24[idx], "fut": fut24[idx],
                                      "vol": vol[idx], "jump": (maxh/sumabs)[idx], "wd": ts.dt.weekday.values[idx]}))
    H = pd.concat(hr_rows).dropna()
    g = H.groupby("hour")["r"]
    out["hourly_ret_by_hour_bp"] = pd.DataFrame({"mean_bp": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.count())), "n": g.count()})
    g = H.groupby("wd")["r"]
    out["hourly_ret_by_weekday_bp"] = pd.DataFrame({"mean_bp": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.count()))})
    B = pd.concat(book).dropna()
    out["book_gross_vs_fee_per_bar_bp"] = pd.DataFrame({"gross_sum_per_coin": B.groupby("coin")["gross"].sum(),
        "fee_sum_per_coin": B.groupby("coin")["fee"].sum(), "mean_abs_pos_active": B[B.pos!=0].groupby("coin")["pos"].mean()})
    out["book_gross_by_hour_bp"] = (B.groupby("hour")["gross"].mean()*1e4)[lambda s: s!=0]
    G = pd.concat(grid).dropna()
    G["pq"] = G.groupby("coin")["past"].transform(lambda s: pd.qcut(s, 5, labels=False))
    G["vq"] = G.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 5, labels=False))
    G["jq"] = G.groupby("coin")["jump"].transform(lambda s: pd.qcut(s, 5, labels=False))
    def tab(k):
        gg = G.groupby(k)["fut"]
        return pd.DataFrame({"mean_bp": gg.mean()*1e4, "t": gg.mean()/(gg.std()/np.sqrt(gg.count())), "n": gg.count()})
    out["fut24_by_past24_quint"] = tab("pq")
    out["fut24_by_vol_quint"] = tab("vq")
    G["sgn_fut"] = G["fut"]*np.sign(G["past"])
    gg = G.groupby("jq")["sgn_fut"]
    out["continuation24_by_jumpiness_quint"] = pd.DataFrame({"mean_bp": gg.mean()*1e4, "t": gg.mean()/(gg.std()/np.sqrt(gg.count())), "n": gg.count()})
    out["coin_mean24_bp"] = G.groupby("coin")["fut"].mean()*1e4
    return out
