from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.messages import constants as messages
from contacts.models import Person, Address, Tnumber, Email, Groups


def home(request):
    return render(request, "contacts/home.html", locals())


def show_all(request):
    people = Person.objects.order_by('surname')
    return render(request, "contacts/show_all.html", locals())


def show_person(request, person_id):
    p = get_object_or_404(Person, pk=person_id)
    tel = Tnumber.objects.filter(person=p)
    mail = Email.objects.filter(person=p)
    if request.method == "GET":
        # jeżeli istnieje adres dla tej osoby, to pobierz dane adresowe do formularza
        if p.address_id:
            a = Address.objects.get(pk=p.address_id)
            city = a.city
            city_code = a.city_code
            street = a.street
            str_no = a.str_no
            number = a.number
        return render(request, "contacts/show.html", locals())


def new_contact(request, msg=None):
    if request.method == 'GET':
        return render(request, "contacts/new_contact.html", locals())
    else:
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        new_person = Person.objects.create(name=name, surname=surname)
        new_person.save()
        msg = 'Dodano nową osobę!'
        return HttpResponseRedirect(reverse('added', kwargs={'msg': msg}))


def modify(request, person_id):
    p = get_object_or_404(Person, pk=person_id)
    tel = Tnumber.objects.filter(person=p)
    mail = Email.objects.filter(person=p)

    if request.method == "GET":
        # jeżeli istnieje adres dla tej osoby, to pobierz dane adresowe do formularza
        if p.address_id:
            a = Address.objects.get(pk=p.address_id)
            city = a.city
            city_code = a.city_code
            street = a.street
            str_no = a.str_no
            number = a.number
        return render(request, "contacts/modify.html", locals())

    else:  # na metodzie POST
        # pobierz dane, jeżeli zostały wprowadzone przez użytkownika
        city = request.POST.get('city')
        city_code = request.POST.get('city_code')
        street = request.POST.get('street')
        str_no = request.POST.get('str_no')
        number = request.POST.get('number')

        tel_number = request.POST.get('tel_number')
        tel_type = request.POST.get('tel_type')

        e_mail = request.POST.get('e_mail')
        e_type = request.POST.get('e_type')

        try:
            new_address = Address.objects.get(city=city, city_code=city_code, street=street, str_no=str_no,
                                              number=number)
        except Address.DoesNotExist:
            new_address = Address.objects.create(city=city, city_code=city_code, street=street, str_no=str_no,
                                                 number=number)
            new_address.save()
        p.address = new_address
        p.save()

        # sprawdza czy w modelu Address są puste adresy (bez Person) - tylko przy modyfikacji adresu
        try:
            empty_a = Address.objects.filter(person__isnull=True).values_list('id', flat=True)
            if not empty_a:
                pass
            else:
                empty_id = empty_a[0]
                Address.objects.get(id=empty_id).delete()
        except Address.DoesNotExist:
            pass

        # dodanie nowego nr telefonu
        if tel_number == "":  # jeżeli pole zostało puste, to idź dalej i nie zapisuj nowego tel.
            pass
        else:  # pobierz nowe dane i zapisz nowy telefon
            new_tel = Tnumber.objects.create(number=tel_number, type=tel_type, person=p)
            new_tel.save()

        # dodaie nowego maila
        if e_mail == "":
            pass
        else:
            new_email = Email.objects.create(email=e_mail, type=e_type, person=p)
            new_email.save()

        return HttpResponseRedirect(reverse('contacts'))


def del_person(request, person_id):
    p = get_object_or_404(Person, pk=person_id)
    if p.address_id:
        a_id = p.address_id
        p.delete()
        try:
            Person.objects.get(address_id=a_id)
            pass
        except Person.MultipleObjectsReturned:
            pass
        except Person.DoesNotExist:
            a = Address.objects.get(pk=a_id)
            a.delete()
    else:
        p.delete()
    return HttpResponseRedirect(reverse('contacts'))
