from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UtilisateurManager(BaseUserManager):
    def create_user(self, email, nom, prenom, nom_utilisateur, password=None, **extra_fields):
        if not email:
            raise ValueError("Le mail est obligatoire!")
        if not nom:
            raise ValueError("Le nom est obligatoire!")
        if not prenom:
            raise ValueError("Le prenom est obligatoire!")
        if not nom_utilisateur:
            raise ValueError("Le nom d'utilisateur est obligatoire!")
        email = self.normalize_email(email)
        user = self.model(email = email, nom = nom, prenom = prenom, nom_utilisateur = nom_utilisateur, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, nom, prenom, nom_utilisateur, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, nom, prenom, nom_utilisateur, password, **extra_fields)


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    ROLE=[
        ('candidat', 'Candidat'),
        ('recruteur', 'Recruteur'),
        ('administrateur', 'Administrateur')
    ]

    STATUT_COMPTE = [
        ('actif', 'Actif'),
        ('desactive_utilisateur', 'Désactivé par l\'utilisateur'),
        ('suspendu_admin', 'Suspendu par l\'administrateur'),
        ('supprime', 'Supprimé'),
    ]

    nom = models.CharField(max_length=60)
    prenom = models.CharField(max_length=100)
    nom_utilisateur = models.CharField(max_length = 70, unique=True)
    email = models.EmailField(unique=True)
    telephone= models.CharField(max_length=15, blank=True, null=True, unique= True)
    date_naissance = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE, default = "candidat")
    photo_profil = models.ImageField(upload_to="photo_profil/", blank=True, null=True)
    date_incription = models.DateTimeField(auto_now_add=True)
    statut_compte = models.CharField(max_length=40, choices=STATUT_COMPTE, default = "actif")
    date_Dernier_Connexion = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    REQUIRED_FIELDS = [
        'nom_utilisateur', 'nom', 'prenom', 'date_naissance', 'role'
    ]
    
    USERNAME_FIELD = "email"

    objects = UtilisateurManager()

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        db_table = "utilisateur"

    def __str__(self):
        return f"{self.nom}, {self.prenom}, {self.email}, {self.nom_utilisateur}"

    def get_full_name(self):
        return f"{self.prenom} {self.nom}"


class Administrateur(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name="administrateur",
        limit_choices_to={"role": "administrateur"},
    )

    class Meta:
        verbose_name        = "Administrateur"
        verbose_name_plural = "Administrateurs"
        db_table            = "administrateur"

    def __str__(self):
        return f"Admin : {self.utilisateur.get_full_name()}"


class Candidat(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete = models.CASCADE,
        related_name = "candidat",
        limit_choices_to={"role": "candidat"},
    )

    # localisation = models.CharField(max_length=100)
    niveau_etude = models.CharField(max_length=100)
    domaine_metier = models.CharField(max_length=100)
    statut_recherche = models.BooleanField(default=True)
    lien_linkedin = models.URLField(max_length=200,blank=True)
    lien_portfolio = models.URLField(max_length=200,blank=True)
    disponibilite = models.DateField(blank=True,null=True)
    
    class Meta:
        verbose_name = "Candidat"
        verbose_name_plural = "Candidats"
        db_table = "candidat"

    def __str__(self):
        return f"Candidat : {self.utilisateur.get_full_name()} {self.domaine_metier}"


class Recruteur(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete = models.CASCADE,
        related_name = "recruteur",
        limit_choices_to = {"role": "recruteur"},
    )

    class Meta:
        verbose_name = "Recruteur"
        verbose_name_plural = "Recruteurs"
        db_table = "recruteur"

    poste = models.CharField(max_length = 60)
    def __str__(self):
        return f"Recruteur : {self.utilisateur.get_full_name()} {self.poste}"