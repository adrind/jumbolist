from django.shortcuts import render_to_response
from jlist.forms import MyUserForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, logout, login


def load_home(request):
    return render_to_response("landing.html")

def register(request):
    form = MyUserForm(request.POST or None)
    non_field_errors = []
    if form.is_valid():
        new_user = form.save()
        new_user.full_clean()
        new_user.save()
        #messages.info(request, "Thanks for registering! You're logged in")
        login(request, authenticate(username=request.POST['username'], password=request.POST['password']))
        request.session['username'] = request.POST['username']
        return HttpResponseRedirect("/signup/")
    return render_to_response("signup.html", {'form': form, 'errors': non_field_errors}, context_instance=RequestContext(request),)


def login_attempt(request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['username'] = username #USE OF SESSION
                # Redirect to a success page.
                    return HttpResponseRedirect("/profile/")
                    #return render_to_response("profile.html", {'user': username,}, context_instance=RequestContext(request),)
            else:
                error = "Sorry the username and password you entered was not valid"
                return render_to_response("login.html", {'error': error,}, context_instance=RequestContext(request),)
        else:
            return render_to_response("login.html", locals(), context_instance=RequestContext(request),)

def profile(request):
    name = request.session['username']
    return render_to_response("profile.html", {'name': name}, context_instance=RequestContext(request),)