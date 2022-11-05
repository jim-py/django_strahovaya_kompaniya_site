import os

import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kursproj.settings')
django.setup()

from belay.models import *
from faker import Faker

fake = Faker('ru-RU')

estate = ClientEstate.objects.values_list('id', flat=True).distinct()

role = StaffRole.objects.values_list('id', flat=True).distinct()
branch = Branch.objects.values_list('id', flat=True).distinct()
post = StaffPost.objects.values_list('id', flat=True).distinct()

type = TypePact.objects.values_list('id', flat=True).distinct()
staff = Staff.objects.values_list('id', flat=True).distinct()
client = Client.objects.values_list('id', flat=True).distinct()
term = Term.objects.values_list('id', flat=True).distinct()

# for _ in range(1):
#     Branch.objects.create(name=fake.city_name(),
#                           city=fake.city_name(),
#                           road=fake.street_title(),
#                           house=fake.building_number(),
#                           office=fake.building_number(),
#                           telephone=fake.postcode())
#
# for _ in range(10):
#     TypePact.objects.create(name=fake.sentence(nb_words=1),
#                             description=fake.sentence(nb_words=10),
#                             stake=random.randint(5, 20),
#                             cost=random.randint(5000, 20000))
#
# for _ in range(20):
#     Term.objects.create(long=_)
#
# for _ in range(50):
#     ClientEstate.objects.create(name=fake.sentence(nb_words=1),
#                                 cost=random.randint(500000, 1500000),
#                                 percent=random.randint(5, 20))
#
# for _ in range(20):
#     StaffRole.objects.create(name=fake.sentence(nb_words=1))
#
# for _ in range(20):
#     StaffPost.objects.create(name=fake.sentence(nb_words=1),
#                              salary=random.randint(15000, 25000))
#
# for _ in range(499):
#     Client.objects.create(estate=fake.random_element(ClientEstate.objects.filter(id=fake.random_element(estate))),
#                           surname=fake.last_name_male(),
#                           name=fake.first_name_male(),
#                           otchestvo=fake.middle_name_male(),
#                           birthday=fake.date_of_birth(minimum_age=25, maximum_age=50),
#                           city=fake.city_name(),
#                           road=fake.street_title(),
#                           house=fake.building_number(),
#                           flat=fake.building_number(),
#                           telephone=fake.postcode(),
#                           inn=fake.businesses_inn(),
#                           passport=fake.postcode())
#
for _ in range(35):
    Staff.objects.create(role=fake.random_element(StaffRole.objects.filter(id=fake.random_element(role))),
                         branch=fake.random_element(Branch.objects.filter(id=13)),
                         post=fake.random_element(StaffPost.objects.filter(id=fake.random_element(post))),
                         last_name=fake.last_name_male(),
                         first_name=fake.first_name_male(),
                         otchestvo=fake.middle_name_male(),
                         birthday=fake.date_of_birth(minimum_age=25, maximum_age=50),
                         city=fake.city_name(),
                         road=fake.street_title(),
                         house=fake.building_number(),
                         flat=fake.building_number(),
                         telephone=fake.postcode(),
                         is_superuser=False,
                         is_staff=False,
                         is_active=True,
                         username=fake.user_name(),
                         password=fake.user_name(),
                         email=fake.free_email())
#
# for _ in range(499):
#     Pact.objects.create(branch=fake.random_element(Branch.objects.filter(id=fake.random_element(branch))),
#                         type=fake.random_element(TypePact.objects.filter(id=fake.random_element(type))),
#                         staff=fake.random_element(Staff.objects.filter(id=29)),
#                         client=fake.random_element(Client.objects.filter(id=fake.random_element(client))),
#                         term=fake.random_element(Term.objects.filter(id=fake.random_element(term))),
#                         ssum=fake.postcode(),
#                         conclusionDate=fake.date_between_dates(1634662338, 1666198338),
#                         archive=False)
#
# for _ in range(50):
#     News.objects.create(name=fake.sentence(nb_words=4),
#                         description=fake.sentence(nb_words=10))
