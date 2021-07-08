import io

import pandas as pd
from django.test import TestCase
from pandas._testing import assert_frame_equal

from app.handle_parquet_and_regex import read_parquet
    
    
def mocked_parquet_file(df):
    
    parquet_file = io.BytesIO()
    df.to_parquet(parquet_file, engine='auto')
    return parquet_file


class TestReadParquet(TestCase):

    def test_read_parquet_returns_right_data(self):
        df = pd.DataFrame(
                [
                    ["0001", "A name", "Description 1", "Rice"],
                    ["0002", "Dhall", "Description 2", "Kebab"],
                ],
                columns=["id_source", "name", "item_description", "category"]
            )
        parquet_file = mocked_parquet_file(df)
        is_valid, data = read_parquet(parquet_file)
        self.assertAlmostEqual(is_valid, True)
        assert_frame_equal(data, df)

    def test_read_parquet_fails_with_missing_columns(self):
        with self.assertRaises(Exception):
            df = pd.DataFrame(
                    [
                        ["0001", "A name", "Description 1", "Rice"],
                        ["0002", "Dhall", "Description 2", "Kebab"],
                    ],
                    columns=["name", "item_description", "category"]
                )
            parquet_file = mocked_parquet_file(df)
            try:
                is_valid, data = read_parquet(parquet_file)
            except ValueError as e:
                self.assertEqual(e.args, '3 columns passed, passed data had 4 columns')
    
