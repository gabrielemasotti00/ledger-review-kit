"""Create a local review packet from bank and ledger exports."""
import argparse
import csv
import json
import re
from collections import defaultdict
from datetime import date
from decimal import Decimal


def load(path):
    rows = {}
    with open(path, encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        fields = ["id", "date", "currency", "amount", "reference"]
        if reader.fieldnames != fields:
            raise ValueError(f"{path}: expected columns {','.join(fields)}")
        for row in reader:
            if None in row or None in row.values():
                raise ValueError(f"{path}:{reader.line_num}: invalid column count")
            key = row["id"].strip()
            if not key or key in rows:
                raise ValueError(f"{path}:{reader.line_num}: missing or repeated id")
            if not re.fullmatch(r"[A-Z]{3}", row["currency"]) or not re.fullmatch(r"-?[0-9]+(?:\.[0-9]+)?", row["amount"]):
                raise ValueError(f"{path}:{reader.line_num}: invalid currency or amount")
            rows[key] = (row["currency"], Decimal(row["amount"]), row["reference"].strip().casefold(), date.fromisoformat(row["date"]))
    return rows


def reconcile(bank, ledger, days=3):
    if days < 0:
        raise ValueError("days must be nonnegative")
    index = defaultdict(list)
    for key, (currency, amount, ref, posted) in ledger.items():
        if ref:
            index[currency, amount, ref].append((key, posted))
    candidates = {}
    claims = defaultdict(list)
    for key, (currency, amount, ref, posted) in bank.items():
        hits = [entry for entry, day in index.get((currency, amount, ref), []) if abs((posted-day).days) <= days]
        candidates[key] = hits
        for entry in hits:
            claims[entry].append(key)
    result = []
    for key, hits in candidates.items():
        status = "unmatched"
        if hits:
            status = "suggested" if len(hits) == 1 and len(claims[hits[0]]) == 1 else "ambiguous"
        result.append(dict(bank_id=key, status=status, ledger_candidates=hits))
    return dict(version=1, bank_review=result, ledger_without_candidate=[key for key in ledger if key not in claims])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bank")
    parser.add_argument("ledger")
    parser.add_argument("--days", type=int, default=3)
    args = parser.parse_args()
    try:
        print(json.dumps(reconcile(load(args.bank), load(args.ledger), args.days), indent=2))
    except (ValueError, OSError, csv.Error) as error:
        parser.exit(2, f"Input error: {error}\n")
