from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Product, Recipe, Article, ShoppingList, Favourite
from django.template.context_processors import csrf
from .forms import SignUpForm


# глобальная переменная
# для сохранения последних просмотренных фактов
fact_cookie = ''


# returns HttpResponse with home.html
def home(request):
    args = {}
    args.update(csrf(request))
    args['product'] = None
    args['facts'] = []
    args['description'] = 'Добро пожаловать на сайт с интересными фактами о продуктах питания и полезными рецептами!'

    if 'last_facts' in request.COOKIES:
        facts = []
        fact_slugs = request.COOKIES.get('last_facts', [])
        fact_slugs = fact_slugs.split(',')[:-1]
        for slug in fact_slugs:
            facts.append(Product.objects.get(slug=slug))
        args['facts'] = facts
        args['description'] = "Недавно вы смотрели эти факты:"

    return render(request, 'home.html', args)


# get all cards with existing products
def facts(request):
    products = Product.objects.all().order_by('-create_time')
    return render(request, 'facts.html', {"products": products})


# get product by slug
def product(request, slug):
    product = Product.objects.get(slug=slug)
    state = "Зарегистрируйтесь, чтобы сохранять любимые факты"
    color = ''

    # set last seen fact to fact_cookie
    global fact_cookie
    facts = []
    my_slug = product.slug + ','
    if my_slug not in fact_cookie:
        fact_cookie = my_slug + fact_cookie
    splitted = fact_cookie.split(',')[:-1]
    if len(splitted) > 5:
        for i in range(0, 5):
            facts.append(splitted[i] + ',')
        fact_cookie = ''.join(facts)

    if request.user.is_authenticated:
        current_user = request.user
        bookmarks = Favourite.objects.get(user=current_user)
        if product in bookmarks.products.all():
            state = "Удалить"
            color = "#ff8080"
        else:
            state = "Добавить"
            color = "#6DB771"

        if request.method == "POST":
            if state == "Добавить":
                bookmarks.products.add(product)
                color = "#ff8080"
                state = "Удалить"
            else:
                bookmarks.products.remove(product)
                color = "#6DB771"
                state = "Добавить"

        response = render(request, 'product.html', {"product": product, "state": state, "color": color})
        response.set_cookie('last_facts', fact_cookie)
        return response

    response = render(request, 'product.html', {"product" : product, "state": state, "color": color})
    response.set_cookie('last_facts', fact_cookie)
    return response


# get cadrs of existing recipes
def recipes(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {"recipes": recipes})


# get recipe by slug
def recipe(request, slug):
    state = "Зарегистрируйтесь, чтобы сохранять любимые рецепты"
    color = ''
    recipe = Recipe.objects.get(slug=slug)
    res_ingredients = recipe.ingredients.all().order_by('-create_time')
    ingredients = []
    for ingredient in res_ingredients:
        ingredients.append(ingredient.name)
    ingredients = ", ".join(ingredients)

    if request.user.is_authenticated:
        current_user = request.user
        bookmarks = Favourite.objects.get(user=current_user)
        if recipe in bookmarks.recipes.all():
            state = "Удалить"
            color = "#ff8080"
        else:
            state = "Добавить"
            color = "#6DB771"

        if request.method == "POST":
            if state == "Добавить":
                bookmarks.recipes.add(recipe)
                color = "#ff8080"
                state = "Удалить"
            else:
                bookmarks.recipes.remove(recipe)
                color = "#6DB771"
                state = "Добавить"
        return render(request, 'recipe.html', {"recipe": recipe, "state": state, "ingredients": ingredients, "color": color})

    return render(request, 'recipe.html', {"recipe": recipe, "state": state, "ingredients": ingredients, "color": color})


# get list of news
def news(request):
    news = Article.objects.all().order_by('-create_time')
    return render(request, 'news.html', {"news": news})


# get article by slug
def article(request, slug):
    article = Article.objects.get(slug=slug)
    return render(request, 'article.html', {"article": article})


# sign up new user
def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            shoplist, bookmarks = ShoppingList(), Favourite()
            shoplist.user = user
            bookmarks.user = user
            shoplist.save()
            bookmarks.save()
            login(request, user)
            return redirect('eater-profile')
    else:
        form = SignUpForm()
    return render(request, 'eater_user/signup.html', {'form': form})


# user account
@login_required(login_url='/login')
def eater_profile(request):
    current_user = request.user
    bookmarks = Favourite.objects.get(user=current_user)
    shoplist = ShoppingList.objects.get(user=current_user)
    products = bookmarks.products.all()
    recipes = bookmarks.recipes.all()

    if request.method == "POST":
        shoplist.content = request.POST.get("shoplist").rstrip().lstrip()
        shoplist.save()
        return render(request, 'eater_user/eater.html', {'user': current_user, 'shoplist': shoplist, 'products': products, 'recipes': recipes})
    return render(request, 'eater_user/eater.html', {'user': current_user, 'shoplist': shoplist, 'products': products, 'recipes': recipes})


# searching
def search_titles(request):
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''
    if search_text != '':
        facts = Product.objects.filter(name__contains=search_text)
    else:
        facts = None

    return render_to_response('ajax_search.html', {'facts': facts})
