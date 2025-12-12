from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from Authentications.models import StudentProfile, User, Course,generate_roll_number
from .forms import UserForm, ProfileForm, PasswordEditForm,UserEditForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import CourseForm


@login_required
def admin_dashboard(request):
    student_count = User.objects.filter(role="student").count()
    course_count = Course.objects.count()

    return render(request, "User/admin_dashboard.html", {
        "student_count": student_count,
        "course_count": course_count,
    })


@login_required
def student_dashboard(request):
    profile = StudentProfile.objects.get(user=request.user)
    courses = profile.courses.all()

    return render(request, "User/student_dashboard.html", {
        "profile": profile,
        "courses": courses,
    })

@login_required
def student_list(request):
    query = request.GET.get("q", "")
    students = User.objects.filter(role="student").order_by("studentprofile__roll_number")

    if query:
        students = students.filter(
            Q(username__icontains=query) |
            Q(studentprofile__roll_number__icontains=query) |
            Q(studentprofile__courses__title__icontains=query)
        ).distinct()


    paginator = Paginator(students, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "User/student_list.html", {
        "students": page_obj,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "query": query,
    })

@login_required
def add_student(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save(commit=False)
            user.role = "student"
            user.set_password(user_form.cleaned_data["password1"])
            user.save()

            profile = StudentProfile.objects.create(
                user=user,
                roll_number=generate_roll_number(),
                year_of_admission=profile_form.cleaned_data["year_of_admission"],
                image=request.FILES.get("image")
            )

            profile.courses.set(profile_form.cleaned_data["courses"])

            messages.success(request, "Student created successfully!")
            return redirect("user:student_list")

    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request, "User/add_student.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })


@login_required
def edit_student(request, user_id):
    student = get_object_or_404(User, id=user_id)
    profile = student.studentprofile

    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=student)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        password_form = PasswordEditForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid() and password_form.is_valid():
            user_form.save()
            profile_form.save()
            profile.courses.set(profile_form.cleaned_data["courses"])
            new_password = password_form.cleaned_data.get("password1")
            if new_password:
                student.set_password(new_password)
                student.save()

            messages.success(request, "Student updated successfully!")
            return redirect("user:student_list")

    else:
        user_form = UserEditForm(instance=student)
        profile_form = ProfileForm(instance=profile)
        password_form = PasswordEditForm()

    return render(request, "User/edit_student.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "password_form": password_form,
        "student": student,
    })


@login_required
def delete_student(request, user_id):
    if request.method == "POST":
        student = get_object_or_404(User, id=user_id, role="student")
        student.delete()
        messages.success(request, "Student deleted.")
    return redirect("user:student_list")


@login_required
def course_list(request):
    courses = Course.objects.all()
    q = request.GET.get("q")
    if q:
        courses = courses.filter(title__icontains=q)
    return render(request, "courses/course_list.html", {"courses": courses})


@login_required
def course_add(request):
    form = CourseForm()

    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course added successfully!")
            return redirect("user:course_list")

    return render(request, "courses/course_form.html", {"form": form, "title": "Add Course"})


@login_required
def course_edit(request, id):
    course = get_object_or_404(Course, id=id)
    form = CourseForm(instance=course)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully!")
            return redirect("user:course_list")

    return render(request, "courses/course_form.html", {"form": form, "title": "Edit Course"})

@login_required
def course_delete(request, id):
    course = get_object_or_404(Course, id=id)
    course.delete()
    messages.success(request, "Course deleted successfully!")
    return redirect("user:course_list")
