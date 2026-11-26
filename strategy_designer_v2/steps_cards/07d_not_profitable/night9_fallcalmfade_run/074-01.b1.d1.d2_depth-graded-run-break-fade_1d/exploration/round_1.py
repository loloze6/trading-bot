def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily returns per window
    rows = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = coin; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index().sort_values(["wn", "day"])
    B = B.dropna()
    val = (1 + B["br"]).cumprod().values
    peak = np.maximum.accumulate(val)
    ddn = val / peak - 1
    B["dd"] = ddn
    out["deepest fall"] = float(ddn.min())
    out["book by window"] = B.groupby("wn").agg(ret=("br", lambda x: (1 + x).prod() - 1), mindd=("dd", "min"), coin=("cr", lambda x: (1 + x).prod() - 1))
    # worst days
    out["worst 10 book days"] = B.nsmallest(10, "br")[["wn", "br", "cr"]].reset_index(drop=True)

    # per-case trades
    cases = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            nxt = c.shift(-1) / c - 1
            nxt2 = c.shift(-2) / c - 1
            down = (r < 0).astype(int)
            # run length before today
            run = np.zeros(len(b)); cnt = 0
            for i in range(len(b)):
                run[i] = cnt
                cnt = cnt + 1 if down.iloc[i] == 1 else 0
            ret60 = c / c.shift(60) - 1
            vratio = sd30 / r.rolling(90, min_periods=60).std()
            a = b["postRebalance_current_allocation"]
            m = (a < 0) & (b["forecast"] < 0)
            for i in np.where(m)[0]:
                cases.append(dict(coin=coin, wn=int(w[1:]), alloc=a[i], fc=b["forecast"][i],
                                  nxt=nxt[i], nxt2=nxt2[i], upz=r[i] / sd30[i] if sd30[i] > 0 else np.nan,
                                  run=run[i], ret60=ret60[i], vr=vratio[i], sd30=sd30[i],
                                  ret5z=(c[i] / c[i - 5] - 1) / sd30[i] if i >= 5 and sd30[i] > 0 else np.nan,
                                  gain=-a[i] * nxt[i]))
    C = pd.DataFrame(cases).dropna(subset=["nxt"])
    C["sret"] = -C["nxt"]
    out["n cases"] = len(C)
    out["short ret mean/t"] = pd.Series({"mean": C.sret.mean(), "t": stats.ttest_1samp(C.sret, 0).statistic,
                                         "mean2d": (-C.nxt2).mean(), "t2d": stats.ttest_1samp((-C.nxt2).dropna(), 0).statistic,
                                         "worst5pct": C.sret.quantile(0.05), "mean_abs_alloc": C.alloc.abs().mean()})
    def grp(col, q=4):
        g = pd.qcut(C[col], q, duplicates="drop")
        return C.groupby(g, observed=True).agg(n=("sret", "size"), mean=("sret", "mean"),
                                               t=("sret", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))),
                                               p5=("sret", lambda x: x.quantile(0.05)), gain=("gain", "mean"),
                                               alloc=("alloc", "mean"))
    out["by up-day size z"] = grp("upz")
    out["by run length"] = C.groupby(C.run.clip(upper=5)).agg(n=("sret", "size"), mean=("sret", "mean"), p5=("sret", lambda x: x.quantile(0.05)))
    out["by 60d return"] = grp("ret60")
    out["by vol ratio 30/90"] = grp("vr")
    out["by |forecast|"] = grp("fc")
    out["by 5d z"] = grp("ret5z")
    out["by coin"] = C.groupby("coin").agg(n=("sret", "size"), mean=("sret", "mean"), gain=("gain", "mean"))
    out["by window"] = C.groupby("wn").agg(n=("sret", "size"), mean=("sret", "mean"), gain=("gain", "sum"))
    return out
