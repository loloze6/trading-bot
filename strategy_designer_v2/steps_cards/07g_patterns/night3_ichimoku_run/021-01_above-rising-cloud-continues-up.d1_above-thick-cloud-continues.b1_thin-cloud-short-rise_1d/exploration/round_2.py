def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(b)
            ten = (hi.rolling(9).max() + lo.rolling(9).min()) / 2
            kij = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
            sa = ((ten + kij) / 2).shift(26)
            sb = ((hi.rolling(52).max() + lo.rolling(52).min()) / 2).shift(26)
            top = np.maximum(sa, sb); bot = np.minimum(sa, sb)
            mid = (sa + sb) / 2
            slope = mid.pct_change(26) * 100
            above = (c > top).astype(float).where(top.notna())
            # days since close crossed above cloud top
            since = pd.Series(np.nan, index=b.index)
            cnt = np.nan
            for i in range(n):
                a = above.iloc[i]
                if np.isnan(a): cnt = np.nan
                elif a == 1: cnt = 1 if (np.isnan(cnt) or cnt == 0) else cnt + 1
                else: cnt = 0
                since.iloc[i] = cnt
            ret26 = c / c.shift(26) - 1
            ret60 = c / c.shift(60) - 1
            fwd = c.shift(-H) / c - 1
            fwd10 = c.shift(-10) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            half = "h1" if int(w[1:]) <= 12 else "h2"
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, half=half, fwd=fwd.iloc[i], fwd10=fwd10.iloc[i], fc=b["forecast"].iloc[i],
                    slope=slope.iloc[i], since=since.iloc[i], ret26=ret26.iloc[i], ret60=ret60.iloc[i],
                    above=above.iloc[i], wd=ts.iloc[i].weekday()))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    out = {}
    def tab(x, col, q):
        x = x.dropna(subset=[col, "ex"])
        g = pd.qcut(x[col].rank(method="first"), q, labels=False)
        r = x.groupby(g)["ex"].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        r["lo"] = x.groupby(g)[col].min(); r["hi"] = x.groupby(g)[col].max()
        return r.round(4)
    def reg(x, col):
        x = x.dropna(subset=[col, "ex"])
        s = stats.linregress(x[col], x["ex"])
        return pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(x)}).round(4)
    out["slope_dec10"] = tab(d, "slope", 10)
    neg = d[d["slope"] < 0]
    out["neg_slope_reg"] = reg(neg, "slope")
    out["neg_slope_reg_by_half"] = pd.DataFrame({h: reg(neg[neg.half == h], "slope") for h in ["h1", "h2"]})
    out["neg_slope_reg_by_coin"] = pd.DataFrame({cn: reg(neg[neg.coin == cn], "slope") for cn in neg.coin.unique()})
    out["ret60_dec"] = tab(d, "ret60", 8)
    ab = d[d["above"] == 1].copy()
    ab["lsince"] = np.log(ab["since"])
    out["since_above_quint"] = tab(ab, "since", 5)
    out["since_reg_log"] = reg(ab, "lsince")
    out["since_reg_by_half"] = pd.DataFrame({h: reg(ab[ab.half == h], "lsince") for h in ["h1", "h2"]})
    out["since_by_coin"] = pd.DataFrame({cn: reg(ab[ab.coin == cn], "lsince") for cn in ab.coin.unique()})
    d["mt"] = d["wd"].isin([0, 1]).astype(float)
    a = d[d.mt == 1]["ex"].dropna(); bb = d[d.mt == 0]["ex"].dropna()
    out["montue_vs_rest_t"] = pd.Series({"diff": a.mean() - bb.mean(), "t": stats.ttest_ind(a, bb, equal_var=False).statistic})
    return out
