from django.db import models


TYPE_CHOICES_PRIVATE = 0
TYPE_CHOICES_BUSINESS =1

TYPE_CHOICES = (
    (TYPE_CHOICES_PRIVATE, 'prywatny'),
    (TYPE_CHOICES_BUSINESS, 'służbowy'),
)

class Address(models.Model):
    city = models.CharField(max_length=128, blank=True, null=True)
    city_code = models.CharField(max_length=6, blank=True, null=True)
    street = models.CharField(max_length=128, blank=True, null=True)
    str_no = models.CharField(max_length=6, blank=True, null=True)
    number = models.CharField(max_length=6, blank=True, null=True)

    # def __str__(self):
    #     return self.city + self.street + self.str_no + "/" + self.number


class Person(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)
    surname = models.CharField(max_length=60, blank=False, null=False)
    comment = models.TextField(null=True)
    address = models.ForeignKey(Address, models.SET_NULL, blank=True, null=True)

    # def __str__(self):
    #     return self.surname

class Tnumber(models.Model):
    number = models.CharField(max_length=20, unique=True, null=False, blank=False)
    type = models.SmallIntegerField(choices=TYPE_CHOICES, default=0)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)

    # def __str__(self):
    #     return self.number

class Email(models.Model):
    email = models.CharField(max_length=20, unique=True, null=False, blank=False)
    type = models.SmallIntegerField(choices=TYPE_CHOICES, default=0)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)

    # def __str__(self):
    #     return self.email

class Groups(models.Model):
    g_name = models.CharField(max_length=128)
    person = models.ManyToManyField(Person)

    # def __str__(self):
    #     return self.g_name





