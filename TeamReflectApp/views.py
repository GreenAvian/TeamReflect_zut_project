from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import FeedbackForm
from .models import Feedback, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def home(request):
    print(request.build_absolute_uri()) #optional
    return render(request,'base.html')

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

def result_feedbacks(request):
    print(request.build_absolute_uri()) #optional
    #form = request.session.pop('form_data', None) # Retrieve the session data
    #   OR
    feedbacks = Feedback.objects.all() # Fetch all Person records or the last inserted one
    return render(request, 'feedback_list.html', {"feedbacks": feedbacks})

#@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html',{'users': users})

def profile_view(request, username):
    profile = UserProfile.objects.get(user__username=username)
    return render(request, 'profile.html', {'profile': profile})

class DeleteUserView(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        if user != request.user and not request.user.is_superuser:
            raise Http404("You are not authorized to delete this user")
        
        user.delete()
        
        return redirect('home')


class ConfirmDeleteUserView(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user != request.user and not request.user.is_superuser:   
            return HttpResponseForbidden("You are not allowed to delete this user.")
        
        return render(request, 'confirm_delete.html', {'user': user})
    
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
         
        if user != request.user and not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowed to delete this user.")
        
        user.delete()
        return redirect('user_list')
    

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"