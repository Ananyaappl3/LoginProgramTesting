import os
import tempfile
import unittest
import login as app


class TestUsernameValidation(unittest.TestCase):

    def test_valid_username(self):
        self.assertTrue(app.valid_username("alice123"))

    def test_username_too_short(self):
        self.assertFalse(app.valid_username("abc"))

    def test_username_too_long(self):
        self.assertFalse(app.valid_username("abcdefghijklmnopqrstu"))

    def test_username_with_spaces(self):
        self.assertFalse(app.valid_username("alice smith"))

    def test_username_with_special_characters(self):
        self.assertFalse(app.valid_username("alice!"))

    def test_empty_username(self):
        self.assertFalse(app.valid_username(""))


class TestPasswordValidation(unittest.TestCase):

    def test_valid_password(self):
        self.assertTrue(app.valid_password("Strong!123"))

    def test_password_too_short(self):
        self.assertFalse(app.valid_password("Abc!123"))

    def test_password_without_uppercase(self):
        self.assertFalse(app.valid_password("strong!123"))

    def test_password_without_lowercase(self):
        self.assertFalse(app.valid_password("STRONG!123"))

    def test_password_without_digit(self):
        self.assertFalse(app.valid_password("Strong!abc"))

    def test_password_without_special_character(self):
        self.assertFalse(app.valid_password("Strong1234"))

    def test_empty_password(self):
        self.assertFalse(app.valid_password(""))


class TestAccountFunctions(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_file = app.STORAGE_FILE
        app.STORAGE_FILE = os.path.join(
            self.temp_dir.name, "storage.txt"
        )

    def tearDown(self):
        app.STORAGE_FILE = self.old_file
        self.temp_dir.cleanup()

    def test_register_account(self):
        success, message = app.register(
            "alice123", "Strong!123"
        )
        self.assertTrue(success)
        self.assertTrue(os.path.exists(app.STORAGE_FILE))

    def test_saved_account_can_be_read(self):
        app.register("alice123", "Strong!123")

        logins = app.read_logins()

        self.assertIn("alice123", logins)
        self.assertEqual(logins["alice123"], "Strong!123")

    def test_duplicate_username_rejected(self):
        app.register("alice123", "Strong!123")

        success, message = app.register(
            "alice123", "Another!123"
        )

        self.assertFalse(success)
        self.assertEqual(len(app.read_logins()), 1)

    def test_invalid_username_not_saved(self):
        success, message = app.register(
            "abc", "Strong!123"
        )

        self.assertFalse(success)
        self.assertFalse(os.path.exists(app.STORAGE_FILE))

    def test_invalid_password_not_saved(self):
        success, message = app.register(
            "alice123", "weak"
        )

        self.assertFalse(success)
        self.assertFalse(os.path.exists(app.STORAGE_FILE))

    def test_login_with_correct_credentials(self):
        app.register("alice123", "Strong!123")

        success, message = app.login(
            "alice123", "Strong!123"
        )

        self.assertTrue(success)

    def test_login_with_wrong_password(self):
        app.register("alice123", "Strong!123")

        success, message = app.login(
            "alice123", "Wrong!123"
        )

        self.assertFalse(success)

    def test_login_with_unknown_username(self):
        success, message = app.login(
            "unknown", "Strong!123"
        )

        self.assertFalse(success)

    def test_two_accounts_are_preserved(self):
        app.register("alice123", "Strong!123")
        app.register("bob1234", "Another!123")

        logins = app.read_logins()

        self.assertIn("alice123", logins)
        self.assertIn("bob1234", logins)
        self.assertEqual(len(logins), 2)


if __name__ == "__main__":
    unittest.main()