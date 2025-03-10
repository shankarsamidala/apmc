from django.urls import path
from users.views import admin_dashboard, login_view, logout_view, faculty_dashboard, update_call_status

urlpatterns = [
    path("", login_view, name="login"),  # ✅ Keep if login should be the homepage
    path("logout/", logout_view, name="logout"),
    path("dashboard/", faculty_dashboard, name="faculty_dashboard"),
    path("update_call_status/", update_call_status, name="update_call_status"),  # ✅ Use underscores for consistency
    path("admin_dashboard/", admin_dashboard, name="admin_dashboard"),  # ✅ Use underscores for consistency
]