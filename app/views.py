from django.shortcuts import render, HttpResponse
from django.contrib import messages

from .forms import ResultsForm
from .handle_parquet_and_regex import regex_results, read_parquet


def list_regex_results(request):
    """View function for showing the results of regex pattern applied on a certain column of the parquet file."""
    
    if request.method == 'POST':
        form = ResultsForm(request.POST)
        if not form.is_valid():
            return render(request, 'app/index.html', {'form': form})
        
        parquet_file = './UK_outlet_meal.parquet.gzip'
        file_is_valid, data = read_parquet(parquet_file)
        if not file_is_valid:
            messages.info(request, data)
            return render(request, 'app/index.html', {'form': form})
        results, errors = regex_results(form, data)
        if errors:
            messages.info(request, errors)
            return render(request, 'app/index.html', {'form': form})
        return render(request, 'app/index.html', {'results': results.to_html(), 'form': form})

    elif request.method == 'GET':
        form = ResultsForm()
        return render(request, 'app/index.html', {'form': form})
    
    return HttpResponse('Method not allowed', status=405)