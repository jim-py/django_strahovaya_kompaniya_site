from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, UpdateView, ListView, CreateView
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from datetime import datetime


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


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = Staff
    form_class = CustomUserChangeForm
    template_name = 'belay/edit_profile.html'

    def get_success_url(self):
        return reverse("profile", kwargs={"username": self.kwargs["username"]})


class DeleteStaff(LoginRequiredMixin, DeleteView):
    login_url = 'entry'
    model = Staff
    template_name = 'belay/staff_delete.html'

    def get_context_data(self, **kwargs):
        context = super(DeleteStaff, self).get_context_data(**kwargs)
        worker = context['staff']
        fio = f'{worker.last_name} {worker.first_name} {worker.otchestvo}'
        context['fio'] = fio
        return context

    def get_success_url(self):
        return self.request.POST.get('previous_page', '/')


def pagination_maker(x, z):
    paginator = Paginator(x, 9)

    try:
        page_data = paginator.page(z)
    except PageNotAnInteger:
        page_data = paginator.page(1)
    except EmptyPage:
        page_data = paginator.page(paginator.num_pages)

    return page_data


class ViewSearchStaff(LoginRequiredMixin, ListView):
    login_url = 'entry'
    model = Staff
    context_object_name = "page_data"

    def get_context_data(self, **kwargs):
        context = super(ViewSearchStaff, self).get_context_data(**kwargs)
        search, page = self.request.GET.get('search'), self.request.GET.get('page')

        if 'branch_id' in self.kwargs:
            if self.extra_context['archive']:
                context['branch_id'] = self.kwargs['branch_id']
                get_staff = Staff.objects.filter(is_active=False, branch_id=self.kwargs['branch_id']).order_by('last_name')
                if search:
                    get_staff = get_staff.filter(is_active=False, branch_id=self.kwargs['branch_id'], last_name__icontains=search).order_by('last_name')
            else:
                context['branch_id'] = self.kwargs['branch_id']
                get_staff = Staff.objects.filter(is_active=True, branch_id=self.kwargs['branch_id']).order_by('last_name')
                if search:
                    get_staff = get_staff.filter(is_active=True, branch_id=self.kwargs['branch_id'], last_name__icontains=search).order_by('last_name')
        else:
            if self.extra_context['archive']:
                get_staff = Staff.objects.filter(is_active=False).order_by('last_name')
                if search:
                    get_staff = get_staff.filter(is_active=False, last_name__icontains=search).order_by('last_name')
            else:
                get_staff = Staff.objects.filter(is_active=True).order_by('last_name')
                if search:
                    get_staff = get_staff.filter(is_active=True, last_name__icontains=search).order_by('last_name')

        context['page_data'] = pagination_maker(get_staff, page)
        context['search'] = search
        today = datetime.today()
        context['month'] = today.strftime("%m")
        context['year'] = today.strftime("%Y")
        return context

    def get_template_names(self):
        if self.extra_context['archive']:
            return ['belay/staff_archive.html']
        else:
            return ['belay/staff.html']


class ViewSearchBranch(LoginRequiredMixin, ListView):
    login_url = 'entry'
    model = Branch
    template_name = 'belay/branch.html'
    context_object_name = "page_data"

    def get_context_data(self, **kwargs):
        context = super(ViewSearchBranch, self).get_context_data(**kwargs)
        search, page = self.request.GET.get('search'), self.request.GET.get('page')

        get_branches = Branch.objects.all().order_by('name')
        if search:
            get_branches = get_branches.filter(name__icontains=search).order_by('name')

        context['page_data'] = pagination_maker(get_branches, page)
        context['search'] = search
        return context


class ViewSearchPact(LoginRequiredMixin, ListView):
    login_url = 'entry'
    model = Pact
    template_name = 'belay/pact.html'
    context_object_name = "page_data"

    def get_context_data(self, **kwargs):
        context = super(ViewSearchPact, self).get_context_data(**kwargs)
        search, page = self.request.GET.get('search'), self.request.GET.get('page')

        if 'pk' in self.kwargs:
            worker = Staff.objects.get(pk=self.kwargs['pk'])
            context['worker_fio'] = f'{worker.last_name} {worker.first_name} {worker.otchestvo}'
            if search:
                get_pacts = [x for x in worker.pact_set.filter(archive=False).order_by('-conclusionDate') if search.lower() in x.client.surname.lower()]
            else:
                get_pacts = worker.pact_set.filter(archive=False).order_by('-conclusionDate')
        else:
            if search:
                get_pacts = []
                for client in Client.objects.filter(surname__icontains=search):
                    get_pacts += client.pact_set.filter(archive=False)
            else:
                get_pacts = Pact.objects.filter(archive=False).order_by('-conclusionDate')

        context['page_data'] = pagination_maker(get_pacts, page)
        context['search'] = search
        return context


class ViewSearchNews(LoginRequiredMixin, ListView):
    login_url = 'entry'
    model = News
    template_name = 'belay/news.html'
    context_object_name = "page_data"

    def get_context_data(self, **kwargs):
        context = super(ViewSearchNews, self).get_context_data(**kwargs)
        search, page = self.request.GET.get('search'), self.request.GET.get('page')

        get_news = News.objects.all().order_by('-addDate')
        if search:
            get_news = get_news.filter(name__icontains=search).order_by('-addDate')

        context['page_data'] = pagination_maker(get_news, page)
        context['search'] = search
        return context


@login_required(login_url='entry')
def profile(request, username):
    user = Staff.objects.get(username=username)

    su = 'Да' if user.is_superuser else 'Нет'
    admin = 'Да' if user.is_staff else 'Нет'
    photo = user.photo if user.photo else '/media/user.png'

    data = {'ФИО': f"{user.last_name} {user.first_name} {user.otchestvo}",
            'Телефон': user.telephone,
            'День рождения': user.birthday.strftime('%d.%m.%Y г.') if user.birthday else user.birthday,
            'Роль': user.role,
            'Филиал': user.branch,
            'Должность': user.post,
            'Логин': user.username,
            'Почта': user.email,
            'Админ': admin,
            'Суперпользователь': su,
            'Адрес': f"г. {user.city}, улица {user.road}, дом {user.house}, квартира {user.flat}",
            'Дата регистрации': user.date_joined.strftime('%d.%m.%Y г.')}
    if request.method == 'POST' and request.FILES:
        file = request.FILES['photo_upload']
        fss = FileSystemStorage()
        filename = fss.save(file.name, file)
        file_url = fss.url(filename)
        user.photo = file_url
        user.save(update_fields=["photo"])
        return render(request, 'belay/profile.html',
                      {'profile': data, 'username': user.username, 'pk': user.pk, 'photo': user.photo})
    return render(request, 'belay/profile.html',
                  {'profile': data, 'username': user.username, 'pk': user.pk, 'photo': photo})


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


@login_required(login_url='entry')
def staff_to_archive(request, pk):
    worker = Staff.objects.get(pk=pk)
    worker.is_active = True if 'archive' in request.META.get('HTTP_REFERER') else False
    worker.save(update_fields=["is_active"])
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='entry')
def staff_graphic(request, pk, year, month):
    today = datetime.today()
    if not int(today.strftime("%Y")) - 11 < year < int(today.strftime("%Y")) + 1:
        return HttpResponseNotFound("WRONG DATE")
    elif year == int(today.strftime("%Y")) - 10 and month < int(today.strftime("%m")):
        return HttpResponseNotFound("WRONG DATE")
    elif year == int(today.strftime("%Y")) and month > int(today.strftime("%m")):
        return HttpResponseNotFound("WRONG DATE")
    worker = Staff.objects.get(pk=pk)
    worker_fio = worker.last_name + ' ' + worker.first_name + ' ' + worker.otchestvo
    worker_pacts = worker.pact_set.filter(conclusionDate__year=year, conclusionDate__month=month).order_by('-conclusionDate')
    if len(str(month)) == 1:
        month = '0' + str(month)
    max_date = f'{today.strftime("%Y")}-{today.strftime("%m")}'
    min_date = f'{int(today.strftime("%Y")) - 10}-{today.strftime("%m")}'
    return render(request, 'belay/graphic.html',
                  {'pact': worker_pacts, 'staff_fio': worker_fio, 'year': year, 'month': month, 'max_date': max_date, 'min_date': min_date})
