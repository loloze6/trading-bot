import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    drows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sma = c.rolling(20).mean()
            sd = r1.rolling(20).std()
            z = (c - sma) / sma / sd
            past5 = c / c.shift(5) - 1
            past20 = c / c.shift(20) - 1
            rz = r1 / sd
            rng = (b["high"] - b["low"]) / c / sd
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            vol20 = sd
            volrank = vol20.rank(pct=True)
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]), "z": z, "past5": past5, "past20": past20,
                "rz": rz, "rng": rng, "clpos": clpos, "volrank": volrank, "f5": f5, "f1": f1,
                "chop": (b["regime"] == "unknown"), "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(df)
        for w, d in data["days"][coin].items():
            dd = d.copy(); dd["coin"] = coin; dd["win"] = w
            drows.append(dd)
    A = pd.concat(rows, ignore_index=True)
    D = pd.concat(drows, ignore_index=True)
    # coin mean 5d drift on grid
    G = A[A["pos"] % 5 == 0].dropna(subset=["f5"]).copy()
    G["drift"] = G.groupby("coin")["f5"].transform("mean")
    G["ex5"] = G["f5"] - G["drift"]
    G["day"] = G["ts"].dt.floor("D")
    out = {}
    def tstat(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    # 1. stretch quintiles, choppy vs not, excess 5d return (unsigned)
    G["zq"] = pd.qcut(G["z"], 5, labels=False)
    out["ex5 by z quintile x chop"] = G.dropna(subset=["z"]).groupby(["chop", "zq"])["ex5"].apply(tstat).unstack()
    # 2. past 5d return quintile (scaled by vol) everywhere
    G["p5s"] = G["past5"] / (G["rz"].abs()*0+1)
    G["p5q"] = pd.qcut(G["past5"], 5, labels=False)
    out["ex5 by past5 quintile x chop"] = G.dropna(subset=["past5"]).groupby(["chop", "p5q"])["ex5"].apply(tstat).unstack()
    # 3. after large 1-day move (rz quintile) -> next 5 days excess, all grid
    G["rzq"] = pd.qcut(G["rz"], 5, labels=False)
    out["ex5 by 1day move zq x chop"] = G.dropna(subset=["rz"]).groupby(["chop", "rzq"])["ex5"].apply(tstat).unstack()
    # 4. close position in day range
    G["cq"] = pd.qcut(G["clpos"], 5, labels=False, duplicates="drop")
    out["ex5 by close-in-range q"] = G.dropna(subset=["clpos"]).groupby("cq")["ex5"].apply(tstat)
    # 5. vol rank in window tercile
    G["vq"] = pd.qcut(G["volrank"], 3, labels=False)
    out["ex5 by vol tercile x chop"] = G.dropna(subset=["volrank"]).groupby(["chop", "vq"])["ex5"].apply(tstat).unstack()
    # 6. past20 quintile
    G["p20q"] = pd.qcut(G["past20"], 5, labels=False)
    out["ex5 by past20 q x chop"] = G.dropna(subset=["past20"]).groupby(["chop", "p20q"])["ex5"].apply(tstat).unstack()
    # 7. weekday daily coin return
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["coin daily ret by weekday"] = D.groupby("wd")["coin_return"].apply(tstat)
    out["book daily ret by weekday"] = D.groupby("wd")["book_return"].apply(tstat)
    # 8. book by year
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    out["book by year"] = D.groupby("yr")["book_return"].apply(tstat)
    # 9. book return by window
    out["book by window"] = D.groupby("win")["book_return"].mean()
    # 10. trades: by side
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tt = t.copy(); tt["coin"] = coin; T.append(tt)
    T = pd.concat(T, ignore_index=True)
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].apply(tstat)
    T["efq"] = pd.qcut(T["entry_forecast"].abs(), 4, labels=False, duplicates="drop")
    out["trades by |entry fc| q x side"] = T.groupby(["side", "efq"])["net_profit_loss_percent"].mean().unstack()
    # 11. 1-day forward within chop by z sign/magnitude (daily, overlapping not; use f1 every bar is independent)
    A2 = A.dropna(subset=["z", "f1"]).copy()
    A2["zq"] = pd.qcut(A2["z"], 5, labels=False)
    out["f1 by z q x chop"] = A2.groupby(["chop", "zq"])["f1"].mean().unstack()
    out["z quintile edges"] = pd.Series(pd.qcut(A2["z"], 5, retbins=True)[1])
    return out
