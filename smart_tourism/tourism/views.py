from django.shortcuts import render
from rest_framework import permissions
from rest_framework import viewsets
from .models import Hotel,Restaurant,Activity,Museum,ArchaeologicalSite,Festival,GuestHouse,Destination,Review,Favorite,Equipment
from .serializers import HotelSerializer,RestaurantSerializer,ActivitySerializer,MuseumSerializer,ArchaeologicalSiteSerializer,FestivalSerializer,GuestHouseSerializer,DestinationSerializer,ReviewSerializer,FavoriteSerializer
from users.permissions import IsAdmin,IsReviewOwnerOrAdmin
from django.db.models import Q
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import SAFE_METHODS
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

import logging
logger = logging.getLogger(__name__)



# Create your views here.
from .models import Hotel
from .serializers import HotelSerializer

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow any user to view hotels
            return [permissions.AllowAny()]
        
        # For create, update, and delete actions, only allow admins
        return [IsAdmin()]
    def get_queryset(self):
        queryset = Hotel.objects.all()

        # Search filters
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        # Filter by number of stars
        stars = self.request.query_params.get('stars', None)
        if stars:
            queryset = queryset.filter(stars=stars)

        # Filter by destination
        destination_name = self.request.query_params.get('destination', None)
        if destination_name:
            queryset = queryset.filter(destination__name__icontains=destination_name)

        # Sorting by price (asc or desc)
        sort_by = self.request.query_params.get('sort_by', 'price')  # Default sorting is by price
        sort_direction = self.request.query_params.get('sort_direction', 'asc')  # Default to ascending order

        if sort_by == 'price':
            if sort_direction == 'asc':
                queryset = queryset.order_by('price')  # Ascending order
            elif sort_direction == 'desc':
                queryset = queryset.order_by('-price')  # Descending order
        print(queryset.query)

        return queryset
    
    def create(self, request, *args, **kwargs):
        """
        Custom create method to handle equipments.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Handle the custom create logic in the serializer
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Custom update method to handle equipments.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        """
        Custom create method to handle equipment assignment after saving guest house.
        """
        hotel = serializer.save()
        equipment_ids = self.request.data.get('equipments', [])  # Get the list of equipment IDs

        for equipment_id in equipment_ids:
            try:
                # Get the equipment by ID
                equipment = Equipment.objects.get(id=equipment_id)
                hotel.equipments.add(equipment)
            except Equipment.DoesNotExist:
                pass  # Handle if equipment doesn't exist, maybe return an error message or log it

    def perform_update(self, serializer):
        """
        Custom update method to handle equipment assignment when updating guest house.
        """
        hotel = serializer.save()
        equipment_ids = self.request.data.get('equipments', [])
        hotel.equipments.clear()  # Clear existing equipment associations
        for equipment_id in equipment_ids:
            try:
                equipment = Equipment.objects.get(id=equipment_id)
                hotel.equipments.add(equipment)
            except Equipment.DoesNotExist:
                pass  # Handle if equipment doesn't exist, maybe return an error message
    

# class RestaurantViewSet(viewsets.ModelViewSet):
#     queryset = Restaurant.objects.all()
#     serializer_class = RestaurantSerializer

#     def get_permissions(self):
#         if self.action in ['list', 'retrieve']:  # Allow normal users to view
#             return [permissions.AllowAny()]
#         return [IsAdmin()]
    
#     def get_queryset(self):
#         queryset = Restaurant.objects.all()
        
#         # Search by category, name, description
#         search = self.request.query_params.get('search', None)
#         if search:
#             queryset = queryset.filter(
#                 Q(name__icontains=search) | Q(description__icontains=search) | Q(category__icontains=search)
#             )

#         # Filter by forks (similar to stars)
#         forks = self.request.query_params.get('forks', None)
#         if forks:
#             queryset = queryset.filter(forks=forks)

#         # Sorting by price (asc or desc)
#         sort_price = self.request.query_params.get('price', None)
#         if sort_price:
#             if sort_price.lower() == 'asc':
#                 queryset = queryset.order_by('price')
#             elif sort_price.lower() == 'desc':
#                 queryset = queryset.order_by('-price')

#         # Filtering by destination name
#         destination = self.request.query_params.get('destination', None)
#         if destination:
#             queryset = queryset.filter(destination__name__icontains=destination)  # Ensure this field exists

#         return queryset




class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdmin()]

    def get_queryset(self):
        queryset = Restaurant.objects.all()
        
        # Search by name or description (category removed)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        # Filter by forks
        forks = self.request.query_params.get('forks', None)
        if forks:
            queryset = queryset.filter(forks=forks)

        # Sort by price
        sort_price = self.request.query_params.get('price', None)
        if sort_price:
            if sort_price.lower() == 'asc':
                queryset = queryset.order_by('price')
            elif sort_price.lower() == 'desc':
                queryset = queryset.order_by('-price')

        # Filter by destination name
        destination = self.request.query_params.get('destination', None)
        if destination:
            queryset = queryset.filter(destination__name__icontains=destination)

        # Filter by cuisine name (new!)
        cuisine = self.request.query_params.get('cuisine', None)
        if cuisine:
            queryset = queryset.filter(cuisine__name__icontains=cuisine)

        return queryset
    

    
class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow normal users to view
            return [permissions.AllowAny()]
        return [IsAdmin()]
    
    def get_queryset(self):
        queryset = Activity.objects.all()
        
        # Get sorting direction from query params (default is ascending)
        sort_by = self.request.query_params.get('sort_by', None)
        sort_direction = self.request.query_params.get('sort_direction', 'asc')  # Default to ascending if not specified
        
        if sort_by == 'price':
            if sort_direction == 'desc':
                queryset = queryset.order_by('-price')  # Sort by price in descending order
            else:
                queryset = queryset.order_by('price')  # Sort by price in ascending order

        return queryset
    
class MuseumViewSet(viewsets.ModelViewSet):
    queryset = Museum.objects.all()
    serializer_class = MuseumSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow normal users to view
            return [permissions.AllowAny()]
        return [IsAdmin()]
    
    def get_queryset(self):
        queryset = Museum.objects.all()  # ✅ Initialize queryset first

        # Search by name or description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        # Get sorting direction from query params (default is ascending)
        sort_by = self.request.query_params.get('sort_by', None)
        sort_direction = self.request.query_params.get('sort_direction', 'asc')  # Default to ascending if not specified

        if sort_by == 'price':
            if sort_direction == 'desc':
                queryset = queryset.order_by('-price')  # Sort by price in descending order
            else:
                queryset = queryset.order_by('price')  # Sort by price in ascending order

        # Filter by destination name
        destination = self.request.query_params.get('destination', None)
        if destination:
            queryset = queryset.filter(destination__name__icontains=destination)

        
        return queryset


class ArchaeologicalSiteViewSet(viewsets.ModelViewSet):
    queryset = ArchaeologicalSite.objects.all()
    serializer_class = ArchaeologicalSiteSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow normal users to view
            return [permissions.AllowAny()]
        return [IsAdmin()]
    
    def get_queryset(self):
        queryset = ArchaeologicalSite.objects.all()  # ✅ Initialize queryset first

        # Search by name or description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

       
        # Filter by destination name
        destination = self.request.query_params.get('destination', None)
        if destination:
            queryset = queryset.filter(destination__name__icontains=destination)

        return queryset
    

class FestivalViewSet(viewsets.ModelViewSet):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow normal users to view
            return [permissions.AllowAny()]
        return [IsAdmin()] 
    
    def get_queryset(self):
        queryset = Festival.objects.all()  # ✅ Initialize queryset first

        # Search by name or description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        # Get sorting direction from query params (default is ascending)
        sort_by = self.request.query_params.get('sort_by', None)
        sort_direction = self.request.query_params.get('sort_direction', 'asc')  # Default to ascending if not specified

        if sort_by == 'price':
            if sort_direction == 'desc':
                queryset = queryset.order_by('-price')  # Sort by price in descending order
            else:
                queryset = queryset.order_by('price')  # Sort by price in ascending order

        # Filter by destination name
        destination = self.request.query_params.get('destination', None)
        if destination:
            queryset = queryset.filter(destination__name__icontains=destination)

        return queryset
    

    

class GuestHouseViewSet(viewsets.ModelViewSet):
    queryset = GuestHouse.objects.all()
    serializer_class = GuestHouseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow normal users to view
            return [permissions.AllowAny()]
        return [IsAdmin()]
    
    def get_queryset(self):
        queryset = GuestHouse.objects.all()  # ✅ Initialize queryset first

        # Search by name or description
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        # Get sorting direction from query params (default is ascending)
        sort_by = self.request.query_params.get('sort_by', None)
        sort_direction = self.request.query_params.get('sort_direction', 'asc')  # Default to ascending if not specified

        if sort_by == 'price':
            if sort_direction == 'desc':
                queryset = queryset.order_by('-price')  # Sort by price in descending order
            else:
                queryset = queryset.order_by('price')  # Sort by price in ascending order

        # Filter by destination name
        destination = self.request.query_params.get('destination', None)
        if destination:
            queryset = queryset.filter(destination__name__icontains=destination)

        return queryset
    
    def create(self, request, *args, **kwargs):
        """
        Custom create method to handle equipments.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Handle the custom create logic in the serializer
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Custom update method to handle equipments.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        """
        Custom create method to handle equipment assignment after saving guest house.
        """
        guest_house = serializer.save()
        equipment_ids = self.request.data.get('equipments', [])  # Get the list of equipment IDs

        for equipment_id in equipment_ids:
            try:
                # Get the equipment by ID
                equipment = Equipment.objects.get(id=equipment_id)
                guest_house.equipments.add(equipment)
            except Equipment.DoesNotExist:
                pass  # Handle if equipment doesn't exist, maybe return an error message or log it

    def perform_update(self, serializer):
        """
        Custom update method to handle equipment assignment when updating guest house.
        """
        guest_house = serializer.save()
        equipment_ids = self.request.data.get('equipments', [])
        guest_house.equipments.clear()  # Clear existing equipment associations
        for equipment_id in equipment_ids:
            try:
                equipment = Equipment.objects.get(id=equipment_id)
                guest_house.equipments.add(equipment)
            except Equipment.DoesNotExist:
                pass  # Handle if equipment doesn't exist, maybe return an error message
    

    

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # Allow normal users to view
            return [permissions.AllowAny()]
        return [IsAdmin()] 
    
    def get_queryset(self):
        queryset = Destination.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) 
            )
        return queryset
    

class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users and admins to manage reviews.
    - Users and admins can create, update, and delete their own reviews.
    - Only admins can delete another user's review (but not another admin's review).
    - Everyone can view reviews.
    - Blocked users cannot post reviews during the block period.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewOwnerOrAdmin]

    def get_queryset(self):
        """
        Filters reviews based on query parameters (entity_type and entity_id).
        """
        queryset = Review.objects.all()
        entity_type = self.request.query_params.get('entity_type', None)
        entity_id = self.request.query_params.get('entity_id', None)

        if entity_type:
            queryset = queryset.filter(entity_type=entity_type)
        if entity_id:
            queryset = queryset.filter(entity_id=entity_id)

        return queryset

    # def perform_create(self, serializer):
    #     """
    #     Prevent blocked users from posting reviews.
    #     """
    #     if self.request.user.is_blocked:
    #         return Response(
    #             {"error": "You are blocked from posting reviews."},
    #             status=status.HTTP_403_FORBIDDEN
    #         )
    #     serializer.save(user=self.request.user)
    def perform_create(self, serializer):
        """
        Prevent blocked users from posting reviews.
        """
        user = self.request.user
        today = timezone.now().date()

        logger.info(f"Checking block status for {user.email}: {user.blockstartdate} - {user.blockenddate}, Today: {today}")

        if user.blockstartdate and user.blockenddate:
            if user.blockstartdate.date() <= today <= user.blockenddate.date():
                logger.warning(f"User {user.email} is blocked from posting reviews!")
                return Response(
                    {"error": "You are blocked from posting reviews."},
                    status=status.HTTP_403_FORBIDDEN
            )

        serializer.save(user=user)




class FavoriteViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        # Only return favorites for the authenticated user
        return Favorite.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def add_to_favorite(self, request):
        entity_type = request.data.get('entity_type')
        entity_id = request.data.get('entity_id')

        # Check if the favorite already exists
        if Favorite.objects.filter(user=request.user, entity_type=entity_type, entity_id=entity_id).exists():
            return Response({'error': 'This item is already in your favorites.'}, status=400)

        # Create the favorite entry
        Favorite.objects.create(user=request.user, entity_type=entity_type, entity_id=entity_id)
        return Response({'message': 'Item added to favorites successfully!'}, status=201)

    @action(detail=False, methods=['post'])
    def remove_from_favorite(self, request):
        entity_type = request.data.get('entity_type')
        entity_id = request.data.get('entity_id')

        try:
            # Find and delete the favorite entry
            favorite = Favorite.objects.get(user=request.user, entity_type=entity_type, entity_id=entity_id)
            favorite.delete()
            return Response({'message': 'Item removed from favorites successfully!'}, status=200)
        except Favorite.DoesNotExist:
            return Response({'error': 'This item is not in your favorites.'}, status=404)

