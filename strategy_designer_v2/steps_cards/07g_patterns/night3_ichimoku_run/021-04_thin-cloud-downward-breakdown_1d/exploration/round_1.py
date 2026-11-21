import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; out = {}
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); h = df["high"].astype(float); l = df["low"].astype(float)
            r1 = c.pct_change()
            f = pd.DataFrame({
                "mom14": c / c.shift(14) - 1,
                "mom7": c / c.shift(7) - 1,
                "kij": c / ((h.rolling(26).max() + l.rolling(26).min()) / 2) - 1,
                "vol14": r1.rolling(14).std(),
                "z1": r1 / r1.rolling(14).std().shift(1),
                "fc": df["forecast"].astype(float),
                "wd": pd.to_datetime(df["timestamp"]).dt.weekday,
            })
            for H in (3, 7, 26):
                fwd = c.shift(-H) / c - 1
                idx = np.arange(0, len(df), H)
                sub = f.iloc[idx].copy(); sub["fwd"] = fwd.iloc[idx].values
                sub["H"] = H; sub["coin"] = coin; sub["win"] = w
                rows.append(sub)
    A = pd.concat(rows).dropna(subset=["fwd"])
    A["drift"] = A.groupby(["coin", "H"])["fwd"].transform("mean")
    A["usual"] = A.groupby(["coin", "H"])["fwd"].transform("std")
    A["un"] = (A["fwd"] - A["drift"]) / A["usual"]
    res = []
    for H in (3, 7, 26):
        B = A[A.H == H]
        for feat in ["mom14", "mom7", "kij", "vol14", "z1"]:
            C = B.dropna(subset=[feat]).copy()
            C["rk"] = C.groupby("coin")[feat].rank(pct=True) - 0.5
            sl, ic, rr, p, se = stats.linregress(C["rk"], C["un"])
            top = C[C.rk > 0.3]["un"]; bot = C[C.rk < -0.3]["un"]
            t_tb = stats.ttest_ind(top, bot, equal_var=False).statistic
            # per coin sign
            cs = C.groupby("coin").apply(lambda g: np.corrcoef(g["rk"], g["un"])[0, 1])
            res.append({"H": H, "feat": feat, "n": len(C), "slope_t": sl / se,
                        "top20_mean": top.mean(), "bot20_mean": bot.mean(), "top_minus_bot_t": t_tb,
                        "coins_pos_corr": int((cs > 0).sum())})
    out["feature_vs_strength"] = pd.DataFrame(res).round(3)
    # weekday daily returns
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            D.append(d)
    D = pd.concat(D)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["cr"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    g = D.dropna(subset=["cr"]).groupby("wd")["cr"]
    out["weekday_coin_unusual"] = pd.DataFrame({"mean": g.mean(), "n": g.size(),
                                                "t": g.mean() / (g.std() / np.sqrt(g.size()))}).round(5)
    # book by year
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    gb = D.dropna(subset=["book_return"]).groupby("yr")
    out["book_by_year"] = pd.DataFrame({"book_mean": gb["book_return"].mean(), "coin_mean": gb["coin_return"].mean(),
                                        "n": gb.size()}).round(5)
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): T.append(t.assign(coin=coin))
    T = pd.concat(T)
    gt = T.groupby("coin")["net_profit_loss_percent"]
    out["trades_by_coin"] = pd.DataFrame({"n": gt.size(), "mean": gt.mean(), "median": gt.median(),
                                          "share_pos": T.assign(p=T.net_profit_loss_percent > 0).groupby("coin")["p"].mean()}).round(3)
    T["dur_d"] = T["duration_minutes"] / 1440
    out["trade_pnl_vs_entryfc"] = pd.Series({"corr_absfc_pnl": np.corrcoef(T.entry_forecast.abs(), T.net_profit_loss_percent)[0, 1],
                                             "mean_dur_days": T.dur_d.mean(), "n": len(T)}).round(3)
    return out
