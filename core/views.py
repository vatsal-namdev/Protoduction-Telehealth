from django.shortcuts import render, redirect, get_object_or_404
from .models import post, comment, query, doctor, ConsultationRequest, Plan, Subscription, Room, Message
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.views import View
from .forms import PostForm
from razorpay import Client
from django.conf import settings
import requests, uuid
import socket
from .decorators import subscription_required

# Create your views here.
def index(request):
    return render(request, 'index.html')


def register(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Exist')
                return redirect('register')

            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Exist')
                return redirect('register')  

            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save();
                return redirect('login')   

        else:
            messages.info(request, 'Password not Same')
            return redirect('register')  

    else:             
        return render(request,'register.html')    


def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials are Invalid')
            return redirect('login')  

    else:          
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('/')

def blog(request):
    bpost = post.objects.all()
    return render(request, 'blog.html',{'bpost':bpost})

def posts(request, slug):
    bpost = post.objects.get(slug=slug)
    # comment = Comment.objects.filter(post=bpost)
    return render(request, 'post.html',{'bpost':bpost})

def save(request):
    if request.method == 'POST':
        user = request.user.username
        post_img = request.FILES.get('image_upload')
        title = request.POST['title']
        body = request.POST['body']

        new_post = post.objects.create(user=user,post_img=post_img,title=title,body=body)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')
    
@login_required
@subscription_required
def pquery(request):
    pq = query.objects.all()
    return render(request,'pquery.html',{'queries':pq})

class AddQueryView(CreateView):
    model = query
    form_class = PostForm
    # fields = ['name','body']
    template_name = 'add_query.html'

def psave(request):
    return render(request, 'psave.html')

def csave(request):
    username = request.POST['username']
    queryn = request.POST['queryn']
    body = request.POST['body']

    new_comment = comment.objects.create(body=body,user=username,queryn=queryn,name=username)
    new_comment.save()
    return redirect(request.META['HTTP_REFERER'])

def LikeView(request, pk):
    p = get_object_or_404(query, id=request.POST.get('queries_id'))
    
    liked = False
    if p.likes.filter(id=request.user.id).exists():
        p.likes.remove(request.user)
        liked = False
    else:
        p.likes.add(request.user)
        liked =True
    return HttpResponseRedirect(reverse('pcomment', args=[str(pk)]))

def pcomment(request, pk):
    username = request.user.username
    pb = query.objects.get(id=pk)
    com = comment.objects.filter(queryn=pk)
    stuff = get_object_or_404(query, id= pk)
    likes_count = stuff.total_likes()

    liked = False
    if stuff.likes.filter(id=request.user.id).exists():
        liked = True
    return render(request, 'comment.html',{'queries':pb,'com':com,'queryn':pk,'username':username,'likes_count':likes_count,'liked':liked})

@login_required(login_url='login')
def knowscore(request):
    return render(request, "knowscore.html")

def score_result(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        date_of_birth = request.POST.get('dob')
        phone_number = request.POST.get('phone')
        specialty = request.POST.get('specialty')
        reason_for_consultation = request.POST.get('reason')

        # Create a new ConsultationRequest object with form data
        consultation = ConsultationRequest.objects.create(
            full_name=full_name,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
            specialty=specialty,
            reason_for_consultation=reason_for_consultation,
        )

        requested_specialty = request.POST.get('specialty')

        if requested_specialty != 'other':
            dd = doctor.objects.filter(specialty=requested_specialty)
        else:
            dd = doctor.objects.all()

        # Handle successful form submission (e.g., confirmation message)
        return render(request, 'scoreresult.html', {'dd':dd})
    else:
        # Render the form for consultation request
        return render(request, 'knowscore.html')

@subscription_required
def diet(request):
    return render(request, "Diet.html")

def dietres(request):
    if  request.method == "POST":
        qr = request.POST['query']
        api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
        query = qr
        response = requests.get(api_url + query, headers={'X-Api-Key': '26FIamwdHuBsY8jrYmJbYA==ucOuylZIrx7jlSfZ'})
        if response.status_code == requests.codes.ok:
            res_dict = dict(json.loads(response.text))
            res = res_dict['items'][0]

            if res['calories'] < 2100:
                wrn = "You have to consume " + str(2500-int(res['calories'])) + " more calories today."

            elif res['calories']>=2100 and res['calories'] <= 2400:
                wrn = "Perfectly balanced diet for a day!"
            else:
                wrn = "You have to consume " + str(int(res['calories'])-2450) + " less calories."


            
        # else:
        #     print("Error:", response.status_code, response.text)
        return render(request, "Dietres.html", {'res':res, 'wrn':wrn})
    
def doctors(request):
    dd = doctor.objects.all()
    return render(request, "doct.html", {'dd':dd})

def dprofile(request, slug):
    doc = doctor.objects.get(slug=slug)
    return render(request, "dprofile.html", {'doc':doc})

@subscription_required
def gencode(request):
    import random
    num = random.randint(111111111,999999999)
    host = socket.gethostbyname(socket.gethostname())
    return render(request, "meetjoin.html", {"code": num, "host":host})

@subscription_required
def genroom(request):
    import random
    room = random.randint(111111111,999999999)
    username = request.POST['username']
    room = str(room)+username
    new_room = Room.objects.create(name=room)
    new_room.save()
    return redirect('/'+room+'/?username='+username)

def videocall(request):
    return render(request, 'videocall.html')

@login_required
def subscription(request, plan_id):
    plan = Plan.objects.get(pk=plan_id)
    return render(request, "buysubscription.html", {'plan':plan})

@subscription_required
def premium(request):
    return render(request, "premium.html")

def plan(request):
    planlist = Plan.objects.all()
    return render(request, "plans.html", {'plans':planlist})

import logging
logger = logging.getLogger(__name__)
import razorpay, json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

RAZORPAY_KEY_ID = settings.RAZORPAY_KEY_ID
RAZORPAY_SECRET = settings.RAZORPAY_SECRET

@csrf_exempt
def payment_process(request):
    if request.method == 'POST':
        try:
            plan_id = request.POST.get('plan_id')
            logger.debug(f'Received plan_id: {plan_id}')
            
            plan = get_object_or_404(Plan, pk=plan_id)
            logger.debug(f'Fetched plan: {plan}')
            
            # Prepare payment details (amount, currency)
            amount = int(plan.price * 100)  # Convert price to paise
            logger.debug(f'Calculated amount: {amount}')
            
            # Initialize Razorpay client
            client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET))
            logger.debug('Initialized Razorpay client')
            
            # Create Razorpay order
            order = client.order.create(dict(
                amount=amount,
                currency='INR',
                payment_capture='1',  # Capture payment immediately
            ))
            logger.debug(f'Created Razorpay order: {order}')
            
            # Prepare response data
            response_data = {
                'order_id': order['id'],
                'key_id': RAZORPAY_KEY_ID,
                'amount': amount,
                'name': plan.name,
                'prefill': {
                    'name': request.user.username,  # Replace with user's name (optional)
                    'email': request.user.email,  # Replace with user's email (optional)
                }
            }
            logger.debug(f'Response data prepared: {response_data}')
            
            return JsonResponse(response_data)
        except Exception as e:
            logger.error(f'Error processing payment: {e}', exc_info=True)
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
@csrf_exempt
def create_subscription(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            plan_id = data.get('plan_id')
            payment_id = data.get('payment_id')
            order_id = data.get('order_id')
            signature = data.get('signature')
            
            plan = get_object_or_404(Plan, pk=plan_id)

            # Verify payment signature here (optional but recommended)
            client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_SECRET))
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            try:
                client.utility.verify_payment_signature(params_dict)
            except razorpay.errors.SignatureVerificationError:
                return JsonResponse({'error': 'Invalid payment signature'})

            # Create the subscription
            subscription = Subscription.objects.create(
                user=request.user,
                plan=plan,
                start_date=timezone.now(),
                is_active=True,
            )
            return JsonResponse({'success': True})
        except Exception as e:
            logger.error(f'Error creating subscription: {e}', exc_info=True)
            return JsonResponse({'error': str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    


@login_required
def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html',{
        'username':username,
        'room':room,
        'room_details':room_details
    })


def send(request):
    username = request.POST['username']
    room_id = request.POST['room_id']
    message = request.POST['message']

    new_message = Message.objects.create(value=message,user=username,room=room_id)
    new_message.save()
    return HttpResponse("Message Sent Succesfully")

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})