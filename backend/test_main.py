import unittest
from unittest.mock import patch

from fastapi import HTTPException

from backend.main import Enquiry, app, create_enquiry


class MainAppTests(unittest.TestCase):
    def test_app_is_available(self):
        self.assertEqual(app.title, "NEXOVERSE API")

    def test_enquiry_requires_database_configuration(self):
        enquiry = Enquiry(
            name="Test User",
            email="test@example.com",
            service="Website Development",
            message="Need a landing page for a new business.",
        )

        with patch("backend.main.supabase", None):
            with self.assertRaises(HTTPException) as exc:
                create_enquiry(enquiry)

        self.assertEqual(exc.exception.status_code, 503)


if __name__ == "__main__":
    unittest.main()
