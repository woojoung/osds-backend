from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, nickname, date_of_birth, password=None):

        if not email:
            raise ValueError('must have user email')
        if not password:
            raise ValueError('must have user password')
        if not nickname:
            raise ValueError('must have user nickname')
        if not date_of_birth:
            raise ValueError('must have user date_of_birth')

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
            date_of_birth=date_of_birth
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, date_of_birth, password=None):

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            nickname=nickname,
            date_of_birth=date_of_birth
        )

        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
        Default Field of AbstractBaseUser
        id
        password = models.CharField(_("password"), max_length=128)
        last_login = models.DateTimeField(_("last login"), blank=True, null=True)
        is_active = True
    """
    user_id = models.BigAutoField(primary_key=True)
    delete_time = models.BigIntegerField(max_length=20, null=False, default=0)
    social_platform_type = models.IntegerField(max_length=11, null=False, default=0)
    social_platform_id = models.CharField(max_length=45, null=False, default='')
    marketing_agree_time = models.BigIntegerField(max_length=20, null=False, default=-1)
    profile_image_url = models.CharField(max_length=192, null=False, default='')
    nickname = models.CharField(max_length=45, null=False, default='')
    date_of_birth = models.DateField(null=False, default='1970-01-01')
    family_id = models.BigIntegerField(max_length=20, null=False, default=0)
    fcm_device_token = models.CharField(max_length=192, null=False, default='')
    fcm_token_timestamp = models.DateTimeField(null=False, default='1970-01-01 00:00:00')

    email = models.EmailField(max_length=255, null=False, default='')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    insert_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, default='1970-01-01 00:00:00')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'date_of_birth', 'nickname']

    class Meta:
        managed = False
        db_table = 'Users'
        unique_together = (('user_id', 'delete_time'), ('social_platform_id', 'delete_time'), ('email', 'delete_time'),)
        verbose_name = 'User'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Family(models.Model):

    family_id = models.BigAutoField(primary_key=True)
    delete_time = models.BigIntegerField(max_length=20, null=False, default=0)
    user_id = models.BigIntegerField(max_length=20, null=False, default=0)
    family_name = models.CharField(max_length=45, null=False, default='')
    family_profile_image_url = models.CharField(max_length=192, null=False, default='')
    invitation_code = models.CharField(max_length=45, null=False, default='')
    is_head_of_family = models.BooleanField(default=False)
    insert_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, default='1970-01-01 00:00:00')

    class Meta:
        managed = False
        db_table = 'Familys'
        unique_together = (('family_id', 'delete_time'),)
        verbose_name = 'Family'


class Album(models.Model):

    album_id = models.BigAutoField(primary_key=True)
    delete_time = models.BigIntegerField(max_length=20, null=False, default=0)
    user_id = models.BigIntegerField(max_length=20, null=False, default=0)
    family_id = models.BigIntegerField(max_length=20, null=False, default=0)
    album_image_url = models.CharField(max_length=192, null=False, default='')
    album_description = models.CharField(max_length=192, null=False, default='')
    insert_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, default='1970-01-01 00:00:00')

    class Meta:
        managed = False
        db_table = 'Albums'
        unique_together = (('album_id', 'delete_time'),)
        verbose_name = 'Album'


class AlbumReply(models.Model):

    album_reply_id = models.BigAutoField(primary_key=True)
    delete_time = models.BigIntegerField(max_length=20, null=False, default=0)
    album_id = models.BigIntegerField(max_length=20, null=False, default=0)
    user_id = models.BigIntegerField(max_length=20, null=False, default=0)
    family_id = models.BigIntegerField(max_length=20, null=False, default=0)
    content = models.CharField(max_length=192, null=False, default='')
    insert_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, default='1970-01-01 00:00:00')

    class Meta:
        managed = False
        db_table = 'AlbumReplys'
        unique_together = (('album_reply_id', 'delete_time'),)
        verbose_name = 'AlbumReply'


class Notification(models.Model):
    notification_id = models.BigAutoField(primary_key=True)
    delete_time = models.BigIntegerField()
    send_user_id = models.BigIntegerField(max_length=20, null=False, default=0)
    receive_user_id = models.BigIntegerField(max_length=20, null=False, default=0)
    notification_type = models.IntegerField(max_length=11, null=False, default=0)
    notification_title = models.CharField(max_length=192, null=False, default='')
    notification_detail = models.CharField(max_length=192, null=False, default='')
    insert_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, default='1970-01-01 00:00:00')

    class Meta:
        managed = False
        db_table = 'Notifications'
        unique_together = (('notification_id', 'deleteTime'),)
        verbose_name = 'Notification'


class Schedule(models.Model):

    schedule_id = models.BigAutoField(primary_key=True)
    delete_time = models.BigIntegerField(max_length=20, null=False, default=0)
    user_id = models.BigIntegerField(max_length=20, null=False, default=0)
    start_time = models.DateTimeField(null=False, default='1970-01-01 00:00:00')
    schedule_type = models.IntegerField(max_length=11, null=False, default=0)
    schedule_detail = models.CharField(max_length=192, null=False, default='')
    schedule_share_type = models.IntegerField(max_length=11, null=False, default=0)
    schedule_repeat_type = models.IntegerField(max_length=11, null=False, default=0)
    schedule_notification_type = models.IntegerField(max_length=11, null=False, default=0)
    insert_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, default='1970-01-01 00:00:00')

    class Meta:
        managed = False
        db_table = 'Schedules'
        unique_together = (('schedule_id', 'delete_time'),)
        verbose_name = 'Schedule'


class Scrab(models.Model):

    scrab_id = models.BigAutoField(primary_key=True)
    delete_time = models.BigIntegerField(max_length=20, null=False, default=0)
    user_id = models.BigIntegerField(max_length=20, null=False, default=0)
    family_id = models.BigIntegerField(max_length=20, null=False, default=0)
    scrab_type = models.IntegerField(max_length=11, null=False, default=0)
    scrab_title = models.CharField(max_length=192, null=False, default='')
    scrab_url = models.CharField(max_length=192, null=False, default='')
    insert_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, default='1970-01-01 00:00:00')

    class Meta:
        managed = False
        db_table = 'Scrabs'
        unique_together = (('scrab_id', 'delete_time'),)
        verbose_name = 'Scrab'


class Notice(models.Model):
    notice_id = models.BigAutoField(primary_key=True)
    delete_time = models.BigIntegerField(max_length=20, null=False, default=0)
    ordering = models.IntegerField(max_length=11, null=False, default=0)
    title = models.CharField(max_length=192)
    content = models.TextField(null=False)
    admin_id = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)
    insert_time = models.DateTimeField(null=False, auto_now_add=True)
    update_time = models.DateTimeField(null=False, default='1970-01-01 00:00:00')

    class Meta:
        managed = False
        db_table = 'Notices'
        unique_together = (('notice_id', 'deleteTime'),)
        verbose_name = 'Notice'
