from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, username, email, mobile_no, password, **extra_fields):
        if not email or not mobile_no:
            raise ValueError('The given email and mobile no must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, mobile_no=mobile_no, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, mobile_no, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(username, email, mobile_no, password, **extra_fields)

    def create_superuser(self, username, email, mobile_no, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, mobile_no, password, **extra_fields)