from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from courseapp.models import Course
from userapp.models import UserProfile
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']  
            user.save()  
            login(request, user)
            return redirect('index')  
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard_redirect(request):
    """Redirect user to the dashboard based on their role."""
    profile = UserProfile.objects.get(user=request.user)
    if profile.role == 'student':
        return redirect('student_dashboard')
    elif profile.role == 'instructor':
        return redirect('instructor_dashboard')
    elif profile.role == 'admin':
        return redirect('admin_dashboard')
    return redirect('index') 

@login_required
@login_required
def student_dashboard(request):
    last_accessed_course_id = request.session.get('last_accessed_course')
    if last_accessed_course_id:
        last_accessed_course = Course.objects.get(id=last_accessed_course_id)
    else:
        last_accessed_course = None  
 
    user_profile = request.user.userprofile   
    available_courses = Course.objects.exclude(enrolled_students=request.user)
    enrolled_courses = Course.objects.filter(enrolled_students=request.user)
    enrolled_course_ids = set(course.id for course in enrolled_courses)  
    return render(request, 'student_dashboard.html', {
        'available_courses': available_courses,
        'enrolled_courses': enrolled_courses,
        'enrolled_course_ids': enrolled_course_ids,
        'last_accessed_course': last_accessed_course

    })

@login_required
def instructor_dashboard(request):
    return render(request, 'instructor_dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def user_logout(request):
    logout(request)
    return redirect('index')



def index(request):
    return render(request, 'index.html')
