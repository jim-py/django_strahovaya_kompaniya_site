from django.shortcuts import render, redirect
from django.views.generic import DeleteView, UpdateView
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.paginator import Paginator


class StaffDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'entry'
    model = Staff
    success_url = '/staff/archive'
    template_name = 'belay/staff_delete.html'


class StaffUpdateView(LoginRequiredMixin, UpdateView):
    model = Staff
    form_class = CustomUserChangeForm
    template_name = 'belay/edit_profile.html'

    def get_success_url(self):
        return reverse("profile", kwargs={"username": self.kwargs["username"]})


@login_required(login_url='entry')
def profile(request, username):
    user = Staff.objects.get(username=username)
    pk = Staff.objects.get(username=username).pk
    if user.is_superuser:
        su = "Да"
    else:
        su = "Нет"
    if user.is_staff:
        admin = "Да"
    else:
        admin = "Нет"
    data = ['s'] * 12

    data[0] = f"ФИО: {user.last_name} {user.first_name} {user.otchestvo}"
    data[1] = f"Телефон: {user.telephone}"
    data[2] = f"День рождения: {user.birthday.strftime('%d.%m.%Y г.')}"
    data[3] = f"Роль: {user.role}"
    data[4] = f"Филиал: {user.branch}"
    data[5] = f"Должность: {user.post}"
    data[6] = f"Логин: {user.username}"
    data[7] = f"Почта: {user.email}"
    data[8] = f"Админ: {admin}"
    data[9] = f"Суперпользователь: {su}"
    data[10] = f"Адрес: г. {user.city}, улица {user.road}, дом {user.house}, квартира {user.flat}"
    data[11] = f"Дата регистрации: {user.date_joined.strftime('%d.%m.%Y г.')}"

    return render(request, 'belay/profile.html', {'profile': data, 'username': user.username, 'pk': pk})


def entry(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('news')
        else:
            messages.error(request, 'Неверные данные!')
    else:
        form = UserLoginForm()
    return render(request, 'belay/entry.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('entry')


def registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('news')
        else:
            messages.error(request, 'Ошибка регистрации!')
    else:
        form = UserRegisterForm()
    return render(request, 'belay/registration.html', {'form': form})


def page_maker(request, massive):
    paginator = Paginator(massive, 8)
    page_num = request.GET.get('page', 1)
    return paginator.get_page(page_num)


@login_required(login_url='entry')
def staff_return(request, pk):
    worker = Staff.objects.get(pk=pk)
    worker.is_active = True
    worker.save(update_fields=["is_active"])
    return redirect('staff_archive')


@login_required(login_url='entry')
def hold_staff(request, pk):
    worker = Staff.objects.get(pk=pk)
    worker.is_active = False
    worker.save(update_fields=["is_active"])
    return redirect('staff')


@login_required(login_url='entry')
def news(request):
    return render(request, 'belay/news.html',
                  {'page_data': page_maker(request, News.objects.all().order_by('-addDate'))})


@login_required(login_url='entry')
def staff_archive(request):
    return render(request, 'belay/staff_archive.html',
                  {'page_data': page_maker(request, Staff.objects.filter(is_active=False).order_by('last_name'))})


@login_required(login_url='entry')
def staff(request):
    return render(request, 'belay/staff.html',
                  {'page_data': page_maker(request, Staff.objects.filter(is_active=True).order_by('last_name'))})


@login_required(login_url='entry')
def branch(request):
    return render(request, 'belay/branch.html',
                  {'page_data': page_maker(request, Branch.objects.all().order_by('name'))})


@login_required(login_url='entry')
def pact(request):
    return render(request, 'belay/pact.html',
                  {'page_data': page_maker(request, Pact.objects.filter(archive=False).order_by('-conclusionDate'))})


@login_required(login_url='entry')
def get_branch(request, branch_id):
    return render(request, 'belay/staff_branch.html',
                  {'page_data': page_maker(request, Staff.objects.filter(branch_id=branch_id).order_by('last_name')), 'branch_id': branch_id})


@login_required(login_url='entry')
def calendar_staff_pacts(request, pk, year, month):
    worker = Staff.objects.get(pk=pk)
    worker_fio = worker.last_name + ' ' + worker.first_name + ' ' + worker.otchestvo
    worker_pacts = worker.pact_set.filter(conclusionDate__year=year, conclusionDate__month=month).order_by(
        '-conclusionDate')
    if len(str(month)) == 1:
        month = '0' + str(month)
    return render(request, 'belay/graphic.html',
                  {'pact': worker_pacts, 'staff_fio': worker_fio, 'year': year, 'month': month})


@login_required(login_url='entry')
def staff_pacts(request, pk):
    worker = Staff.objects.get(pk=pk)
    worker_fio = worker.last_name + ' ' + worker.first_name + ' ' + worker.otchestvo
    worker_pacts = worker.pact_set.all().order_by('-conclusionDate')
    return render(request, 'belay/pact.html',
                  {'page_data': page_maker(request, worker_pacts), 'staff_fio': worker_fio})


@login_required(login_url='entry')
def add_pact(request):
    if request.method == 'POST':
        form = PactForm(request.POST)
        if form.is_valid():
            Pact.objects.create(**form.cleaned_data)
            return redirect('pact')
    else:
        form = PactForm()
    return render(request, 'belay/add_pact.html', {'form': form})


@login_required(login_url='entry')
def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            Staff.objects.create(**form.cleaned_data)
            return redirect('staff')
    else:
        form = StaffForm()
    return render(request, 'belay/add_staff.html', {'form': form})


@login_required(login_url='entry')
def add_branch(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            Branch.objects.create(**form.cleaned_data)
            return redirect('branch')
    else:
        form = BranchForm()
    return render(request, 'belay/add_branch.html', {'form': form})


@login_required(login_url='entry')
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            News.objects.create(**form.cleaned_data)
            return redirect('news')
    else:
        form = NewsForm()
    return render(request, 'belay/add_news.html', {'form': form})


@login_required(login_url='entry')
def search_branch(request):
    branch_name = request.GET.get('search')
    if request.method == 'GET':
        if branch_name == "":
            place = Branch.objects.all().order_by('first_name')
        else:
            place = Branch.objects.filter(name__contains=branch_name).order_by('name')
        return render(request, 'belay/branch.html', {'page_data': page_maker(request, place)})
    else:
        return render(request, "belay/branch.html")


@login_required(login_url='entry')
def search_staff(request):
    search_staffs = request.GET.get('search')
    if request.method == 'GET':
        if search_staffs == "":
            staffs = Staff.objects.all().order_by('last_name')
        else:
            staffs = Staff.objects.filter(last_name__contains=search_staffs).order_by('last_name')
        return render(request, 'belay/staff.html', {'page_data': page_maker(request, staffs)})
    else:
        return render(request, "belay/staff.html", {})


@login_required(login_url='entry')
def search_staff_archive(request):
    search_staffs = request.GET.get('search')
    if request.method == 'GET':
        if search_staffs == "":
            staffs = Staff.objects.filter(is_active=False).order_by('last_name')
        else:
            staffs = Staff.objects.filter(last_name__contains=search_staffs, is_active=False).order_by('last_name')
        return render(request, 'belay/staff_archive.html', {'page_data': page_maker(request, staffs)})
    else:
        return render(request, "belay/staff_archive.html", {})


@login_required(login_url='entry')
def get_branch_search(request, branch_id):
    search_staffs = request.GET.get('search')
    if request.method == 'GET':
        if search_staffs == "":
            staffs = Staff.objects.filter(is_active=False).order_by('last_name')
        else:
            staffs = Staff.objects.filter(last_name__contains=search_staffs, branch_id=branch_id).order_by('last_name')
        return render(request, 'belay/staff_branch.html', {'page_data': page_maker(request, staffs), 'branch_id': branch_id})
    else:
        return render(request, "belay/staff_branch.html", {})


@login_required(login_url='entry')
def search_news(request):
    search_new = request.GET.get('search')
    if request.method == 'GET':
        if search_new == "":
            news_get = News.objects.all().order_by('-addDate')
        else:
            news_get = News.objects.filter(name__contains=search_new).order_by('name')
        return render(request, 'belay/news.html', {'page_data': page_maker(request, news_get)})
    else:
        return render(request, "belay/news.html", {})


@login_required(login_url='entry')
def search_pact(request):
    search_pacts = request.GET.get('search')
    if request.method == 'GET':
        if search_pacts == "":
            pacts = Pact.objects.filter(archive=False).order_by('-conclusionDate')
        else:
            pacts = []
            for _ in Client.objects.filter(surname__contains=search_pacts):
                pacts += _.pact_set.filter(archive=False)
        return render(request, 'belay/pact.html', {'page_data': page_maker(request, pacts)})
    else:
        return render(request, "belay/pact.html", {})
