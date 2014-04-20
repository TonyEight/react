# -*- coding: utf8 -*-
# Django modules
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


class Company(models.Model):
    name = models.CharField(_(u'name'), max_length='255', unique=True)

    class Meta:
        verbose_name = _(u'Company')
        verbose_name_plural = _(u'Companies')

    def __unicode__(self):
        return u'%s' % self.name


class Contact(models.Model):
    first_name = models.CharField(_(u'first_name'), max_length='750')
    last_name = models.CharField(_(u'last_name'), max_length='750')
    email = models.EmailField(_(u'email'), unique=True)
    company = models.ForeignKey(
        Company, verbose_name=_(u'company'), related_name=u'contacts')

    class Meta:
        verbose_name = _(u'Contact')
        verbose_name_plural = _(u'Contacts')

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.upper()
        super(Contact, self).save(*args, **kwargs)


class Contract(models.Model):
    name = models.CharField(_(u'name'), max_length='750')
    client = models.ForeignKey(
        Contact, verbose_name=_(u'client'), related_name=u'owned_contracts')
    start = models.DateField(_(u'start'))
    end = models.DateField(_(u'end'))
    days = models.DecimalField(
        _(u'number of days'), max_digits=6, decimal_places=2)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL,
                              verbose_name=_(u'actor'),
                              related_name=u'contracts')

    class Meta:
        verbose_name = _('Contract')
        verbose_name_plural = _('Contracts')

    def __unicode__(self):
        return u'%s' % self.name

    def clean(self):
        if self.days is not None:
            if self.days < 0:
                raise ValidationError(
                    _(u'Number of days must be stickly positive.'))
        if self.start is not None and self.end is not None:
            if self.start > self.end:
                raise ValidationError(
                    _(u'Start date must be less or equal to end date.'))
            else:
                max_days = 1
                if self.start != self.end:
                    delta = self.end - self.start
                    max_days = delta.days
                if self.days > max_days:
                    raise ValidationError(
                        _(u'Number of days must be must be less or equal to '
                          u'the maximum delta in days between start '
                          u'end dates.'))
