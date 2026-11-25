import numpy as np
import pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            rng = (b["high"] - b["low"])
            mr = rng.shift(1).rolling(30, min_periods=20).mean()
            r0 = c.pct_change()
            sm = (c - c.shift(1)) / mr
            cl = (b["close"] - b["low"]) / rng.replace(0, np.nan)
            tr60 = 100 * (c / c.shift(60) - 1)
            df = pd.DataFrame({
                "coin": coin, "w": w, "ts": b["timestamp"],
                "inprof": (b["regime"] == "unknown").astype(int),
                "sm": sm, "r0": r0, "cl": cl, "tr60": tr60,
                "r1": c.shift(-1) / c - 1,
                "r2": c.shift(-2) / c.shift(-1) - 1,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    cm = d.groupby("coin")["r0"].mean()
    d["r1x"] = d["r1"] - d["coin"].map(cm)
    d["r2x"] = d["r2"] - d["coin"].map(cm)

    def ct(s, col, wcol=None):
        s = s.dropna(subset=[col] + ([wcol] if wcol else []))
        if len(s) < 10:
            return pd.Series({"n": len(s), "mean%": np.nan, "t": np.nan, "days": 0})
        wt = s[wcol] if wcol else pd.Series(1.0, index=s.index)
        m = (s[col] * wt).sum() / wt.sum()
        dev = wt * (s[col] - m)
        g = dev.groupby(s["ts"]).sum()
        se = np.sqrt((g ** 2).sum()) / wt.sum()
        return pd.Series({"n": len(s), "mean%": 100 * m, "t": m / se if se > 0 else np.nan, "days": g.size})

    def slope(s, x, y):
        s = s.dropna(subset=[x, y])
        if len(s) < 10:
            return np.nan, np.nan
        X = s[x].values; Y = s[y].values
        bta = np.cov(X, Y)[0, 1] / np.var(X, ddof=1)
        res = Y - Y.mean() - bta * (X - X.mean())
        # cluster by day
        g = pd.Series(res * (X - X.mean())).groupby(s["ts"].values).sum()
        se = np.sqrt((g ** 2).sum()) / ((X - X.mean()) ** 2).sum()
        return bta, bta / se

    d["prof"] = np.where(d.inprof == 1, "fall_agit",
                 np.where(d.tr60 < -10, "fall_calm",
                 np.where(d.tr60 > 10, "rising", np.where(d.tr60.notna(), "choppy", "na"))))
    out = {}
    # up-day reversal graded, by profile; down-day rebound graded, by profile
    res = []
    for p, s in d.groupby("prof"):
        up = s[s.sm > 0].copy(); up["neg"] = -up["r1x"]
        dn = s[s.sm < 0].copy(); dn["mag"] = -dn["sm"]
        a = ct(up, "neg", "sm"); bb = ct(dn, "r1x", "mag")
        su = slope(up, "sm", "neg"); sd = slope(dn, "mag", "r1x")
        res.append(pd.Series({"up n": a["n"], "up wmean -r1x%": a["mean%"], "up t": a["t"], "up slope t": su[1],
                              "dn n": bb["n"], "dn wmean r1x%": bb["mean%"], "dn t": bb["t"], "dn slope t": sd[1]}, name=p))
    out["graded reversal by profile (weighted by |scaled move|)"] = pd.DataFrame(res)
    ip = d[d.inprof == 1].copy()
    ip["abs"] = ip.sm.abs()
    ip["neg_signed"] = -np.sign(ip.sm) * ip.r1x
    ip["neg_signed2"] = -np.sign(ip.sm) * ip.r2x
    out["inprof symmetric reversal r1 / r2"] = pd.DataFrame({
        "r1": ct(ip, "neg_signed", "abs"), "r2": ct(ip, "neg_signed2", "abs")})
    ipu = ip[ip.sm > 0].copy(); ipu["neg"] = -ipu.r1x
    out["inprof up-days by year"] = ipu.groupby(pd.to_datetime(ipu.ts).dt.year).apply(lambda s: ct(s, "neg", "sm"))
    out["inprof up-days by coin"] = ipu.groupby("coin").apply(lambda s: ct(s, "neg", "sm"))
    ipu["clbin"] = pd.cut(ipu.cl, [-0.01, 0.5, 0.8, 1.01])
    out["inprof up-days by close loc"] = ipu.groupby("clbin", observed=True).apply(lambda s: ct(s, "neg", "sm"))
    # book's largest days
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            dd.append(t.assign(coin=coin, w=w))
    D = pd.concat(dd)
    B = D.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna()
    B = B[B.br != 0]
    q = B.br.quantile([0.05, 0.95])
    out["book extreme days: coin mean return"] = pd.DataFrame({
        "n": [int((B.br <= q.iloc[0]).sum()), int((B.br >= q.iloc[1]).sum())],
        "book%": [100 * B.br[B.br <= q.iloc[0]].mean(), 100 * B.br[B.br >= q.iloc[1]].mean()],
        "coins%": [100 * B.cr[B.br <= q.iloc[0]].mean(), 100 * B.cr[B.br >= q.iloc[1]].mean()]},
        index=["worst5%", "best5%"])
    out["book share of gain from top 10% days"] = float(B.br[B.br >= B.br.quantile(0.9)].sum() / B.br.sum())
    return out
