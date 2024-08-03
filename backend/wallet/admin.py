from django.contrib import admin
from .models import Coin, Wallet, WalletCoin, Transaction
class WalletCoinInline(admin.TabularInline):
    model = WalletCoin
    extra = 0  # Set to 0 to avoid displaying extra empty forms
    can_delete = False
    readonly_fields = ('coin', 'balance', 'updated_date')
    fields = ('coin', 'balance', 'updated_date')
    show_change_link = True 
    def has_add_permission(self, request, obj=None): return False  


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'price')
    search_fields = ('symbol',)
    list_filter = ('symbol',)
    list_editable=("price",)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('owner', 'address', 'created_date', 'updated_date')
    search_fields = ('owner__username', 'owner__email', 'address')
    readonly_fields = ('address', 'created_date', 'updated_date')
    list_filter = ('created_date',)
    ordering = ('-created_date',)
    inlines = [WalletCoinInline]  # Add this line to include the inline


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('source_wallet', 'recipient_wallet', 'amount', 'transaction_type', 'date')
    search_fields = ('source_wallet__owner__username', 'recipient_wallet__owner__username')
    list_filter = ('transaction_type', 'date')
    readonly_fields = ('date','amount','source_wallet', 'recipient_wallet','transaction_type')

    def has_add_permission(self, request):
        # Disables the add functionality in the admin interface
        return False