from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse 
from .models import Question, Exam, Answer
from django.utils import timezone
from datetime import timedelta 
from django.shortcuts import get_object_or_404

def signup(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        pass1 = request.POST.get('pass1')
        email = request.POST.get('email')
        pass2 = request.POST.get('pass2')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=pass1,
            first_name=full_name
        )
        user.save()

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'signup.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            print("login success:", user.username)
            request.session['entry_time']=timezone.localtime().timestamp()
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')


    return render(request, 'login.html')


@login_required(login_url='login')
def exam_page(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = Question.objects.filter(exam=exam)

    now = timezone.localtime()

    # entry window check (same for all users)
    if exam.start_time:
        entry_end = timezone.localtime(exam.start_time) + timedelta(minutes=exam.entry_window)

        if now > entry_end:
            return render(request, "entry_closed.html")
        
    if request.method == "POST":
        print("POST DATA:", request.POST)

        # पुराना answers delete (optional but better)
        Answer.objects.filter(
            user=request.user,
            exam=exam
        ).delete()

        for key, value in request.POST.items():
            if not key.startswith("q"):
                continue

            q_id = int(key[1:])
            selected = value
            try:
                question = Question.objects.get(id=q_id)

                if value == "1":
                    full_answer = question.option1

                elif value == "2":
                    full_answer = question.option2

                elif value == "3":
                    full_answer = question.option3

                elif value == "4":
                    full_answer = question.option4

                else:
                    full_answer = "Not Answered"

                Answer.objects.create(
                    user=request.user,
                    exam=exam,
                    question=question,
                    selected_option=value,
                    selected_answer=full_answer
                )

                print("Saved:", q_id, selected)

            except Question.DoesNotExist:
                print("question not found :", q_id)

        return HttpResponse("Answer Saved ")
        # return redirect('/')  # बाद में बना लेना    
        
    if 'end_time' not in request.session:

        request.session['end_time'] = (
            now + timedelta(minutes=exam.duration)
        ).isoformat()

    end_time = request.session['end_time']

    return render(request, 'exam.html', {
        'exam': exam,
        'questions': questions,
        'end_time': end_time
    })


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login') 
def index(request):
    exam = Exam.objects.first()  # ya specific exam select karo
    return render(request, 'index.html', {'exam': exam})


@login_required(login_url='login')
def instructions(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    now = timezone.localtime()

    if exam.start_time is None:
        entry_end = now + timedelta(minutes=exam.entry_window)
    else:
        entry_end = exam.start_time + timedelta(minutes=exam.entry_window)

    if now > entry_end:
        return render(request, "entry_closed.html", {
            "entry_end":entry_end
            })

    context = {
        "exam": exam,
        "entry_end": entry_end,
    }

    return render(request, "instructions.html", context)