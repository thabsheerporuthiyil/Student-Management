from django.urls import path
from . import views


app_name = "user"

urlpatterns = [
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("student-dashboard/", views.student_dashboard, name="student_dashboard"),

    # Student Management
    path("students/", views.student_list, name="student_list"),
    path("students/add/", views.add_student, name="add_student"),
    path("students/edit/<int:user_id>/", views.edit_student, name="edit_student"),
    path("students/delete/<int:user_id>/", views.delete_student, name="delete_student"),

    # courses
    path("courses/", views.course_list, name="course_list"),
    path("courses/add/", views.course_add, name="course_add"),
    path("courses/edit/<int:id>/", views.course_edit, name="course_edit"),
    path("courses/delete/<int:id>/", views.course_delete, name="course_delete"),
]
