import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render
from .models import Resume
from .graph import generate_heatmap

import matplotlib
import matplotlib.colors as mcolors


matplotlib.use("Agg")


def create_heatmap_image(heatmap, start_date):
    max_reunions_per_day = np.max(heatmap)
    # Configuration de la taille et des couleurs
    fig, ax = plt.subplots(figsize=(36, 6))  # Plus de hauteur pour mieux afficher
    cmap = mcolors.ListedColormap(
        ["#f7feff", "#e5f5ff", "#c7e9ff", "#98d6fe", "#50baff"]
    )
    bounds = [
        0,
        max_reunions_per_day * 0.2,
        max_reunions_per_day * 0.4,
        max_reunions_per_day * 0.6,
        max_reunions_per_day * 0.8,
        max_reunions_per_day,
    ]  # Définir les seuils pour chaque niveau de couleur
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    # Transposer la matrice pour correspondre à l'ordre visuel (jours en lignes, semaines en colonnes)
    heatmap = heatmap.T[
        ::-1
    ]  # Transposer la matrice et inverser l'ordre vertical (axe 0)

    # Afficher la heatmap
    cax = ax.imshow(
        heatmap, cmap=cmap, norm=norm, aspect="equal", interpolation="nearest"
    )

    # Configuration des axes
    ax.set_yticks(range(7))  # 7 jours par semaine
    ax.set_yticklabels(
        ["Sun", "Sat", "Fri", "Thu", "Wed", "Tue", "Mon"], fontsize=10
    )  # Jours
    ax.set_xticks(range(53))  # 53 semaines
    ax.set_xticklabels(range(1, 54), fontsize=8)  # Numéros des semaines

    # Centrer le graphe
    ax.set_xlim(-0.5, 52.5)  # Limiter les bords horizontaux pour centrer
    ax.set_ylim(-0.5, 6.5)  # Limiter les bords verticaux pour centrer

    # Supprimer les grilles et le fond gris
    ax.grid(False)
    fig.patch.set_facecolor("white")  # Fond de la figure en blanc
    ax.set_facecolor("white")  # Fond des axes en blanc

    # Ajouter les contours autour des cases si besoin (désactivé pour un design épuré)
    for i in range(len(heatmap)):
        for j in range(len(heatmap[i])):
            ax.add_patch(
                plt.Rectangle(
                    (j - 0.5, i - 0.5), 1, 1, fill=False, edgecolor="white", lw=5
                )
            )

    # Placer le titre
    ax.set_title(f"({start_date.year})", fontsize=14, pad=20)

    # Supprimer les bordures inutiles
    ax.spines[:].set_visible(False)
    ax.tick_params(left=False, top=False, bottom=False, right=False)

    # Sauvegarder l'image dans un buffer
    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight", dpi=300)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()
    plt.close(fig)

    return f"data:image/png;base64,{image_base64}"


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


def login(request):
    return render(request, "logging/login.html")


def tutorial(request):
    return render(request, "tutorial/tutorial.html")


def my_summaries(request):
    user_summaries = Resume.objects.filter(attendees=request.user)
    return render(request, "summaries/summaries.html", {"summaries": user_summaries})


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


def summaries(request):
    my_summaries = Resume.objects.all()
    return render(
        request,
        "summaries/summaries.html",
        {"summaries": my_summaries},
    )


def summary(request, id):
    summary = Resume.objects.get(id=id)
    return render(request, "summaries/summary.html", {"summary": summary})
