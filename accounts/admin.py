from django.contrib import admin
from .models import UserProfile, JuristeProfile, Review

# 🔍 Admin pour le profil utilisateur général
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'created_at')
    search_fields = ('user__username', 'role')
    list_filter = ('role', 'created_at')
    ordering = ('-created_at',)

# 🧑‍⚖️ Admin pour le profil professionnel des juristes
@admin.register(JuristeProfile)
class JuristeProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user_full_name',
        'profession',
        'ville',
        'institution',
        'average_rating_display',
        'created_at'
    )
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'profession',
        'ville',
        'institution'
    )
    list_filter = ('profession', 'ville', 'created_at')
    ordering = ('-created_at',)

    def user_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_full_name.short_description = "Juriste"

    def average_rating_display(self, obj):
        return obj.average_rating() or "—"
    average_rating_display.short_description = "Note moyenne"

# ⭐ Admin pour les avis
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'juriste_display',
        'reviewer_display',
        'rating',
        'created_at'
    )
    search_fields = (
        'juriste__user__username',
        'reviewer__username',
        'comment'
    )
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)

    def juriste_display(self, obj):
        return obj.juriste.user.get_full_name() or obj.juriste.user.username
    juriste_display.short_description = "Juriste"

    def reviewer_display(self, obj):
        return obj.reviewer.get_full_name() if obj.reviewer else "Anonyme"
    reviewer_display.short_description = "Auteur de l’avis"
