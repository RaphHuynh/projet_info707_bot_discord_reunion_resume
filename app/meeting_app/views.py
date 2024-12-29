from django.shortcuts import render, redirect
from .models import Resume
from .graph import generate_heatmap
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .lib import generate_pdf_for_all
import os


def home(request):
    recent_summaries = [
        {
            "id": 1,
            "title": "Team Sync - Nov 15",
            "short_description": "A summary of the team sync meeting covering major updates and next steps.",
        },
        {
            "id": 2,
            "title": "Project Kickoff - Nov 10",
            "short_description": "Discussion on project goals, timelines, and team responsibilities.",
        },
    ]
    return render(request, "home/home.html", {"recent_summaries": recent_summaries})


def tutorial(request):
    return render(request, "tutorial/tutorial.html")


@user_passes_test(test_func=lambda u: u.is_authenticated, login_url="/oauth2/login")
def my_summaries(request):
    user_summaries = Resume.objects.filter(attendees=request.user)
    return render(request, "summaries/summaries.html", {"summaries": user_summaries})


@user_passes_test(test_func=lambda u: u.is_authenticated, login_url="/oauth2/login")
def profile(request):
    my_summaries = Resume.objects.filter(attendees=request.user)
    total_meetings = my_summaries.count()
    recent_meetings = my_summaries.order_by("-date")[:4]
    meeting_dates = list(my_summaries.values_list("date", flat=True))
    heatmap, _ = generate_heatmap(meeting_dates)

    heatmap = heatmap.T

    return render(
        request,
        "profile/profile.html",
        {
            "summaries": my_summaries,
            "total_meetings": total_meetings,
            "heatmap": zip(heatmap, ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]),
            "months": [
                {"full_name": "January", "short_name": "Jan", "colspan": 4},
                {"full_name": "February", "short_name": "Feb", "colspan": 4},
                {"full_name": "March", "short_name": "Mar", "colspan": 5},
                {"full_name": "April", "short_name": "Apr", "colspan": 4},
                {"full_name": "May", "short_name": "May", "colspan": 4},
                {"full_name": "June", "short_name": "Jun", "colspan": 5},
                {"full_name": "July", "short_name": "Jul", "colspan": 4},
                {"full_name": "August", "short_name": "Aug", "colspan": 4},
                {"full_name": "September", "short_name": "Sep", "colspan": 5},
                {"full_name": "October", "short_name": "Oct", "colspan": 4},
                {"full_name": "November", "short_name": "Nov", "colspan": 4},
                {"full_name": "December", "short_name": "Dec", "colspan": 5},
            ],
            "recent_meetings": recent_meetings,
        },
    )

@user_passes_test(test_func=lambda u: u.is_authenticated, login_url="/oauth2/login")
def summaries(request):
    my_summaries = Resume.objects.all()
    return render(
        request,
        "summaries/summaries.html",
        {"summaries": my_summaries},
    )


def summary(request, id):
    summary = Resume.objects.get(id=id)
    if request.user not in summary.attendees.all():
        return redirect("/summaries/")

    return render(request, "summaries/summary.html", {"summary": summary})


@csrf_exempt
def generate_pdf_combined_view(request):
    if request.method == "POST":
        try:
            # Récupérer les données JSON envoyées par la requête
            data = json.loads(request.body)
            
            # Vérifier que les données sont bien présentes
            resume = data.get("resume", None)
            if not resume:
                return JsonResponse({"error": "Resume data is missing"}, status=400)

            # Nom du fichier PDF à générer
            output_file = "combined_summary.pdf"

            # Appeler une fonction pour générer le PDF (vous devez définir cette fonction)
            # Vous devrez probablement ajuster la fonction generate_pdf_for_all selon vos besoins
            generate_pdf_for_all(resume, output_file)
            
            # Vérifier si le fichier a bien été généré
            if not os.path.exists(output_file):
                return JsonResponse({"error": "Failed to generate the PDF file."}, status=500)

            # Retourner le fichier PDF en réponse à l'utilisateur
            response = FileResponse(open(output_file, 'rb'), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{output_file}"'

            # Supprimer le fichier PDF après l'envoi
            os.remove(output_file)
            return response

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            # Gérer d'autres erreurs
            return JsonResponse({"error": str(e)}, status=500)
    
    # Si la méthode n'est pas POST
    return JsonResponse({"error": "Invalid request method"}, status=405)
