from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from users.models import Faculty
from django.shortcuts import render
from django.db.models import Count, Q
from .models import StudentCall, Faculty

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from users.models import StudentCall
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import StudentCall, Faculty


def login_view(request):
    if request.method == "POST":
        emp_id = request.POST.get("emp_id")
        password = request.POST.get("password")

        try:
            faculty = Faculty.objects.get(emp_id=emp_id)  # Lookup Faculty by emp_id
            user = authenticate(request, username=faculty.username, password=password)

            if user:
                login(request, user)

                # Redirect based on role
                if faculty.role == "admin":
                    return redirect("admin_dashboard")  # Redirect Admin
                else:
                    return redirect("faculty_dashboard")  # Redirect Staff

            else:
                messages.error(request, "Invalid credentials")
        except Faculty.DoesNotExist:
            messages.error(request, "Faculty ID not found")

    return render(request, "users/login.html")  # Load login template


def logout_view(request):
    logout(request)
    return redirect("login")  # Redirect to login page


from django.utils.timezone import now
from django.db.models import Count

@login_required
def faculty_dashboard(request):
    faculty = request.user  
    calls = StudentCall.objects.filter(faculty=faculty).only(
        "id", "student_name", "phone_1", "inter_marks", "inter_group", "exam_rank", "call_1_status", "status", "rmarks"
    )

    # Status-wise student counts
    status_counts = StudentCall.objects.filter(faculty=faculty).values("status").annotate(count=Count("status"))
    
    # Organize counts in a dictionary for easy template access
    student_status_counts = {
        "NI": 0,  # Not Interested
        "I": 0,   # Interested
        "WD": 0,  # Willing to Degree
        "WE": 0,  # Willing to Engineering
        "ND": 0,  # Not Decided
        "J": 0    # Joined
    }

    # Update dictionary with actual counts
    for entry in status_counts:
        student_status_counts[entry["status"]] = entry["count"]

    context = {
        "faculty": faculty,
        "calls": calls,
        "last_updated": now().strftime("%d %b %Y"),
        "student_status_counts": student_status_counts,
        "csrf_token": request.COOKIES.get('csrftoken'),
        "inter_group_choices": StudentCall.INTER_GROUP_CHOICES,
        "call_status_choices": StudentCall.CALL_STATUS_CHOICES,
        "student_status_choices": StudentCall.STUDENT_STATUS_CHOICES
    }
    return render(request, "users/faculty_dashboard.html", context)

@csrf_exempt  
def update_call_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            call_id = data.get("call_id")
            new_status = data.get("call_status")
            new_marks = data.get("inter_marks")
            new_group = data.get("inter_group")
            new_rank = data.get("exam_rank")
            new_student_status = data.get("student_status")
            new_remarks = data.get("remarks")

            if not call_id:
                return JsonResponse({"success": False, "message": "Missing call_id"}, status=400)

            updated_rows = StudentCall.objects.filter(id=call_id).update(
                call_1_status=new_status,
                inter_marks=new_marks if new_marks else None,
                inter_group=new_group,
                exam_rank=new_rank if new_rank else None,
                status=new_student_status,
                comments=new_remarks
            )

            if updated_rows == 0:
                return JsonResponse({"success": False, "message": "Unauthorized or Call Not Found!"}, status=403)

            return JsonResponse({"success": True, "message": "Call details updated successfully!"})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


from django.db.models import Count, Q
from django.utils.timezone import now


@login_required
def admin_dashboard(request):
    # Get summary of calls made by each faculty, EXCLUDING Admins
    faculty_summary = Faculty.objects.filter(is_staff=False).annotate(
        # Call-related statuses
        total_calls=Count('calls'),
        calls_made=Count('calls', filter=~Q(calls__call_1_status="P")),  # Exclude Pending
        pending_calls=Count('calls', filter=Q(calls__call_1_status="P")),
        answered_calls=Count('calls', filter=Q(calls__call_1_status="A")),
        not_answered_calls=Count('calls', filter=Q(calls__call_1_status="NA")),
        interested_calls=Count('calls', filter=Q(calls__call_1_status="I")),
        not_interested_calls=Count('calls', filter=Q(calls__call_1_status="NI")),

        # Student-related statuses
        willing_degree_calls=Count('calls', filter=Q(calls__status="WD")),
        willing_engineering_calls=Count('calls', filter=Q(calls__status="WE")),
        not_decided_calls=Count('calls', filter=Q(calls__status="ND")),
        joined_calls=Count('calls', filter=Q(calls__status="J")),
    )

    # Aggregate total counts for summary cards
    call_stats = {
        # Call-related stats
        "total_calls": sum(f.total_calls for f in faculty_summary),
        "answered": sum(f.answered_calls for f in faculty_summary),
        "not_answered": sum(f.not_answered_calls for f in faculty_summary),
        "interested": sum(f.interested_calls for f in faculty_summary),
        "not_interested": sum(f.not_interested_calls for f in faculty_summary),

        # Student-related stats
        "willing_degree": sum(f.willing_degree_calls for f in faculty_summary),
        "willing_engineering": sum(f.willing_engineering_calls for f in faculty_summary),
        "not_decided": sum(f.not_decided_calls for f in faculty_summary),
        "joined": sum(f.joined_calls for f in faculty_summary),
    }

    context = {
        "faculty_summary": faculty_summary,
        "call_stats": call_stats,
        "last_updated": now().strftime("%d %b %Y"),
    }
    return render(request, "admin/admin_dashboard.html", context)