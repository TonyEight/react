# -*- coding: utf8 -*-
# Django modules
from django.contrib import admin
# React modules
from business.models import (
    Company,
    Contact,
    Contract
)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'email', 'company')

class ContractAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'days', 'start', 'end', 'actor')

admin.site.register(Company)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Contract, ContractAdmin)
