from datetime import datetime, timedelta
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from bistrooapp_admin.models import Category, Menuu, Theme
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from .forms import (CurrentDate, ThemeForm, ThemeUpdateForm,
                    SublineUpdateForm, SublineForm, CategoryForm, DuplicateDate, MenuuSearchForm)

class CategoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "bistrooapp_admin/category.html"
    model = Category
    context_object_name = "categories"

    def test_func(self):
        return self.request.user.groups.filter(name='kasutajad').exists()


class CategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = "bistrooapp_admin/category_create.html"
    model = Category
    success_url = reverse_lazy("bistrooapp_admin:category")
    form_class = CategoryForm

    def test_func(self):
        return self.request.user.groups.filter(name='kasutajad').exists()


class CategoryDeleteView(DeleteView):
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        category_name = category.category_name
        category.delete()
        messages.error(request, f"\"{category_name}\" kustutatud.")

        return HttpResponseRedirect(reverse("bistrooapp_admin:category"))


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "bistrooapp_admin/category_form_update.html"
    model = Category

    success_url = reverse_lazy("bistrooapp_admin:category")
    form_class = CategoryForm

    def test_func(self):
        return self.request.user.groups.filter(name='kasutajad').exists()


def is_user(user):
    return user.groups.filter(name='kasutajad').exists()


@user_passes_test(is_user)
def menuu_list(request):
    categories = Category.objects.all()

    if request.method == "POST":
        if request.POST.get("valitud_kp"):
            valitud_kp = request.POST.get("valitud_kp")
            request.session['menu_date'] = valitud_kp
        else:
            valitud_kp = datetime.today()
            request.session['menu_date'] = valitud_kp.strftime("%Y-%m-%d")

    elif request.session.get("menu_date"):
        valitud_kp = request.session.get('menu_date')
    else:
        valitud_kp = datetime.today()
        request.session['menu_date'] = valitud_kp.strftime("%Y-%m-%d")

    request.session.set_expiry(timedelta(hours=2))

    q_result_menuu = Menuu.objects.filter(menu_date=valitud_kp)
    q_result_theme = Theme.objects.filter(menu_date=valitud_kp)

    theme_id = None
    if q_result_theme.exists():
        theme_id = q_result_theme.first().id

    if isinstance(valitud_kp, str):
        kp_obj = datetime.strptime(valitud_kp, "%Y-%m-%d")
        formatted_date = kp_obj.strftime("%d.%m.%Y")
        default_date = kp_obj.strftime("%Y-%m-%d")
    else:
        formatted_date = valitud_kp.strftime("%d.%m.%Y")
        default_date = valitud_kp.strftime("%Y-%m-%d")
        kp_obj = datetime.strptime(default_date, "%Y-%m-%d")

    current_date_str = datetime.today().strftime("%Y-%m-%d")
    if kp_obj >= datetime.strptime(current_date_str, "%Y-%m-%d"):
        is_current = True
    else:
        is_current = False

    datePicker = CurrentDate(initial={"valitud_kp": default_date})

    if request.session.get('menu_date_duplicate'):
        dup_date = request.session.get('menu_date_duplicate')
        duplicate_date = DuplicateDate(initial={"duplikaadi_kp": dup_date})
    else:
        duplicate_date = DuplicateDate(initial={"duplikaadi_kp": datetime.today()})

    context = {
        'categories': categories,
        'menuu_items': q_result_menuu,
        'themes': q_result_theme,
        'datePicker': datePicker,
        'formatted_date':  formatted_date,
        'theme_id': theme_id,
        "duplicate_date": duplicate_date,
        "is_current": is_current
    }
    return render(request, 'bistrooapp_admin/menuu_list.html', context)


@user_passes_test(is_user)
def add_subline(request, category):

    valitud_kp = request.session.get("menu_date")

    categoryus = Category.objects.get(category_name=category)

    if request.method == "POST":
        subline_form = SublineForm(request.POST)
        if subline_form.is_valid():
            subline_form.save()
            return redirect("bistrooapp_admin:menuu_list")
    else:
        subline_form = SublineForm(initial={"menu_date": valitud_kp, "category_name": categoryus})

    current_date = datetime.strptime(valitud_kp, "%Y-%m-%d")
    context = {
        "subline_form": subline_form,
        "categoryus": categoryus,
        "current_date": current_date
        }

    return render(request, "bistrooapp_admin/menuu_add.html", context)


@user_passes_test(is_user)
def add_theme(request):
    valitud_kp = request.session.get("menu_date")
    current_date = datetime.strptime(valitud_kp, "%Y-%m-%d")

    if not Theme.objects.filter(menu_date=valitud_kp).exists():
        theme_formike = ThemeForm(initial={"menu_date": valitud_kp})
    else:
        theme_id = Theme.objects.get(menu_date=valitud_kp).id

        theme_instance = get_object_or_404(Theme, id=theme_id)
        theme_formike = ThemeForm(instance=theme_instance)

    if request.method == "POST":
        menu_date = request.POST.get("menu_date")
        theme = request.POST.get("theme")
        recommenders = request.POST.get("recommenders")
        author = request.POST.get("author")

        if theme or recommenders or author:
            if not Theme.objects.filter(menu_date=menu_date).exists():
                theme_formike = ThemeForm(request.POST)
                if theme_formike.is_valid():
                    theme_formike.save()
                    return redirect("bistrooapp_admin:menuu_list")

            else:
                theme_id = Theme.objects.get(menu_date=menu_date).id
                theme_instance = get_object_or_404(Theme, id=theme_id)
                theme_formike = ThemeForm(request.POST, instance=theme_instance)
                if theme_formike.is_valid():
                    theme_formike.save()
                    return redirect("bistrooapp_admin:menuu_list")
        else:

            return redirect("bistrooapp_admin:menuu_list")

    return render(request, 'bistrooapp_admin/theme_add.html',
                  {"theme_formike": theme_formike, "current_date": current_date})


@user_passes_test(is_user)
def update_theme(request, theme_id):
    valitud_kp = request.session.get("menu_date")
    current_date = datetime.strptime(valitud_kp, "%Y-%m-%d")

    theme_instance = get_object_or_404(Theme, id=theme_id)
    if request.method == "POST":
        theme_up_form = ThemeUpdateForm(request.POST, instance=theme_instance)
        if theme_up_form.is_valid():
            theme_up_form.save()
            return redirect("bistrooapp_admin:menuu_list")
    else:
        theme_up_form = ThemeUpdateForm(instance=theme_instance)

    return render(request,"bistrooapp_admin/theme_update.html",
                  {"theme_up_form": theme_up_form, "theme_id": theme_id, "current_date": current_date})

def mytoday(request):
    if 'menu_date' in request.session:
        del request.session['menu_date']

    return redirect('bistrooapp_admin:menuu_list')


def move_back(request):
    if 'menu_date' in request.session:
        menu_date = request.session.get("menu_date")
        kp_obj = datetime.strptime(menu_date, "%Y-%m-%d")
        kp_obj = kp_obj - timedelta(days=1)
        menu_date = kp_obj.strftime("%Y-%m-%d")
        request.session['menu_date'] = menu_date
    else:
        kp = datetime.today() - timedelta(days=1)
        request.session['menu_date'] = kp.strftime("%Y-%m-%d")
    return redirect('bistrooapp_admin:menuu_list')


def move_forward(request):
    if 'menu_date' in request.session:
        menu_date = request.session.get("menu_date")
        kp_obj = datetime.strptime(menu_date, "%Y-%m-%d")
        kp_obj = kp_obj + timedelta(days=1)
        menu_date = kp_obj.strftime("%Y-%m-%d")
        request.session['menu_date'] = menu_date
    else:
        kp = datetime.today() + timedelta(days=1)
        request.session['menu_date'] = kp.strftime("%Y-%m-%d")
    return redirect('bistrooapp_admin:menuu_list')


def delete_author(request, theme_id):
    theme_instance = Theme.objects.get(id=theme_id)
    author = theme_instance.author
    if theme_instance.theme:
        theme_instance.author = None
        theme_instance.save()
    elif theme_instance.theme is None:
        theme_instance.delete()

    messages.success(request, author + " kustutatud")
    return redirect('bistrooapp_admin:menuu_list')


def delete_theme(request, theme_id):
    theme_instance = Theme.objects.get(id=theme_id)
    theme = theme_instance.theme
    if theme_instance.author is None:
        theme_instance.delete()
    elif theme_instance.author:
        theme_instance.theme = None
        theme_instance.recommenders = None
        theme_instance.save()
    messages.success(request, theme + " kustutatud")
    return redirect('bistrooapp_admin:menuu_list')


@user_passes_test(is_user)
def update_subline(request, line_id):
    valitud_kp = request.session.get("menu_date")
    current_date = datetime.strptime(valitud_kp, "%Y-%m-%d")

    line_instance = get_object_or_404(Menuu, id=line_id)
    if request.method == "POST":
        subline_up_form = SublineUpdateForm(request.POST, instance=line_instance)
        if subline_up_form.is_valid():
            subline_up_form.save()
            return redirect("bistrooapp_admin:menuu_list")
    else:
        subline_up_form = SublineUpdateForm(instance=line_instance)

    return render(request, "bistrooapp_admin/menuu_update.html",
                  {"subline_up_form": subline_up_form, "line_id": line_id, "current_date": current_date})

def delete_subline(request, line_id):
    line_instance = get_object_or_404(Menuu, id=line_id)
    description = line_instance.description
    line_instance.delete()
    messages.success(request, description + " kustutatud")
    return HttpResponseRedirect(reverse("bistrooapp_admin:menuu_list"))


def dublicate_message(request):
    if request.method == "POST":
        duplikaadi_kp = request.POST.get("duplikaadi_kp")
        request.session['menu_date_duplicate'] = duplikaadi_kp
        duplikaadi_kp = datetime.strptime(duplikaadi_kp, "%Y-%m-%d")

    valitud_kp = request.session.get("menu_date")
    valitud_kp = datetime.strptime(valitud_kp, "%Y-%m-%d")

    return render(request, "bistrooapp_admin/duplicate_message.html",
                  {"duplikaadi_kp": duplikaadi_kp, "valitud_kp": valitud_kp})


def duplicate_menu(request):
    duplikaadi_kp = request.session.get("menu_date_duplicate")
    valitud_kp = request.session.get("menu_date")

    if not duplikaadi_kp == valitud_kp:
        q_result_menuu = Menuu.objects.filter(menu_date=valitud_kp)
        q_result_theme = Theme.objects.filter(menu_date=valitud_kp)

        q_result_menuu_dub = Menuu.objects.filter(menu_date=duplikaadi_kp)
        q_result_theme_dub = Theme.objects.filter(menu_date=duplikaadi_kp)
        if q_result_theme_dub:
            theme_instance_dub = Theme.objects.get(menu_date=duplikaadi_kp)
            theme_instance_dub.delete()
        if q_result_menuu_dub:
            for obj in q_result_menuu_dub:
                obj.delete()

        if q_result_theme:
            theme_instance = Theme.objects.get(menu_date=valitud_kp)
            new_theme_instance = Theme.objects.create(
                menu_date=duplikaadi_kp,
                theme=theme_instance.theme,
                recommenders=theme_instance.recommenders,
                author=theme_instance.author
            )
            new_theme_instance.save()

        if q_result_menuu:
            for menu_instance in q_result_menuu:
                new_menu_instance = Menuu.objects.create(
                    menu_date=duplikaadi_kp,
                    category_name=menu_instance.category_name,
                    description=menu_instance.description,
                    price_full=menu_instance.price_full,
                    price_half=menu_instance.price_half
                )
                new_menu_instance.save()

    return HttpResponseRedirect(reverse("bistrooapp_admin:menuu_list"))


@user_passes_test(is_user)
def menuu_search(request):
    menuu_search_form = MenuuSearchForm()
    return render(request, "bistrooapp_admin/menuu_search.html",
                  {"menuu_search_form": menuu_search_form})


@user_passes_test(is_user)
def menuu_search_list(request):

    if request.method == "POST":
        menuu_search_form = MenuuSearchForm(request.POST)
        if menuu_search_form.is_valid():
            search_phrase = menuu_search_form.cleaned_data["search_phrase"]
            request.session['search_phrase'] = search_phrase
            search_result_menuu = Menuu.objects.filter(description__contains=search_phrase)

        else:
            return render(request, "bistrooapp_admin/menuu_search.html",
                          {"menuu_search_form": menuu_search_form})

    else:
        search_phrase = request.session.get('search_phrase')
        search_result_menuu = Menuu.objects.filter(description__contains=search_phrase)

    list_count = search_result_menuu.count()

    page = request.GET.get('page', 1)
    paginator = Paginator(search_result_menuu, 10)
    try:
        search_result_menuu = paginator.page(page)
    except PageNotAnInteger:
        search_result_menuu = paginator.page(1)
    except EmptyPage:
        search_result_menuu = paginator.page(paginator.num_pages)

    return render(request, "bistrooapp_admin/menuu_search_list.html",
                      {"search_result_menuu": search_result_menuu, "list_count": list_count, "search_phrase":search_phrase})

def hide_row(request):
    checkboxId = request.GET.get('checkboxId', None)
    line_instance = get_object_or_404(Menuu, id=checkboxId)
    if line_instance.is_hided:
        line_instance.is_hided = False
    else:
        line_instance.is_hided = True
    line_instance.save()

    return HttpResponse()


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.WARNING, 'Oled välja logitud, jätkamiseks palun logi sisse')
    return redirect("login")

def changeMenuuDate(request, line_id):
    line_instance = get_object_or_404(Menuu, id=line_id)
    kp_obj = line_instance.menu_date
    menu_date = kp_obj.strftime("%Y-%m-%d")
    request.session['menu_date'] = menu_date
    return redirect("bistrooapp_admin:menuu_list")
