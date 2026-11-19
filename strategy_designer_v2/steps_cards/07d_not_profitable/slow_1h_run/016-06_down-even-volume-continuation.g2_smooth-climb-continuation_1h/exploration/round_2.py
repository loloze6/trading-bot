import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    hyp = []
    for coin, wins in data["bars"].items():
        hr_all = np.concatenate([b["close"].pct_change().values[1:] for b in wins.values()])
        muh = np.nanmean(hr_all)
        for w, b in wins.items():
            c = b["close"].values
            pos = b["postRebalance_current_allocation"].fillna(0).values
            prev = b["previous_allocation"].fillna(0).values
            ch = np.abs(pos - prev)
            reg = b["regime"].values
            regprev = np.roll(reg, 1); regprev[0] = reg[0]
            flip = reg != regprev
            fc = b["forecast"].fillna(0).values
            rows.append(dict(coin=coin, win=w, turn_flip=ch[flip].sum(), turn_in=ch[~flip & (reg == "trending")].sum(),
                             turn_other=ch[~flip & (reg != "trending")].sum(), hours=len(b),
                             share_trend=(reg == "trending").mean(),
                             fc_absdiff=np.abs(np.diff(fc)).sum()))
            # hypothetical: raw ER position (no standardisation), vol-scaled like book
            r1 = np.append(c[1:] / c[:-1] - 1, np.nan)
            d = np.abs(np.diff(c, prepend=np.nan))
            s = pd.Series(d).rolling(72).sum().values
            ret72 = pd.Series(c).pct_change(72).values
            er = np.abs(c - np.roll(c, 72)) / s
            er[:72] = np.nan
            vol = pd.Series(r1).shift(1).rolling(720, min_periods=100).std().values * np.sqrt(8760)
            raw = np.where(ret72 > 0, er, 0.0)
            hp = np.clip(np.nan_to_num(raw * 2 * 0.382 / vol), 0, 2)
            # also only rebalance every 24h
            hp24 = hp.copy()
            for i in range(len(hp24)):
                if i % 24 != 0:
                    hp24[i] = hp24[i - 1] if i > 0 else 0
            for name, p in [("rawER_hourly", hp), ("rawER_daily", hp24), ("book", pos)]:
                g = np.nansum(p[:-1] * r1[:-1])
                tv = np.abs(np.diff(p, prepend=0)).sum()
                hyp.append(dict(coin=coin, win=w, kind=name, gross=g, turnover=tv, hours=len(b), mkt=np.nansum(p[:-1]) * muh))
    r = pd.DataFrame(rows)
    t = r[["turn_flip", "turn_in", "turn_other", "fc_absdiff", "hours"]].sum()
    out["turnover per day by source"] = (t[["turn_flip", "turn_in", "turn_other"]] / t["hours"] * 24)
    out["forecast abs change per day"] = t["fc_absdiff"] / t["hours"] * 24
    out["share of bars trending"] = r["share_trend"].mean()
    h = pd.DataFrame(hyp).groupby("kind")[["gross", "turnover", "hours", "mkt"]].sum()
    for k in ["gross", "turnover", "mkt"]:
        h[k + "_perday"] = h[k] / h["hours"] * 24
    h["timing_perday"] = h["gross_perday"] - h["mkt_perday"]
    h["fee_est_perday"] = h["turnover_perday"] * 0.00108
    out["book vs raw-ER hypothetical"] = h[[c for c in h.columns if "perday" in c]]
    # daily book falls: worst days book vs coin, regime share
    dd = pd.concat([d.assign(coin=coin, win=w) for coin, wins in data["days"].items() for w, d in wins.items()])
    out["book daily mean sd sharpe"] = pd.Series(dict(mean=dd["book_return"].mean(), sd=dd["book_return"].std(),
                                                      sharpe=dd["book_return"].mean() / dd["book_return"].std() * np.sqrt(365)))
    return out
