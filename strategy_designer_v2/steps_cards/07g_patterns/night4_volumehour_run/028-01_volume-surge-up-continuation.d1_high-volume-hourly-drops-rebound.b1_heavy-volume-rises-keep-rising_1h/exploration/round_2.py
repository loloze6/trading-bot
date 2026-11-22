def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(720, min_periods=240).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "r1": r1, "sd": sd,
                               "hour": ts.dt.hour, "wd": ts.dt.weekday, "year": ts.dt.year,
                               "month": ts.dt.month,
                               "ret24p": c/c.shift(24)-1, "ret6p": c/c.shift(6)-1,
                               "vr": b["volume"]/b["volume"].rolling(720, min_periods=240).mean()})
            df["f1"] = c.shift(-1)/c - 1
            df["f2"] = c.shift(-2)/c - 1
            df["f24"] = c.shift(-24)/c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    def st(g):
        return pd.DataFrame({"n": g.size(), "mean_bp": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.size()))}).round(2)
    # Hours 20-21 return (bar opening at 19 and 20 closes into 20,21): f2 from bar with hour 19
    E = D[D.hour == 19].dropna(subset=["f2"]).copy()
    E["dst"] = E["month"].between(4, 10)
    out["h20_21_by_coin_year"] = st(E.groupby(["coin", "year"])["f2"])
    out["h20_21_by_dst"] = st(E.groupby(["coin", "dst"])["f2"])
    out["h20_21_by_wd"] = st(E.groupby("wd")["f2"])
    # graded? by the move over US session so far (6h return to 19:00 close), scaled
    E["m6"] = E["ret6p"] / (E["sd"]*np.sqrt(6))
    E = E.dropna(subset=["m6"])
    E["q"] = pd.qcut(E["m6"], 5, labels=False)
    out["h20_21_by_prior6h_quint"] = st(E.groupby("q")["f2"])
    E["vq"] = pd.qcut(E["sd"].rank(pct=True), 3, labels=False)
    out["h20_21_by_volterc"] = st(E.groupby("vq")["f2"])
    # share of windows with positive mean
    wm = E.groupby(["coin", "w"])["f2"].mean()
    out["h20_21_share_windows_pos"] = float((wm > 0).mean())
    # 24h reversal: per coin, per year, graded
    S = D[D.pos % 24 == 0].dropna(subset=["ret24p", "f24", "sd"]).copy()
    drift = D[D.pos % 24 == 0].groupby("coin")["f24"].mean()
    S["u"] = S["f24"] - S["coin"].map(drift)
    S["m"] = S["ret24p"]/(S["sd"]*np.sqrt(24))
    S["mb"] = pd.qcut(S["m"], 5, labels=False)
    out["rev_coin_q"] = st(S.groupby(["coin", "mb"])["u"])
    out["rev_corr"] = pd.Series({c: np.corrcoef(g["m"], g["u"])[0, 1] for c, g in S.groupby("coin")}).round(4)
    S["yq"] = S["mb"].isin([0]).map({True: "low", False: "rest"})
    out["rev_low_by_year"] = st(S[S.mb == 0].groupby("year")["u"])
    # weekday by year
    W = D[(D.pos % 24 == 0)].dropna(subset=["f24"])
    out["wd_by_year_t"] = W.groupby(["year", "wd"])["f24"].apply(lambda x: x.mean()/(x.std()/np.sqrt(len(x)))).unstack().round(2)
    # book days: largest gains/losses context
    dd = pd.concat([d.assign(coin=c, w=w) for c in data["days"] for w, d in data["days"][c].items()])
    dd = dd.dropna(subset=["book_return", "coin_return"])
    dd["bq"] = pd.qcut(dd["book_return"], 10, labels=False)
    out["book_dec"] = dd.groupby("bq").agg(n=("book_return", "size"), book_bp=("book_return", lambda x: x.mean()*1e4),
                                           coin_bp=("coin_return", lambda x: x.mean()*1e4)).round(1)
    out["book_coin_corr"] = float(np.corrcoef(dd["book_return"], dd["coin_return"])[0, 1])
    return out
