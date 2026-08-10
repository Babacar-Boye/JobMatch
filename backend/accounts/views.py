from django.shortcuts import render
from .forms import UtilisateurForm, CandidatForm
from django.shortcuts import render, redirect

# Create your views here.


# def liste_utilisateur(request):
#     if request.method == "POST":


def ajouter_utilisateur(request):
    if request.method == "POST":
        form_utilisateur = UtilisateurForm(request.POST, request.FILES)

        if form_utilisateur.is_valid():
            form_utilisateur.save()
            return redirect('connexion')
    else:
        form_utilisateur = UtilisateurForm()

    return render(request, 'inscription_utilisateur.html', {'form_utilisateur': form_utilisateur})


def ajouter_candidat(request):

    if request.method == "POST":

        form_utilisateur = UtilisateurForm(request.POST,request.FILES)

        form_candidat = CandidatForm(request.POST)

        if form_utilisateur.is_valid() and form_candidat.is_valid():

            utilisateur = form_utilisateur.save()

            candidat = form_candidat.save(commit=False)
            candidat.utilisateur = utilisateur
            candidat.save()

            return redirect("connexion")

    else:

        form_utilisateur = UtilisateurForm()
        form_candidat = CandidatForm()

    return render(
        request,
        "inscription_candidat.html",
        {
            "form_utilisateur": form_utilisateur,
            "form_candidat": form_candidat,
        }
    )


def ajouter_recruteur(request):
    if request.method == "POST":
        form_recruteur = RecruteurForm(request.POST)

        if form_recruteur.is_valid():
            form_recruteur.save()
            return redirect('connexion')
    else:
        form_recruteur = RecruteurForm()

    return render(request, 'ajouter_recruteur.html', {'form_recruteur' : form_recruteur})


def modifier_utilisateur(request, pk):
    utilisateur = get_object_or_404(Utilisateur, pk = pk)

    form_utilisateur = UtilisateurForm(request.POST or None, request.FILES or None, instance = utilisateur)

    if form_utilisateur.is_valid():
        form_utilisateur.save()
        return redirect('profil_utilisateur')

    return render(request, 'modifier_profil.html', {'form_utilisateur': form_utilisateur})