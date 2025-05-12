from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from .forms import FeedbackForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Avg, Count
import json  # Do konwersji danych do JSON


def home(request):
    print(request.build_absolute_uri()) #optional
    return render(request,'base.html')

@login_required
def group_list(request):
    """Lista grup, do których należy zalogowany użytkownik"""
    groups = request.user.groups.all()  # Pobieranie grup, do których należy użytkownik
    return render(request, 'group_list.html', {'groups': groups})

@login_required
def group_detail(request, group_id):
    """Szczegóły grupy, dodawanie/usuwanie członków i ustawianie lidera"""
    group = get_object_or_404(Group, id=group_id)

    # Sprawdzenie, czy użytkownik jest członkiem grupy
    if group not in request.user.groups.all():
        raise PermissionDenied("Nie masz dostępu do tej grupy.")

    members = group.user_set.all()

    if request.method == "POST":
        if "add_member" in request.POST:
            username = request.POST.get("username")
            if username:
                try:
                    user = User.objects.get(username=username)
                    if user in group.user_set.all():
                        messages.error(request, f"Użytkownik {username} jest już członkiem grupy.")
                    else:
                        group.user_set.add(user)
                        Member = Groupmembership()
                        Member.id_user = user.id
                        Member.id_group = group.id
                        Member.is_leader = False
                        Member.save()
                        messages.success(request, f"Użytkownik {username} został dodany do grupy.")
                except User.DoesNotExist:
                    messages.error(request, "Nie znaleziono użytkownika.")
                return redirect("group_detail", group_id=group.id)

        if "remove_member" in request.POST:
            user_id = request.POST.get("user_id")
            remover_id = request.user.id
            
            user = get_object_or_404(User, id=user_id)
            
            Member = get_object_or_404(Groupmembership, id_user=remover_id, id_group = group.id)
            Target = get_object_or_404(Groupmembership, id_user = user.id, id_group = group.id)
            
            print("czy jest liderem: ",Member.is_leader)
            
            print("czlonek tej grupy: ",Member.id_group)
            
            print("id tej grupy: ",group.id)
            
            
            
            
            if (Member.is_leader == 1 and int(Member.id_group) == group.id):
                
                group.user_set.remove(user)
                group.save()
                messages.success(request, f"Użytkownik {user.username} został usunięty z grupy.")
                Target.delete()
                print("POPRAWNE")
            else:    
                messages.error(request, f"Nie masz uprawnień do usuwania członków grupy")     
                print("NIEPOPRAWNE")
            print("wykonane")    
                    
            return redirect("group_detail", group_id=group.id)

        if "set_leader" in request.POST:
            # Sprawdź, czy aktualny użytkownik jest liderem
            if not hasattr(request.user, 'profile') or not request.user.profile.is_leader:
                raise PermissionDenied("Tylko lider grupy może zmienić lidera.")

            user_id = request.POST.get("user_id")
            user = get_object_or_404(User, id=user_id)

            # Sprawdź, czy użytkownik należy do grupy
            if user not in group.user_set.all():
                raise PermissionDenied("Użytkownik nie jest członkiem tej grupy.")

            # Ustaw wszystkich jako nie-liderów
            UserProfile.objects.filter(user__in=group.user_set.all()).update(is_leader=False)

            # Ustaw nowego lidera
            if not hasattr(user, 'profile'):
                raise Exception(f"Użytkownik {user.username} nie ma przypisanego profilu.")
            user.profile.is_leader = True
            user.profile.save()
            messages.success(request, f"Użytkownik {user.username} został nowym liderem.")
            return redirect("group_detail", group_id=group.id)
        
    users = User.objects.exclude(id__in=members.values_list('id', flat=True))
    return render(request, "group_detail.html", {"group": group, "members": members, "users":users})

@login_required
def create_group(request):
    """Tworzenie nowej grupy"""
    if request.method == 'POST':
        group_name = request.POST.get('name')
        if not group_name:
            return render(request, 'create_group.html', {'error': 'Nazwa grupy jest wymagana.'})

      
        if Group.objects.filter(name=group_name).exists():
            return render(request, 'create_group.html', {
                'error': f'Grupa o nazwie "{group_name}" już istnieje.',
                'group_name': group_name,
            })
        #print("etap1")
        
        user = request.user
        #print("etap2")
        group = Group.objects.create(name=group_name)
        group.user_set.add(request.user)  
        GroupLeader = Groupmembership()
        GroupLeader.id_membership = 1#???
        GroupLeader.id_user = user.id
        GroupLeader.id_group = group.id
        GroupLeader.is_leader = True
        GroupLeader.save()
        #print("etap3")
        #user.profile.is_leader = True
        #user.profile.which_group_is_leader.append(group_name)
        #user.profile.save()
        #print("etap4")
        #print("Kto jest liderem",user.profile.which_group_is_leader)
        #print("Lider tej grupy", GroupLeader.id_user)
        #print("Twórcą grupy jest",user.id )
        return redirect('group_list')

    return render(request, 'create_group.html')

@login_required
def leader_post_form(request):
    return render(request,'post_form.html')

@login_required
def leader_post(request):
    topic = request.POST.get('topic')
    content = request.POST.get('content')
    tag = request.POST.get('tag')
    poll_options = request.POST.getlist('pollOption[]')  #Grabs all poll options

    if (topic and content):
        leader_post = LeaderPost.objects.create(created_by=request.user.username, topic=topic, content=content, tag=tag)
        for option in poll_options:
            if option.strip():  #Avoid saving empty options
                LeaderPollItem.objects.create(leader_post=leader_post, content=option)
        return redirect('post_view', post_id=leader_post.id_post)
    return redirect('group_list')

@login_required #TODO -- extend this
def comment_post(request):
    
    id_item = request.POST.get('id_item')
    item = LeaderPollItem.objects.get(id_item=id_item)
    post = item.leader_post
    content = request.POST.get('content')
    rating = request.POST.get('rating')
    
    comment = Comment.objects.create(created_by=request.user, rating=rating, leader_poll_item=item, content=content)
    #if (content):
        #comment.content = content
    
    return redirect('post_view', post_id=post.id_post)

def post_view(request, post_id):
    post = LeaderPost.objects.get(id_post=post_id)
    profile = UserProfile.objects.get(user__username=post.created_by)
    poll = post.poll_items.all()
    comments = Comment.objects.all()
    return render(request, 'group_post.html', {'post': post, 'poll':poll, 'profile':profile, 'comments':comments})

@login_required
def delete_group(request, group_id):
    """Usuwanie grupy"""
    group = get_object_or_404(Group, id=group_id)

   
    if not group.user_set.filter(id=request.user.id).exists():
        raise PermissionDenied("Nie jesteś członkiem tej grupy.")

    group.delete()
    return redirect('group_list')

def feedback_form(request, is_prefilled = False):
    if request.method == "POST":
        if (not is_prefilled): # Check if we're allowed to make a simple empty form
            # create a form instance and populate it with data from the request:
            form = FeedbackForm(request.POST)
            if form.is_valid():
                # If you don't do it this way it won't work
                feedback = form.save(commit=False)
                feedback.created_by = request.user
                feedback.save()
                return HttpResponseRedirect(reverse('feedback_list'))
        else: # There are fields that need prefilling
            prefilled_field = request.POST.get('field')
            prefilled_val = request.POST.get('prefilled_val')
            if prefilled_field == "for_post":
                related_instance = get_object_or_404(LeaderPost, id_post=prefilled_val) # Can't just fill the field with an ID, you gotta grab the object instance
                form = FeedbackForm(initial={
                    'created_by': request.user.username,
                    prefilled_field: related_instance,
                })
            elif prefilled_field == "for_user":
                related_instance = get_object_or_404(User, id=prefilled_val)
                form = FeedbackForm(initial={
                    'created_by': request.user.username,
                    prefilled_field: related_instance,
                })
            elif prefilled_field == "for_group":
                related_instance = get_object_or_404(Group, id=prefilled_val)
                form = FeedbackForm(initial={
                    'created_by': request.user.username,
                    prefilled_field: related_instance,
                })
            else:
                raise PermissionDenied("You are trying to fill a column that doesn't exist")
    # On normal GET
    else:
        form = FeedbackForm(initial={'created_by': request.user.username})
        
    return render(request, "feedback_form.html", {"form": form})
def get_priority_value(priority):
    mapping = {
        "niski": 3,
        "średni": 2,
        "wysoki": 1
    }
    return mapping.get(priority.lower(), 0)
def feedback_list(request):
    sort = request.GET.get('sort', 'newest')  # domyślne sortowanie

    if sort == 'oldest':
        feedbacks = Feedback.objects.all().order_by('created_at')
    elif sort == 'priority':
        feedbacks = sorted(Feedback.objects.all(), key=lambda f: get_priority_value(f.priority))
    elif sort == 'priority_desc':
        feedbacks = sorted(Feedback.objects.all(), key=lambda f: get_priority_value(f.priority), reverse=True)
    elif sort == 'author':
         feedbacks = Feedback.objects.all().order_by('created_by')
    elif sort == 'rating_desc':
         feedbacks = Feedback.objects.all().order_by('-rating', 'created_at')  
    elif sort == 'rating':
         feedbacks = Feedback.objects.all().order_by('rating', 'created_at')  
    else:  # 'newest'
        feedbacks = Feedback.objects.all().order_by('-created_at')

    priority_order = ["Niski", "Średni", "Wysoki"]

    feedback_counts = Feedback.objects.values("priority").annotate(count=Count("id_feedback"))
    data_priority_count_unsorted = {f["priority"]: f["count"] for f in feedback_counts if f["count"] > 0}
    data_priority_count = {
        k: data_priority_count_unsorted[k]
        for k in priority_order if k in data_priority_count_unsorted
}
# Średnie oceny
    feedback_avg = Feedback.objects.values("priority").annotate(avg_rating=Avg("rating"))
    data_priority_avg_unsorted = {f["priority"]: f["avg_rating"] for f in feedback_avg if f["avg_rating"] is not None}
    data_priority_avg = {k: data_priority_avg_unsorted[k] for k in priority_order if k in data_priority_avg_unsorted}


    # ŚREDNIA ocena dla typu odbiorcy (słupkowy)
    feedback_avg_type = {
        "Dla użytkownika": Feedback.objects.filter(for_user__isnull=False).aggregate(avg=Avg("rating"))["avg"],
        "Dla grupy": Feedback.objects.filter(for_group__isnull=False).aggregate(avg=Avg("rating"))["avg"],
        "Do posta": Feedback.objects.filter(for_post__isnull=False).aggregate(avg=Avg("rating"))["avg"],
    }
    data_target_avg = {k: v for k, v in feedback_avg_type.items() if v is not None}

    # LICZBA feedbacków dla typu odbiorcy (kołowy)
    feedback_counts_type = {
        "Dla użytkownika": Feedback.objects.filter(for_user__isnull=False).count(),
        "Dla grupy": Feedback.objects.filter(for_group__isnull=False).count(),
        "Do posta": Feedback.objects.filter(for_post__isnull=False).count(),
    }
    data_target_count = {k: v for k, v in feedback_counts_type.items() if v > 0}

    print("Feedback count for post:", feedback_counts_type["Do posta"])
    print("Feedback count for user:", feedback_counts_type["Dla użytkownika"])
    print("Feedback count for group:", feedback_counts_type["Dla grupy"])
    print("DATA TARGET:", data_target_count)

    return render(request, "feedback_list.html", {
        "feedbacks": feedbacks,
        "data_priority_avg": json.dumps(data_priority_avg),
        "data_priority_count": json.dumps(data_priority_count),
        "data_target_avg": json.dumps(data_target_avg),
        "data_target_count": json.dumps(data_target_count),
    })


#@login_required
def post_list(request):
    sort = request.GET.get('sort', 'newest')

    if sort == 'title_asc':
        posts = LeaderPost.objects.all().order_by('topic')
    elif sort == 'title_desc':
        posts = LeaderPost.objects.all().order_by('-topic')
    elif sort == 'tag_ankieta':
        posts = LeaderPost.objects.filter(tag__iexact='ankieta')
    elif sort == 'tag_ogolny':
        posts = LeaderPost.objects.filter(tag__iexact='ogólny')
    elif sort == 'tag_zadanie':
        posts = LeaderPost.objects.filter(tag__iexact='zadanie')
    elif sort == 'oldest':
        posts = LeaderPost.objects.all().order_by('id_post')  # lub 'created_at' jeśli istnieje
    else:
        posts = LeaderPost.objects.all().order_by('-id_post')  # domyślnie najnowsze

    return render(request, 'post_list.html', {
        'posts': posts,
        'sort': sort
    })

#@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html',{'users': users})

def profile_view(request, username):
    profile = UserProfile.objects.get(user__username=username)
    feedbacks = Feedback.objects.filter(created_by=username)
    print(f"Feedbacks for {username}: {feedbacks.count()} entries found.")
    can_edit = False
    if request.user == profile.user or request.user.is_superuser:
        can_edit = True
    return render(request, 'profile.html', {'profile': profile, 'can_edit': can_edit, 'feedbacks' : feedbacks})

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
        elif field == "image":
            if 'image' in request.FILES:
                profile.profile_image = request.FILES['image']
            else:
                raise PermissionDenied("No image uploaded.")
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
    
    

    
   