# -*- coding: utf8 -*-
# Built-in modules
import datetime
# Django modules
from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
# React modules
from business.models import (
    Company,
    Contact,
    Contract
)


class CompanyModelTest(TestCase):

    def setUp(self):
        Company.objects.create(
            name=u'GREEN'
        )

    def test_a_company_name_must_be_unique(self):
        """
        Tests that company names are unique.
        """
        self.assertRaises(
            IntegrityError,
            Company.objects.create,
            name=u'GREEN'
        )

    def test_b_company_can_be_modified(self):
        """
        Tests that companies can be modified.
        """

        company = Company.objects.get(name=u'GREEN')
        company.name = u'GREEN Conseil'
        company.save()
        company = Company.objects.get(pk=company.pk)
        self.assertEquals(
            u'GREEN Conseil',
            company.name
        )

    def test_c_company_can_be_deleted(self):
        """
        Tests that companies can be deleted.
        """
        company = Company.objects.get(name=u'GREEN')
        company.delete()
        self.assertRaises(
            Company.DoesNotExist,
            Company.objects.get,
            name=u'GREEN'
        )

    def test_d_company_must_have_a_name(self):
        """
        Tests that companies can be deleted.
        """
        company = Company.objects.get(name=u'GREEN')
        company.delete()
        self.assertRaises(
            Company.DoesNotExist,
            Company.objects.get,
            name=u'GREEN'
        )


class ContactModelTest(TestCase):

    def setUp(self):
        company = Company.objects.create(
            name=u'SSII'
        )
        Contact.objects.create(
            first_name=u'John',
            last_name=u'Doe',
            email=u'john.doe@ssii.org',
            company=company
        )

    def test_a_contact_must_have_a_company(self):
        """
        Tests that a company is required to define a contact.
        """
        contact = Contact(
            first_name=u'Tee',
            last_name=u'shirt',
            email=u'tee.shirt@ssii.org'
        )
        self.assertRaises(
            ValidationError,
            Contact.full_clean,
            contact
        )

    def test_b_contact_must_have_an_email(self):
        """
        Tests that an email is required to define a contact.
        """
        contact = Contact(
            first_name=u'Tee',
            last_name=u'shirt',
            company=Company.objects.get(name=u'SSII')
        )
        self.assertRaises(
            ValidationError,
            Contact.full_clean,
            contact
        )

    def test_c_contact_email_must_be_unique(self):
        """
        Tests that an email must be unique a contact.
        """
        self.assertRaises(
            IntegrityError,
            Contact.objects.create,
            first_name=u'Tee',
            last_name=u'shirt',
            email=u'john.doe@ssii.org',
            company=Company.objects.get(name=u'SSII')
        )

    def test_d_contact_must_have_a_first_name(self):
        """
        Tests that the first name is required to define a contact.
        """
        contact = Contact(
            last_name=u'shirt',
            email=u'tee.shirt@ssii.org',
            company=Company.objects.get(name=u'SSII')
        )
        self.assertRaises(
            ValidationError,
            Contact.full_clean,
            contact
        )

    def test_e_contact_must_have_a_last_name(self):
        """
        Tests that the last name is required to define a contact.
        """
        contact = Contact(
            first_name=u'tee',
            email=u'tee.shirt@ssii.org',
            company=Company.objects.get(name=u'SSII')
        )
        self.assertRaises(
            ValidationError,
            Contact.full_clean,
            contact
        )

    def test_f_contact_can_be_modified(self):
        """
        Tests that contacts can be modified.
        """

        contact = Contact.objects.get(email=u'john.doe@ssii.org')
        contact.email = u'test@test.org'
        contact.save()
        contact = Contact.objects.get(pk=contact.pk)
        self.assertEquals(
            u'test@test.org',
            contact.email
        )

    def test_g_contact_can_be_deleted(self):
        """
        Tests that contacts can be deleted.
        """
        contact = Contact.objects.get(email=u'john.doe@ssii.org')
        contact.delete()
        self.assertRaises(
            Contact.DoesNotExist,
            Contact.objects.get,
            email=u'john.doe@ssii.org'
        )

    def test_h_contact_first_and_last_name_format(self):
        """
        Tests that contact first name and last name have the correct format.
        """
        contact = Contact.objects.create(
            first_name=u'john',
            last_name=u'smith',
            email=u'john.smith@ssii.org',
            company=Company.objects.get(name=u'SSII')
        )
        self.assertTrue(
            contact.first_name == u'John'
        )
        self.assertTrue(
            contact.last_name == u'SMITH'
        )


class ContractModelTest(TestCase):

    def setUp(self):
        company = Company.objects.create(
            name=u'SSII'
        )
        Contact.objects.create(
            first_name=u'John',
            last_name=u'Doe',
            email=u'john.doe@ssii.org',
            company=company
        )
        get_user_model().objects.create_user(
            username='Test',
            password='test'
        )
        Contract.objects.create(
            name='test',
            client=Contact.objects.get(email=u'john.doe@ssii.org'),
            start=datetime.date(2014, 1, 1),
            end=datetime.date(2014, 1, 31),
            days=10,
            actor=get_user_model().objects.get(username='Test')
        )

    def test_a_contract_must_have_a_name(self):
        """
        Tests that a name is required to define a contract.
        """
        contract = Contract(
            client=Contact.objects.get(email=u'john.doe@ssii.org'),
            start=datetime.date(2014, 1, 1),
            end=datetime.date(2014, 1, 31),
            days=10,
            actor=get_user_model().objects.get(username='Test')
        )
        self.assertRaises(
            ValidationError,
            Contract.full_clean,
            contract
        )

    def test_b_contract_dates_must_be_coherent(self):
        """
        Tests that dates are coherent to define a contract.
        """
        contract = Contract(
            name='test',
            client=Contact.objects.get(email=u'john.doe@ssii.org'),
            start=datetime.date(2014, 1, 31),
            end=datetime.date(2014, 1, 1),
            days=10,
            actor=get_user_model().objects.get(username='Test')
        )
        self.assertRaises(
            ValidationError,
            Contract.full_clean,
            contract
        )

    def test_c_contract_number_of_days_must_be_coherent(self):
        """
        Tests that number of days is coherent with dates to define a contract.
        """
        contract = Contract(
            name='test',
            client=Contact.objects.get(email=u'john.doe@ssii.org'),
            start=datetime.date(2014, 1, 1),
            end=datetime.date(2014, 1, 31),
            days=100,
            actor=get_user_model().objects.get(username='Test')
        )
        self.assertRaises(
            ValidationError,
            Contract.full_clean,
            contract
        )

    def test_d_contract_must_have_dates(self):
        """
        Tests that both start and end dates must be set
        to define a contract.
        """
        contract_a = Contract(
            name='test',
            client=Contact.objects.get(email=u'john.doe@ssii.org'),
            start=datetime.date(2014, 1, 1),
            days=10,
            actor=get_user_model().objects.get(username='Test')
        )
        contract_b = Contract(
            name='test',
            client=Contact.objects.get(email=u'john.doe@ssii.org'),
            end=datetime.date(2014, 1, 31),
            days=10,
            actor=get_user_model().objects.get(username='Test')
        )
        self.assertRaises(
            ValidationError,
            Contract.full_clean,
            contract_a
        )
        self.assertRaises(
            ValidationError,
            Contract.full_clean,
            contract_b
        )

    def test_e_contract_must_have_number_of_days(self):
        """
        Tests that a number of days must be set
        to define a contract.
        """
        contract = Contract(
            name='test',
            client=Contact.objects.get(email=u'john.doe@ssii.org'),
            start=datetime.date(2014, 1, 1),
            end=datetime.date(2014, 1, 31),
            actor=get_user_model().objects.get(username='Test')
        )
        self.assertRaises(
            ValidationError,
            Contract.full_clean,
            contract
        )

    def test_f_contract_must_have_an_actor(self):
        """
        Tests that an actor must be set to define a contract.
        """
        contract = Contract(
            name='test',
            client=Contact.objects.get(email=u'john.doe@ssii.org'),
            start=datetime.date(2014, 1, 1),
            end=datetime.date(2014, 1, 31),
            days=10
        )
        self.assertRaises(
            ValidationError,
            Contract.full_clean,
            contract
        )

    def test_g_contract_must_have_a_client(self):
        """
        Tests that a client must be set to define a contract.
        """
        contract = Contract(
            name='test',
            start=datetime.date(2014, 1, 1),
            end=datetime.date(2014, 1, 31),
            days=10,
            actor=get_user_model().objects.get(username='Test')
        )
        self.assertRaises(
            ValidationError,
            Contract.full_clean,
            contract
        )

    def test_h_contract_number_of_days_must_be_strickly_positive(self):
        """
        Tests that number of days is strickly positive to define a contract.
        """
        contract = Contract(
            name='test',
            client=Contact.objects.get(email=u'john.doe@ssii.org'),
            start=datetime.date(2014, 1, 1),
            end=datetime.date(2014, 1, 31),
            days=-5.25,
            actor=get_user_model().objects.get(username='Test')
        )
        self.assertRaises(
            ValidationError,
            Contract.full_clean,
            contract
        )

    def test_i_contract_can_be_modified(self):
        """
        Tests that a contract can be modified.
        """
        contract = Contract.objects.get(pk=1)
        days = contract.days
        contract.days = 4.50
        contract.save()
        contract = Contract.objects.get(pk=1)
        self.assertNotEqual(
            days,
            contract.days
        )

    def test_j_contract_can_be_deleted(self):
        """
        Tests that a contract can be deleted.
        """
        contract = Contract.objects.get(pk=1)
        contract.delete()
        self.assertRaises(
            Contract.DoesNotExist,
            Contract.objects.get,
            pk=1
        )
