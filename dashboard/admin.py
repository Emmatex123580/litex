from django.contrib import admin
from .models import Asset, WalletAddress, Crypto, CustomUser, Wallets, WalletTransaction
from django.contrib.auth.models import Group
# Register your models here.
class AssetAdmin(admin.ModelAdmin):
    pass
admin.site.register(Asset,AssetAdmin)

class WalletAddressAdmin(admin.ModelAdmin):
    pass
admin.site.register(WalletAddress,WalletAddressAdmin)

class CryptoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Crypto,CryptoAdmin)


# def debit_user(modeladmin,request,queryset):
#     form = Debit(request.POST)
#     if request.method == 'POST':
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = request.user
#             bvn = cd['transactionReference']
#             amount = cd['amount']
#             new_wallet = wallets.debit_user(
#             transactionReference = bvn,
#             amount = amount,
#             phone_number = user.phone_number,
         

        

#             )


# class DebitAdmin(admin.ModelAdmin):
#    pass


# admin.site.register(Debit,DebitAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','email','phone_number', 'date_of_birth'
    ]
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Wallets)
admin.site.register(WalletTransaction)
admin.site.unregister(Group)