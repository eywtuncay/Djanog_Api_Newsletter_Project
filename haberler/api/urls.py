from django.urls import path
from haberler.api import views as api_views

urlpatterns = [
    path('makaleler/', api_views.MakaleListCreateAPIView.as_view(), name='makale-listesi'),
    path('yazarlar/', api_views.GazeteciListCreateAPIView.as_view(), name='yazar-listesi'),
    path('makaleler/<int:pk>', api_views.MakaleDetailView.as_view(), name='makale-detay'),  # Slash eklendi
]


# # ----------------- FUNCTİON METHOD VIEWS ------------------- # #
# urlpatterns = [
#     path('makaleler/', api_views.makale_list_create_api_view, name='makale-listesi'),
#     path('makaleler/<int:pk>', api_views.makale_details_api_view, name='makale-detay'),
# ]
