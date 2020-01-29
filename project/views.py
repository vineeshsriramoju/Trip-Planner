from django.shortcuts import render,redirect
from django.db import connection,transaction
from .models import package
from  .forms import CreatePackage
from django.http import HttpResponse
def home(request):
    if request.method=="POST":
        print("\n\n")
        print("hellllllloooooooooooo")
        value=request.POST.get('button')
        value=value.replace('button','')
        origin=request.POST.get('origin{}'.format(value))
        destination=request.POST.get('destination{}'.format(value))
        train=request.POST.get('transport{}'.format(value))
        hotel=request.POST.get('hotel{}'.format(value))
        no_of_days=request.POST.get('no_of_days{}'.format(value))
        money=request.POST.get('money{}'.format(value))

        details=[]
        details.append(origin)
        details.append(destination)
        details.append(train)
        details.append(hotel)
        details.append(no_of_days)
        details.append(money)
        print(details)
        return render(request,'project/show_details.html',{'details':details})

    else:
    #packages123 = package.objects.all()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM project_package")
        packages123=cursor.fetchall()

        # cursor = connection.cursor()
        # cursor.execute("SELECT * FROM packages;")
        # packages=cursor.fetchall()
        print(packages123)
        l=[]
        for i in range(len(packages123)):
            n=[]
            n.append('origin'+str(i+1))
            n.append('destination'+str(i+1))
            n.append('transport'+str(i+1))
            n.append('hotel'+str(i+1))
            n.append('no_of_days'+str(i+1))
            n.append('money'+str(i+1))
            n.append('button'+str(i+1))
            l.append(n)
        total_list=zip(packages123,l)
        # transaction.commit()
        return render(request, 'project/index2.html',context={'total_list':total_list})# Create your views here.

# def package_details(request):
#     cursor = connection.cursor()
#     cursor.execute("INSERT INTO project_package(user_id,package_id,origin,destination,train,hotel,no_of_days,money) VALUES(%s,%s,%s,%s,%s,%s,%s,%s);", (userid,packageid,origin,destination,train,hotel,noofdays,money))
#     transaction.commit()


def package_create(request):

    if request.method=='POST':
        print('\n\n')
        print("entered")
        #form = CreatePackage(request.POST)

        userid = request.user.id
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        train = request.POST.get('transport')
        hotel = request.POST.get('hotel')
        noofdays = request.POST.get('no of days')
        money = request.POST.get('money')
        print("\n\n")
        print(type( money),type(noofdays))
        cursor = connection.cursor()
        cursor.execute("INSERT INTO project_package(user_id,origin,destination,train,hotel,no_of_days,money) VALUES(%s,%s,%s,%s,%s,%s,%s);", (userid,origin,destination,train,hotel,noofdays,money))
        transaction.commit()
        return redirect('package_display')

    else:
        form = CreatePackage()
        return render(request, 'project/index.html',{'form':form})
    #return redirect(package_create)
    
