# -*- coding: utf8 -*-
# Built-in modules
import re
import datetime
# Django modules
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.contenttypes.models import ContentType


class HolidayQuerySet(models.QuerySet):
    def __getitem__(self, k):
        result = super(HolidayQuerySet, self).__getitem__(k)
        if isinstance(result, models.Model) :
            return result.as_leaf_class()
        else :
            return result
    
    def __iter__(self):
        for item in super(HolidayQuerySet, self).__iter__():
            yield item.as_leaf_class()

    def get_fixed(self):
        return self.filter(content_type=ContentType.objects.get_for_model(FixedHoliday))

    def get_nonfixed(self):
        return self.filter(content_type=ContentType.objects.get_for_model(NonFixedHoliday))

    def get_get_year(self, year):
        return self.get_fixed() | self.get_nonfixed().filter(date__year=year)

class HolidayManager(models.Manager):
    def get_queryset(self):
        return HolidayQuerySet(self.model)
    
    def get_fixed(self):
        return self.get_queryset().get_fixed()

    def get_nonfixed(self):
        return self.get_queryset().get_nonfixed()

    def get_year(self, year=datetime.date.today().year):
        return self.get_queryset().get_year(year=year)

class Holiday(models.Model):
    content_type = models.ForeignKey(ContentType, editable=False, null=True)

    class Meta:
        verbose_name = _('Holiday')
        verbose_name_plural = _('Holidays')

    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(Holiday, self).save(*args, **kwargs)

    def as_leaf_class(self):
        content_type = self.content_type
        model = content_type.model_class()
        if (model == Holiday):
            return self
        return model.objects.get(id=self.id)

    objects = HolidayManager()


class FixedHoliday(Holiday):
    name = models.CharField(_(u'name'), max_length='255', unique=True)
    date = models.CharField(_(u'date'), max_length='5',
                            validators=[RegexValidator(
                                regex=r'^(\d{2})\\(\d{2})$')
                            ],
                            unique=True)

    objects = models.Manager()

    class Meta:
        verbose_name = _('Fixed Holiday')
        verbose_name_plural = _('Fixed Holidays')

    def __unicode__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super(FixedHoliday, self).save(*args, **kwargs)

    def clean(self):
        if self.date is not None:
            date = unicode(self.date)
            regex = re.compile(r'^(\d{2})\\(\d{2})$')
            if regex.match(date) is None:
                raise ValidationError(
                    _(u'Invalid format : please use the '
                      u'following format \'DD/MM\' to define date.'))
            date_components = date.split(u'/')
            day = int(date_components[0])
            month = int(date_components[1])
            if month > 12:
                raise ValidationError(
                    _(u'Month number cannot be greater than 12.'))
            if month in [1, 3, 5, 7, 8, 10, 12]:
                if day > 31:
                    raise ValidationError(
                        _(u'Day number cannot be greater '
                          u'than 31 for this month.'))
            else:
                if month == 2:
                    if day > 28:
                        raise ValidationError(
                            _(u'Day number cannot be greater '
                              u'than 28 for this month.'))
                else:
                    if day > 30:
                        raise ValidationError(
                            _(u'Day number cannot be greater than '
                              u'30 for this month.'))


class NonFixedHoliday(Holiday):
    name = models.CharField(_(u'name'), max_length='255')
    date = models.DateField(_(u'date'), unique=True)

    objects = models.Manager()

    class Meta:
        verbose_name = _('Non Fixed Holiday')
        verbose_name_plural = _('Non Fixed Holidays')

    def __unicode__(self):
        return u'%s' % self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super(NonFixedHoliday, self).save(*args, **kwargs)
