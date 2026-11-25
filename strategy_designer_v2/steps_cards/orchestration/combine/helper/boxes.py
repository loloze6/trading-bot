"""combine, the box reader (card: ../card.md, "The words"; common/market_profile.md): for each book of the similarity
register, its presence in each box (a market profile and a side), the market's own share of each profile on the same
coins and dates, its times the market, its boxes (presence at least 10 %), and its mean daily return on its days in a
position inside its boxes.

  python3 orchestration/combine/helper/boxes.py [--kind paying] [--out FILE]

A coin-day is one coin on one day, read at the day's last bar (hourly books too). The position held at a day's close
earns the next day's return; that day is read in the box of the position's side and the coin's profile at the close
it was decided on. A coin-day whose profile is not yet known (under a year of history for the agitation) is left out
of the shares.
Why this cannot leak: it reads finished records after the fact; each day's profile uses closes up to that day.
"""
import argparse, functools, json, sys
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
STEPS = HERE.parents[2]
DATA = STEPS.parents[1] / "trading-bot" / "local_data"
REGISTER = STEPS / "orchestration" / "ideas_similarities_check" / "register"
sys.path.insert(0, str(STEPS / "common"))
from lib import coin_profile, PROFILES  # noqa: E402

PLACE = 0.10                           # the card's rule 1: a box holding at least 10 % of its days in a position
BOXES = [(p, s) for p in PROFILES for s in ("long", "short")]


@functools.lru_cache(None)
def profiles(coin, data=DATA):
    d = pd.read_csv(Path(data) / f"kraken_{coin}_1d.csv", usecols=["timestamp", "close"])
    d["day"] = pd.to_datetime(d.timestamp, format="ISO8601", utc=True).dt.tz_localize(None).dt.normalize()
    c = d.drop_duplicates("day").set_index("day").close
    p = coin_profile(c)
    return (p.trend + " " + p.agitation).where(p.trend.notna() & p.agitation.notna())


def coin_days(record):
    """One row per coin, window and day: the position at the day's close and the coin's value then (the chart file,
    else the bars kept on this machine)."""
    record = Path(record)
    chart = record / "chart_bars.csv.gz"
    if chart.exists():
        b = pd.read_csv(chart, usecols=["coin", "window", "timestamp", "position", "value"])
    else:
        parts = []
        for f in sorted(record.glob("*/w*/bars.csv.gz")):
            x = pd.read_csv(f, usecols=["timestamp", "postRebalance_current_allocation", "postRebalance_total_value"])
            parts.append(x.rename(columns={"postRebalance_current_allocation": "position", "postRebalance_total_value": "value"})
                         .assign(coin=f.parent.parent.name, window=f.parent.name))
        if not parts:
            return None
        b = pd.concat(parts, ignore_index=True)
    b["day"] = pd.to_datetime(b.timestamp, format="ISO8601", utc=True).dt.tz_localize(None).dt.normalize()
    b = b.sort_values(["coin", "window", "timestamp"]).groupby(["coin", "window", "day"], as_index=False).last()
    b["position"] = b.position.fillna(0.0)
    return b


def read_book(record, data=DATA):
    """The book's presence, market share, times the market and return per box, and its boxes."""
    b = coin_days(record)
    if b is None or b.empty:
        return None
    b["profile"] = None
    for coin, g in b.groupby("coin"):
        b.loc[g.index, "profile"] = g.day.map(profiles(coin, data)).values
    g = b.groupby(["coin", "window"])
    b["next_return"] = g.value.shift(-1) / b.value - 1            # what the position held at this close earned
    known = b[b.profile.notna()]
    held = known[known.position.abs() > 1e-9].copy()
    held["side"] = held.position.gt(0).map({True: "long", False: "short"})
    out = {}
    for p, s in BOXES:
        inbox = held[(held.profile == p) & (held.side == s)]
        presence = len(inbox) / len(held) if len(held) else 0.0
        market = (known.profile == p).mean() if len(known) else 0.0
        out[(p, s)] = {"presence": presence, "market": market, "times_market": presence / market if market else None,
                       "return": inbox.next_return.mean() if len(inbox) else None, "days": len(inbox)}
    boxes = [k for k, v in out.items() if v["presence"] >= PLACE]
    inside = held[[(p, s) in boxes for p, s in zip(held.profile, held.side)]]
    return {"boxes": boxes, "cells": out, "days_held": len(held), "return_in_boxes": inside.next_return.mean() if len(inside) else None}


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--kind", default="paying")
    a.add_argument("--out", type=Path, default=HERE.parent / "boxes.csv")
    args = a.parse_args()
    rows = []
    for r in json.loads((REGISTER / "books.json").read_text()):
        if r.get("kind", "paying") != args.kind:
            continue
        res = read_book(STEPS / "04_backtest" / r["run"] / "backtests" / r["id"])
        if res is None:
            rows.append({"key": r["key"], "status": "no record on this machine"}); continue
        for (p, s), v in res["cells"].items():
            rows.append({"key": r["key"], "run": r["run"], "id": r["id"], "side": r.get("side"), "profile": p, "box_side": s,
                         **{k: (round(x, 5) if isinstance(x, float) else x) for k, x in v.items()},
                         "in_boxes": (p, s) in res["boxes"], "return_in_boxes": res["return_in_boxes"], "days_held": res["days_held"]})
    pd.DataFrame(rows).to_csv(args.out, index=False)
    print(f"boxes: {len({x['key'] for x in rows})} books -> {args.out}")


if __name__ == "__main__":
    main()
