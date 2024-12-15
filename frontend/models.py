from django.db import models

class Person(models.Model): # --- Example model, delete this later !!! ---
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Feedback(models.Model):
    id_feedback = models.TextField(db_column='id_Feedback', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    type = models.TextField(db_column='Type', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    created_at = models.TextField(db_column='Created_at', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    priority = models.TextField(db_column='Priority', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    created_by = models.TextField(db_column='Created_by', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    content = models.TextField(db_column='Content', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Feedback'


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


class Groups(models.Model):
    id_groups = models.TextField(db_column='id_Groups', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Groups'


class Roles(models.Model):
    id_role = models.TextField(db_column='id_Role', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Roles'


class Users(models.Model):
    id_users = models.TextField(db_column='id_Users', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    first_name = models.TextField(db_column='First_name', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    last_name = models.TextField(db_column='Last_name', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    email = models.TextField(db_column='Email', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    rating = models.TextField(db_column='Rating', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    role_id = models.TextField(db_column='Role_id', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'Users'
