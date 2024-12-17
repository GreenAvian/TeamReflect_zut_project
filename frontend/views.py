from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import NameForm, FeedbackForm
from .models import Person, Feedback


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
            # request.session['form_data'] = form.cleaned_data    # Store data in the session
            #   OR
            form.save() # Save it to the database
            return HttpResponseRedirect(reverse('result_page')) # Pass data to the result page

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
    return render(request, "name.html", {"form": form})

def get_feedback(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = FeedbackForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # request.session['form_data'] = form.cleaned_data    # Store data in the session
            #   OR
            form.save() # Save it to the database
            return HttpResponseRedirect(reverse('result_feedbacks')) # Pass data to the result page

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FeedbackForm()
    return render(request, "feedback_form.html", {"form": form})

def result_page(request):
    print(request.build_absolute_uri()) #optional
    #form = request.session.pop('form_data', None) # Retrieve the session data
    #   OR
    people = Person.objects.all() # Fetch all Person records or the last inserted one
    return render(request, 'thanks.html', {"people": people})

def result_feedbacks(request):
    print(request.build_absolute_uri()) #optional
    #form = request.session.pop('form_data', None) # Retrieve the session data
    #   OR
    feedbacks = Feedback.objects.all() # Fetch all Person records or the last inserted one
    return render(request, 'feedback_list.html', {"feedbacks": feedbacks})