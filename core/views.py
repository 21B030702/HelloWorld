from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User, Category, Supplier, Item, Auction, Review, Purchase
from .serializers import (
    UserSerializer, CategorySerializer, SupplierSerializer, 
    ItemSerializer, AuctionSerializer, ReviewSerializer, PurchaseSerializer
)
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.db import transaction
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

@api_view(['POST'])
def regist(request):
    try:
        user = User.objects.create(
            username=request.data['username'],
            password=make_password(request.data['password']),
            email=request.data['email']
        )
        user.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_user(request):
    data = request.data
    data['password'] = make_password(data['password'])
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def browsing_items(request, category_id=None):
    if category_id:
        items = Item.objects.filter(category_id=category_id)
    else:
        items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def searching_items(request):
    query_params = request.query_params
    items = Item.objects.all()
    if 'keyword' in query_params:
        items = items.filter(name__icontains=query_params['keyword'])
    if 'price_min' in query_params and 'price_max' in query_params:
        items = items.filter(price__gte=query_params['price_min'], price__lte=query_params['price_max'])
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_item(request):
    user = request.user
    item_id = request.data.get('item_id')
    with transaction.atomic():
        try:
            item = Item.objects.select_for_update().get(pk=item_id, status='In Stock')
            item.status = 'Sold'
            item.save()
            purchase = Purchase.objects.create(
                user=user,
                item=item,
                amount=item.price
            )
            return Response({"message": "Item purchased successfully."}, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            return Response({"error": "Item not available or does not exist."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def auction_item(request):
    user = request.user
    data = request.data
    try:
        if data['end_time'] <= timezone.now().isoformat():
            return Response({"error": "End time must be in the future."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            item = Item.objects.create(
                supplier=user.supplier,  # Предполагаем, что пользователь является поставщиком
                name=data['name'],
                description=data['description'],
                category_id=data['category_id'],
                price=data['price'],
                reserve_price=data['reserve_price'],
                status='Auction',
                location=data['location']
            )
            Auction.objects.create(
                item=item,
                starting_price=data['starting_price'],
                current_bid=data['starting_price'],
                start_time=timezone.now(),
                end_time=data['end_time']
            )
            return Response({"message": "Item put up for auction successfully."}, status=status.HTTP_201_CREATED)
    except KeyError as e:
        return Response({"error": f"Missing field {e.args[0]}"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bid_item(request):
    user = request.user
    item_id = request.data.get('item_id')
    bid_amount = float(request.data.get('bid_amount'))
    with transaction.atomic():
        try:
            auction = Auction.objects.select_for_update().get(item_id=item_id, end_time__gt=timezone.now())
            if bid_amount <= auction.current_bid + 2 or (auction.item.reserve_price and bid_amount < auction.item.reserve_price):
                return Response({"error": "Bid must be at least $2 higher than the current bid and higher than reserve price."}, status=status.HTTP_400_BAD_REQUEST)
            auction.current_bid = bid_amount
            auction.save()
            return Response({"message": "Bid placed successfully."}, status=status.HTTP_200_OK)
        except Auction.DoesNotExist:
            return Response({"error": "Auction not available, already ended, or does not exist."}, status=status.HTTP_404_NOT_FOUND)