from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import StudentProfile


class StudentRegistrationForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password1",
            "password2"
        ]


class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email address"
            }
        )
    )

    class Meta:
        model = User
        fields = ["email"]


class StudentProfileUpdateForm(forms.ModelForm):

    DEPARTMENT_CHOICES = [
        ("Computer Science", "Computer Science"),
        ("Electrical Engineering", "Electrical Engineering"),
        ("Mathematics", "Mathematics"),
        ("Physics", "Physics"),
        ("Business Administration", "Business Administration"),
        ("Mechanical Engineering", "Mechanical Engineering"),
        ("Civil Engineering", "Civil Engineering"),
        ("Economics", "Economics"),
        ("Information Technology", "Information Technology"),
    ]

    LEVEL_CHOICES = [
        ("100 Level", "100 Level"),
        ("200 Level", "200 Level"),
        ("300 Level", "300 Level"),
        ("400 Level", "400 Level"),
        ("500 Level", "500 Level"),
        ("Postgraduate", "Postgraduate"),
    ]

    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    level = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your age",
                "min": "10",
                "max": "100"
            }
        )
    )

    class Meta:
        model = StudentProfile
        fields = ["department", "level", "age"]
