from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .admin import UserCreationForm, UserChangeForm
from .forms import LoginForm, SearchForm
from .models import Employee
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import resolve_url
from django.db.models import Q


# Create your views here.
class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'employee/login.html'

class LogoutView(LogoutView):
    template_name = 'employee/logout.html'

class IndexView(LoginRequiredMixin, generic.ListView):
    model = Employee
    paginate_by = 3

    def get_context_data(self):
        context = super().get_context_data()
        context['form'] = SearchForm(self.request.GET)
        return context

    def get_queryset(self):
        form = SearchForm(self.request.GET)
        form.is_valid()

        queryset = super().get_queryset()

        name = form.cleaned_data['name']
        if name:
            queryset = queryset.filter(
                Q(first_name__icontains=name) | 
                Q(last_name__icontains=name) |
                Q(id__icontains=name) |
                Q(email__icontains=name)
            )

        department = form.cleaned_data['department']
        if department:
            queryset = queryset.filter(department=department)

        skill = form.cleaned_data['skill']
        if skill:
            queryset = queryset.filter(skill__skill_name=skill)    
            
        training = form.cleaned_data['training']
        if training:
            queryset = queryset.filter(training__training_name=training)  

        return queryset

class AddView(generic.CreateView):
    model = Employee
    form_class = UserCreationForm
    template_name = "employee/employee_add.html"
    success_url = reverse_lazy('employee:index')

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee

class OnlyYouMixIn(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_admin

class UpdateView(OnlyYouMixIn, generic.UpdateView):
    model = Employee
    form_class = UserChangeForm
    template_name = "employee/employee_update.html"

    def get_success_url(self):
        return resolve_url('employee:detail', pk=self.kwargs['pk'])