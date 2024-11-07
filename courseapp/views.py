from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Course
from .forms import CourseForm
from django.contrib.auth import get_user_model

def is_instructor_or_admin(user):
    return user.userprofile.role in ['instructor', 'admin']

@login_required
@user_passes_test(is_instructor_or_admin)
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            
            # If the user is an instructor, assign them as the instructor automatically
            if request.user.userprofile.role == 'instructor':
                course.instructor = request.user
            else:
                # If admin, get the selected instructor from the form
                instructor_id = request.POST.get('instructor')
                course.instructor = User.objects.get(id=instructor_id)

            course.save()
            return redirect('admin_dashboard')
    else:
        form = CourseForm()

        # If the user is an admin, add instructors to the form context
        if request.user.userprofile.role == 'admin':
            instructors = User.objects.filter(userprofile__role='instructor')
        else:
            instructors = None

    return render(request, 'course_form.html', {'form': form, 'instructors': instructors})

@login_required
@user_passes_test(is_instructor_or_admin)
def course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'course_form.html', {'form': form})

@login_required
@user_passes_test(is_instructor_or_admin)
def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect('course_list')

@login_required
def course_list(request):
    courses = Course.objects.filter(instructor=request.user)
    last_accessed_course_id = request.session.get('last_accessed_course')
    last_accessed_course = None
    if last_accessed_course_id:
        last_accessed_course = Course.objects.filter(id=last_accessed_course_id).first()

    return render(request, 'course_list.html', {
        'courses': courses,
        'last_accessed_course': last_accessed_course
    })

@login_required
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.userprofile.role == 'student':
        course.enrolled_students.add(request.user)
        course.save()
    return redirect('student_dashboard')

def admin_dashboard(request):
    users = User.objects.all() 
    courses = Course.objects.all()  
    return render(request, 'admin_dashboard.html', {'users': users, 'courses': courses})

User = get_user_model()
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user_edit.html', {'user': user})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_dashboard')

@login_required
def view_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    request.session['last_accessed_course'] = course.id 
    return render(request, 'view_course.html', {'course': course})

@login_required
def dashboard(request):
    last_accessed_course_id = request.session.get('last_accessed_course_id')
    last_accessed_course_name = request.session.get('last_accessed_course_name')
    
    context = {
        'last_accessed_course_id': last_accessed_course_id,
        'last_accessed_course_name': last_accessed_course_name,
    }
    
    return render(request, 'view_course.html', context)

