"""
Kraken forward recorder (roadmap Phase 2.4).

Standalone, additive package. Imports NOTHING from `trading-bot/` and modifies
nothing there; the only contact with the bot tree is the output directory
`trading-bot/local_data/recorded_reserved/`, which is excluded from publication
by the `.gitignore` rule `trading-bot/local_data/*/`.

Data written by this package is RESERVED, not searchable. See
`strategy-research/config/campaign_data_policy.yaml:kraken_ws_forward_recorder`.
No stage, prescreen or diagnostic may read any recorded window until an
explicit, separately-committed designation releases it.
"""

__all__ = [
    "book_state",
    "compaction",
    "journal",
    "kraken_crc",
    "shard_reader",
    "shard_writer",
    "whale_features",
    "whale_report",
]
