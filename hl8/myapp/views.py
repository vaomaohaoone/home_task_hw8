from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from myapp.forms import CreateForm, EditForm, CreateRoadMap, AnotherCreateForm, CreateUser, LoginForm, EditUser, \
    EditPassword
from django.views.decorators.csrf import csrf_exempt
from .models import Task, RoadMap, Scores, User
from django.db import transaction
import datetime
from django.contrib.auth import login, logout
from django.contrib.messages import error
from django.core.mail import EmailMessage



@csrf_exempt
def show_tasks(request):
    tasks = Task.objects.all()
    ctx = {'titles': tasks}
    return render_to_response('tasks.html', ctx)


@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        instance = get_object_or_404(RoadMap, rd_id=request.POST.get('road_map'))
        a = Task(title=request.POST.get('title'),
                 estimate=request.POST.get('estimate'),
                 road_map=instance)
        a.save()
        return HttpResponseRedirect('/tasks/')
    form = CreateForm()
    return render_to_response('form1.html', {'form': form})


@csrf_exempt
def edit_task(request, context, context1, context2):
    instance = get_object_or_404(Task, my_id=context)
    if request.method == 'POST':
        form = EditForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            my_url = '/' + 'roadmap' + '/' + context1 + '/' + context2
            return HttpResponseRedirect(my_url)
    else:
        form = EditForm(instance=instance)
    return render_to_response('form2.html', {'form': form})


@csrf_exempt
def delete_task(request, context, context1, context2):
    get_object_or_404(Task, my_id=context).delete()
    my_url = '/roadmap/' + context1 + '/' + context2
    return HttpResponseRedirect(my_url)


@csrf_exempt
def start(request, context):
    return render_to_response('start_session.html', {'context': context})


@csrf_exempt
def start_page(request):
    return render_to_response('start_page.html')


@csrf_exempt
def create_roadmap(request, context):
    if request.method == 'POST':
        a = RoadMap(rd_id=request.POST.get('rd_id'), name=request.POST.get('name'), us_id=str(context))
        a.save()
        my_url = '/start/' + context
        return HttpResponseRedirect(my_url)
    form = CreateRoadMap()
    return render_to_response('create_roadmap.html', {'form': form, 'context': context})


@csrf_exempt
def delete_roadmap(request, context, context1):
    get_object_or_404(RoadMap, rd_id=context).delete()
    return start(request, context1)


@csrf_exempt
def roadmaps(request, context):
    roads = RoadMap.objects.filter(us_id=context)
    ctx = {'roads': roads, 'context': context}
    return render_to_response('roadmaps.html', ctx)


@csrf_exempt
def roadmap(request, context, context1):
    tasks = Task.objects.filter(road_map=context)
    ctx = {'titles': tasks, 'context': context, 'context1': context1}
    return render_to_response('tasks_in_roadmap.html', ctx)


@csrf_exempt
def add_to_roadmap(request, context, context1):
    if request.method == 'POST':
        a = Task(title=request.POST.get('title'),
                 estimate=request.POST.get('estimate'),
                 road_map_id=str(context)
                 )
        a.save()
        return roadmap(request, context, context1)
    form = AnotherCreateForm()
    return render_to_response('form1.html', {'form': form, 'context': context})


@csrf_exempt
@transaction.atomic(savepoint=False)
def created_and_solved(request, context):
    tasks = Task.objects.filter(road_map=context)
    created = {}
    solved = {}
    for day in tasks:
        key = day.create_date.isocalendar()[1]
        if key not in created:
            list = []
            list.append(day.create_date)
            created[key] = []
            created[key].append(list)
            if day.state == 'ready':
                zn = 1
                sp = [zn]
                solved[key] = []
                solved[key].append(sp)
            else:
                zn = 0
                sp = [zn]
                solved[key] = []
                solved[key].append(sp)
        else:
            flag = False
            for i in range(len(created[key])):
                if day.create_date.isocalendar()[0] == created[key][i][0].isocalendar()[0]:
                    created[key][i].append(day.create_date)
                    flag = True
                    break
            if flag == True:
                if day.state == 'ready':
                    solved[key][i][0] = solved[key][i][0] + 1
                continue
            list = []
            list.append(day.create_date)
            created[key] = []
            created[key].append(list)
            if day.state == 'ready':
                zn = 1
                sp = [zn]
                solved[key] = []
                solved[key].append(sp)
            else:
                zn = 0
                sp = [zn]
                solved[key] = []
                solved[key].append(sp)
    my_dict = {}
    for key in created:
        spis = []
        for ind in range(len(created[key])):
            spis.append(first_and_last_day_in_week(created[key][ind][0]))
        my_dict[key] = spis
    created_end = {}
    for key in created:
        spis = []
        for ind in range(len(created[key])):
            spis.append(len(created[key][ind]))
        created_end[key] = spis
    for key in solved:
        spis = []
        for ind in range(len(solved[key])):
            spis.append(solved[key][ind][0])
        solved[key] = spis
    ctx = {'ctx': get_table(my_dict, created_end, solved)}
    return render_to_response('Stat1.html', ctx)


@csrf_exempt
@transaction.atomic(savepoint=False)
def points(request, context):
    tasks = Task.objects.filter(road_map=context)
    diff = calculate_max_estimate(tasks)
    for values in tasks:
        a = Scores(task_id=values.my_id, points=calculate_points(values, diff))
        a.save()
    point = Scores.objects.all()
    res = {}
    for key in point:
        year = key.date.strftime("%Y")
        month = key.date.strftime("%m")
        string = year + "-" + month
        if string not in res:
            res[string] = key.points
        else:
            res[string] = res[string] + key.points
    Scores.objects.all().delete()
    return render_to_response('points.html', {"res": res})


@csrf_exempt
def create_use(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            email=request.POST.get('email'),
            password=request.POST.get('password'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            phone=request.POST.get('phone'),
            age=request.POST.get('age'),
            region=request.POST.get('region')
        )
        return HttpResponseRedirect('/start_page/')
    form = CreateUser()
    return render_to_response('create_user.html', {'form': form})


@csrf_exempt
def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.authenticate_user()
            if not user:
                error(request, 'Wrong credentials!')
                return render_to_response('login.html')
            login(request, user)
            context = user.id
            return start(request, context)
    return render_to_response('login.html', {'form': form})


@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return HttpResponseRedirect('/start_page/')


@csrf_exempt
def edit_profile(request, context):
    instance = get_object_or_404(User, id=context)
    if request.method == 'POST':
        form = EditUser(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            my_url = '/start/' + context + '/'
            return HttpResponseRedirect(my_url)
    else:
        form = EditUser(instance=instance)
    return render_to_response('form3.html', {'form': form})


@csrf_exempt
def get_profile(request, context):
    user = User.objects.filter(id=context)
    return render_to_response('profile.html', {'first_name': user[0].first_name, 'last_name': user[0].last_name,
                                               'age': user[0].age, 'region': user[0].region,
                                               'phone': user[0].phone, 'context': context})


@csrf_exempt
def change_password(request, context):
    instance = get_object_or_404(User, id=context)
    if request.method == 'POST':
        form = EditPassword(request.POST)
        if form.is_valid():
            if request.POST.get('new_password') == request.POST.get('confirm_password'):
                message = "Пожалуйста, перейдите по ссылке для подтверждения пароля " + "http://127.0.0.1:8000/success/" + context + '/'
                mailto = instance.email
                email = EmailMessage('ChangePassword', message, to=[mailto])
                email.send()
                my_url = "/was_sent/" + context + "/"
                instance.tmp_password = request.POST.get('new_password')
                instance.flag_for_change = True
                instance.save()
                return HttpResponseRedirect(my_url)

    form = EditPassword()
    return render_to_response('form4.html', {'form': form})


@csrf_exempt
def was_sent(request, context):
    return render_to_response('mail_was_sent.html')


@csrf_exempt
def success(request, context):
    instance = get_object_or_404(User, id=context)
    instance.flag_for_change = False
    instance.set_password(instance.tmp_password)
    instance.tmp_password = ''
    instance.save()
    return render_to_response('success.html')


def calculate_points(self, max_estimate):
    if self.state == "ready":
        points = ((datetime.date.today() - self.create_date) / (self.estimate - self.create_date)) + (
            (self.estimate - self.create_date) / max_estimate)
        return points
    else:
        return 0


def get_table(my_dict, created_end, solved):
    result = {}
    for key in my_dict:
        list = []
        for ind in range(len(my_dict[key])):
            list.append(my_dict[key][ind])
            list.append(created_end[key][ind])
            list.append(solved[key][ind])
        result[key] = list
    return result


def first_and_last_day_in_week(value):
    monday = value - datetime.timedelta(datetime.datetime.weekday(value))
    sunday = value + datetime.timedelta(6 - datetime.datetime.weekday(value))
    sunday = sunday.strftime("%Y-%m-%d")
    monday = monday.strftime("%Y-%m-%d")
    a = monday + "-" + sunday
    return a


def calculate_max_estimate(tmp):
    maximum = datetime.date.today() - datetime.date.today()
    for x in tmp:
        value = x.estimate - x.create_date
        if value > maximum:
            maximum = value
    return maximum
