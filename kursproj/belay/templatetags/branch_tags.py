from django import template
from calendar import monthrange
from belay.models import *


register = template.Library()


@register.simple_tag()
def staff_salary(staff_pk):
    salary = 0
    for pact in Staff.objects.get(pk=staff_pk).pact_set.filter(conclusionDate__year=2022, conclusionDate__month=10):
        salary += pact.type.cost / 100 * pact.type.stake * pact.term.long
        salary += pact.client.estate.cost / 100 * pact.client.estate.percent
    if salary < 25000:
        salary = 25000
    return round(salary)


@register.simple_tag()
def get_massive_columns(year, month):
    days_of_month = get_days_of_month(year, int(month))
    columns = [0] * days_of_month
    for column in range(1, days_of_month + 1):
        columns[column - 1] = column
    return columns


@register.simple_tag()
def staff_salary_of_pact(pk, year, month):
    return staff_salary_graphic(0, pk, year, int(month))


@register.simple_tag()
def salary_of_days(pacts, year, month):
    days_of_month = get_days_of_month(year, int(month))
    days = [0] * days_of_month
    for _ in pacts:
        days[int(_.conclusionDate.strftime("%d")) - 1] = staff_salary_graphic(days[int(_.conclusionDate.strftime("%d")) - 1], _.pk, year, int(month))
    maximum_salary_pay = 0
    day_i = 0
    for day_pay in days:
        if day_pay == 0:
            if day_pay > maximum_salary_pay:
                maximum_salary_pay = day_pay
            else:
                days[day_i] = maximum_salary_pay
        else:
            if day_i != days_of_month - 1:
                days[day_i + 1] += day_pay
        day_i += 1
    return days


@register.simple_tag()
def get_staff_count(branch_pk):
    return Branch.objects.get(pk=branch_pk).staff_set.all().count()


def staff_salary_graphic(salary, pact, year, month):
    p = Pact.objects.get(pk=pact, conclusionDate__year=year, conclusionDate__month=month)
    salary += p.type.cost / 100 * p.type.stake * p.term.long
    salary += p.client.estate.cost / 100 * p.client.estate.percent
    if salary < 25000:
        salary = 25000
    return round(salary)


def get_days_of_month(year, month): return monthrange(year, month)[1]
