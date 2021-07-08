import pandas as pd


def read_parquet(parquet_file):
    """Reads parquet file."""

    try:
        df = pd.read_parquet(parquet_file, engine='auto', columns=['id_source', 'name', 'item_description', 'category']).iloc[0:100000]
        file_is_valid = True
    except Exception as e:
        file_is_valid = False
        return file_is_valid, e
    return file_is_valid, df


def regex_results(form, data):
    """Fetches the rows of the parquet file or the possible errors according to user's input."""

    results = None
    errors = {
        "column_name":"Column does not exist", 
        "column_type":"Regex pattern cannot be applied on type of int"
    }

    type_of_search = form.cleaned_data['type_of_search']
    column = form.cleaned_data['column']
    pattern = form.cleaned_data['pattern']
    
    if column not in data.columns:
        return results, errors["column_name"]

    if type_of_search == 'contains':
        try:
            results = data[data[column].str.contains(pattern, na=False, regex=True)]
        except AttributeError:
            return results, errors["column_type"]
    elif type_of_search == 'match_in':
        try:
            results = data[data[column].str.match(f'(?:^|\W){pattern}(?:$|\W)', na=False)]
        except AttributeError:
            return results, errors["column_type"]
    elif type_of_search == 'match_out':
        try:
            results = data[~data[column].str.match(f'(?:^|\W){pattern}(?:$|\W)', na=False)]
        except AttributeError:
            return results, errors["column_type"]
    
    return results, False