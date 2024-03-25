from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Manager)
admin.site.register(Branch)
admin.site.register(Bank)
admin.site.register(Customer)
admin.site.register(UserAccount)
admin.site.register(Transaction)
admin.site.register(Notification)

