import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    out = {}
    # ---- book daily returns by window
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day", "book_return", "coin_return"]].copy(); dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    def sh(x):
        x = x.dropna(); return x.mean() / x.std() * np.sqrt(365) if x.std() > 0 else np.nan
    bw = B.groupby("w").agg(n=("book_return", "size"), book_mean=("book_return", "mean"),
                            book_sh=("book_return", sh), hold_sh=("coin_return", sh))
    bw["book_sum"] = B.groupby("w")["book_return"].sum()
    out["book_by_window"] = bw
    out["book_by_coin"] = D.groupby("coin")["book_return"].agg(["mean", "sum", "count"])
    # ---- cases and bar gains
    cases = []; gains = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(cl)
            f = b["forecast"].fillna(0).values
            al = b["postRebalance_current_allocation"].fillna(0).values
            r1 = np.r_[cl[1:] / cl[:-1] - 1, np.nan]
            lr = np.r_[np.nan, np.diff(np.log(cl))]
            vol30 = pd.Series(lr).rolling(30, min_periods=20).std().values
            volrank = pd.Series(vol30).expanding(min_periods=30).apply(lambda s: (s <= s[-1]).mean(), raw=True).values
            r7b = np.r_[[np.nan] * 7, cl[7:] / cl[:-7] - 1]
            r30b = np.r_[[np.nan] * 30, cl[30:] / cl[:-30] - 1]
            g = pd.DataFrame({"coin": c, "w": w, "gain": al * r1, "alloc": al, "f": f, "regime": b["regime"].values})
            gains.append(g)
            for t in range(0, n, 7):
                rec = {"coin": c, "w": w, "t": t, "f": f[t], "alloc": al[t], "regime": b["regime"].iloc[t],
                       "vol30": vol30[t], "volrank": volrank[t], "r7b": r7b[t], "r30b": r30b[t],
                       "day": str(b["timestamp"].iloc[t])[:10]}
                for h in (7, 14, 21):
                    rec[f"fwd{h}"] = cl[t + h] / cl[t] - 1 if t + h < n else np.nan
                cases.append(rec)
    C = pd.DataFrame(cases); G = pd.concat(gains)
    for h in (7, 14, 21):
        C[f"drift{h}"] = C.groupby("coin")[f"fwd{h}"].transform("mean")
        C[f"ex{h}"] = -(C[f"fwd{h}"] - C[f"drift{h}"])
        C[f"tot{h}"] = -C[f"fwd{h}"]
    S = C[C.f < 0].copy()
    S["terc"] = pd.qcut(S.f.abs().rank(method="first"), 3, labels=["small", "mid", "large"])
    def summ(df, h=7):
        x = df[f"ex{h}"].dropna(); y = df[f"tot{h}"].dropna()
        return pd.Series({"n": len(x), "ex_mean": x.mean(), "ex_t": x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan,
                          "tot_mean": y.mean(), "tot_t": y.mean() / y.std() * np.sqrt(len(y)) if len(y) > 2 else np.nan})
    out["cases_by_tercile_h7"] = S.groupby("terc").apply(summ)
    out["cases_by_tercile_h14"] = S.groupby("terc").apply(lambda d: summ(d, 14))
    out["cases_by_tercile_h21"] = S.groupby("terc").apply(lambda d: summ(d, 21))
    out["cases_by_window_h7"] = S.groupby("w").apply(summ)
    S["volhi"] = S.volrank > 0.5
    out["cases_by_vol_h7"] = S.groupby(["volhi", "terc"]).apply(summ)
    S["r7neg"] = S.r7b < 0
    out["cases_by_last7_h7"] = S.groupby(["r7neg", "terc"]).apply(summ)
    # alloc per tercile
    out["alloc_by_tercile"] = S.groupby("terc")[["alloc", "f"]].mean()
    # gains of the book by forecast state
    G["state"] = np.where(G.alloc < 0, "short", np.where(G.alloc > 0, "long", "flat"))
    out["gain_by_state"] = G.groupby("state")["gain"].agg(["count", "sum", "mean"])
    G["fbin"] = pd.cut(G.f, [-20.1, -10, -2, -0.0001, 0.0001, 20.1])
    out["gain_by_fbin_short"] = G[G.alloc < 0].groupby("fbin")["gain"].agg(["count", "sum", "mean"])
    # trades
    T = pd.concat([t.assign(coin=c, w=w) for c in trades for w, t in trades[c].items() if len(t)])
    out["trades"] = pd.Series({"n": len(T), "pl_mean": T.profit_loss_percent.mean(), "net_mean": T.net_profit_loss_percent.mean(),
                               "dur_days_mean": T.duration_minutes.mean() / 1440, "short_share": (T.side == "SHORT").mean()})
    T["durbin"] = pd.cut(T.duration_minutes / 1440, [0, 7, 8, 14, 30, 200])
    out["trades_by_dur"] = T.groupby("durbin")[["profit_loss_percent", "net_profit_loss_percent"]].agg(["count", "mean"])
    return out
