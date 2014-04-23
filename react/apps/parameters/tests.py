# -*- coding: utf8 -*-
# Built-in modules
import datetime
# Django modules
from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
# React modules
from parameters.models import (
    Holiday,
    FixedHoliday,
    NonFixedHoliday
)


class FixedHolidayModelTest(TestCase):

    def setUp(self):
        FixedHoliday.objects.create(
            name=u'Nouvel An',
            date=u'01/01'
        )

    def test_a_name_is_required_and_unique(self):
        """
        Tests that holiday names are required and unique.
        """
        fholiday = FixedHoliday(
            name=u'',
            date=u'05/04'
        )
        self.assertRaises(
            ValidationError,
            FixedHoliday.full_clean,
            fholiday
        )
        fholiday = FixedHoliday(
            name=u'Nouvel An',
            date=u'05/04'
        )
        self.assertRaises(
            ValidationError,
            FixedHoliday.full_clean,
            fholiday
        )

    def test_b_date_is_required_and_unique(self):
        """
        Tests that holiday dates are required and unique.
        """
        fholiday = FixedHoliday(
            name=u'Test',
        )
        self.assertRaises(
            ValidationError,
            FixedHoliday.full_clean,
            fholiday
        )
        fholiday = FixedHoliday(
            name=u'Test',
            date=u'01/01'
        )
        self.assertRaises(
            ValidationError,
            FixedHoliday.full_clean,
            fholiday
        )

    def test_c_date_must_respect_day_month_format(self):
        """
        Tests that holiday dates use the format 'DD/MM'.
        """
        fholiday = FixedHoliday(
            name=u'Test',
            date=01
        )
        self.assertRaises(
            ValidationError,
            FixedHoliday.full_clean,
            fholiday
        )
        fholiday = FixedHoliday(
            name=u'Test',
            date=datetime.date(2015, 9, 5)
        )
        self.assertRaises(
            ValidationError,
            FixedHoliday.full_clean,
            fholiday
        )
        fholiday = FixedHoliday(
            name=u'Test',
            date=u'12/25'
        )
        self.assertRaises(
            ValidationError,
            FixedHoliday.full_clean,
            fholiday
        )
        fholiday = FixedHoliday(
            name=u'Test',
            date=u'45/12'
        )
        self.assertRaises(
            ValidationError,
            FixedHoliday.full_clean,
            fholiday
        )
        fholiday = FixedHoliday(
            name=u'Test',
            date=u'-4.5/456'
        )
        self.assertRaises(
            ValidationError,
            FixedHoliday.full_clean,
            fholiday
        )
        fholiday = FixedHoliday(
            name=u'Test',
            date=u'1/09'
        )
        self.assertRaises(
            ValidationError,
            FixedHoliday.full_clean,
            fholiday
        )
        fholiday = FixedHoliday(
            name=u'Test',
            date=u'01/9'
        )
        self.assertRaises(
            ValidationError,
            FixedHoliday.full_clean,
            fholiday
        )
        fholiday = FixedHoliday.objects.create(
            name=u'Test',
            date=u'24/06'
        )
        self.assertIsNotNone(
            fholiday.pk
        )

    def test_d_holiday_can_be_modified(self):
        """
        Tests that holiday can be modified.
        """
        fholiday = FixedHoliday.objects.get(
            pk=1
        )
        fholiday.name = u'Noël'
        fholiday.save()
        fholiday = FixedHoliday.objects.get(
            pk=1
        )
        self.assertEqual(
            fholiday.name,
            u'Noël'
        )

    def test_e_holiday_can_be_deleted(self):
        """
        Tests that holiday can be deleted.
        """
        fholiday = FixedHoliday.objects.get(
            pk=1
        )
        fholiday.delete()
        self.assertRaises(
            FixedHoliday.DoesNotExist,
            FixedHoliday.objects.get,
            pk=1
        )


class NonNonFixedHolidayModelTest(TestCase):

    def setUp(self):
        nfholiday = NonFixedHoliday.objects.create(
            name=u'Pâques',
            date=datetime.date(2014, 4, 21)
        )

    def test_a_name_is_required(self):
        """
        Tests that holiday names are required and unique.
        """
        nfholiday = NonFixedHoliday(
            date=datetime.date(2015, 4, 21)
        )
        self.assertRaises(
            ValidationError,
            NonFixedHoliday.full_clean,
            nfholiday
        )

    def test_b_date_is_required_and_unique(self):
        """
        Tests that holiday dates are required and unique.
        """
        nfholiday = NonFixedHoliday(
            name=u'Test',
        )
        self.assertRaises(
            ValidationError,
            NonFixedHoliday.full_clean,
            nfholiday
        )
        nfholiday = NonFixedHoliday(
            name=u'Test',
            date=datetime.date(2014, 4, 21)
        )
        self.assertRaises(
            ValidationError,
            NonFixedHoliday.full_clean,
            nfholiday
        )

    def test_c_holiday_can_be_modified(self):
        """
        Tests that holiday can be modified.
        """
        nfholiday = NonFixedHoliday.objects.get(
            pk=1
        )
        nfholiday.name = u'Noël'
        nfholiday.save()
        nfholiday = NonFixedHoliday.objects.get(
            pk=1
        )
        self.assertEqual(
            nfholiday.name,
            u'Noël'
        )

    def test_d_holiday_can_be_deleted(self):
        """
        Tests that holiday can be deleted.
        """
        nfholiday = NonFixedHoliday.objects.get(
            pk=1
        )
        nfholiday.delete()
        self.assertRaises(
            NonFixedHoliday.DoesNotExist,
            NonFixedHoliday.objects.get,
            pk=1
        )


class HolidayModelTest(TestCase):

    def setUp(self):
        NonFixedHoliday.objects.create(
            name=u'Pâques',
            date=datetime.date(2014, 4, 21)
        )
        FixedHoliday.objects.create(
            name=u'Nouvel An',
            date=u'01/01'
        )

    def test_a_fixed_holidays_are_set_for_all_years(self):
        """
        Tests that fixed holidays are defined once for every year 
        and are easy to fetch through a shortcut method.
        """
        fixed_holidays = Holiday.objects.get_fixed()
        for f in fixed_holidays:
            self.assertEqual(
                f,
                FixedHoliday.objects.get(
                    pk=f.pk
                )
            )
        years = range(2013, 2020)
        for year in years:
            self.assertEqual(
                fixed_holidays[0].date_for_year(year=year),
                datetime.date(year, 1, 1)
            )

    def test_b_non_fixed_holidays_are_simple_to_fetch(self):
        """
        Tests that non fixed holidays are easy to fetch through a shortcut method.
        """
        nonfixed_holidays = Holiday.objects.get_nonfixed()
        for nf in nonfixed_holidays:
            self.assertEqual(
                nf,
                NonFixedHoliday.objects.get(
                    pk=nf.pk
                )
            )
        nonfixed_holidays = Holiday.objects.get_year(year=2014).get_nonfixed()
        self.assertEqual(
            nonfixed_holidays[0].date,
            datetime.date(2014, 1, 1)
        )

    def test_c_holidays_are_simple_to_fetch(self):
        """
        Tests that all holidays are easy to fetch through a shortcut method.
        """
        holidays = Holiday.objects.get_year(year=2014)
        self.assertIn(
            NonFixedHoliday.objects.get(
                pk=1
            ),
            holidays
        )
        self.assertIn(
            FixedHoliday.objects.get(
                pk=1
            ),
            holidays
        )
