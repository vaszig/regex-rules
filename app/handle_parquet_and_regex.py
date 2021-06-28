from django.shortcuts import render, HttpResponse
from django.contrib import messages
import pandas as pd

from .forms import ResultsForm


def read_parquet():
    """Reads parquet file."""

    parquet_file = './UK_outlet_meal.parquet.gzip'
    try:
        df = pd.read_parquet(parquet_file, engine='auto', columns=['id_source', 'name', 'item_description', 'category']).iloc[0:100000]
        is_valid = True
    except Exception as e:
        is_valid = False
        return is_valid, e
    return is_valid, df


def regex_results(request, form):
    """Fetches the rows of the parquet file or the possible errors according to user's input."""

    type_of_search = form.cleaned_data['type_of_search']
    column = form.cleaned_data['column']
    pattern = form.cleaned_data['pattern']
    
    is_valid, data = read_parquet()

    if not is_valid:
        messages.info(request, data)
        return render(request, 'app/index.html', {'form': form})
    
    if column not in data.columns:
        messages.info(request, 'Column does not exist')
        return render(request, 'app/index.html', {'form': form})

    if type_of_search == 'contains':
        try:
            results = data[data[column].str.contains(pattern, na=False, regex=True)]
        except AttributeError:
            messages.info(request, 'Regex pattern cannot be applied on type of int')            
            return render(request, 'app/index.html', {'form': form})
    elif type_of_search == 'match_in':
        try:
            results = data[data[column].str.match(f'(?:^|\W){pattern}(?:$|\W)', na=False)]
        except AttributeError:
            messages.info(request, 'Regex pattern cannot be applied on type of int')            
            return render(request, 'app/index.html', {'form': form})
    elif type_of_search == 'match_out':
        try:
            results = data[~data[column].str.match(f'(?:^|\W){pattern}(?:$|\W)', na=False)]
        except AttributeError:
            messages.info(request, 'Regex pattern cannot be applied on type of int')            
            return render(request, 'app/index.html', {'form': form})
    
    return render(request, 'app/index.html', {'results': results.to_html(), 'form': form})