from rest_framework import generics
from .models import Banner
from .serializers import BannerSerializer
from .models import Discount
from .serializers import DiscountSerializer

class BannerListCreateView(generics.ListCreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer





class DiscountListCreateView(generics.ListCreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer