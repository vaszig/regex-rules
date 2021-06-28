from django.shortcuts import render, HttpResponse

from .forms import ResultsForm
from .handle_parquet_and_regex import regex_results


def list_regex_results(request):
    """View function for showing the results of regex pattern applied on a certain column of the parquet file."""
    
    if request.method == 'POST':
        form = ResultsForm(request.POST)
        if not form.is_valid():
            return render(request, 'app/index.html', {'form': form})
        return regex_results(request, form)

    elif request.method == 'GET':
        form = ResultsForm()
        return render(request, 'app/index.html', {'form': form})
    
    return HttpResponse('Method not allowed', status=405)
