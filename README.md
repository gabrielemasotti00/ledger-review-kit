# Ledger Review Kit

Compare a bank export with a ledger export and generate a small JSON packet for a reviewer or an AI assistant. Runs offline with Python 3.10+ and its standard library.

## Try the synthetic example

```sh
python review.py bank.example.csv ledger.example.csv --days 3
python -m unittest -v
```

B1 points to L1. B2 has two candidates and needs a reviewer. B3 uses a different currency and has no candidate. L4 appears separately as a ledger entry without a bank candidate.

## Bring your own data

Prepare one UTF-8 comma-delimited CSV per source using the example headers in order. Give each row a unique opaque ID within its file. Use YYYY-MM-DD dates, uppercase three-letter currency codes and signed decimals with a period. Use the same sign convention on both sides. IDs are returned verbatim. Use one bank account per run.

A candidate requires the same currency, exact decimal amount and nonblank reference after trimming and case folding. The date difference may be up to the configured number of calendar days in either direction. A suggestion requires exactly one candidate on both sides. Split payments, exchange differences and missing references require manual investigation.

## Use with an AI assistant

Inspect the JSON before sharing it. Amounts, dates and references stay out of the packet. With opaque IDs, a reviewer can map questions back to the original rows locally. For example, give your assistant the synthetic output and ask: “List each ambiguous bank ID, cite all its candidate IDs, and suggest one supporting document to inspect. Leave unresolved items open.”

The tool only generates review suggestions. Confirm against source documents before posting adjustments. To contribute, add a synthetic regression case and run the test suite from the repository root.

## License

MIT. See LICENSE.
