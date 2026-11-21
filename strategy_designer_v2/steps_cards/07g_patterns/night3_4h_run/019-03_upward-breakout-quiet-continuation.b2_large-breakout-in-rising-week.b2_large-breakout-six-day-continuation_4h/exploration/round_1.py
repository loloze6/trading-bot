def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 36
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            rng = (hi - lo)
            mr180 = rng.rolling(180, min_periods=45).mean()
            mr12 = rng.rolling(12).mean()
            hh12 = hi.shift(1).rolling(12).max()
            ll12 = lo.shift(1).rolling(12).min()
            br_up = (c - hh12) / mr180
            br_dn = (ll12 - c) / mr180
            ret42 = c / c.shift(42) - 1
            ret180 = c / c.shift(180) - 1
            ret1 = c / c.shift(1) - 1
            ret6 = c / c.shift(6) - 1
            vol180 = ret1.rolling(180, min_periods=45).std()
            comp = mr12 / mr180
            fwd = c.shift(-H) / c - 1
            fwd6 = c.shift(-6) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                "br_up": br_up, "br_dn": br_dn, "ret42": ret42, "ret180": ret180, "ret6": ret6,
                "comp": comp, "vol": vol180, "fwd": fwd, "fwd6": fwd6, "ret1s": ret1 / vol180,
                "hour": ts.dt.hour, "wd": ts.dt.weekday, "year": ts.dt.year,
                "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A.pos % H == 0) & A.fwd.notna()].copy()
    drift = G.groupby("coin").fwd.mean()
    sd = G.groupby("coin").fwd.std()
    G["un"] = (G.fwd - G.coin.map(drift)) / G.coin.map(sd)  # strength units
    G["unp"] = G.fwd - G.coin.map(drift)
    out = {}
    def tab(col, q=5, sub=None):
        d = G if sub is None else sub
        d = d.dropna(subset=[col, "un"])
        try:
            k = pd.qcut(d[col].rank(method="first"), q, labels=False)
        except Exception:
            return None
        g = d.groupby(k)
        r = pd.DataFrame({"lo": g[col].min(), "hi": g[col].max(), "n": g.size(),
                          "mean_unusual_pct": g.unp.mean() * 100, "strength": g.un.mean(),
                          "t": g.un.mean() / (g.un.std() / np.sqrt(g.size()))})
        return r.round(4)
    out["by_ret42"] = tab("ret42")
    out["by_ret180"] = tab("ret180")
    out["by_comp_quiet"] = tab("comp")
    out["by_vol"] = tab("vol")
    out["by_ret6"] = tab("ret6")
    out["by_brup_when_break"] = tab("br_up", 4, G[G.br_up > 0])
    out["by_brdn_when_break"] = tab("br_dn", 4, G[G.br_dn > 0])
    out["by_comp_when_upbreak"] = tab("comp", 3, G[G.br_up > 0])
    # absolute size of move after quiet (brief's core claim)
    d = G.dropna(subset=["comp"]).copy()
    d["absz"] = (d.fwd.abs()) / d.coin.map(sd)
    k = pd.qcut(d.comp.rank(method="first"), 5, labels=False)
    out["abs_move_by_comp"] = d.groupby(k).absz.agg(["mean", "count"]).round(3)
    yr = G.groupby("year").agg(n=("un", "size"), strength=("un", "mean"))
    out["grid_by_year"] = yr.round(3)
    # book days
    D = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd[["book_return", "coin_return"]].copy(); x["win"] = w; x["coin"] = coin
            x["year"] = pd.to_datetime(dd["day"]).dt.year
            D.append(x)
    D = pd.concat(D)
    bd = D.groupby(["win", D.groupby(["win", "coin"]).cumcount()]).agg(b=("book_return", "mean"), h=("coin_return", "mean"))
    bd = bd.reset_index()
    bd["year"] = D.groupby(["win", D.groupby(["win", "coin"]).cumcount()]).year.first().values
    out["book_by_window"] = bd.groupby("win").agg(book=("b", "sum"), hold=("h", "sum"), n=("b", "size")).round(3)
    out["book_by_year"] = bd.groupby("year").agg(book_mean=("b", "mean"), hold_mean=("h", "mean"),
                                                  book_sh=("b", lambda s: s.mean() / s.std() * np.sqrt(365))).round(4)
    return out
