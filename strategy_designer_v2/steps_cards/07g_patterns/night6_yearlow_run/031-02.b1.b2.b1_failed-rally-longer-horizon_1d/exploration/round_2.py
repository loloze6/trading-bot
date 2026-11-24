def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]

    def build(h):
        rows = []
        for coin, ws in bars.items():
            per = []; fr = []
            for w, df in ws.items():
                df = df.reset_index(drop=True)
                c = df["close"]; lr = np.log(c).diff()
                f = {
                    "vol10": lr.rolling(10).std(),
                    "vol20": lr.rolling(20).std(),
                    "vol40": lr.rolling(40).std(),
                    "volratio": lr.rolling(10).std() / lr.rolling(60, min_periods=40).std(),
                    "ret5": c / c.shift(5) - 1,
                    "ret40": c / c.shift(40) - 1,
                    "hl20": ((df["high"] - df["low"]) / df["close"]).rolling(20).mean(),
                    "lowprox": df.get("debug_info.components.low_prox.last_history_value", pd.Series(np.nan, index=df.index)),
                }
                cv = c.values; n = len(cv)
                for i in range(0, n - h, h):
                    r = cv[i + h] / cv[i] - 1; fr.append(r)
                    ts = pd.Timestamp(df["timestamp"].iloc[i])
                    d = {"coin": coin, "w": w, "wn": int(w[1:]), "day": str(ts.date()), "yr": ts.year, "r": r}
                    for k, v in f.items(): d[k] = v.iloc[i]
                    per.append(d)
            if len(fr) < 3: continue
            m = np.mean(fr); s = np.std(fr, ddof=1)
            for d in per:
                d["ex"] = d["r"] - m; d["exz"] = (d["r"] - m) / s
            rows += per
        return pd.DataFrame(rows)

    def slope_t(g, k):
        g = g.dropna(subset=[k, "exz"]).copy()
        g["x"] = g.groupby("coin")[k].rank(pct=True) - 0.5
        x = g["x"].values; y = g["exz"].values
        xc = x - x.mean(); b = (xc * (y - y.mean())).sum() / (xc ** 2).sum()
        e = y - y.mean() - b * xc
        g["s"] = xc * e
        S = g.groupby("day")["s"].sum()
        se = np.sqrt((S ** 2).sum()) / (xc ** 2).sum()
        return b, b / se, len(g), g["day"].nunique()

    for h in (10, 20, 40, 60):
        D = build(h)
        res = {}
        for k in ["vol10", "vol20", "vol40", "volratio", "hl20", "ret5", "ret40", "lowprox"]:
            b, t, n, nd = slope_t(D, k)
            res[k] = {"slope_exz": b, "t_day": t, "n": n, "days": nd}
        out[f"h{h}_slopes"] = pd.DataFrame(res).T.round(4)
        if h in (20, 40):
            sub = {}
            for lab, g in [("w1-12", D[D.wn <= 12]), ("w13-24", D[D.wn > 12]),
                           ("ret40>0", D[D.ret40 > 0]), ("ret40<=0", D[D.ret40 <= 0]),
                           ("BTC/ETH/LTC/XMR", D[D.coin.isin(["BTCUSD", "ETHUSD", "LTCUSD", "XMRUSD"])]),
                           ("others", D[~D.coin.isin(["BTCUSD", "ETHUSD", "LTCUSD", "XMRUSD"])])]:
                b, t, n, nd = slope_t(g, "vol20")
                sub[lab] = {"slope_exz": b, "t_day": t, "n": n, "days": nd}
            out[f"h{h}_vol20_subsets"] = pd.DataFrame(sub).T.round(4)
            g = D.dropna(subset=["vol20"]).copy()
            g["q"] = pd.cut(g.groupby("coin")["vol20"].rank(pct=True), [0, .2, .4, .6, .8, 1], labels=False, include_lowest=True)
            out[f"h{h}_vol20_byyear_lowminushigh"] = g.groupby("yr").apply(
                lambda x: pd.Series({"low_q_ex%": 100 * x[x.q == 0]["ex"].mean(), "high_q_ex%": 100 * x[x.q == 4]["ex"].mean(), "n": len(x)})).round(2)
            out[f"h{h}_vol20_quint_raw"] = g.groupby("q").agg(n=("r", "size"), total_ret_pct=("r", lambda x: 100 * x.mean()), ex_pct=("ex", lambda x: 100 * x.mean()), up_share=("r", lambda x: (x > 0).mean())).round(3)
    return out
