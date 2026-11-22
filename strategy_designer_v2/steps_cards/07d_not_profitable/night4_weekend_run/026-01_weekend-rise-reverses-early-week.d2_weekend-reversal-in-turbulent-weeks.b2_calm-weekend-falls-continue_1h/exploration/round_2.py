def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    sig = []; dd = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values
            n = len(b)
            al = b["postRebalance_current_allocation"].fillna(0).values
            r = pd.Series(cl).pct_change()
            vol720 = r.rolling(720, min_periods=200).std()
            vrank = vol720.rolling(2000, min_periods=300).rank(pct=True)
            idx = np.where((ts.dt.dayofweek == 6) & (ts.dt.hour == 23))[0]
            for i in idx:
                if i + 48 >= n or i - 48 < 0: continue
                wk = cl[i] / cl[i - 48] - 1
                fwd = cl[i + 48] / cl[i] - 1
                g = np.sum(al[i:i + 48] * (cl[i + 1:i + 49] / cl[i:i + 48] - 1))
                sig.append(dict(coin=c, window=w, year=ts[i].year, fc=b["forecast"].iloc[i], wk=wk,
                                fwd=fwd, al=al[i], bookg=g, vr=vrank.iloc[i],
                                pre7=cl[i] / cl[max(0, i - 168)] - 1,
                                wkvol=r.iloc[i - 47:i + 1].std(), v720=vol720.iloc[i]))
    S = pd.DataFrame(sig)
    S["short"] = -S["fwd"]
    S["fall"] = S["wk"] < 0
    S["z"] = S["wk"] / (S["v720"] * np.sqrt(48))
    def agg(g):
        return pd.Series(dict(n=len(g), short_mean=g["short"].mean(), t=g["short"].mean() / (g["short"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                              mean_al=g["al"].mean(), bookg=g["bookg"].mean()))
    out["all_sunday_bars_by_fc_sign"] = S.groupby(np.sign(S["fc"])).apply(agg)
    A = S[S["fc"] < 0].copy()
    A["fcb"] = pd.cut(A["fc"], [-21, -10, -5, -2, -1, 0])
    out["active_by_fc_bucket"] = A.groupby("fcb").apply(agg)
    out["active_by_coin"] = A.groupby("coin").apply(agg)
    out["active_by_year"] = A.groupby("year").apply(agg)
    F = S[S["fall"]].copy()
    F["zq"] = pd.qcut(F["z"], 4, labels=False)
    out["all_weekend_falls_by_z_quartile"] = F.groupby("zq").apply(agg)
    F["vrq"] = pd.qcut(F["vr"], 4, labels=False)
    out["all_weekend_falls_by_volrank_quartile"] = F.groupby("vrq").apply(agg)
    F["preq"] = pd.qcut(F["pre7"], 4, labels=False)
    out["weekend_falls_by_prior7d_quartile"] = F.groupby("preq").apply(agg)
    out["corr_z_short_falls"] = float(np.corrcoef(F["z"], F["short"])[0, 1])
    R = S[~S["fall"]].copy()
    R["zq"] = pd.qcut(R["z"], 4, labels=False)
    out["weekend_rises_by_z_quartile_shortdir"] = R.groupby("zq").apply(agg)
    # book: daily returns by weekday and in-trade vs residual
    D = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["wd"] = pd.to_datetime(d["day"]).dt.dayofweek; D.append(d)
    D = pd.concat(D)
    out["book_daily_by_wd_bp"] = D.groupby("wd")["book_return"].agg(lambda x: x.mean() * 1e4)
    # long trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items() if t is not None and len(t)])
    T["dur_h"] = T["duration_minutes"] / 60
    T["db"] = pd.cut(T["dur_h"], [-1, 2, 47, 49, 200, 5000])
    out["trades_by_duration"] = T.groupby("db").agg(n=("side", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    return out
