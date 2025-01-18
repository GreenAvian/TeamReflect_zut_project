from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class Groups(models.Model):
    id_groups = models.TextField(db_column='id_Groups', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Groups'
        
class LeaderPost(models.Model):
    id_post = models.AutoField(db_column='id_Post', primary_key=True)
    created_by = models.CharField(db_column='Created_by', max_length=50, null=True)  
    topic = models.CharField(db_column='Topic', max_length=50, null=True)  # Field name made lowercase. This field type is a guess.
    content = models.TextField(db_column='Content', null=True)

    def __str__(self):
        return self.name
    class Meta:
        managed = True
        db_table = 'Leader_Post'
                
class LeaderPollItem(models.Model):
    id_item = models.AutoField(db_column='id_Item', primary_key=True)
    leader_post = models.ForeignKey(LeaderPost, db_column='Leader_post', on_delete=models.CASCADE, related_name='poll_items', blank=True, null=True)
    content = models.CharField(db_column='Content', max_length=150, blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        managed = True
        db_table = 'Leader_Poll'
        
        
class Feedback(models.Model):
    id_feedback = models.AutoField(db_column='id_Feedback', primary_key=True)
    title = models.CharField(db_column='Title', max_length=50, null=True)
    type = models.CharField(db_column='Type', max_length=50, null=True)
    rating = models.IntegerField(db_column='Rating', default = 0, blank=True)  # Field name made lowercase. This field type is a guess. 
    created_at = models.DateTimeField(db_column='Created_at', auto_now_add=True, null=True)
    priority = models.CharField(db_column='Priority', max_length=50, null=True)  # Field name made lowercase. This field type is a guess.
    created_by = models.CharField(db_column='Created_by', max_length=50, null=True)  # Field name made lowercase. This field type is a guess.
    content = models.TextField(db_column='Content', null=True)
    status = models.CharField(db_column='Status', max_length=50, null=True)
    likes = models.IntegerField(db_column='Likes', default = 0, blank=True)
    '''for_post = models.ForeignKey(LeaderPost, db_column='For_Post', on_delete=models.CASCADE, blank=True, null=True)
    for_user = models.ForeignKey(User, db_column='For_User', on_delete=models.CASCADE, blank=True, null=True)
    for_group = models.ForeignKey(Groups, db_column='For_Group', on_delete=models.CASCADE, blank=True, null=True)'''
    

    def __str__(self):
        return self.name
    class Meta:
        managed = True
        db_table = 'Feedback'

class FeedbackReview(models.Model):
    id_feedback = models.AutoField(db_column='id_Feedback', primary_key=True)
    user = models.CharField(db_column='User', max_length=50, null=True)  
    rating = models.IntegerField(db_column='Rating', default = 0, blank=True, null=False)  # Field name made lowercase. This field type is a guess.
    review = models.CharField(db_column='Review', max_length=50, null=True)  # Field name made lowercase. This field type is a guess.
    created_at = models.DateTimeField(db_column='Created_at', auto_now_add=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        managed = True
        db_table = 'Feedback_Review'        

class Feedbackvisibility(models.Model):
    id_feedbackvisibility = models.TextField(db_column='id_FeedbackVisibility', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    id_feedback = models.TextField(db_column='id_Feedback', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    id_users = models.TextField(db_column='id_Users', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    access_time = models.TextField(db_column='Access_time', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'FeedbackVisibility'


class Forms(models.Model):
    id_forms = models.TextField(db_column='id_Forms', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    type = models.TextField(db_column='Type', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    created_by = models.TextField(db_column='Created_by', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    created_at = models.TextField(db_column='Created_at', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Forms'


class Groupmembership(models.Model):
    id_membership = models.TextField(db_column='id_Membership', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    id_users = models.TextField(db_column='id_Users', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    id_groups = models.TextField(db_column='id_Groups', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    is_leader = models.TextField(db_column='is_Leader', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'GroupMembership'





class Roles(models.Model):
    id_role = models.TextField(db_column='id_Role', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Roles'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # Field name made lowercase. This field type is a guess.
    rating = models.IntegerField(db_column='Rating', default = 0, blank=True, null=False)  # Field name made lowercase. This field type is a guess.
    #role_id = models.TextField(db_column='Role_id', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    description = models.TextField(db_column='Description', blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(db_column='Phone_number', validators=[phone_regex], max_length=17, blank=True) # Validators should be a listhone_number = models.PhoneNumberField(db_column='Phone_number', null=False, blank=False, unique=True)
    is_leader = models.BooleanField(default=False) 
    profile_image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        managed = True
        db_table = 'User Profile'
        
        
        
