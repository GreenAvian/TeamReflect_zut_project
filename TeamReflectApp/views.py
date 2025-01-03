from django.views.generic import CreateView, UpdateView
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from .forms import FeedbackForm
from .models import Feedback, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group


def home(request):
    print(request.build_absolute_uri()) #optional
    return render(request,'base.html')

@login_required
def group_list(request):
    """Lista grup"""
    groups = Group.objects.all()
    return render(request, 'group_list.html', {'groups': groups})

@login_required
def group_detail(request, group_id):
    """Szczegóły grupy, dodawanie/usuwanie członków i ustawianie lidera"""
    group = get_object_or_404(Group, id=group_id)
    members = group.user_set.all()  

    if request.method == "POST":
        # Dodawanie członka
        if "add_member" in request.POST:
            username = request.POST.get("username")
            if username:
                try:
                    user = User.objects.get(username=username)
                    group.user_set.add(user)  
                except User.DoesNotExist:
                    return render(request, "group_detail.html", {
                        "group": group,
                        "members": members,
                        "error": "Nie znaleziono użytkownika.",
                    })
                return redirect("group_detail", group_id=group.id)

        
        if "remove_member" in request.POST:
            user_id = request.POST.get("user_id")
            user = get_object_or_404(User, id=user_id)
            group.user_set.remove(user)  
            return redirect("group_detail", group_id=group.id)

       
        if "set_leader" in request.POST:
            user_id = request.POST.get("user_id")
            user = get_object_or_404(User, id=user_id)
            if user not in group.user_set.all():
                raise PermissionDenied("Użytkownik nie jest członkiem tej grupy.")

            
            UserProfile.objects.filter(user__in=group.user_set.all()).update(is_leader=False)
          
            user.profile.is_leader = True
            user.profile.save()
            return redirect("group_detail", group_id=group.id)

    return render(request, "group_detail.html", {"group": group, "members": members})

@login_required
def create_group(request):
    """Tworzenie nowej grupy"""
    if request.method == 'POST':
        group_name = request.POST.get('name')
        if not group_name:
            return render(request, 'create_group.html', {'error': 'Nazwa grupy jest wymagana.'})

        group = Group.objects.create(name=group_name)
        group.user_set.add(request.user)  
        return redirect('group_list')

    return render(request, 'create_group.html')

@login_required
def delete_group(request, group_id):
    """Usuwanie grupy"""
    group = get_object_or_404(Group, id=group_id)

   
    if not group.user_set.filter(id=request.user.id).exists():
        raise PermissionDenied("Nie jesteś członkiem tej grupy.")

    group.delete()
    return redirect('group_list')

def get_feedback(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # If you don't do it this way it won't work
            feedback = form.save(commit=False)
            feedback.created_by = request.user
            feedback.save()
            return HttpResponseRedirect(reverse('result_feedbacks'))
        
    # GET
    else:
        form = FeedbackForm(initial={'created_by': request.user.username})
        
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
    can_edit = False
    if request.user == profile.user or request.user.is_superuser:
        can_edit = True
    return render(request, 'profile.html', {'profile': profile, 'can_edit': can_edit})

def feedback_view(request, id_feedback):
    feedback = Feedback.objects.get(id_feedback=id_feedback)
    if request.method == "POST":
        feedback.likes = feedback.likes + int(request.POST.get('likes', feedback.rating))
        feedback.save()
    return render(request, 'feedback.html', {'feedback': feedback})

@login_required
def edit_profile(request, username):
    profile = get_object_or_404(UserProfile, user__username=username)

    # Check if the user is the owner of the profile or a superuser
    if request.user != profile.user and not request.user.is_superuser:
        raise PermissionDenied("You are not authorized to edit this profile.")

    if request.method == "POST":
        field = request.POST.get('field')

        if field == "name":
            profile.user.first_name = request.POST.get('first_name', profile.user.first_name)
            profile.user.last_name = request.POST.get('last_name', profile.user.last_name)
            profile.user.save()
        elif field == "phone_number":
            profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        elif field == "description":
            profile.description = request.POST.get('description', profile.description)
        elif field == "rating":
            profile.rating = profile.rating + int(request.POST.get('rating', profile.rating))
        else:
            raise PermissionDenied("Invalid field.")

        profile.save()
    return redirect('profile_view', username=profile.user.username)

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
   