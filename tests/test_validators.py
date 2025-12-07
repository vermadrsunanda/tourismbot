"""
Unit tests for input validators.
"""
import unittest
from src.validators import (
    validate_and_sanitize_input,
    validate_destination_name,
    validate_email
)


class TestValidators(unittest.TestCase):
    """Test cases for validator functions."""

    def test_validate_and_sanitize_input_valid(self):
        """Test sanitization of valid input."""
        result = validate_and_sanitize_input("Hello, world!")
        self.assertEqual(result, "Hello, world!")

    def test_validate_and_sanitize_input_empty(self):
        """Test that empty string returns None."""
        result = validate_and_sanitize_input("")
        self.assertIsNone(result)

    def test_validate_and_sanitize_input_non_string(self):
        """Test that non-string input returns None."""
        result = validate_and_sanitize_input(123)
        self.assertIsNone(result)

    def test_validate_and_sanitize_input_too_long(self):
        """Test that overly long input returns None."""
        long_string = "a" * 1001
        result = validate_and_sanitize_input(long_string)
        self.assertIsNone(result)

    def test_validate_destination_name_valid(self):
        """Test valid destination name."""
        self.assertTrue(validate_destination_name("Paris"))
        self.assertTrue(validate_destination_name("New York"))
        self.assertTrue(validate_destination_name("San Francisco"))

    def test_validate_destination_name_invalid(self):
        """Test invalid destination names."""
        self.assertFalse(validate_destination_name("123"))
        self.assertFalse(validate_destination_name(""))
        self.assertFalse(validate_destination_name(None))

    def test_validate_email_valid(self):
        """Test valid email addresses."""
        self.assertTrue(validate_email("test@example.com"))
        self.assertTrue(validate_email("user.name@domain.co.uk"))

    def test_validate_email_invalid(self):
        """Test invalid email addresses."""
        self.assertFalse(validate_email("notanemail"))
        self.assertFalse(validate_email("@example.com"))
        self.assertFalse(validate_email(""))


if __name__ == '__main__':
    unittest.main()
