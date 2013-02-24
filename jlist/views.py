from django.shortcuts import render_to_response
from jlist.forms import MyUserForm, ItemForm
from jlist.models import UserProfile, Item
from jlist.forms import MyUserForm, ItemForm, EmailForm
from jlist.models import UserProfile, Item
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, logout, login
from django.forms import ValidationError
from jlist.models import Item, UserProfile, User
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from collections import defaultdict
from decimal import Decimal
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
import ast
from django.core.mail import send_mail

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
            return HttpResponseRedirect("/profile/")

        except ValidationError:
            render_to_response("signup.html", {'form': form, 'errors': ['User Already Exists']},
                               context_instance=RequestContext(request))
    return render_to_response("signup.html", {'form': form, 'errors': non_field_errors},
                              context_instance=RequestContext(request), )


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
            return render_to_response("login.html", {'error': error, }, context_instance=RequestContext(request), )
    else:
        return render_to_response("login.html", locals(), context_instance=RequestContext(request), )


def filter_attempt(request):
    if request.method == 'POST':
        print "postmethod"
        user_id = str(request.session['username'])
        currentUser = UserProfile.objects.get(user=User.objects.get(username=user_id))
        items = Item.objects.exclude(seller__exact=currentUser)
        fields = Item._meta.fields
        lowprice = request.POST['lowprice']
        highprice = request.POST['highprice']
        if lowprice:
            lowprice = Decimal(lowprice)
            print str(lowprice) + "low"
            items = items.filter(price__gte=lowprice)
        if highprice:
            highprice = Decimal(highprice)
            items = items.filter(price__lte=highprice)
        seller_names = []
        for item in items:
            #userP = UserProfile.objects.get(item.seller)
            user = User.objects.get(profile=item.seller)
            seller_names.append(user.username)
        paginator = Paginator(items, 10)
        page = request.GET.get('page', 1)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            items = paginator.page(paginator.num_pages)
        return redirect("marketplace.html", {'items': items, 'fields': fields, 'seller_names': seller_names},
            context_instance=RequestContext(request), )                #return render_to_response("profile.html", {'user': username,}, context_instance=RequestContext(request),)


@login_required
def profile(request):
    name = request.session['username']
    return render_to_response("profile.html", {'name': name}, context_instance=RequestContext(request), )


@login_required
def sellers_page(request):
    return render_to_response("sell.html", context_instance=RequestContext(request), )


@login_required
def buyers_page(request):
    return render_to_response("buy.html", context_instance=RequestContext(request), )


@login_required
def item_page(request, item_id):
    item = Item.objects.get(id=item_id)
    return render_to_response("item.html", {'item':item}, context_instance=RequestContext(request),)

@login_required
def watched_item(request, item_id):
    item = Item.objects.get(id=item_id)
    print item_id
    print item.name
    return render_to_response("watched_item.html", {'item':item}, context_instance=RequestContext(request),)



@login_required
def display_items(request):
    user_id = str(request.session['username'])
    currentUser = UserProfile.objects.get(user=User.objects.get(username=user_id))
    fields = Item._meta.fields

    if request.method == 'POST':
        itemidlist = request.POST['itemidlist']
        list1 = ast.literal_eval(itemidlist)
        items = Item.objects.filter(id__in=list(list1))
        lowprice = request.POST['lowprice']
        highprice = request.POST['highprice']
        if lowprice:
            lowprice = Decimal(lowprice)
            print str(lowprice) + "low"
            items = items.filter(price__gte=lowprice)
        if highprice:
            highprice = Decimal(highprice)
            items = items.filter(price__lte=highprice)
    else:
        items = Item.objects.exclude(seller__exact=currentUser)


    seller_names = []
    itemlist = items
    itemidlist = [i.id for i in itemlist]
    for item in items:
        user = User.objects.get(profile=item.seller)
        seller_names.append(user.username)
    paginator = Paginator(items, 10)
    page = request.GET.get('page', 1)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)

    return render_to_response("marketplace.html", {'itemlist':itemlist, 'itemidlist':itemidlist,'items': items, 'fields': fields, 'seller_names': seller_names},
        context_instance=RequestContext(request), )


@login_required

def display_watched_items(request):
    user_id = str(request.session['username'])
    currentUser = UserProfile.objects.get(user=User.objects.get(username=user_id))
    watchedItems = currentUser.watched_items.all()

    fields = Item._meta.fields

    seller_names = defaultdict(list)
    for item in watchedItems:
        #userP = UserProfile.objects.get(item.seller)
        user = User.objects.get(profile=item.seller)
        item.seller_name = user.username

    return render_to_response("watcheditems.html", {'items': watchedItems, 'fields': fields, 'seller_names': seller_names},
        context_instance=RequestContext(request), )


#soooo hacky
def additem(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        non_field_errors = []
        if form.is_valid():
            new_item = form.save()
            user_id = str(request.session['username'])
            u = UserProfile.objects.get(user=User.objects.get(username=user_id))
            new_item.photo = request.FILES['photo']
            new_item.seller = u
            new_item.save()
            return render_to_response("additem.html", {'form': None, 'success': True, 'item': new_item.name, 'pic': new_item.photo.url},
                                      context_instance=RequestContext(request), )
        return render_to_response("additem.html", {'form': form, 'errors': non_field_errors, },
                                  context_instance=RequestContext(request), )
    form = ItemForm(None)
    return render_to_response("additem.html", {'form': form}, context_instance=RequestContext(request), )

@login_required
def manage(request):
    user_id = str(request.session['username'])
    u = UserProfile.objects.get(user=User.objects.get(username=user_id))
    items = list(Item.objects.filter(seller=u))
    if items:
      paginator = Paginator(items, 10)
      page = request.GET.get('page', 1)
      try:
          items = paginator.page(page)
      except PageNotAnInteger:
          # If page is not an integer, deliver first page.
          items = paginator.page(1)
      except EmptyPage:
          # If page is out of range (e.g. 9999), deliver last page of results.
          items = paginator.page(paginator.num_pages)
    return render_to_response("manage.html", {'items': items, })


def save_item(request, item_id):
    item = Item.objects.get(id=item_id)
    user_id = str(request.session['username'])
    u = UserProfile.objects.get(user=User.objects.get(username=user_id))
    u.watched_items.add(item)
    u.save()
    return HttpResponseRedirect("/saveditems/")

def remove_item(request, item_id):
    item = Item.objects.get(id=item_id)
    user_id = str(request.session['username'])
    u = UserProfile.objects.get(user=User.objects.get(username=user_id))
    u.watched_items.remove(item)
    u.save()
    return HttpResponseRedirect("/saveditems/")

def send_email(request, item_id):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = request.POST['subject']
            message = request.POST['message']
            u = User.objects.get(username=str(request.session['username']))
            item = Item.objects.get(id=item_id)
            seller = User.objects.get(profile=item.seller)
            send_mail(subject, message, u.email,
                [seller.email], fail_silently=False)
            return render_to_response('email.html', {'success' : True, 'name' : u.username }, context_instance=RequestContext(request),)
    else:
        form = EmailForm()

    return render_to_response('email.html', {'form' : form}, context_instance=RequestContext(request),)