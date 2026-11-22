import numpy as np, pandas as pd

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            r1 = pd.Series(c).pct_change()
            mabs = r1.abs().rolling(720, min_periods=200).mean()
            vr = (b["volume"] / b["volume"].rolling(720, min_periods=200).mean()).values
            z = (r1 / mabs).values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for H in [1, 2, 4, 6]:
                idx = np.arange(0, len(b) - H, H)
                fr = c[idx + H] / c[idx] - 1
                rows.append(pd.DataFrame(dict(coin=coin, w=w, yr=yr[idx], H=H, z=z[idx], vr=vr[idx], fr=fr)))
    d = pd.concat(rows).dropna()
    d["ex"] = d.fr - d.groupby(["coin", "H"])["fr"].transform("mean")
    d["sz"] = d.z.abs()
    # signed with the move direction: positive = continuation
    d["cont"] = np.sign(d.z) * d.ex
    big = d[d.sz > 2.5].copy()
    big["vb"] = pd.cut(big.vr, [0, 1.5, 3, 5, np.inf])
    big["dir"] = np.where(big.z > 0, "up", "down")
    def agg(g):
        return pd.Series(dict(n=len(g), mean_cont_pct=100 * g.cont.mean(),
                              t=g.cont.mean() / (g.cont.std() / np.sqrt(len(g)))))
    out["continuation after |z|>2.5 hour by H, dir, vol band"] = big.groupby(["H", "dir", "vb"], observed=True).apply(agg).reset_index()
    s = big[(big.vr > 3) & (big.H == 2)]
    out["down-hour vr>3, H=2, bounce by coin"] = s[s.dir == "down"].groupby("coin").apply(agg)
    out["down-hour vr>3, H=2, bounce by year"] = s[s.dir == "down"].groupby("yr").apply(agg)
    out["up-hour vr>3, H=2/6 cont by coin"] = big[(big.vr > 3) & (big.dir == "up") & big.H.isin([2, 6])].groupby(["H", "coin"]).apply(agg)
    # trades
    t = pd.concat([t for wins in data["trades"].values() for t in wins.values()])
    t["px"] = -(t.exit_price / t.entry_price - 1) * 100
    t["fb"] = pd.qcut(t.entry_forecast.abs(), 4, duplicates="drop")
    out["trades by |entry forecast| quartile"] = t.groupby("fb", observed=True).agg(
        n=("px", "size"), short_price_move_pct=("px", "mean"), pl=("profit_loss_percent", "mean"),
        net=("net_profit_loss_percent", "mean"), dur_h=("duration_minutes", lambda x: x.mean() / 60))
    # days book
    dd = pd.concat([x.assign(coin=k) for k, wins in data["days"].items() for x in wins.values()])
    out["book daily"] = pd.Series(dict(mean=dd.book_return.mean(), sd=dd.book_return.std(),
                                       coin_mean=dd.coin_return.mean()))
    return out
