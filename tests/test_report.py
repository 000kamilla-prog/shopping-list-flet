import importlib.util
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from storage import PairStorage


@unittest.skipUnless(importlib.util.find_spec("flet") is not None, "Flet не установлен")
class ReportTests(unittest.TestCase):
    def test_report_is_saved_in_required_format(self):
        import app as app_module
        from app import ShoppingApp

        application = ShoppingApp.__new__(ShoppingApp)
        application.session = PairStorage()
        application.session.set("login", "student")
        application.session.set("time_in", datetime(2026, 10, 13, 12, 30, 15))

        with tempfile.TemporaryDirectory() as folder:
            fake_file = Path(folder) / "app.py"
            with patch.object(app_module, "__file__", str(fake_file)):
                application.save_report()

            report = (Path(folder) / "reports" / "report.txt").read_text(encoding="utf-8")
            self.assertIn("login", report)
            self.assertIn("time_in", report)
            self.assertIn("time_out", report)
            self.assertIn("student", report)
            self.assertIn("13.10.2026 12:30:15", report)
            self.assertRegex(report, r"\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}")


if __name__ == "__main__":
    unittest.main()
