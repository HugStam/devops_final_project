from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from tours_DB.models import Customers
from tours_DB.serializers import CustomerSerializer
from rest_framework.decorators import api_view

# Create your views here.
# def index(request):
#     return render(request, "Customers/index.html")


def index(request):
    print("------------------------- I AM HERE")
    queryset = Customers.objects.all()
    return render(request, "Customers/index.html", {'Customers': queryset})


class index(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Customers/index.html'

    def get(self, request):
        queryset = Customers.objects.all()
        return Response({'Customers': queryset})


class list_all_Customers(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Customers/Customer_list.html'

    def get(self, request):
        queryset = Customers.objects.all()
        return Response({'Customers': queryset})


# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def Customer_list(request):
    if request.method == 'GET':
        Customers = Customers.objects.all()

        title = request.GET.get('title', None)
        if title is not None:
            Customers = Customers.filter(title__icontains=title)

        Customers_serializer = CustomerSerializer(Customers, many=True)
        return JsonResponse(Customers_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        Customer_data = JSONParser().parse(request)
        Customer_serializer = CustomerSerializer(data=Customer_data)
        if Customer_serializer.is_valid():
            Customer_serializer.save()
            return JsonResponse(Customer_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(Customer_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Customers.objects.all().delete()
        return JsonResponse(
            {
                'message':
                '{} Customers were deleted successfully!'.format(count[0])
            },
            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def Customer_detail(request, pk):
    try:
        Customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        return JsonResponse({'message': 'The Customer does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        Customer_serializer = CustomerSerializer(Customer)
        return JsonResponse(Customer_serializer.data)

    elif request.method == 'PUT':
        Customer_data = JSONParser().parse(request)
        Customer_serializer = CustomerSerializer(Customer, data=Customer_data)
        if Customer_serializer.is_valid():
            Customer_serializer.save()
            return JsonResponse(Customer_serializer.data)
        return JsonResponse(Customer_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Customer.delete()
        return JsonResponse({'message': 'Customer was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def Customer_list_published(request):
    Customers = Customers.objects.filter(published=True)

    if request.method == 'GET':
        Customers_serializer = CustomerSerializer(Customers, many=True)
        return JsonResponse(Customers_serializer.data, safe=False)