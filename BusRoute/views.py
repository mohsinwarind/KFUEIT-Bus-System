from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from .models import *
from .forms import MissingComplaintForm,DriverReviewForm
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

# Create your views here.

def index(request):
    bus_routes = BusRoute.objects.all()[:3]
    drivers = BusDriver.objects.all()[:3]

    return render(request, "BusRoute/index.html",{
        'bus_routes':bus_routes,
        'drivers' : drivers
    })

def login_view(request):
    if request.method == "POST":

        
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "BusRoute/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "BusRoute/login.html")
    
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "BusRoute/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "BusRoute/register.html")
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def bus_route_form_view(request):
    if request.method == 'POST':
        bus_route_id = request.POST.get('bus_route')
        new_route_name = request.POST.get('new_route_name')

        try:
            if bus_route_id == 'new' and new_route_name:
                if BusRoute.objects.filter(name=new_route_name).exists():
                    return render(request, 'BusRoute/bus_route_form.html', {
                        'error_message': 'A route with this name already exists.',
                        'bus_routes': BusRoute.objects.all()
                    })
                bus_route = BusRoute.objects.create(name=new_route_name)
            else:
                bus_route = BusRoute.objects.get(id=bus_route_id)

            pickup_data = {}
            i = 0
            while True:
                name = request.POST.get(f'pickup[{i}][name]')
                if name is None:
                    break
                times = [request.POST.get(f'pickup[{i}][time][{j}]') for j in range(10) if request.POST.get(f'pickup[{i}][time][{j}]')]
                pickup_data[i] = {'name': name, 'times': times}
                i += 1

            for index, data in pickup_data.items():
                stop_point, _ = StopPoint.objects.get_or_create(name=data['name'])
                for time in data['times']:
                    PickupPoint.objects.create(
                        bus_route=bus_route,
                        stop_point=stop_point,
                        time=time
                    )

            drop_data = {}
            i = 0
            while True:
                name = request.POST.get(f'drop[{i}][name]')
                if name is None:
                    break
                times = [request.POST.get(f'drop[{i}][time][{j}]') for j in range(10) if request.POST.get(f'drop[{i}][time][{j}]')]
                drop_data[i] = {'name': name, 'times': times}
                i += 1

            for index, data in drop_data.items():
                stop_point, _ = StopPoint.objects.get_or_create(name=data['name'])
                for time in data['times']:
                    DropPoint.objects.create(
                        bus_route=bus_route,
                        stop_point=stop_point,
                        time=time
                    )

            return redirect('bus_route_detail', bus_route_id=bus_route.id)

        except IntegrityError as e:
            print(f"Error: {e}")
            return render(request, 'BusRoute/bus_route_form.html', {
                'error_message': 'An error occurred while saving the route.',
                'bus_routes': BusRoute.objects.all()
            })

    bus_routes = BusRoute.objects.all()
    return render(request, 'BusRoute/bus_route_form.html', {'bus_routes': bus_routes})


def bus_route_detail_view(request, bus_route_id):
    bus_route = get_object_or_404(BusRoute, id=bus_route_id)

    pickup_points = {}
    max_pickup_times = 0
    for pickup in PickupPoint.objects.filter(bus_route=bus_route):
        stop_name = pickup.stop_point.name
        if stop_name not in pickup_points:
            pickup_points[stop_name] = []
        pickup_points[stop_name].append(pickup.time)
        max_pickup_times = max(max_pickup_times, len(pickup_points[stop_name]))

    drop_points = {}
    max_drop_times = 0
    for drop in DropPoint.objects.filter(bus_route=bus_route):
        stop_name = drop.stop_point.name
        if stop_name not in drop_points:
            drop_points[stop_name] = []
        drop_points[stop_name].append(drop.time)
        max_drop_times = max(max_drop_times, len(drop_points[stop_name]))

    pickup_time_range = range(max_pickup_times)
    drop_time_range = range(max_drop_times)

    context = {
        'bus_route': bus_route,
        'pickup_points': pickup_points.items(),  
        'drop_points': drop_points.items(),      
        'max_pickup_times': max_pickup_times,
        'max_drop_times': max_drop_times,
        'pickup_time_range': pickup_time_range,
        'drop_time_range': drop_time_range,
    }
    

    return render(request, 'BusRoute/bus_route_detail.html', context)


def update_route(request):
    if request.method == 'POST':
        route_id = request.POST.get('id')
        title = request.POST.get('title')
        pickup_data = json.loads(request.POST.get('pickup_data', '[]'))
        drop_data = json.loads(request.POST.get('drop_data', '[]'))

        

        try:
            bus_route = get_object_or_404(BusRoute, id=route_id)
            
            if title:
                bus_route.name = title
                bus_route.save()
                

            PickupPoint.objects.filter(bus_route=bus_route).delete()
            DropPoint.objects.filter(bus_route=bus_route).delete()
            

           
            for pickup in pickup_data:
                stop_point, _ = StopPoint.objects.get_or_create(name=pickup['name'])
                
                for time in pickup['times']:
                    PickupPoint.objects.create(bus_route=bus_route, stop_point=stop_point, time=time)
                    

            
            for drop in drop_data:
                stop_point, _ = StopPoint.objects.get_or_create(name=drop['name'])
                
                for time in drop['times']:
                    DropPoint.objects.create(bus_route=bus_route, stop_point=stop_point, time=time)
                    

            return JsonResponse({'message': 'Route updated successfully'})
        except BusRoute.DoesNotExist:
            print("BusRoute not found")
            return JsonResponse({'error': 'Bus route not found'}, status=404)
        except Exception as e:
            print('Error: ', str(e))
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def delete_bus_route(request,bus_route_id):
    if request.method == "POST":
        bus_route = get_object_or_404(BusRoute,id=bus_route_id)
        bus_route.delete()
        messages.success(request, "Bus Route deleted Successfully")
        return redirect('index')
    return redirect('bus_route_detail',bus_route_id=bus_route_id)

@login_required
def report_and_view_missing_items(request):
    form = MissingComplaintForm()
    
    if request.method == 'POST':
        form = MissingComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user
            complaint.save()

            response_data = {
                'id': complaint.id,
                'item_name': complaint.item_name,
                'description': complaint.description,
                'location': complaint.location,
                'date_lost': complaint.date_lost.strftime('%Y-%m-%d'),
                'status': complaint.status,
                'date_reported': complaint.date_reported.strftime('%Y-%m-%d %H:%M:%S'),
                'image_url': complaint.image.url if complaint.image else '',
                'contact_email': complaint.contact_email,
                'contact_phone': complaint.contact_phone,
            }
            return JsonResponse(response_data)
        else:
            print("Form errors: ", form.errors)
    
    complaints = MissingComplaint.objects.filter(student=request.user).order_by('-date_reported')
    
    return render(request, 'BusRoute/report_and_view_missing_items.html', {
        'form': form,
        'complaints': complaints,
    })


@login_required
def edit_missing_item(request, pk):
    complaint = get_object_or_404(MissingComplaint, pk=pk, student=request.user)

    if request.method == 'POST':
        form = MissingComplaintForm(request.POST, request.FILES, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('report_and_view_missing_items')
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    form = MissingComplaintForm(instance=complaint)
    return render(request, 'BusRoute/edit_missing_item.html', {'form': form, 'complaint': complaint})

@login_required
def delete_missing_item(request, pk):
    complaint = get_object_or_404(MissingComplaint, pk=pk, student=request.user)

    if request.method == 'POST':
        complaint.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def update_missing_item_status(request, pk):
    complaint = get_object_or_404(MissingComplaint, pk=pk, student=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            complaint.status = new_status
            complaint.save()
            return JsonResponse({'success': True, 'status': complaint.status})
    return JsonResponse({'success': False, 'error': 'Invalid status update'})


def driver_profile(request, pk):
    driver = get_object_or_404(BusDriver, pk=pk)
    reviews = DriverReview.objects.filter(driver=driver)
    form = DriverReviewForm()

    if request.method == 'POST':
        form = DriverReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.driver = driver
            review.student = request.user
            review.save()
            # Update driver rating
            average_rating = DriverReview.objects.filter(driver=driver).aggregate(Avg('rating'))['rating__avg']
            driver.rating = average_rating
            driver.save()
            return redirect('driver_profile', pk=driver.pk)
    
    return render(request, 'BusRoute/driver_profile.html', {
        'driver': driver,
        'reviews': reviews,
        'form': form,
        'star_range': range(1, 6), 
    })


def all_routes(request):
    bus_routes= BusRoute.objects.all()
    return render(request,"BusRoute/all_routes.html",{
        'bus_routes':bus_routes
    })

def all_missing_complaints(request):
    complaints = MissingComplaint.objects.all()
    return render(request,"BusRoute/all_missing_complaints.html",{
        'complaints':complaints
    })


def all_drivers(request):
    drivers = BusDriver.objects.all()
    return render(request,"BusRoute/drivers.html",{
        "drivers":drivers
    })



def bus_tracker_view(request):
    return render(request, "BusRoute/bus_tracker.html")