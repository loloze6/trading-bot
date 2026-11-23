def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["window"].str[1:].astype(int)
    B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"]).dropna()
    val = (1 + B["book_return"]).cumprod().values
    peak = np.maximum.accumulate(val); ddv = val / peak - 1
    B["dd"] = ddv
    # worst drawdown episodes: find troughs
    B = B.reset_index(drop=True)
    eps = []
    i = 0
    n = len(B)
    while i < n:
        if B.loc[i, "dd"] < 0:
            j = i
            while j < n and B.loc[j, "dd"] < 0: j += 1
            seg = B.iloc[i:j]
            k = seg["dd"].idxmin()
            eps.append(dict(start_wn=B.loc[i, "wn"], trough_wn=B.loc[k, "wn"], depth=seg["dd"].min(), days_to_trough=k - i + 1,
                            coin_during=(1 + B.loc[i:k, "coin_return"]).prod() - 1,
                            book_during=(1 + B.loc[i:k, "book_return"]).prod() - 1))
            i = j
        else:
            i += 1
    E = pd.DataFrame(eps).sort_values("depth").head(8)
    out["worst drawdown episodes"] = E.reset_index(drop=True)
    # cases with conditions
    drift = {}
    cases = []
    for c, ws in data["bars"].items():
        rr = []
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            if len(cl) > 3: rr += list(cl[3::3] / cl[0:-3:3] - 1)
            ts = pd.to_datetime(b["timestamp"])
            r1 = pd.Series(cl).pct_change()
            v20 = r1.rolling(20).std().values; v60 = r1.rolling(60).std().values
            v5 = r1.rolling(5).std().values
            r20 = pd.Series(cl).pct_change(20).values
            ma50 = pd.Series(cl).rolling(50).mean().values
            for i in range(len(b) - 3):
                if ts[i].dayofweek != 6: continue
                a = b["postRebalance_current_allocation"].iloc[i]
                path = cl[i + 1:i + 4] / cl[i] - 1
                cases.append(dict(coin=c, wn=int(w[1:]), date=ts[i].normalize(), fc=b["forecast"].iloc[i], alloc=a,
                                  r1=r1.iloc[i], r20=r20[i], vrat=v20[i] / v60[i] if v60[i] else np.nan,
                                  v5rat=v5[i] / v60[i] if v60[i] else np.nan,
                                  above50=float(cl[i] > ma50[i]) if not np.isnan(ma50[i]) else np.nan,
                                  fwd=cl[i + 3] / cl[i] - 1, minpath=path.min()))
        drift[c] = np.mean(rr)
    C = pd.DataFrame(cases)
    C["ex"] = C["fwd"] - C["coin"].map(drift)
    C["pnl"] = C["alloc"] * C["fwd"]
    A = C[C["fc"] > 0].copy()
    N = C[~(C["fc"] > 0)].copy()
    def summ(g):
        return pd.Series(dict(n=len(g), mean_ex=g["ex"].mean(),
                              t=g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                              mean_alloc=g["alloc"].mean(), sum_pnl=g["pnl"].sum(), p10_pnl=g["pnl"].quantile(0.1)))
    cuts = list(A["vrat"].quantile([.25, .5, .75]))
    A["vq"] = pd.cut(A["vrat"], [-np.inf] + cuts + [np.inf], labels=False)
    N["vq"] = pd.cut(N["vrat"], [-np.inf] + cuts + [np.inf], labels=False)
    out["active by vrat q"] = A.groupby("vq").apply(summ)
    out["nonactive sundays by vrat q (condition alone)"] = N.groupby("vq").apply(summ)
    out["active by above 50d mean"] = A.groupby("above50").apply(summ)
    out["nonactive by above 50d mean"] = N.groupby("above50").apply(summ)
    # cross-coin clustering: per date
    G = A.groupby("date").agg(k=("ex", "size"), ex=("ex", "mean"), pnl=("pnl", "sum"))
    G["kq"] = pd.cut(G["k"], [0, 2, 5, 9, 30])
    out["by number of coins active same Sunday"] = G.groupby("kq").agg(dates=("ex", "size"), mean_ex=("ex", "mean"),
                                                                       sd_ex=("ex", "std"), sum_pnl=("pnl", "sum"), worst_pnl=("pnl", "min"))
    # worst case-dates
    out["worst 10 dates pnl, coins and mean ex"] = G.sort_values("pnl").head(10).reset_index(drop=True)
    # within window 2 / window 7 / 17 active stats
    out["active in drawdown windows"] = A[A["wn"].isin([2, 3, 7, 17])].groupby("wn").apply(summ)
    # vrat in worst dates
    A2 = A.merge(G[["pnl"]].rename(columns={"pnl": "dpnl"}), left_on="date", right_index=True)
    A2["worstdate"] = A2["dpnl"] <= G["pnl"].quantile(0.1)
    out["worst-decile dates vs others: vrat, r1, r20"] = A2.groupby("worstdate")[["vrat", "r1", "r20", "alloc", "ex"]].mean()
    # weighted forecast effect: per-case pnl by v5rat quartile
    A["v5q"] = pd.qcut(A["v5rat"], 4, labels=False)
    out["active by v5/v60 q"] = A.groupby("v5q").apply(summ)
    return out
