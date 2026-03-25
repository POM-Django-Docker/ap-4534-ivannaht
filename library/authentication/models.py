from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

ROLE_CHOICES = (
    (0, "visitor"),
    (1, "librarian"),
)


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of username.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", 0)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", 1)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    This class represents a basic user.

    Attributes:
    -----------
    param first_name: Describes first name of the user
    type first_name: str max length=20
    param last_name: Describes last name of the user
    type last_name: str max length=20
    param middle_name: Describes middle name of the user
    type middle_name: str max length=20
    param email: Describes the email of the user
    type email: str, unique, max length=100
    param password: Describes the password of the user
    type password: str
    param created_at: Describes the date when the user was created. Can't be changed.
    type created_at: int (timestamp)
    param updated_at: Describes the date when the user was modified
    type updated_at: int (timestamp)
    param role: user role, default role (0, 'visitor')
    type role: int (choices)
    param is_active: user activity state
    type is_active: bool
    """

    first_name = models.CharField(max_length=20, default="")
    last_name = models.CharField(max_length=20, default="")
    middle_name = models.CharField(max_length=20, default="")
    email = models.EmailField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        """
        Magic method is redefined to show all information about CustomUser.
        :return: user id, user first_name, user middle_name, user last_name,
                 user email, user updated_at, user created_at,
                 user role, user is_active
        """
        return (
            f"'id': {self.id}, "
            f"'first_name': '{self.first_name}', "
            f"'middle_name': '{self.middle_name}', "
            f"'last_name': '{self.last_name}', "
            f"'email': '{self.email}', "
            f"'created_at': {int(self.created_at.timestamp())}, "
            f"'updated_at': {int(self.updated_at.timestamp())}, "
            f"'role': {self.role}, "
            f"'is_active': {self.is_active}"
        )

    def __repr__(self):
        """
        This magic method is redefined to show class and id of CustomUser object.
        :return: class, id
        """
        return f"{CustomUser.__name__}(id={self.id})"

    @staticmethod
    def get_by_id(user_id):
        """
        :param user_id: SERIAL: the id of a user to be found in the DB
        :return: user object or None if a user with such ID does not exist
        """
        custom_user = CustomUser.objects.filter(id=user_id).first()
        return custom_user if custom_user else None

    @staticmethod
    def get_by_email(email):
        """
        Returns user by email
        :param email: email by which we need to find the user
        :type email: str
        :return: user object or None if a user with such email does not exist
        """
        custom_user = CustomUser.objects.filter(email=email).first()
        return custom_user if custom_user else None

    @staticmethod
    def delete_by_id(user_id):
        """
        :param user_id: an id of a user to be deleted
        :type user_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        user_to_delete = CustomUser.objects.filter(id=user_id).first()
        if user_to_delete:
            user_to_delete.delete()
            return True
        return False

    @staticmethod
    def create(email, password, first_name=None, middle_name=None, last_name=None, role=0):
        """
        :param first_name: first name of a user
        :type first_name: str
        :param middle_name: middle name of a user
        :type middle_name: str
        :param last_name: last name of a user
        :type last_name: str
        :param email: email of a user
        :type email: str
        :param password: password of a user
        :type password: str
        :param role: role id
        :type role: int
        :return: a new user object which is also written into the DB
        """
        first_name = first_name or ""
        middle_name = middle_name or ""
        last_name = last_name or ""

        if (
            len(first_name) <= 20
            and len(middle_name) <= 20
            and len(last_name) <= 20
            and len(email) <= 100
            and len(email.split("@")) == 2
            and len(CustomUser.objects.filter(email=email)) == 0
        ):
            return CustomUser.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                role=role,
            )
        return None

    def to_dict(self):
        """
        :return: user id, user first_name, user middle_name, user last_name,
                 user email, user updated_at, user created_at, user is_active
        """
        return {
            "id": self.id,
            "first_name": f"{self.first_name}",
            "middle_name": f"{self.middle_name}",
            "last_name": f"{self.last_name}",
            "email": f"{self.email}",
            "created_at": int(self.created_at.timestamp()),
            "updated_at": int(self.updated_at.timestamp()),
            "role": self.role,
            "is_active": self.is_active,
        }

    def update(
        self,
        first_name=None,
        last_name=None,
        middle_name=None,
        password=None,
        role=None,
        is_active=None,
    ):
        """
        Updates user profile in the database with the specified parameters.
        """
        if first_name is not None and len(first_name) <= 20:
            self.first_name = first_name
        if last_name is not None and len(last_name) <= 20:
            self.last_name = last_name
        if middle_name is not None and len(middle_name) <= 20:
            self.middle_name = middle_name
        if password is not None:
            self.set_password(password)
        if role is not None:
            self.role = role
        if is_active is not None:
            self.is_active = is_active

        self.save()

    @staticmethod
    def get_all():
        """
        returns data for json request with QuerySet of all users
        """
        return CustomUser.objects.all()

    def get_role_name(self):
        """
        returns str role name
        """
        return ROLE_CHOICES[self.role][1]