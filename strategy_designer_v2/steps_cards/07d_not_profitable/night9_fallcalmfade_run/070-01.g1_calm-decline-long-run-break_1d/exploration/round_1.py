def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    bars = data["bars"]
    for coin, wd in bars.items():
        for w, b in wd.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            ret1 = np.r_[c[1:] / c[:-1] - 1, np.nan]
            prev = np.r_[np.nan, c[1:] / c[:-1] - 1]
            # run of down days before today's up close
            run = np.zeros(n)
            cnt = 0
            for i in range(1, n):
                if prev[i] > 0:
                    run[i] = cnt
                    cnt = 0
                elif prev[i] < 0:
                    cnt += 1
                    run[i] = -1
                else:
                    cnt = 0
            fwd = {}
            for h in (1, 2, 3, 5):
                fwd[h] = np.r_[c[h:] / c[:-h] - 1, [np.nan] * h]
            ret5back = np.r_[[np.nan] * 5, c[5:] / c[:-5] - 1]
            ret20back = np.r_[[np.nan] * 20, c[20:] / c[:-20] - 1]
            alloc = b["postRebalance_current_allocation"].values
            for i in range(n):
                rows.append(dict(coin=coin, w=w, i=i, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 fc=b["forecast"].iloc[i], reg=b["regime"].iloc[i], alloc=alloc[i],
                                 run=run[i], upret=prev[i], r1=fwd[1][i], r2=fwd[2][i], r3=fwd[3][i], r5=fwd[5][i],
                                 back5=ret5back[i], back20=ret20back[i]))
    df = pd.DataFrame(rows)
    drift = df.groupby("coin")["r1"].mean()
    df["x1"] = df["r1"] - df["coin"].map(drift)
    falls = df[df.reg == "unknown"]
    brk = df[(df.run >= 1)]
    brk = brk.assign(fc_in=(brk.fc < 0), prof=(brk.reg == "unknown"))
    def summ(g, col="r1"):
        s = g[col].dropna()
        return pd.Series({"n": len(s), "mean_short": -s.mean(), "t": -s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    brk["runb"] = pd.cut(brk.run, [0, 1, 2, 3, 4, 6, 30], labels=["1", "2", "3", "4", "5-6", "7+"])
    out["breaks_by_run_profile_r1"] = brk.groupby(["prof", "runb"]).apply(summ).round(4)
    cases = df[df.fc < 0]
    out["cases_by_h"] = pd.DataFrame({h: summ(cases, f"r{h}") for h in (1, 2, 3, 5)}).T.round(4)
    out["cases_by_coin"] = cases.groupby("coin").apply(summ).round(4)
    out["cases_by_year"] = cases.groupby("year").apply(summ).round(4)
    out["cases_by_w"] = cases.groupby("w").apply(summ).round(4)
    cases = cases.assign(upq=pd.qcut(cases.upret, 3, labels=["smallup", "midup", "bigup"]),
                         b20q=pd.qcut(cases.back20, 3, labels=["b20low", "b20mid", "b20high"]))
    out["cases_by_upsize"] = cases.groupby("upq").apply(summ).round(4)
    out["cases_by_back20"] = cases.groupby("b20q").apply(summ).round(4)
    # profile all-day drift (condition alone)
    out["falling_calm_all_days"] = summ(falls).round(4)
    out["alloc_on_cases"] = cases["alloc"].describe().round(3)
    # book daily: mean over coins per day
    dl = []
    for coin, wd in data["days"].items():
        for w, d in wd.items():
            dl.append(d.assign(coin=coin, w=w))
    D = pd.concat(dl)
    book = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["w", "day"])
    v = (1 + book.book_return.fillna(0)).cumprod()
    dd = v / v.cummax() - 1
    book["dd"] = dd.values
    out["book_maxdd"] = float(dd.min())
    out["book_dd_by_w"] = book.groupby("w").agg(minret=("book_return", "min"), meanret=("book_return", "mean"), dd_end=("dd", "min")).round(4)
    out["book_worst10_days_coinret"] = book.nsmallest(10, "book_return")[["book_return", "coin_return"]].reset_index(drop=True).round(4)
    return out
