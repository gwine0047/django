from django.shortcuts import render, redirect
from  .forms import CreateUserForm, LoginForm, AddRecordForm, UpdateRecordForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required
from .models import Record
from django.contrib import messages


# homepage
def home(request):
    return render(request, 'webapp/index.html')

# register 
def register(request):
    form = CreateUserForm()
# if data is being sent to database
    if request.method == "POST":
        form = CreateUserForm(request.POST)

    if form.is_valid():
        form.save()
        messages.success(request,"Account successfully created!")
        return redirect('login')

# collect the form in a dict and send it to register.html as 'context'
    context = {'form':form}
    return render(request, 'webapp/register.html', context=context)

def login(request):
    form  = LoginForm()

# The request object is used by the form to access session data, authentication information, and other contextual details.
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")

    context = {'form':form}
    return render(request, 'webapp/login.html', context=context)

# dashboard
@login_required(login_url='login')
def dashboard(request):

    my_records = Record.objects.all()
    context = {'records': my_records}
    return render(request, 'webapp/dashboard.html', context=context)

#  create a record
@login_required(login_url='login')
def create_record(request):
    form = AddRecordForm()

    if request.method == "POST":
        form = AddRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Record successfully created!")
            return redirect("dashboard")
        
    context = {'form':form} #passed to create_record.html as context
    return render(request, 'webapp/create-record.html', context)

# update a record
@login_required(login_url='login')
def update_record(request, pk):
    record = Record.objects.get(id=pk)

    form = UpdateRecordForm(instance=record)

    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():
            form.save()
            messages.success(request,"Record successfully updates!")
            return redirect("dashboard")
        
    context = {'form': form}
    return render(request, 'webapp/update-record.html', context=context)

# logout
def logout(request):
    auth.logout(request)
    messages.success(request,"Logout successfully!")
    return redirect("login")

# read or view a singular record
@login_required(login_url='login')
def view_record(request, pk):
    
    all_records = Record.objects.get(id=pk)

    context = {'record': all_records}
    return render(request, 'webapp/view-record.html', context =context)

# delet a record

@login_required(login_url='login')
def delete_record(request, pk):

    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request,"Record successfully deleted!")
    return redirect("dashboard")