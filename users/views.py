from django.views.generic import CreateView
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        new_user = form.save()
        authenticated_user = authenticate(
            username=new_user.username,
            password=self.request.POST['password1']
        )
        login(self.request, authenticated_user)

        return HttpResponseRedirect(reverse('market:home'))
