from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import NameForm


def home(request):
    print(request.build_absolute_uri()) #optional
    return render(request,'home.html')

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            request.session['form_data'] = form.cleaned_data    # Store data in the session
            return HttpResponseRedirect(reverse('result_page')) # Pass data to the result page

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
    return render(request, "name.html", {"form": form})

def result_page(request):
    print(request.build_absolute_uri()) #optional
    form = request.session.pop('form_data', None)
    return render(request,'thanks.html', {"form": form})