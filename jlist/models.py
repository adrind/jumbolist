from django.db import models
from django.contrib.auth.models import User



class Item(models.Model):
    #id = models.AutoField(primary_key=True)
    seller = models.ForeignKey('UserProfile', unique=False, related_name="item" )
    name = models.CharField(max_length = 50)
    description = models.CharField("Description",max_length = 1000)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    sold = models.BooleanField()
    date_added = models.DateField(auto_now_add=True)
    photo = models.FileField(upload_to='photos/%Y/%m/%d')

    def get_fields(self):
        return [(field, field.verbose_name(self)) for field in Item._meta.fields]

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name="profile")
    items_for_sale = models.ManyToManyField(Item, related_name="profile")
    watched_items = models.ManyToManyField(Item, related_name="user_prof")

    def get_user_name(self):
        u = User.objects.get(user=user)
        return self.u.name

    def __unicode__(self):
        return self.user.username




class Offer(models.Model):
    seller = models.ForeignKey(UserProfile, unique=False, related_name="seller_offer")
    buyer = models.ForeignKey(UserProfile, unique=False, related_name="buyer_offer")
    item = models.ForeignKey(Item, unique=False, related_name="item_offer")
    date = models.DateField(auto_now_add=True)
    bid = models.DecimalField(decimal_places=2, max_digits=6) #default should be item price


