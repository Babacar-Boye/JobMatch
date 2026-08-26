from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Chaque app expose ses routes sous son propre préfixe
    path('api/accounts/', include('accounts.urls')),
    path('api/candidats/', include('candidats.urls')),
    path('api/offres/', include('offres.urls')),          
    path('api/candidatures/', include('candidatures.urls')),
    path('api/entreprises/', include('entreprises.urls')), 
    #path('api/mistral/', include('mistral_ai.urls')),        
]

# Sert les fichiers médias (photos de profil, CV, etc.) en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)