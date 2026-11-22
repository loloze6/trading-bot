def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    drift48 = {}
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            rs += list(c[idx + 48] / c[idx] - 1)
        drift48[coin] = np.mean(rs)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].values; v = b["volume"].values
            fc = b["forecast"].values
            sun = np.where((ts.dt.weekday == 6) & (ts.dt.hour == 23))[0]
            for i in sun:
                if i < 168 + 720 or i + 96 >= len(c):
                    continue
                r = {"coin": coin, "win": w, "year": ts[i].year,
                     "fc": fc[i],
                     "wk_ret": c[i] / c[i - 48] - 1,
                     "vr": v[i - 47:i + 1].mean() / v[i - 167:i - 47].mean(),
                     "ret30": c[i] / c[i - 720] - 1,
                     "ret7wd": c[i - 48] / c[i - 168] - 1}
                for h in (12, 24, 48, 72, 96):
                    r[f"f{h}"] = c[i + h] / c[i] - 1
                r["d48"] = drift48[coin]
                rows.append(r)
    df = pd.DataFrame(rows)
    df["short_unus48"] = -(df["f48"] - df["d48"])
    df["short_tot48"] = -df["f48"]
    act = df[df["fc"] < 0].copy()
    out["n_active_n_all"] = pd.Series({"active": len(act), "all_sundays": len(df)})
    g = {}
    for h in (12, 24, 48, 72, 96):
        x = -act[f"f{h}"]
        g[f"short_total_f{h}"] = [x.mean(), x.mean() / (x.std() / np.sqrt(len(x)))]
    out["active_short_total_by_h"] = pd.DataFrame(g, index=["mean", "t"]).T
    def summ(gr):
        x = gr["short_tot48"]; u = gr["short_unus48"]
        return pd.Series({"n": len(x), "tot": x.mean(), "t_tot": x.mean() / (x.std() / np.sqrt(len(x))), "unus": u.mean()})
    out["active_by_year"] = act.groupby("year").apply(summ)
    out["active_by_coin"] = act.groupby("coin").apply(summ)
    act["q_fc"] = pd.qcut(act["fc"].abs().rank(method="first"), 4, labels=False)
    out["active_by_fc_quart"] = act.groupby("q_fc").apply(summ)
    act["q_ret30"] = pd.qcut(act["ret30"].rank(method="first"), 4, labels=False)
    out["active_by_ret30_quart"] = act.groupby("q_ret30").apply(summ)
    act["q_7wd"] = pd.qcut(act["ret7wd"].rank(method="first"), 4, labels=False)
    out["active_by_weekdayret_quart"] = act.groupby("q_7wd").apply(summ)
    # all sundays: weekend return vs next 48h, by sign and vr
    df["side"] = np.where(df["wk_ret"] > 0, "rise", "fall")
    df["thin"] = np.where(df["vr"] < 1, "thin", "thick")
    df["rev48"] = -np.sign(df["wk_ret"]) * (df["f48"] - df["d48"])
    out["all_sundays_reversal_unusual"] = df.groupby(["side", "thin"]).apply(
        lambda gr: pd.Series({"n": len(gr), "rev_unus": gr["rev48"].mean(),
                              "t": gr["rev48"].mean() / (gr["rev48"].std() / np.sqrt(len(gr)))}))
    df["q_wk"] = pd.qcut(df["wk_ret"].rank(method="first"), 5, labels=False)
    out["all_sundays_by_wkret_quint_next48"] = df.groupby("q_wk").apply(
        lambda gr: pd.Series({"wk_ret": gr["wk_ret"].mean(), "f48": gr["f48"].mean(), "f48_minus_drift": (gr["f48"] - gr["d48"]).mean(),
                              "t": (gr["f48"] - gr["d48"]).mean() / ((gr["f48"] - gr["d48"]).std() / np.sqrt(len(gr)))}))
    # trades
    tr = pd.concat([t for wins in data["trades"].values() for t in wins.values() if len(t)])
    out["trades"] = pd.Series({"n": len(tr), "gross_mean": tr["profit_loss_percent"].mean(),
                               "net_mean": tr["net_profit_loss_percent"].mean(),
                               "win_share": (tr["net_profit_loss_percent"] > 0).mean(),
                               "dur_h_mean": tr["duration_minutes"].mean() / 60})
    # book by year
    d = pd.concat([x.assign(coin=c) for c, wins in data["days"].items() for x in wins.values()])
    d["year"] = pd.to_datetime(d["day"]).dt.year
    out["book_by_year"] = d.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    return out
