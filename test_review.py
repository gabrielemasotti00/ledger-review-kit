import unittest
from review import load, reconcile


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.bank = load("bank.example.csv")
        self.ledger = load("ledger.example.csv")

    def test_demo(self):
        report = reconcile(self.bank, self.ledger)
        self.assertEqual([r["status"] for r in report["bank_review"]], ["suggested", "ambiguous", "unmatched"])
        self.assertEqual(report["ledger_without_candidate"], ["L4"])

    def test_shared_candidate_is_ambiguous(self):
        report = reconcile({"A": self.bank["B1"], "B": self.bank["B1"]}, self.ledger)
        self.assertTrue(all(r["status"] == "ambiguous" for r in report["bank_review"]))

    def test_date_window(self):
        self.assertEqual(reconcile(self.bank, self.ledger, 0)["bank_review"][0]["status"], "unmatched")
