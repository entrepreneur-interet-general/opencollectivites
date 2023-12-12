from django.test import TestCase
from django.core.exceptions import ValidationError

from francedata.services.validators import (
    validate_insee_region,
    validate_insee_departement,
    validate_insee_commune,
    validate_siren,
)


class ValidateInseeRegionTestCase(TestCase):
    def test_valid_id_is_accepted(self) -> None:
        self.assertIsNone(validate_insee_region(53))
        self.assertIsNone(validate_insee_region("01"))

    def test_one_digit_id_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            validate_insee_region("1")

        with self.assertRaises(ValidationError):
            validate_insee_region(1)

    def test_three_digits_id_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            validate_insee_region("100")

        with self.assertRaises(ValidationError):
            validate_insee_region(643)

    def test_non_numeric_id_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            validate_insee_region("A53")


class ValidateInseeDepartementTestCase(TestCase):
    def test_valid_id_is_accepted(self) -> None:
        self.assertIsNone(validate_insee_departement(44))
        self.assertIsNone(validate_insee_departement("01"))
        self.assertIsNone(validate_insee_departement("2A"))
        self.assertIsNone(validate_insee_departement("976"))

    def test_one_digit_id_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            validate_insee_departement("1")

        with self.assertRaises(ValidationError):
            validate_insee_departement(1)

    def test_id_20_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            validate_insee_departement("20")

    def test_id_96_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            validate_insee_departement("96")

    def test_invalid_id_97x_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            validate_insee_departement("975")
            validate_insee_departement("978")

    def test_invalid_3_digit_id_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            validate_insee_departement("221")


class ValidateInseeCommuneTestCase(TestCase):
    def test_valid_id_is_accepted(self) -> None:
        self.assertIsNone(validate_insee_commune(35001))
        self.assertIsNone(validate_insee_commune("02345"))
        self.assertIsNone(validate_insee_commune("2B054"))
        self.assertIsNone(validate_insee_commune("97403"))

    def test_four_digits_id_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            validate_insee_commune("1001")

        with self.assertRaises(ValidationError):
            validate_insee_commune(3456)

    def test_id_20xxx_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            validate_insee_commune("20001")

    def test_id_96xxx_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            validate_insee_commune("96789")

    def test_invalid_id_97xxx_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            validate_insee_commune("97501")
            validate_insee_commune("97801")


class ValidateSirenTestCase(TestCase):
    def test_valid_siren_is_accepted(self) -> None:
        self.assertIsNone(validate_siren("233500016"))

    def test_siren_is_numeric(self) -> None:
        with self.assertRaises(ValidationError):
            validate_siren("invalid")

    def test_siren_has_correct_length(self) -> None:
        with self.assertRaises(ValidationError):
            validate_siren("3")
            validate_siren("23350001600040")

    def test_siren_validates_control_key(self) -> None:
        with self.assertRaises(ValidationError):
            validate_siren("233500018")
