from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from haberler.models import Makale, Gazeteci
from haberler.api.serializers import MakaleSerializer, GazeteciSerializers

# class views
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404



# ----------------- CLASS METHOD BAŞLANGIÇ ------------------- #
# ----------------- CLASS METHOD BAŞLANGIÇ ------------------- #



class GazeteciListCreateAPIView(APIView):
    def get(self, request):
        yazarlar = Gazeteci.objects.all()                   
        serializer = GazeteciSerializers(yazarlar, many=True, context={'request': request})                  
        return Response(serializer.data) 


    def post(self, request):
        serializer = GazeteciSerializers(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class MakaleListCreateAPIView(APIView):
    def get(self, request):
        # GET isteği ile filtreleme işlemi
        baslik = request.query_params.get('baslik', None)
        sehir = request.query_params.get('sehir', None)
        aktif = request.query_params.get('aktif', None)
        aciklama = request.query_params.get('aciklama', None)

        # Tüm aktif makaleleri getir
        makaleler = Makale.objects.filter(aktif=True)

        # Parametreler varsa filtreleme yap
        if baslik:
            makaleler = makaleler.filter(baslik__icontains=baslik)
        if sehir:
            makaleler = makaleler.filter(sehir__iexact=sehir)
        if aktif is not None:
            aktif_bool = aktif.lower() == 'true'
            makaleler = makaleler.filter(aktif=aktif_bool)
        if aciklama:
            makaleler = makaleler.filter(aciklama__icontains=aciklama)

        # Verileri serileştir ve geri dön
        serializer = MakaleSerializer(makaleler, many=True)
        return Response(serializer.data)

    def post(self, request):
        # POST isteğinde gelen JSON verileri
        baslik = request.data.get('baslik', None)
        sehir = request.data.get('sehir', None)
        aktif = request.data.get('aktif', None)

        # Eğer filtreleme yapılacaksa, filtrele
        if baslik or sehir or aktif is not None:
            makaleler = Makale.objects.filter(aktif=True)

            if baslik:
                makaleler = makaleler.filter(baslik__icontains=baslik)
            if sehir:
                makaleler = makaleler.filter(sehir__iexact=sehir)
            if aktif is not None:
                aktif_bool = aktif.lower() == 'true'
                makaleler = makaleler.filter(aktif=aktif_bool)

            # Filtrelenmiş sonuçları döndür
            serializer = MakaleSerializer(makaleler, many=True)
            return Response(serializer.data)

        # Eğer filtreleme verisi yoksa, yeni bir makale oluştur
        serializer = MakaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MakaleDetailView(APIView):
    def get_object(self, pk):
        makale_instance = get_object_or_404(Makale, pk=pk)
        return makale_instance
    
    def get(self, request, pk):
        makale = self.get_object(pk=pk)
        serializer = MakaleSerializer(makale)        
        return Response(serializer.data)

    def put(self, request, pk):
        makale = self.get_object(pk=pk)
        serializer = MakaleSerializer(makale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        makale = self.get_object(pk=pk)
        makale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# ----------------- CLASS METHOD BİTİŞ ------------------- #
# ----------------- CLASS METHOD BİTİŞ ------------------- #



# .
# .
# .
# .



# ----------------- FUNCTİON METHOD BAŞLANGIÇ ------------------- #
# ----------------- FUNCTİON METHOD BAŞLANGIÇ ------------------- #

# @api_view(['GET', 'POST'])
# def makale_list_create_api_view(request):
    
#     if request.method == 'GET':                                                 # gelen istek GET isteği ise,
#         makaleler = Makale.objects.filter(aktif=True)                           # aktif=True olanları Makaleler modelinden çeker. Bu, bir queryset (birden fazla nesne döndüren sorgu) döndürür.
#         serializer = MakaleSerializer(makaleler, many=True)                     # DB'deki makale nesnelerini JSON formatına döndürür. many=True parametresi, birden fazla nesneyi serialize edeceğimizi belirtir (çünkü bir queryset listesi dönüyor).
#         return Response(serializer.data)                                        # JSON formatına dönüştürülmüş veriyi yanıt olarak döner.
    
#     elif request.method == 'POST':
#         serializer = MakaleSerializer(data=request.data)                        # Bu aşamada gelen veriler yeni bir makale oluşturmak için kullanılıyor. MakaleSerializer ile işliyoruz.
#         if serializer.is_valid():                                               # gelen veri doğru formatta mı diye kontrol.
#             serializer.save()                                                   # doğruyla yeni bir makale veritabanına kaydedilir.
#             return Response(serializer.data, status = status.HTTP_201_CREATED)  # oluşturulan yeni makale bilgilerini geri döndürür.
#         return Response(status=status.HTTP_400_BAD_REQUEST)                     # veriler geçersizse 400 hatası döndürülür.




# @api_view(['GET', 'PUT', 'DELETE'])
# def makale_details_api_view(request, pk):
#     try:                                                                        # pk (birincil anahtar) ile veritabanında bir makale olup olmadığını kontrol ediyorum.  
#         makale_instance = Makale.objects.get(pk=pk)                             # pk'e göre DB'de makale bulmaya çalışıyorum.
#     except Makale.DoesNotExist:                                                 # eğer makale bulamazsam hata fırlatıyorum.
#         return Response(
#             {
#                 'errors':{
#                     'code': 404,
#                     'message': f'id: {pk} ile ilgili bir makale bulunamadı.'
#                 }
#             },
#             status=status.HTTP_404_NOT_FOUND
#         )
    
#     if request.method == 'GET':                                                 # eğer GET isteği gelirse,
#         serializer = MakaleSerializer(makale_instance)                          # makale nesnesini JSON formatına dönüştür.         
#         return Response(serializer.data)                                        # JSON verisi, HTTP 200 yanıtıyla istemciye geri gönderilir.


#     elif request.method == 'PUT':                                               # eğer PUT isteği gelirse,
#         serializer = MakaleSerializer(makale_instance, data=request.data)       # gelen veriyi (request.data) kullanarak mevcut makale nesnesini günceller.                    
#         if serializer.is_valid():                                               # gelen veri geçerliyse, güncelleme işlemi yapılır ve veritabanına kaydedilir.                      
#             serializer.save()                                                   # güncelleme DB'e kaydedilir.                                        
#             return Response(serializer.data)                                    # güncellenen veriler tekrar JSON formatında istemciye gönderilir.
#         return Response(status=status.HTTP_400_BAD_REQUEST)                     # Eğer geçersiz veri gönderilmişse, 400 BAD REQUEST hatası döndürülür.           


#     elif request.method == 'DELETE':                                            # eğer DELETE isteği gelirse,
#         makale_instance.delete()                                                # DB'den ilgili makale silinir.
#         return Response(                                                        # Silme işlemi başarılı olduktan sonra, 204 NO CONTENT statüsü ile bir yanıt döndürülür.
#             {
#                 'işlem':{
#                     'code': 204,
#                     'message': f'id: {pk} numaralı makale silinmiştir.'
#                 }
#             },
#             status = status.HTTP_204_NO_CONTENT
#         )

# ----------------- FUNCTİON METHOD BİTİŞ ------------------- #
# ----------------- FUNCTİON METHOD BİTİŞ ------------------- #

