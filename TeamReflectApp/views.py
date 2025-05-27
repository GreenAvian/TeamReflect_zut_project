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
from django.contrib import messages
from django.shortcuts import redirect
import json  # Do konwersji danych do JSON
from django.http import JsonResponse, HttpResponseNotFound
from .models import LeaderPost, LeaderReport
from django.views.decorators.http import require_POST
import os
import traceback
import requests
from django.conf import settings
import logging


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
    # rating = request.POST.get('rating')
    
    comment = Comment.objects.create(created_by=request.user,
     #rating=rating, 
     leader_poll_item=item, content=content)
    #if (content):
        #comment.content = content
    return redirect('post_view', post_id=post.id_post)

@login_required
def vote_poll_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(LeaderPollItem, pk=item_id)
                
        # Update vote count and add user to voters
        if request.user in item.voters.all():
            # Remove vote
            item.votes -= 1
            item.voters.remove(request.user)
        else:
            # Add vote
            item.votes += 1
            item.voters.add(request.user)
                
        item.save()    
        return redirect('post_view', post_id=item.leader_post.id_post)
    return redirect('post_view', post_id=item.leader_post.id_post)

def post_view(request, post_id):
    post = LeaderPost.objects.get(id_post=post_id)

    for feedback in post.feedback_set.all():
        if feedback.for_group and request.user not in feedback.for_group.user_set.all():
            raise PermissionDenied("Nie należysz do grupy przypisanej do tego posta.")

    profile = UserProfile.objects.get(user__username=post.created_by)
    poll = post.poll_items.all()
    comments = Comment.objects.all()

    poll_data = {
    "labels": [],
    "votes": []
    }
    for item in poll:
        poll_data["labels"].append(item.content)
        poll_data["votes"].append(item.votes)

    # ⬇️ Dodajemy do kontekstu
    context = {
        'post': post,
        'poll': poll,
        'profile': profile,
        'comments': comments,
        'poll_data_json': json.dumps(poll_data)  # JSON dla wykresów
    }
    
    print("WYKRES:", poll_data)
    return render(request, 'group_post.html', context)

@login_required
def delete_group(request, group_id):
    """Usuwanie grupy"""
    group = get_object_or_404(Group, id=group_id)

   
    if not group.user_set.filter(id=request.user.id).exists():
        raise PermissionDenied("Nie jesteś członkiem tej grupy.")

    group.delete()
    return redirect('group_list')

def feedback_form(request, is_prefilled=False):
    if request.method == "POST":
        if not is_prefilled:
            form = FeedbackForm(request.POST)
            form.fields['for_group'].queryset = request.user.groups.all()  # filtrujemy tylko grupy użytkownika

            if form.is_valid():
                selected_group = form.cleaned_data.get('for_group')
                if selected_group and selected_group not in request.user.groups.all():
                    messages.error(request, "Nie możesz przypisać feedbacku do grupy, do której nie należysz.")
                    return redirect('get_feedback')

                feedback = form.save(commit=False)
                feedback.created_by = request.user
                feedback.save()
                return redirect('feedback_list')

        else:
            prefilled_field = request.POST.get('field')
            prefilled_val = request.POST.get('prefilled_val')
            if prefilled_field == "for_post":
                related_instance = get_object_or_404(LeaderPost, id_post=prefilled_val)
            elif prefilled_field == "for_user":
                related_instance = get_object_or_404(User, id=prefilled_val)
            elif prefilled_field == "for_group":
                related_instance = get_object_or_404(Group, id=prefilled_val)

                # dodane zabezpieczenie dla prefill grupy
                if related_instance not in request.user.groups.all():
                    messages.error(request, "Nie możesz dodać feedbacku dla grupy, do której nie należysz.")
                    return redirect('get_feedback')
            else:
                raise PermissionDenied("Niepoprawne pole prefillingu.")

            form = FeedbackForm(initial={
                'created_by': request.user.username,
                prefilled_field: related_instance,
            })

            # ustaw filtr także dla tego formularza (ważne!)
            form.fields['for_group'].queryset = request.user.groups.all()

    else:
        form = FeedbackForm(initial={'created_by': request.user.username})
        form.fields['for_group'].queryset = request.user.groups.all()  

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

    user_groups = request.user.groups.all()
    feedbacks = [f for f in feedbacks if not f.for_group or f.for_group in user_groups]

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
    ratings = list(Feedback.objects.values_list('rating', flat=True))
    rating_count = {i: 0 for i in range(1, 6)}  # Oceny 1–5

    for r in ratings:
        if r in rating_count:
           rating_count[r] += 1

    rating_labels = list(map(str, rating_count.keys()))  # ["1", "2", "3", "4", "5"]
    rating_values = list(rating_count.values())

    avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else 0

    return render(request, "feedback_list.html", {
    "feedbacks": feedbacks,
    "data_priority_avg": json.dumps(data_priority_avg),
    "data_priority_count": json.dumps(data_priority_count),
    "data_target_avg": json.dumps(data_target_avg),
    "data_target_count": json.dumps(data_target_count),
    "rating_labels": json.dumps(rating_labels),
    "rating_values": json.dumps(rating_values),
    "avg_rating": avg_rating,
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

    
    if feedback.for_group and request.user not in feedback.for_group.user_set.all():
       messages.error(request, "Nie masz dostępu do tego feedbacku, ponieważ nie należysz do przypisanej grupy.")
       return redirect("feedback_list") 
    
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
        print(request.POST)  # See all POST data
        
        if field == "all":
            profile.user.first_name = request.POST.get('first_name', profile.user.first_name)
            profile.user.last_name = request.POST.get('last_name', profile.user.last_name)
            profile.phone_number = request.POST.get('phone_number', profile.phone_number)
            profile.description = request.POST.get('description', profile.description)
        else:
            if field == "name":
                profile.user.first_name = request.POST.get('first_name', profile.user.first_name)
                profile.user.last_name = request.POST.get('last_name', profile.user.last_name)
                # profile.user.save()
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


        profile.user.save()
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
    
    
@login_required
@require_POST
def generate_leader_report(request, post_id):
    # Upewnij się, że użytkownik to lider
    #if not hasattr(request.user, 'profile') or not request.user.profile.is_leader:
        #return JsonResponse({'error': 'Brak uprawnień - tylko lider może generować raport.'}, status=403)

    try:
        post = LeaderPost.objects.prefetch_related('poll_items__comment_set').get(id_post=post_id)
    except LeaderPost.DoesNotExist:
        return HttpResponseNotFound("Nie znaleziono posta lidera.")

    feedback_context = f"Tytuł ankiety: {post.topic}\nTemat: {post.tag}\n\n"

    for i, item in enumerate(post.poll_items.all(), 1):
        feedback_context += f"Pytanie {i}: {item.content}\n"
        avg_rating = item.comment_set.aggregate(avg=Avg('rating'))['avg']
        if avg_rating:
            feedback_context += f"  Średnia ocena: {avg_rating:.2f}/5\n"
        for j, comment in enumerate(item.comment_set.all(), 1):
            user = comment.created_by.username if comment.created_by else "Anonimowy"
            feedback_context += f"  Odpowiedź {j} [{user}, ocena {comment.rating}/5]: {comment.content}\n"
        feedback_context += "\n"

    prompt = f"""
Na podstawie poniższej ankiety oraz komentarzy uczestników, wygeneruj raport dla lidera. Uwzględnij:
- Najczęstsze pozytywne obserwacje
- Obszary wymagające poprawy
- Średnie oceny (jeśli to możliwe)
- Ogólne wrażenie zespołu
- Rekomendacje

{feedback_context}
"""

    # Wyślij do zewnętrznego LLM (OLLAMA)
    try:
        response = requests.post(
            f"{settings.OLLAMA_API_URL}/api/generate",
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            },
            #timeout=300  # ważne, by nie zawiesić serwera #nie właśnie nie jest to ważne, zarówno django jak i nginx mają własne timeouty
        )

        logger = logging.getLogger(__name__)

        logger.info(f"Ollama response status: {response.status_code}")
        logger.info(f"Ollama response headers: {response.headers}")
        logger.info(f"Ollama response content: {response.text[:500]}")  # First 500 chars

        response.raise_for_status()
        result = response.json()
        summary = result.get("response", "Brak wygenerowanego raportu.")

    except Exception as e: 
        logger.error("Błąd połączenia z LLM:", exc_info=True)
        # traceback.print_exc()
        return JsonResponse({'error': f"Błąd LLM: {str(e)}"}, status=500)

    # Zapisz raport do bazy
    LeaderReport.objects.update_or_create(
        leader_post=post,
        defaults={'content': summary}
    )

    return JsonResponse({'report': summary})


def leader_post_detail(request, post_id):
    # Pobieranie posta lidera
    post = get_object_or_404(LeaderPost, id_post=post_id)

    # Pobieranie pytań ankiety
    poll_items = post.poll_items.all()
    report = LeaderReport.objects.filter(leader_post=post).first()

    # Przekazywanie danych do szablonu
    return render(request, 'leader_post_detail.html', {
        'post': post,
        'poll_items': poll_items,
        'report': report
    })

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"   
    
    
    

    
   