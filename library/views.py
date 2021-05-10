from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import User,Collection

# Create your views here.

def index(request):
    return render(request,"base.html")  # Shows the homepage

def user_login(request):
    if request.user.is_authenticated:   # checking if user is already autheticated then go to direct homepage not login page on clicking on back button
        return redirect("index")
    else:
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['pass']

            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("user_profile")
            else:
                messages.error(request, "Invalid credentials!")
                return redirect("login")

        return render(request,"login.html")

def register(request):
    if request.method == "POST":
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        address = request.POST['address']
        email = request.POST['email']
        password = request.POST['pass']

        user = User.objects.create_user(first_name=first_name, last_name=last_name, address=address,email=email, password=password)
        user.save()
        return redirect("login")
    else:
        return render(request, "register.html")

def user_logout(request):
    logout(request)
    return redirect("/")

@login_required
def user_profile(request):
    current = request.user      # It checks the current loggined user.
    if request.user.is_authenticated:   # checks the user visited is authenticated or not.
        if request.method == "POST":
            title = request.POST['title']
            author = request.POST['author']
            genre = request.POST['sel1']
            type = request.POST['sel2']
            review_rating = request.POST['sel3']
            review = request.POST['review']
            favourite = request.POST['sel4']

            collect = Collection(title=title,author=author,genre=genre,type=type,review_rating=review_rating,review=review,favourite=favourite,user=current)
            collect.save()
            messages.success(request, "Book has been added!")

            collect = Collection.objects.filter(user=current.id)  # It will show data of Collection to dashboard.
            return render(request, "user_profile.html", {'data': collect})
        else:
            if request.user.is_admin == True:       # Checks whether authenticated user is admin or not.
                return redirect("admin_panel")
            else:
                collect = Collection.objects.filter(user=current.id)    # If not then show data accordingly to user.
                return render(request, "user_profile.html", {'data': collect})
    else:
        return redirect("user_login")

@login_required
def admin_panel(request):
    users = User.objects.all()
    return render(request,"admin.html",{'data':users})

@login_required
def user_details(request,id):
    if request.user.is_authenticated:
        p_id= Collection.objects.filter(user=id)
        return render(request, "user_profile.html",{'data': p_id})
    else:
        return redirect("user_login")

@login_required
def update_data(request,us_id,id):
    user_id = User.objects.get(id=us_id)
    col_id = Collection.objects.get(id=id)
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        genre = request.POST['sel1']
        type = request.POST['sel2']
        review_rating = request.POST['sel3']
        review = request.POST['review']
        favourite = request.POST['sel4']
        collect = Collection(id=id,title=title, author=author, genre=genre, type=type, review_rating=review_rating,
                             review=review, favourite=favourite,user=user_id)
        collect.save()
        messages.success(request, "Book data has been Updated!")
        return redirect("user_profile")
    return render(request, "update.html",{'data':col_id})

@login_required
def delete_data(request,id):
    if request.method == "POST":
        user_id = Collection.objects.get(pk=id)
        user_id.delete()
    return redirect("user_profile")