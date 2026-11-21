import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    H = 5
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr.extend(list(c[idx + H] / c[idx] - 1))
        drift[coin] = np.mean(allr) if allr else np.nan
        usual[coin] = np.std(allr) if allr else np.nan
    raw_col = "debug_info.components.break_touches.last_history_value"
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vol20 = pd.Series(r1).rolling(20).std().values
            ret20 = np.r_[np.full(20, np.nan), c[20:] / c[:-20] - 1] if n > 20 else np.full(n, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            raw = b[raw_col].values if raw_col in b else np.full(n, np.nan)
            for i in range(0, n - H, H):
                f = {}
                for h in (5, 10, 20):
                    f["fwd%d" % h] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                # any break in this grid cell -> first break bar
                cell = range(i, min(i + H, n - H))
                brk = [j for j in cell if (not np.isnan(raw[j])) and raw[j] > 0]
                j = brk[0] if brk else i
                rows.append(dict(coin=coin, win=w, brk=bool(brk), raw=raw[j] if brk else 0.0,
                                 fc=b["forecast"].values[j],
                                 f5=c[j + H] / c[j] - 1 if j + H < n else np.nan,
                                 f10=c[j + 10] / c[j] - 1 if j + 10 < n else np.nan,
                                 f20=c[j + 20] / c[j] - 1 if j + 20 < n else np.nan,
                                 r1=r1[j], vol=vol20[j], ret20=ret20[j],
                                 wd=ts.iloc[j].weekday(), yr=ts.iloc[j].year,
                                 drift=drift[coin], usual=usual[coin]))
    d = pd.DataFrame(rows)
    d["u5"] = d["f5"] - d["drift"]
    d["s5"] = d["u5"] / d["usual"]
    def summ(g, col="u5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["break_vs_not_u5"] = d.groupby("brk").apply(summ)
    out["break_vs_not_f10"] = d.groupby("brk").apply(lambda g: summ(g, "f10"))
    out["break_vs_not_f20"] = d.groupby("brk").apply(lambda g: summ(g, "f20"))
    bk = d[d.brk].copy()
    out["forecast_on_break_desc"] = bk["fc"].describe()
    out["raw_on_break_desc"] = bk["raw"].describe()
    bk["rawq"] = pd.qcut(bk["raw"].rank(method="first"), 4, labels=False)
    out["break_by_raw_quartile"] = bk.groupby("rawq").apply(summ)
    out["break_by_raw_quartile_f20"] = bk.groupby("rawq").apply(lambda g: summ(g, "f20"))
    # all cells: by prior 1-day move size (normalised)
    d["z1"] = d["r1"] / d["vol"]
    d["z1q"] = pd.qcut(d["z1"].rank(method="first"), 5, labels=False)
    out["all_by_prior_day_z_quintile"] = d.groupby("z1q").apply(summ)
    d["r20q"] = pd.qcut(d["ret20"].rank(method="first"), 5, labels=False)
    out["all_by_prior_20d_ret_quintile"] = d.groupby("r20q").apply(summ)
    d["volq"] = pd.qcut(d["vol"].rank(method="first"), 5, labels=False)
    out["all_by_vol_quintile"] = d.groupby("volq").apply(summ)
    out["break_by_year"] = bk.groupby("yr").apply(summ)
    out["break_by_prior20_tercile"] = bk.assign(q=pd.qcut(bk["ret20"].rank(method="first"), 3, labels=False)).groupby("q").apply(summ)
    # book: gain decomposition
    br, held, cm = [], [], []
    for coin, wins in bars.items():
        for w, b in wins.items():
            c = b["close"].values
            a = b["postRebalance_current_allocation"].values
            g = a[:-1] * (c[1:] / c[:-1] - 1)
            br.extend(g); held.extend(a[:-1])
    allday = []
    for coin, wins in days.items():
        for w, dd in wins.items():
            allday.append(dd[["coin_return", "book_return"]].dropna())
    D = pd.concat(allday)
    out["book_bar_gain_mean"] = float(np.mean(br))
    out["mean_alloc"] = float(np.mean(held))
    out["share_bars_in_position"] = float(np.mean(np.abs(held) > 1e-6))
    # trades
    tr = pd.concat([t for wins in data["trades"].values() for t in wins.values() if len(t)])
    out["trades_summary"] = tr[["profit_loss_percent", "net_profit_loss_percent", "duration_minutes"]].describe()
    return out
