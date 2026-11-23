import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]; days = data["days"]
    out = {}
    agree = []; rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); r1 = c.pct_change()
            sd = r1.rolling(24).std(); z = r1 / sd
            al = b["postRebalance_current_allocation"].astype(float)
            f = b["forecast"].astype(float)
            g1 = r1.shift(-1)
            agree.append([(np.sign(al) == np.sign(f)).mean(),
                          np.corrcoef(al.fillna(0), f.fillna(0))[0, 1],
                          (al * g1).mean() * 24, (al.mean() * g1.mean()) * 24,
                          (np.sign(al).diff().abs() > 0).sum() / (len(b) / 24)])
            ts = pd.to_datetime(b["timestamp"], utc=True)
            fwd = c.shift(-24) / c - 1
            zs = z.rolling(24).sum() / np.sqrt(24)  # slow part: last 24h scaled moves
            z6 = z.rolling(6).sum() / np.sqrt(6)
            idx = np.arange(0, len(b), 24)
            rows.append(pd.DataFrame({"coin": coin, "w": w, "z": z.iloc[idx].values,
                "zs": zs.iloc[idx].values, "z6": z6.iloc[idx].values,
                "fwd": fwd.iloc[idx].values, "hour": ts.dt.hour.iloc[idx].values,
                "year": ts.dt.year.iloc[idx].values}))
    A = np.array(agree)
    out["book vs forecast"] = pd.Series(np.nanmean(A, 0), index=["share alloc sign = forecast sign",
        "corr alloc,forecast", "pos gain per day %/100", "of which drift per day", "sign flips per day"]).round(5)
    g = pd.concat(rows).dropna()
    g["drift"] = g.groupby("coin")["fwd"].transform("mean")
    g["ex"] = g["fwd"] - g["drift"]
    def sig(df, col, cap=2.0):
        p = np.clip(-df[col] / cap, -1, 1)
        gross = p * df["fwd"]
        n = len(df)
        return pd.Series({"n": n, "gross%": gross.mean() * 100,
            "net_full_turn%": (gross - 0.0019 * p.abs()).mean() * 100,
            "t": gross.mean() / (gross.std() / np.sqrt(n)),
            "unusual%": (p * df["ex"]).mean() * 100,
            "strength_slope_t": np.polyfit(-df[col], df["ex"], 1)[0] / (np.std(df["ex"]) / np.std(df[col]) / np.sqrt(n)) if n > 10 else np.nan})
    out["24h-held graded book by formation length"] = pd.DataFrame({
        "last 1h z": sig(g, "z"), "last 6h": sig(g, "z6"), "last 24h": sig(g, "zs")}).round(4)
    # strong cases of slow part
    g["azs"] = g["zs"].abs()
    g["b"] = pd.cut(g["azs"], [0, 0.5, 1, 1.5, 2, 3, 100])
    g["tot"] = -np.sign(g["zs"]) * g["fwd"]
    a = g.groupby("b", observed=True)["tot"].agg(["size", "mean", "std"])
    a["t"] = a["mean"] / (a["std"] / np.sqrt(a["size"])); a["mean"] *= 100
    out["24h formation |zs| bins: move % in reversal dir"] = a.drop(columns="std").round(3)
    # settlement hours: 1h z reversal at settle vs not
    g["settle"] = g["hour"].isin([0, 8, 16, 23, 7, 15])
    g["tot1"] = -np.sign(g["z"]) * g["fwd"]
    g["az"] = g["z"].abs()
    s = g[g.az > 0.5].groupby("settle")["tot1"].agg(["size", "mean", "std"])
    s["t"] = s["mean"] / (s["std"] / np.sqrt(s["size"])); s["mean"] *= 100
    out["1h z>0.5 by settle hour"] = s.drop(columns="std").round(3)
    out["hours in grid"] = g["hour"].value_counts().head(10)
    # book deepest falls by window
    D = pd.concat([d.assign(coin=c, w=w) for c in days for w, d in days[c].items()])
    bd = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    bd["yr"] = pd.to_datetime(bd["day"]).dt.year
    out["book vs hold by year mean daily %"] = (bd.groupby("yr")[["book_return", "coin_return"]].mean() * 100).round(3)
    out["corr book daily with hold daily"] = round(bd[["book_return", "coin_return"]].corr().iloc[0, 1], 3)
    return out
