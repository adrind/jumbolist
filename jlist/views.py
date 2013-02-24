from django.shortcuts import render_to_response
from jlist.forms import MyUserForm, ItemForm
from jlist.models import UserProfile, Item
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, logout, login
from django.forms import ValidationError
from jlist.models import Item, UserProfile, User


def load_home(request):
    return render_to_response("landing.html")

def register(request):
    form = MyUserForm(request.POST or None)
    non_field_errors = []
    if form.is_valid():
        try:
            new_user = form.save()
            new_user.full_clean()
            new_user.save()
                #messages.info(request, "Thanks for registering! You're logged in")
            login(request, authenticate(username=request.POST['username'], password=request.POST['password']))
            request.session['username'] = request.POST['username']
            return HttpResponseRedirect("/signup/")

        except ValidationError:
            render_to_response("signup.html", {'form': form, 'errors': ['User Already Exists']}, context_instance=RequestContext(request))
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

def sellers_page(request):
    return render_to_response("sell.html", context_instance=RequestContext(request),)


def display_items(request):
    items = Item.objects.all()
    fields    = Item._meta.fields

    seller_names = []
    for item in items:
        #userP = UserProfile.objects.get(item.seller)
        user = User.objects.get(profile=item.seller)
        seller_names.append(user.username)

    return render_to_response("displayItems.html", {'items':items, 'fields':fields, 'seller_names':seller_names}, context_instance=RequestContext(request),)

#soooo hacky
def additem(request):
    form = ItemForm(request.POST or None)
    if request.method == 'POST':
        non_field_errors = []
        if form.is_valid():
            new_item = form.save()
            user_id = str(request.session['username'])
            u = UserProfile.objects.get(user=User.objects.get(username = user_id))
            new_item.seller = u
            new_item.save()
            return render_to_response("additem.html", {'form':None, 'success' : True}, context_instance=RequestContext(request),)
        return render_to_response("additem.html", {'form': form, 'errors': non_field_errors, }, context_instance=RequestContext(request),)
    return render_to_response("additem.html", {'form': form},  context_instance=RequestContext(request),)

def manage(request):
    user_id = str(request.session['username'])
    u = UserProfile.objects.get(user=User.objects.get(username = user_id))
    items = list(Item.objects.filter(seller=u))
    return render_to_response("manage.html", {'items':items,})


#soooo hacky
def additem(request):
    form = ItemForm(request.POST or None)
    if request.method == 'POST':
        non_field_errors = []
        if form.is_valid():
            new_item = form.save()
            user_id = str(request.session['username'])
            u = UserProfile.objects.get(user=User.objects.get(username = user_id))
            new_item.seller = u
            new_item.save()
            return render_to_response("additem.html", {'form':None, 'success' : True}, context_instance=RequestContext(request),)
        return render_to_response("additem.html", {'form': form, 'errors': non_field_errors, }, context_instance=RequestContext(request),)
    return render_to_response("additem.html", {'form': form},  context_instance=RequestContext(request),)

def manage(request):
    user_id = str(request.session['username'])
    u = UserProfile.objects.get(user=User.objects.get(username = user_id))
    items = list(Item.objects.filter(seller=u))
    return render_to_response("manage.html", {'items':items,})