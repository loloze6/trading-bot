import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float)
            r1 = cl.pct_change()
            r7 = cl / cl.shift(7) - 1
            r30 = cl / cl.shift(30) - 1
            er = (cl - cl.shift(30)).abs() / cl.diff().abs().rolling(30).sum()
            vol = r1.rolling(30).std()
            sc = r7 / (vol * np.sqrt(7))
            f7 = cl.shift(-7) / cl - 1
            f1 = cl.shift(-1) / cl - 1
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": c, "w": w, "pos": np.arange(len(b)), "r1": r1, "r7": r7, "r30": r30,
                              "er": er, "vol": vol, "sc": sc, "f7": f7, "f1": f1,
                              "fc": b["forecast"].astype(float), "reg": b["regime"].astype(str),
                              "alloc": b["postRebalance_current_allocation"].astype(float),
                              "wd": ts.dt.weekday, "yr": ts.dt.year})
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    G = A[A["pos"] % 7 == 0].copy()
    drift = G.groupby("coin")["f7"].mean()
    G["u7"] = G["f7"] - G["coin"].map(drift)
    G = G.dropna(subset=["sc", "er", "u7", "r30"])
    G["agree"] = np.sign(G["r7"]) == np.sign(G["r30"])
    G["erb"] = pd.cut(G["er"], [0, 0.15, 0.3, 0.5, 1.01], labels=["<.15", ".15-.3", ".3-.5", ">.5"])
    G["s_u"] = np.sign(G["sc"]) * G["u7"]
    def summ(g):
        n = len(g); m = g["s_u"].mean(); s = g["s_u"].std()
        sl = stats.linregress(g["sc"], g["u7"]) if n > 5 else None
        return pd.Series({"n": n, "mean_signed_u7": m, "t": m / (s / np.sqrt(n)) if n > 1 else np.nan,
                          "slope_u7_on_sc": sl.slope if sl else np.nan,
                          "t_slope": sl.slope / sl.stderr if sl else np.nan})
    out = {}
    out["by_er_agree"] = G.groupby(["erb", "agree"], observed=True).apply(summ)
    G["scb"] = pd.qcut(G["sc"].abs(), 3, labels=["lo", "mid", "hi"])
    out["by_er_agree_size"] = G[G["er"] < 0.3].groupby(["agree", "scb"], observed=True).apply(summ)
    out["highER_by_size"] = G[G["er"] >= 0.3].groupby(["agree", "scb"], observed=True).apply(summ)
    # vol level
    G["volr"] = G.groupby("coin")["vol"].rank(pct=True)
    G["volb"] = pd.cut(G["volr"], [0, .33, .67, 1.0], labels=["lowvol", "midvol", "hivol"])
    out["by_vol_agree"] = G.groupby(["volb", "agree"], observed=True).apply(summ)
    out["by_year"] = G[(G["er"] < 0.3) & G["agree"]].groupby("yr").apply(summ)
    # 30d return alone as signal
    G["s30"] = np.sign(G["r30"]) * G["u7"]
    out["r30_sign_by_er"] = G.groupby("erb", observed=True)["s30"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # weekday on daily coin returns
    D = A.dropna(subset=["f1"])
    out["weekday_next_ret"] = D.groupby("wd")["f1"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # book
    bd = []
    for c in days:
        for w, d in days[c].items():
            dd = d.copy(); dd["coin"] = c; dd["w"] = w; bd.append(dd)
    B = pd.concat(bd, ignore_index=True)
    B["yr"] = pd.to_datetime(B["day"]).dt.year
    out["book_by_year"] = B.groupby("yr")[["book_return", "coin_return"]].mean()
    out["book_by_coin"] = B.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "std"])
    T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values()], ignore_index=True)
    out["trades_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median", "std"])
    T["dur_d"] = T["duration_minutes"] / 1440
    T["durb"] = pd.cut(T["dur_d"], [0, 8, 15, 30, 1000])
    out["trades_dur"] = T.groupby(["side", "durb"], observed=True)["net_profit_loss_percent"].agg(["count", "mean"])
    return out
