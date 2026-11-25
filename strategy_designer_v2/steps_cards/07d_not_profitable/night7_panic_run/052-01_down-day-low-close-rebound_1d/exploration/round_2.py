import numpy as np, pandas as pd

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            r1 = c / c.shift(1) - 1
            nxt = c.shift(-1) / c - 1
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            nl = (b["high"] - c) / rng
            ret60 = c / c.shift(60) - 1
            ret30 = c / c.shift(30) - 1
            sd30 = r1.rolling(30).std()
            sdmed = sd30.expanding(30).median()
            df = pd.DataFrame({"coin": coin, "win": w, "wn": int(w[1:]), "pos": np.arange(len(b)), "r1": r1, "nxt": nxt, "nl": nl,
                               "ret60": ret60, "ret30": ret30, "agit": sd30 > sdmed, "has_agit": sdmed.notna(),
                               "alloc": b["postRebalance_current_allocation"]})
            df["gain"] = df["alloc"] * df["nxt"]
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].mean()
    d["unus"] = d["nxt"] - d["coin"].map(drift)
    d["tr60"] = pd.cut(d["ret60"], [-9, -0.1, 0.1, 9], labels=["falling", "choppy", "rising"])
    d["tr30"] = pd.cut(d["ret30"], [-9, -0.1, 0.1, 9], labels=["falling", "choppy", "rising"])
    d["down"] = d["r1"] < 0
    def agg(g):
        return pd.Series({"n": len(g), "mean_nxt%": 100*g["nxt"].mean(), "unus%": 100*g["unus"].mean(),
                          "t": g["unus"].mean()/(g["unus"].std()/np.sqrt(len(g))), "gain%": 100*g["gain"].mean(),
                          "alloc": g["alloc"].mean()})
    dv = d[d["nxt"].notna()].copy()
    dn = dv[dv["down"] & dv["nl"].notna()].copy()
    dn["nlq"] = dn.groupby("coin")["nl"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=[1,2,3]))
    out["share_with_ret60"] = dv["ret60"].notna().mean()
    out["trend60_x_nl"] = dn.groupby(["tr60","nlq"]).apply(agg)
    out["trend60_all_bars"] = dv.groupby("tr60").apply(agg)
    out["trend60_up_days"] = dv[~dv["down"]].groupby("tr60").apply(agg)
    out["trend30_x_nl"] = dn.groupby(["tr30","nlq"]).apply(agg)
    out["trend30_all_bars"] = dv.groupby("tr30").apply(agg)
    da = dn[dn["has_agit"]]
    out["agit_x_nl"] = da.groupby(["agit","nlq"]).apply(agg)
    # book gain share by trend30 state (where the book loses)
    out["book_gain_by_tr30"] = dv.groupby("tr30").agg(n=("gain","size"), gain_sum=("gain","sum"), gain_mean=("gain","mean"), alloc=("alloc","mean"))
    # simple books: alloc=nl on down days, all / only when tr30 not falling; daily chain
    def book(mask):
        x = dv.copy()
        x["p"] = np.where(x["down"] & mask(x), x["nl"].fillna(0), 0.0)
        x["g"] = x["p"]*x["nxt"] - 0.0019*x["p"].diff().abs().fillna(x["p"])
        dd = x.groupby(["wn","pos"])["g"].mean().sort_index()
        v = (1+dd).cumprod(); mdd = (v/v.cummax()-1).min()
        yrs = len(dd)/365; yr = v.iloc[-1]**(1/yrs)-1
        return pd.Series({"days": len(dd), "mean%": 100*dd.mean(), "sharpe": dd.mean()/dd.std()*np.sqrt(365), "yearly%": 100*yr, "maxdd%": 100*mdd, "calmar": yr/abs(mdd)})
    out["sim_books"] = pd.DataFrame({
        "all_down": book(lambda x: pd.Series(True, index=x.index)),
        "not_fall30": book(lambda x: x["tr30"].astype(str) != "falling"),
        "rising30": book(lambda x: x["tr30"].astype(str) == "rising"),
        "not_fall60": book(lambda x: x["tr60"].astype(str) != "falling"),
    }).T
    return out
