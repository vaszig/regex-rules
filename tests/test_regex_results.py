import pandas as pd
from django.test import TestCase
from pandas._testing import assert_frame_equal

from app.handle_parquet_and_regex import regex_results


class MockedForm:
    
    def __init__(self, type_of_search, column, pattern):
        self.type_of_search = type_of_search
        self.column = column
        self.pattern = pattern
    
    @property
    def cleaned_data(self):
        form_data = {
            "type_of_search":self.type_of_search, 
            "column":self.column,
            "pattern": self.pattern
        }
        return form_data



class TestRegexResults(TestCase):

    def test_regex_results_returns_right_data(self):
        df = pd.DataFrame(
                [
                    ["0001", "A name", "Description 1", "Rice"],
                    ["0002", "Dhall", "Description 2", "Kebab"],
                ],
                columns=["id_source", "name", "item_description", "category"]
            )
        form = MockedForm('contains', 'category', 'Rice')
        results, _ = regex_results(form, df)
        expected_df = pd.DataFrame(
                [
                    ["0001", "A name", "Description 1", "Rice"]
                ],
                columns=["id_source", "name", "item_description", "category"]
            )
        assert_frame_equal(results, expected_df)

    def test_regex_results_fails_with_wrong_column(self):
        df = pd.DataFrame(
                [
                    ["0001", "A name", "Description 1", "Rice"],
                    ["0002", "Dhall", "Description 2", "Kebab"],
                ],
                columns=["id_source", "name", "item_description", "category"]
            )
        
        form = MockedForm('contains', 'wrong column', 'Rice')
        results, errors = regex_results(form, df)
        self.assertEqual(errors, 'Column does not exist')
        self.assertEqual(results, None)

    def test_regex_results_fails_with_wrong_type_of_column(self):
        with self.assertRaises(Exception):
            df = pd.DataFrame(
                    [
                        ["0001", "A name", "Description 1", "Rice"],
                        ["0002", "Dhall", "Description 2", "Kebab"],
                    ],
                    columns=["id_source", "name", "item_description", "category"]
                )
            form = MockedForm('contains', 'id_source', 6)
            try:
                results, errors = regex_results(form, df)
            except ValueError as e:
                self.assertEqual(e.args, 'Regex pattern cannot be applied on type of int')