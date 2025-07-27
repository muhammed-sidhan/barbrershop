from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from .forms import BarberSignUpForm,CustomerSignUpForm
from django.contrib.auth.decorators import login_required
from .models import QueueEntry,BarberProfile,CustomerProfile,BlockedCustomer
#index
def index(request):
    if request.user.is_authenticated:
        return redirect('role_based_home') 
    return render(request,'index.html')


@login_required
def role_based_home(request):
    if request.user.role == 'barber':
        return redirect('barber_dashboard')
    elif request.user.role == 'customer':
        return redirect('customer_dashboard')
    else:
        return redirect('login')

# Views-AUTH
def barber_register(request):
    if request.method == 'POST':
        form=BarberSignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user) #log in the new barber
            return redirect("barber_dashboard")
    else:
        form=BarberSignUpForm()
    return render (request,'registration/barber_registration.html',{'form':form})
def customer_register(request):
    if request.method == 'POST':
        form=CustomerSignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user) # login new customer
            return redirect("customer_dashboard")
    else:
        form=CustomerSignUpForm()
    return render (request,'registration/customer_registration.html',{'form':form})
    
# Dashboard
@login_required
def barber_dashboard(request):
    if request.user.role != 'barber':
        return redirect ('customer_dashboard')
    barber_profile , created=BarberProfile.objects.get_or_create(user=request.user)
    # Get all active queue entries for this barber
    queue = QueueEntry.objects.filter(barber=barber_profile, is_active=True).order_by('joined_at')
    return render (request,'dashboard/barber_dashboard.html',{'queue':queue,'barber_profile':barber_profile},)
@login_required
def customer_dashboard (request):
    if request.user.role != 'customer':
        return redirect ('barber_dashboard')
    
    
    customer_profile=request.user.customerprofile
    active_entry=QueueEntry.objects.filter(customer=customer_profile,is_active=True).order_by(
        'joined_at').first()
    return render (request,'dashboard/customer_dashboard.html',{'active_entry':active_entry})

#views to list barber

def customer_barber_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.role != 'customer':
        return redirect ('barber_dashboard')
    barbers=BarberProfile.objects.filter(is_open=True)
    if not barbers:
        messages.info(request,"No barbers currently available")
    return render (request,'queue/barber_list.html',{'barbers':barbers})
#views queue
@login_required
def join_queue(request,barber_id):
    if request.user.role!='customer':
        return redirect('barber_dashboard')
    barber=get_object_or_404(BarberProfile,id=barber_id)
    customer=request.user.customerprofile
    #check if this customer is blocked by this barber
    blocked= BlockedCustomer.objects.filter(
        barber=barber,
        customer=customer
    ).exists()
     #if blocked, redirect to customer dashboard with error message
    if blocked:
        messages.error(request, "You are blocked from joining this barber's queue.")
        return redirect('customer_dashboard')  
    #check if already queued for this barber
    existing=QueueEntry.objects.filter(customer=customer,barber=barber,is_active=True)
    #already in the queue
    if existing.exists():
        messages.warning(request,"you're already in this barber's queue")
        return redirect ('customer_dashboard')
    #create new enrty queue
    QueueEntry.objects.create(customer=customer,barber=barber)
    messages.success(request,f"you're joined queue at {barber.shop_name}")
    return redirect('customer_dashboard')
#view to block customer
@login_required
def block_customer(request,customer_id):

    if request.user.role != 'barber':
        return redirect('role_based_home')
    entry=get_object_or_404(QueueEntry,id=customer_id)
    barber= request.user.barberprofile
    customer=entry.customer
    # Check if this customer is already blocked
    if BlockedCustomer.objects.filter(barber=barber, customer=customer).exists():
        messages.error(request, "This customer is already blocked.")
        return redirect('barber_queue')
    # Create a new BlockedCustomer entry
    else:
        BlockedCustomer.objects.create(barber=barber,customer=customer)
        entry.is_active = False  # Mark the queue entry as inactive
        entry.save()
        messages.success(request, f"{customer.user.username} has been blocked.")
        return redirect('barber_queue')
    
@login_required
def unblock_customer(request,customer_id):
    if request.user.role != 'barber':
        return redirect('role_based_home')
    barber=request.user.barberprofile
    customer=get_object_or_404(CustomerProfile,id=customer_id)
    # Check if this customer is blocked
    blocked_customer=BlockedCustomer.objects.filter(barber=barber,customer=customer).first()
    if blocked_customer:
        blocked_customer.delete()
        messages.success(request, f"{customer.user.username} has been unblocked.")
    else:
        messages.error(request, "This customer is not blocked.")
    return redirect('blocked_customers')
@login_required
def blocked_customers(request):
    if request.user.role != 'barber':
        return redirect('role_based_home')
    barber=request.user.barberprofile
    blocked_customers=BlockedCustomer.objects.filter(barber=barber,)
    return render(request,'queue/blocked_customers.html',{'blocked_customers':blocked_customers})
@login_required 
def barber_queue(request):
    if request.user.role != 'barber':
        return redirect ('customer_dashboard')
    barber_profile=request.user.barberprofile

    queue_entries=QueueEntry.objects.filter(
        barber=barber_profile,
        is_active=True
        ).order_by('joined_at')
    return render(request,'queue/barber_queue.html',{'queue_entries':queue_entries})

@login_required
def mark_served(request,entry_id):
    if request.user.role != 'barber':
        return redirect('customer_dashboard')
    entry=get_object_or_404(QueueEntry,id=entry_id)
    #Checking this entry belongs to this barber
    if entry.barber != request.user.barberprofile:
        return  redirect('barber_queue')
    entry.is_active=False
    messages.success(request,f"{ entry.customer} Marked as served")
    entry.save()
    return redirect('barber_queue')

@login_required
def leave_queue(request,entry_id):
    if request.user.role != 'customer':
        return redirect ('barber_dashboard')
    entry=get_object_or_404(QueueEntry,id=entry_id)
    if entry.customer != request.user.customerprofile :
        return redirect ('customer_dashboard')
    entry.is_active=False
    entry.save()
    return redirect('customer_dashboard')
