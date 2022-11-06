from django.shortcuts import render, redirect
from django.views.generic import DeleteView, UpdateView, ListView, CreateView
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class AddNews(LoginRequiredMixin, CreateView):
    login_url = 'entry'
    model = News
    template_name = 'belay/add_news.html'
    form_class = NewsForm
    success_url = '/news/'


class AddBranch(LoginRequiredMixin, CreateView):
    login_url = 'entry'
    model = Branch
    template_name = 'belay/add_branch.html'
    form_class = BranchForm
    success_url = '/branch/'


class AddStaff(LoginRequiredMixin, CreateView):
    login_url = 'entry'
    model = Staff
    template_name = 'belay/add_staff.html'
    form_class = StaffForm
    success_url = '/staff/'


class AddPact(LoginRequiredMixin, CreateView):
    login_url = 'entry'
    model = Pact
    template_name = 'belay/add_pact.html'
    form_class = PactForm
    success_url = '/pact/'


class IndexSearchNews(LoginRequiredMixin, ListView):
    login_url = 'entry'
    model = News
    template_name = 'belay/news.html'
    context_object_name = "page_data"
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(IndexSearchNews, self).get_context_data(**kwargs)
        search, page = self.request.GET.get('search'), self.request.GET.get('page')

        get_news = News.objects.all().order_by('-addDate')
        if search:
            get_news = get_news.filter(name__icontains=search).order_by('-addDate')
        paginator = Paginator(get_news, self.paginate_by)

        try:
            page_data = paginator.page(page)
        except PageNotAnInteger:
            page_data = paginator.page(1)
        except EmptyPage:
            page_data = paginator.page(paginator.num_pages)

        context['page_data'] = page_data
        context['search'] = search
        return context


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
    archive = 0
    branch_name = Branch.objects.get(pk=branch_id).name
    return render(request, 'belay/staff_branch.html',
                  {'page_data': page_maker(request, Staff.objects.filter(branch_id=branch_id, is_active=True).order_by(
                      'last_name')),
                   'branch_id': branch_id, 'branch_name': branch_name, 'check': archive})


@login_required(login_url='entry')
def staff_branch_archive(request, branch_id):
    archive = 1
    branch_name = Branch.objects.get(pk=branch_id).name
    return render(request, 'belay/staff_branch.html',
                  {'page_data': page_maker(request, Staff.objects.filter(branch_id=branch_id, is_active=False).order_by(
                      'last_name')),
                   'branch_id': branch_id, 'branch_name': branch_name, 'check': archive})


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
        return render(request, 'belay/staff_branch.html',
                      {'page_data': page_maker(request, staffs), 'branch_id': branch_id})
    else:
        return render(request, "belay/staff_branch.html", {})


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
