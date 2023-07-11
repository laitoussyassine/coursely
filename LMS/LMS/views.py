from django.contrib import messages
from django.shortcuts import redirect,render,get_object_or_404
from app.models import Categories,Course,Level,Video,UserCourse,Review
from django.template.loader import render_to_string
# import json
from django.http import JsonResponse
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required

from .settings import *
import razorpay
from time import time

from django.shortcuts import render
from django.core.mail import send_mail
from app.forms import SubscriptionForm,ReviewForm


 


# client = razorpay.Client(auth=(KEY_ID,KEY_SECRET))

def BASE(request):
    return render(request,'base.html')



def HOME(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status = 'PUBLISH').order_by('-id')
    print(course)

    context = {
        'category': category,
        'course': course,
    }
    return render(request,'Main/home.html',context)

def SINGLE_COURSE(request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    FreeCourse_count = Course.objects.filter(price = 0).count()
    PaidCourse_count = Course.objects.filter(price__gte=1) .count()
    context = {
        'category':category,
        'level': level,
        'course': course,
        'FreeCourse_count': FreeCourse_count,
        'PaidCourse_count': PaidCourse_count,
    }
    return render(request,'Main/single_course.html',context)



def filter_data(request):
    category = request.GET.getlist('category[]')
    print(category)
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')

    if price == ['PriceFree']:
        course = Course.objects.filter(price=0)
    elif price == ['PricePaid']:
        course = Course.objects.filter(price__gte=1)
    elif price == ['PriceAll']:
        course = Course.objects.all()
    elif category:
        course = Course.objects.filter(category__id__in = category).order_by('id')
    elif level:
        course = Course.objects.filter(level__id__in = level).order_by('-id')
    else:
        course = Course.objects.all().order_by('id')

    context = {
        'course':course
    }

    t = render_to_string('ajax/course.html',context)
    return JsonResponse({'data': t})




def CONTACT_US(request):
    category = Categories.get_all_category(Categories)

    context = {
        'category': category
    }
    return render(request,'Main/contact_us.html',context)



def ABOUT_US(request):
    category = Categories.get_all_category(Categories)

    context = {
        'category': category
    }
    return render(request,'Main/about_us.html',context)


def SEARCH_COURSE(request):
    category = Categories.get_all_category(Categories)

    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query)
    print(course)

    context = {
        'course':course,
        'category': category
    }
    return render(request,'search/search.html',context)


@login_required
def COURSE_DETAILS(request,slug):
    category = Categories.get_all_category(Categories)
    time_duration = Video.objects.filter(course__slug = slug).aggregate(sum=Sum('time_duration'))

    course_id = Course.objects.get(slug = slug)
    try:
        check_enroll = UserCourse.objects.get(user = request.user, course = course_id)

    except UserCourse.DoesNotExist:
        check_enroll = None
    course = Course.objects.filter(slug = slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    
    context = {
        'course':course,
        'category': category,
        'time_duration': time_duration,
        'check_enroll': check_enroll,
    }
    return render(request,'course/course_details.html',context)


def PAGE_NOT_FOUND(request):
    category = Categories.get_all_category(Categories)

    context = {
        'category': category
    }
    return render(request,'error/404.html',context)


def CHECKOUT(request,slug):
    course = Course.objects.get(slug = slug)
    order = None
    if course.price == 0:
        course = UserCourse(
            user = request.user,
            course = course,

        )
        course.save()
        messages.success(request,'Course Are Successfully Enrolled !')
        return redirect('my-course')
    elif course.price != 0:
        pass

    context = {
        'course':course,
        'order':order,
    }
    return render(request,'checkout/checkout.html',context)


@login_required
def MY_COURSE(request):
    course = UserCourse.objects.filter(user = request.user)
    context = {
        'course':course,
    }
    return render(request,'course/my-course.html',context)


def VERIFY_PAYMENT(request):
    # body = json.loads(request.body)
    # print('BODY:', body)
    # return JsonResponse('Payment completed!', safe=False)
    return None

def WATCH_COURSE(request,slug):
    course = Course.objects.filter(slug = slug)
    lecture = request.GET.get('lecture')
    video = Video.objects.get(id =lecture)
    print(video)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')

    context = {
        'course': course,
        'video': video,
    }
    return render(request,'course/watch-course.html',context)








def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscriber = form.save()

            # Send confirmation email
            send_mail(
                'Cursely Confirmation Email',
                'Thank you for subscribing to our newsletter!',
                'yassinelaitouss2380@gmail.com',
                [subscriber.email],
                fail_silently=False,
            )

            messages.success(request, 'Subscribed successfully!')
            return redirect('home')  # Redirect to the home page or any other desired page
    else:
        form = SubscriptionForm()

    return render(request, 'sub/subscribe.html', {'form': form})







def add_review(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.user = request.user
            review.save()

            messages.success(request, 'Review added successfully.')
            return redirect('watch_course', slug=course.slug)
    else:
        form = ReviewForm()

    context = {
        'course': course,
        'form': form,
    }
    return render(request, 'course/course_details.html', context)

