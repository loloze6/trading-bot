def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 48
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            rs += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(rs)
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            f = b["forecast"].fillna(0).values
            n = len(c)
            r720 = pd.Series(c).pct_change(720).values
            r168 = pd.Series(c).pct_change(168).values
            r24 = pd.Series(c).pct_change(24).values
            lr = np.log(pd.Series(c)).diff()
            vol_s = lr.rolling(168).std().values
            vol_l = lr.rolling(720).std().values
            year = pd.to_datetime(b["timestamp"]).dt.year.values
            for s in range(0, n - H, H):
                seg = np.where(f[s:s + H] >= 2)[0]
                if len(seg) == 0:
                    continue
                t = s + seg[0]
                if t + H >= n:
                    continue
                fr = c[t + H] / c[t] - 1
                rows.append(dict(coin=coin, w=w, year=year[t], f=f[t], ex=fr - drift[coin], tot=fr,
                                 r720=r720[t], r168=r168[t], r24=r24[t],
                                 vr=vol_s[t] / vol_l[t] if vol_l[t] > 0 else np.nan))
    d = pd.DataFrame(rows)
    def summ(g):
        return pd.Series(dict(n=len(g), mean_ex=g.ex.mean(), t=g.ex.mean() / (g.ex.std() / np.sqrt(len(g))),
                              mean_tot=g.tot.mean()))
    out["all"] = summ(d)
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fq"] = pd.cut(d.f, [0, 2.5, 8.4, 19.99, 20.1])
    out["by_forecast"] = d.groupby("fq").apply(summ)
    d["q720"] = pd.qcut(d.r720, 5)
    out["by_30d_return_q"] = d.groupby("q720").apply(summ)
    d["q168"] = pd.qcut(d.r168, 5)
    out["by_7d_return_q"] = d.groupby("q168").apply(summ)
    d["qvr"] = pd.qcut(d.vr, 5)
    out["by_volratio_q"] = d.groupby("qvr").apply(summ)
    # book daily
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            x = t[["day", "book_return", "coin_return"]].copy(); x["w"] = w; x["coin"] = coin
            dd.append(x)
    dd = pd.concat(dd)
    pf = dd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    pf["wn"] = pf.w.str[1:].astype(int)
    pf = pf.sort_values(["wn", "day"]).dropna()
    bw = pf.groupby("wn").agg(book=("book_return", lambda x: (1 + x).prod() - 1),
                              hold=("coin_return", lambda x: (1 + x).prod() - 1), days=("book_return", "size"))
    eq = (1 + pf.book_return).cumprod().values
    peak = np.maximum.accumulate(eq); ddn = eq / peak - 1
    i_tr = ddn.argmin(); i_pk = eq[:i_tr + 1].argmax()
    out["book_by_window"] = bw
    out["deepest_fall"] = pd.Series(dict(depth=ddn.min(), peak_w=pf.wn.values[i_pk], trough_w=pf.wn.values[i_tr],
                                         days=i_tr - i_pk,
                                         hold_over_fall=(1 + pf.coin_return.values[i_pk + 1:i_tr + 1]).prod() - 1))
    return out
