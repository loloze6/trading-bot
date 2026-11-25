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
            sd30 = r1.rolling(30).std()
            sdmed = sd30.expanding(30).median()
            df = pd.DataFrame({"coin": coin, "wn": int(w[1:]), "pos": np.arange(len(b)), "r1": r1, "nxt": nxt, "nl": nl,
                               "ret60": ret60, "agit": (sd30 > sdmed), "has_agit": sdmed.notna(),
                               "alloc": b["postRebalance_current_allocation"], "sd30": sd30,
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["nxt"].mean()
    d["unus"] = d["nxt"] - d["coin"].map(drift)
    d["down"] = d["r1"] < 0
    d["tr60"] = pd.cut(d["ret60"], [-9, -0.1, 0.1, 9], labels=["falling", "choppy", "rising"]).astype(str)
    dv = d[d["nxt"].notna()].copy()
    def agg(g):
        return pd.Series({"n": len(g), "mean_nxt%": 100*g["nxt"].mean(), "unus%": 100*g["unus"].mean(),
                          "t": g["unus"].mean()/(g["unus"].std()/np.sqrt(len(g)))})
    da = dv[dv["has_agit"]].copy()
    dn = da[da["down"] & da["nl"].notna()].copy()
    dn["nlq"] = dn.groupby("coin")["nl"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=[1,2,3]))
    # condition alone: agitation on all bars, up days, down days of low terciles
    out["agit_all_bars"] = da.groupby("agit").apply(agg)
    out["agit_up_days"] = da[~da["down"]].groupby("agit").apply(agg)
    out["agit_down_by_nlq"] = dn.groupby(["agit","nlq"]).apply(agg)
    out["agit_x_tr60_top"] = dn[dn["nlq"]==3].groupby(["agit","tr60"]).apply(agg)
    out["agit_top_by_year"] = dn[(dn["nlq"]==3)].groupby(["year","agit"]).apply(agg)
    out["agit_top_by_coin"] = dn[(dn["nlq"]==3)].groupby(["coin","agit"]).apply(agg)
    def book(mask, size):
        x = dv.copy()
        m = x["down"] & mask(x)
        x["p"] = np.where(m, size(x).fillna(0), 0.0)
        x["p"] = x["p"].clip(0, 2)
        x["g"] = x["p"]*x["nxt"] - 0.0019*x.groupby(["coin","wn"])["p"].diff().abs().fillna(x["p"])
        dd = x.groupby(["wn","pos"])["g"].mean().sort_index()
        v = (1+dd).cumprod(); mdd = (v/v.cummax()-1).min()
        yrs = len(dd)/365; yr = v.iloc[-1]**(1/yrs)-1
        inpos = (x["p"]>0).mean()
        return pd.Series({"mean%": 100*dd.mean(), "sharpe": dd.mean()/dd.std()*np.sqrt(365), "yearly%": 100*yr,
                          "maxdd%": 100*mdd, "calmar": yr/abs(mdd), "inpos": inpos})
    tv = 0.02
    volsz = lambda x: x["nl"] * (tv / x["sd30"]).clip(0, 2)
    out["sim_books"] = pd.DataFrame({
        "all_nl": book(lambda x: pd.Series(True, index=x.index), lambda x: x["nl"]),
        "all_nl_sq": book(lambda x: pd.Series(True, index=x.index), lambda x: x["nl"]**2),
        "agit_nl": book(lambda x: x["agit"] & x["has_agit"], lambda x: x["nl"]),
        "agit_nl_sq": book(lambda x: x["agit"] & x["has_agit"], lambda x: x["nl"]**2),
        "agit_nl_vol": book(lambda x: x["agit"] & x["has_agit"], volsz),
        "all_nl_vol": book(lambda x: pd.Series(True, index=x.index), volsz),
        "fall_agit_nl": book(lambda x: x["agit"] & x["has_agit"] & (x["tr60"]=="falling"), lambda x: x["nl"]),
        "calm_nl": book(lambda x: (~x["agit"]) & x["has_agit"], lambda x: x["nl"]),
    }).T
    return out
