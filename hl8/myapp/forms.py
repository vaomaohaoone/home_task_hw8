from django import forms
import datetime
from myapp.models import Task, RoadMap, User
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate

class CreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'estimate', 'road_map']

    def clean_road_map(self):
        roadmap = self.cleaned_data['road_map']
        return roadmap.name

    def clean_estimate(self):
        estimate = self.cleaned_data['estimate']
        if estimate < datetime.date.today():
            raise forms.ValidationError("Дата меньше сегодняшней")
        if type(estimate) != type(datetime.date.today()):
            raise forms.ValidationError("Неверный тип даты")
        return estimate

    def clean_title(self):
        title = self.cleaned_data['title']
        if type(title) != type(''):
            raise forms.ValidationError("Неверный тип заголовка")


class AnotherCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'estimate']

    def clean_estimate(self):
        estimate = self.cleaned_data['estimate']
        if estimate < datetime.date.today():
            raise forms.ValidationError("Дата меньше сегодняшней")
        if type(estimate) != type(datetime.date.today()):
            raise forms.ValidationError("Неверный тип даты")
        return estimate

    def clean_title(self):
        title = self.cleaned_data['title']
        if type(title) != type(''):
            raise forms.ValidationError("Неверный тип заголовка")


class CreateUser(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    phone = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    region = forms.CharField()
    age = forms.IntegerField(min_value=0, max_value=120)


class EditUser(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'age', 'region']


class EditPassword(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    new_password = forms.CharField(widget=forms.PasswordInput(render_value=False))
    confirm_password = forms.CharField(widget=forms.PasswordInput(render_value=False))


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=False)
    )

    def clean(self):
        user = self.authenticate_via_email()
        if not user:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        else:
            self.user = user
        return self.cleaned_data

    def authenticate_user(self):
        return authenticate(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
         )

    def authenticate_via_email(self):
        """
            Authenticate user using email.
            Returns user object if authenticated else None
        """
        email = self.cleaned_data['email']
        if email:
            try:
                user = User.objects.get(email__iexact=email)
                if user.check_password(self.cleaned_data['password']):
                    return user
            except ObjectDoesNotExist:
                pass
        return None


class CreateRoadMap(ModelForm):
    class Meta:
        model = RoadMap
        fields = ['rd_id', 'name']


class EditForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'estimate', 'state', 'road_map']

        # def clean_estimate(self):
        #    estimate = self.cleaned_data['estimate']
        #  if estimate < datetime.date.today():
        #      raise forms.ValidationError("Дата меньше сегодняшней")
        #  if type(estimate) != type(datetime.date.today()):
        #      raise forms.ValidationError("Неверный тип даты")
        #  return estimate

        # def clean_title(self):
        #    title = self.cleaned_data['title']
        #    if type(title) != type(''):
        #       raise forms.ValidationError("Неверный тип заголовка")

        # def clean_state(self):
        #    state = self.cleaned_data['state']
        #    if state!='in_progress' and state!='ready':
        #        raise forms.ValidationError("Невалидный статус")
