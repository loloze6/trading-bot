"""
Kraken WS v2 forward recorder.

Captures verbatim L2 order-book (depth 10) and trade data from Kraken's
public WebSocket API for 19 USD-quoted pairs, with an attested coverage
journal, an hourly zstd-compacted shard layout, and a supervised restart
policy for unattended long-running capture.

See README.md for what this captures and why, and OPERATOR_HANDOVER.md for
install/monitor/data-handback instructions.
"""

__all__ = [
    "book_state",
    "compaction",
    "coverage_report",
    "disk_guard",
    "journal",
    "journal_mark",
    "kraken_crc",
    "liveness",
    "record_kraken_ws",
    "retrieval_manifest",
    "shard_writer",
]
