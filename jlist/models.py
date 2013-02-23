from django.db import models



class UserProfile(models.model):
    user = models.ForeignKey(User, unique=True, related_name="profile")
    items = models.ManyToManyField(Item, related_name="profile")



class Item(models.model):
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(UserProfile, unique=False, related_name="item" )
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 1000)
    price = models.DecimalField()
    sold = models.BooleanField()
    date_added = models.DateField(auto_now_add=True)
    photo = models.URLField(max_length=200)


    

