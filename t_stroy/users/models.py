from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

GENDER_CHOICES = (
    (0, 'Mail'),
    (1, 'Femail'),
    (2, 'Not to disclose'),

)
# 기본 유저 모델은 username 을 id로 사용한다. 
# 커스텀 유저 모델을 사용할 땐 AbstractUser 클래스 사용한다.
# email로 로그인을 하기 위해서 BaseUserManager 클래스를 가져와서 오버라이딩을 해주는 것.
class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_field):
        '''
        Create and Save a user with the given username, email, and password.
        '''
        if not email:
            raise ValueError('The Given email must be set')
        email = self.normalize_email(email)
        # username = self.normalize_username(username)
        user = self.model(email=email, username=username, **extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username='', password=None, **extra_field):
        extra_field.setdefault('is_staff',False)
        extra_field.setdefault('is_superuser',False)
        return self._create_user(email, username, password, **extra_field)

    def create_superuser(self, email, username, password, **extra_field):
        extra_field.setdefault('is_staff', True)
        extra_field.setdefault('is_superuser', True)

        if extra_field.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_field.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, username, password, **extra_field)

# AbstractUser는 django User모델을 커스터마이징 할 때 사용한다.
class User(AbstractUser):
    email = models.EmailField(verbose_name='email',max_length=255, unique=True)

    username = models.CharField(max_length=30)

    objects = UserManager()
    USERNAME_FIELD = 'email' # username이 아닌 email을 기본 id로 사용. django User모델은 기본적으로 username을 id로 사용. 즉 identifying field로 사용하고 싶은 것을 지정하는 부분이다.
    REQUIRED_FIELDS = [] # 필수로 받고 싶은 필드들 넣기 위해

    def __str__(self):
        return "<%d %s>" % (self.pk, self.email)