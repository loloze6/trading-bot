def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # drift per coin over 24 bars, non-overlapping grid
    drift = {}; usual = {}
    for c, ws in data["bars"].items():
        rs = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 24, 24)
            rs.append(cl[idx + 24] / cl[idx] - 1)
        rs = np.concatenate(rs); drift[c] = rs.mean(); usual[c] = rs.std()
    cases = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            r1 = pd.Series(cl).pct_change()
            vol24 = r1.rolling(24).std()
            vol30d = r1.rolling(720).std()
            tr7 = pd.Series(cl) / pd.Series(cl).shift(168) - 1
            tr1 = pd.Series(cl) / pd.Series(cl).shift(24) - 1
            ts = pd.to_datetime(b["timestamp"])
            m = (b["regime"] == "mean_reversion") & (b["forecast"] != 0)
            day = ts.dt.floor("D")
            sel = b[m].groupby(day[m]).head(1).index
            for i in sel:
                if i + 24 >= len(cl): continue
                f = b["forecast"].iat[i]; s = np.sign(f)
                fwd = cl[i + 24] / cl[i] - 1
                # bar-by-bar path: worst adverse excursion
                path = cl[i:i + 25] / cl[i] - 1
                cases.append(dict(coin=c, w=w, year=ts.iat[i].year, f=f, s=s,
                    ex=s * (fwd - drift[c]), tot=s * fwd, mae=(s * path).min(),
                    volratio=vol24.iat[i] / vol30d.iat[i] if vol30d.iat[i] > 0 else np.nan,
                    tr7=tr7.iat[i], tr1=tr1.iat[i], alloc=abs(b["postRebalance_current_allocation"].iat[i])))
    d = pd.DataFrame(cases)
    out["n_cases"] = len(d)
    def g(col):
        x = d.groupby(col)["ex"].agg(["count", "mean", "std"])
        x["t"] = x["mean"] / (x["std"] / np.sqrt(x["count"])); return x
    d["side"] = np.where(d.s > 0, "long", "short")
    out["by_side"] = g("side")
    d["fb"] = pd.cut(d.f.abs(), [0, 5, 10, 15, 20.1])
    out["by_absf"] = g("fb")
    d["vb"] = pd.qcut(d.volratio, 5)
    out["by_volratio_q"] = g("vb")
    d["with7"] = np.where(np.sign(d.tr7) == d.s, "signal_with_7d_trend", "signal_against_7d_trend")
    out["by_7dtrend_align"] = g("with7")
    d["tr7q"] = pd.qcut(d.s * d.tr7, 5)
    out["by_signed_7d_trend_q"] = g("tr7q")
    d["tr1q"] = pd.qcut(d.s * d.tr1, 5)
    out["by_signed_24h_q"] = g("tr1q")
    out["by_year"] = g("year")
    out["by_coin"] = g("coin")
    # book daily
    dd = []
    for c, ws in data["days"].items():
        for w, x in ws.items():
            x = x.copy(); x["coin"] = c; x["w"] = w; dd.append(x)
    dd = pd.concat(dd)
    bk = dd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    bk["wn"] = bk.w.str[1:].astype(int); bk = bk.sort_values(["wn", "day"]).dropna()
    v = (1 + bk.book_return).cumprod(); dds = v / v.cummax() - 1
    out["max_dd"] = float(dds.min())
    # per window stats
    pw = bk.groupby("wn").apply(lambda z: pd.Series({"mean_bp": z.book_return.mean()*1e4,
        "dd": ((1+z.book_return).cumprod()/(1+z.book_return).cumprod().cummax()-1).min(),
        "coin_mean_bp": z.coin_return.mean()*1e4, "coin_absmean_bp": z.coin_return.abs().mean()*1e4}))
    out["per_window"] = pw
    # worst book days: coin abs move
    bk["q"] = pd.qcut(bk.book_return, 10, labels=False)
    out["book_decile_vs_coin_absmove"] = bk.groupby("q").agg(book=("book_return","mean"), coin_abs=("coin_return", lambda z: z.abs().mean()), n=("book_return","size"))
    out["mae_q"] = d["mae"].describe()
    return out
