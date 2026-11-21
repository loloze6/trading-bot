import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    H = 24
    rows = []
    bookrows = []
    for coin, wins in data["bars"].items():
        # normal drift over all windows
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr.append(c[idx + H] / c[idx] - 1)
        allr = np.concatenate(allr)
        drift = allr.mean(); usual = allr.std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            v = b["volume"].values
            n = len(c)
            r24 = pd.Series(c).pct_change(24).values
            r72 = pd.Series(c).pct_change(72).values
            r240 = pd.Series(c).pct_change(240).values
            hr = pd.Series(c).pct_change().values
            absr = pd.Series(np.abs(hr))
            # share of the 24h move's absolute path in the largest 3 hours (jumpiness)
            top3 = absr.rolling(24).apply(lambda x: np.sort(x)[-3:].sum() / (x.sum() + 1e-12), raw=True).values
            vol24 = absr.rolling(24).sum().values
            vol240 = absr.rolling(240).sum().values / 10
            vshare = (pd.Series(v).rolling(24).max() / (pd.Series(v).rolling(24).sum() + 1e-12)).values
            f = b["forecast"].values
            idx = np.arange(0, n - H, H)
            for i in idx:
                if f[i] > 0 and not np.isnan(r24[i]):
                    rows.append(dict(coin=coin, w=w, f=f[i], fwd=c[i + H] / c[i] - 1, ex=c[i + H] / c[i] - 1 - drift,
                                     usual=usual, r72=r72[i], r240=r240[i], top3=top3[i], volratio=vol24[i] / vol240[i] if vol240[i] > 0 else np.nan,
                                     vshare=vshare[i], hour=pd.Timestamp(b["timestamp"].iloc[i]).hour))
            # turnover
            a = b["postRebalance_current_allocation"].values
            pa = b["previous_allocation"].values
            turn = np.nansum(np.abs(a - pa))
            gross = np.nansum(a[:-1] * (c[1:] / c[:-1] - 1))
            fees = np.nansum(b["postRebalance_total_value"].values - b["total_portfolio_value"].values) / np.nanmean(b["total_portfolio_value"].values)
            bookrows.append(dict(coin=coin, turn=turn, gross=gross, fees=fees, n=n, meanalloc=np.nanmean(a), inshare=np.mean(np.abs(a) > 1e-6)))
    d = pd.DataFrame(rows)
    d["dec"] = pd.qcut(d["f"], 5, labels=False)
    g = d.groupby("dec").agg(n=("ex", "size"), f=("f", "mean"), ex=("ex", "mean"), fwd=("fwd", "mean"))
    out["by_forecast_quintile"] = g
    for col in ["r72", "r240", "top3", "volratio", "vshare"]:
        dd = d.dropna(subset=[col]).copy()
        dd["q"] = pd.qcut(dd[col], 3, labels=False)
        gg = dd.groupby("q").agg(n=("ex", "size"), x=(col, "mean"), ex=("ex", "mean"), f=("f", "mean"))
        gg["t"] = dd.groupby("q")["ex"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
        out["by_" + col] = gg
    # deep falls only (top 40% forecast) x r240
    dd = d[d["dec"] >= 3].dropna(subset=["r240"]).copy()
    dd["q"] = pd.qcut(dd["r240"], 3, labels=False)
    out["deep_fall_by_r240"] = dd.groupby("q").agg(n=("ex", "size"), x=("r240", "mean"), ex=("ex", "mean"))
    dd = d[d["dec"] >= 3].dropna(subset=["top3"]).copy()
    dd["q"] = pd.qcut(dd["top3"], 3, labels=False)
    out["deep_fall_by_top3"] = dd.groupby("q").agg(n=("ex", "size"), x=("top3", "mean"), ex=("ex", "mean"))
    bk = pd.DataFrame(bookrows).groupby("coin").sum()
    bk["gross_per_turn_bps"] = bk["gross"] / bk["turn"] * 1e4
    bk["fee_per_turn_bps"] = -bk["fees"] / bk["turn"] * 1e4
    bk["turn_per_day"] = bk["turn"] / bk["n"] * 24
    out["book_by_coin"] = bk[["gross_per_turn_bps", "fee_per_turn_bps", "turn_per_day"]]
    # days
    dr = []
    for coin, wins in data["days"].items():
        for w, dy in wins.items():
            dr.append(dy.assign(coin=coin, w=w))
    D = pd.concat(dr)
    out["book_vs_coin_by_window"] = D.groupby("w")[["book_return", "coin_return"]].mean().mul(1e4)
    return out
