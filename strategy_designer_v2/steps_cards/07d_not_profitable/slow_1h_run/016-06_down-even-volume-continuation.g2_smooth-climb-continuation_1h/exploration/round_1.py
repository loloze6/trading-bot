import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    grid = []
    for coin, wins in data["bars"].items():
        # coin mean 72-bar return over all windows (grid)
        allfwd = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 72, 72)
            allfwd += list(c[idx + 72] / c[idx] - 1)
        mu72 = np.mean(allfwd)
        # mean hourly return over all windows
        hr = np.concatenate([b["close"].pct_change().values[1:] for b in wins.values()])
        muh = np.nanmean(hr)
        for w, b in wins.items():
            c = b["close"].values
            pos = b["postRebalance_current_allocation"].fillna(0).values
            r1 = np.append(c[1:] / c[:-1] - 1, np.nan)
            gross = pos * r1
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]).clip(lower=0) / b["total_portfolio_value"]
            rows.append(dict(coin=coin, win=w, gross=np.nansum(gross), mkt=np.nansum(pos[:-1]) * muh,
                             fees=fee.sum(), hours=len(b), meanpos=np.mean(pos),
                             turnover=np.abs(b["postRebalance_current_allocation"].fillna(0) - b["previous_allocation"].fillna(0)).sum()))
            ret72 = pd.Series(c).pct_change(72).values
            d = np.abs(np.diff(c, prepend=np.nan))
            s = pd.Series(d).rolling(72).sum().values
            er = np.abs(c - np.roll(c, 72)) / s
            er[:72] = np.nan
            idx = np.arange(0, len(c) - 72, 72)
            for i in idx:
                if ret72[i] > 0 and not np.isnan(er[i]):
                    grid.append(dict(coin=coin, win=w, er=er[i], fc=b["forecast"].iloc[i], ret72=ret72[i],
                                     ex=c[i + 72] / c[i] - 1 - mu72, pos=pos[i]))
    r = pd.DataFrame(rows)
    tot = r.groupby("coin")[["gross", "mkt", "fees", "hours", "turnover"]].sum()
    tot["timing"] = tot["gross"] - tot["mkt"]
    for k in ["gross", "mkt", "fees", "timing"]:
        tot[k + "_perday"] = tot[k] / tot["hours"] * 24
    tot["turnover_perday"] = tot["turnover"] / tot["hours"] * 24
    out["book components per coin"] = tot[[c for c in tot.columns if "perday" in c]]
    out["all coins per day gross/mkt/fees/timing"] = tot[[c for c in tot.columns if "perday" in c]].mean()
    g = pd.DataFrame(grid)
    g["er_q"] = pd.qcut(g["er"], 3, labels=["low", "mid", "high"])
    g["fc_q"] = pd.qcut(g["fc"].rank(method="first"), 3, labels=["low", "mid", "high"])
    g["ret_q"] = pd.qcut(g["ret72"], 3, labels=["small", "mid", "big"])
    out["fwd excess by raw ER tercile"] = g.groupby("er_q")["ex"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["fwd excess by forecast tercile"] = g.groupby("fc_q")["ex"].agg(["mean", "count"])
    out["fwd excess by ret72 tercile x ER tercile"] = g.pivot_table(index="ret_q", columns="er_q", values="ex", aggfunc="mean")
    out["corr fc vs raw er"] = g[["fc", "er"]].corr().iloc[0, 1]
    sl = stats.linregress(g["er"], g["ex"])
    out["slope raw er t"] = sl.slope / sl.stderr
    # daily book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, win=w))
    dd = pd.concat(dd)
    out["book vs coin daily mean by year"] = dd.assign(year=pd.to_datetime(dd["day"]).dt.year).groupby("year")[["book_return", "coin_return"]].mean()
    return out
