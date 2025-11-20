from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('select-pet/', views.select_pet, name='select_pet'),
    path('pet-gender/', views.pet_gender, name='pet_gender'),
    path('pet-birthdate/', views.pet_birthdate, name='pet_birthdate'),
    path('pet-breed/', views.pet_breed, name='pet_breed'),
    path('cat-breed/', views.cat_breed, name='cat_breed'),
    path('pet-name/', views.pet_name, name='pet_name'),
    path('pet-documents/', views.pet_documents, name='pet_documents'),
    path('health-status/', views.health_status, name='health_status'),
    path('dog-health-conditions/', views.dog_health_conditions, name='dog_health_conditions'),
    path('cat-health-conditions/', views.cat_health_conditions, name='cat_health_conditions'),
    path('insurance-programs/', views.insurance_programs, name='insurance_programs'),
    path('non-covered/', views.non_covered, name='non_covered'),
    path('user-data/', views.user_data, name='user_data'),
    path('contact-info/', views.contact_info, name='contact_info'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('handle-application/', views.handle_application_submission, name='handle_application_submission'),
    
    # API endpoints
    path('api/validate-affiliate-code/', views.validate_affiliate_code, name='validate_affiliate_code'),
    path('api/upload-pet-document/', views.upload_pet_document, name='upload_pet_document'),
    path('api/upload-pet-photo/', views.upload_pet_photo, name='upload_pet_photo'),
    
    # File serving endpoint
    path('media/<str:file_type>/<int:file_id>/', views.serve_file, name='serve_file'),
]
