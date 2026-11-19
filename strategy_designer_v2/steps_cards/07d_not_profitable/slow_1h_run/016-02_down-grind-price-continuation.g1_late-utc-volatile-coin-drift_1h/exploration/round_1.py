import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    slot = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"], utc=True)
            r1 = b["close"].shift(-1) / b["close"] - 1
            pos = b["postRebalance_current_allocation"].fillna(0)
            gross = pos * r1
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            turn = (b["postRebalance_current_allocation"] - b["previous_allocation"]).abs()
            nd = b["ts"].dt.floor("D").nunique()
            rows.append(dict(coin=coin, window=w, days=nd, gross=gross.sum(), fee=fee.sum(),
                             turnover=turn.sum(), meanpos_active=pos[pos != 0].mean()))
            # slot cases at 20:00 bars
            h = b["ts"].dt.hour
            c = b["close"].values
            idx = np.where(h.values == 20)[0]
            idx = idx[idx + 2 < len(b)]
            for i in idx:
                slot.append(dict(coin=coin, window=w, year=b["ts"].iloc[i].year,
                                 ret=c[i+2]/c[i]-1, pos=pos.iloc[i+1], fc=b["forecast"].iloc[i]))
    R = pd.DataFrame(rows); S = pd.DataFrame(slot)
    byc = R.groupby("coin")[["days","gross","fee","turnover"]].sum()
    byc["gross_per_day"] = byc.gross/byc.days; byc["fee_per_day"] = byc.fee/byc.days
    byc["fee_per_unit_turn"] = byc.fee/byc.turnover
    S["fcq"] = pd.qcut(S.fc.rank(method="first"), 5, labels=False)
    sl = S.groupby("coin").ret.agg(["mean","std","count"])
    sl["t"] = sl["mean"]/(sl["std"]/np.sqrt(sl["count"]))
    slq = S.groupby("fcq").agg(ret=("ret","mean"), pos=("pos","mean"), fc=("fc","mean"), n=("ret","size"))
    sly = S.groupby("year").ret.agg(["mean","count"])
    # book daily
    br = pd.concat([d["book_return"] for c in days for d in days[c].values()]).dropna()
    allr = R[["days","gross","fee","turnover"]].sum()
    return {"by_coin": byc, "overall": allr, "slot_ret_by_coin": sl, "slot_by_fc_quintile": slq,
            "slot_by_year": sly, "book_daily_mean": br.mean(), "book_daily_sd": br.std(),
            "mean_pos_active": R.meanpos_active.mean()}
