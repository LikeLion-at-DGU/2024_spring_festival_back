import secrets, requests

from decouple import config

from django.db.models import Count, Q
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Booth, BoothLike, TYPE_CHOICES, Comment

from .serializers import BoothListSerializer, BoothSerializer, LikeSerializer, CommentSerializer
# Create your views here.

DEPLOY = config('DJANGO_DEPLOY', default=False, cast=bool)

class BoothFilter(filters.FilterSet):
    type = filters.MultipleChoiceFilter(field_name='type', choices=TYPE_CHOICES)
    date = filters.CharFilter(method='filter_by_date_range')

    class Meta:
        model = Booth
        fields = ['location', 'type', 'date']

    def filter_by_date_range(self, queryset, name, value):
        try:
            day = int(value)

            queryset = queryset.filter(
                Q(start_at__day__lte=day) & Q(end_at__day__gte=day)
            )
            return queryset
        
        except ValueError:
            return queryset.none()
        
class BoothViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    filter_backends = [DjangoFilterBackend]
    filterset_class = BoothFilter

    def get_queryset(self):
        queryset = Booth.objects.annotate(
            like_cnt = Count('likes'),
        )
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BoothListSerializer
        return BoothSerializer
    
    # 좋아요
    @action(methods=['POST', 'DELETE'], detail=True)
    def likes(self, request, pk=None):
        booth = self.get_object()
        booth_id = str(booth.id)

        if request.method == 'POST':
            if booth_id in request.COOKIES:
                return Response({'error': '이미 좋아요를 눌렀습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            key = secrets.token_hex(5)
            booth_like = BoothLike.objects.create(booth=booth, key=key)
            serializer = LikeSerializer(booth_like)
            response = Response(serializer.data)
            # 3일간 쿠키 유효 / Deploy시 secure=True로 바꿀것
            response.set_cookie(booth_id, key, max_age=3*24*60*60, secure=DEPLOY, httponly=True)  
            
            return response
        
        elif request.method == 'DELETE':
            # cookie가 booth_id를 가지고 있지 않은 경우
            if booth_id not in request.COOKIES:
                return Response({'error': '좋아요를 누르지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            key = request.COOKIES[booth_id]
            booth_like = BoothLike.objects.filter(booth=booth, key=key)

            if booth_like.exists():
                booth_like.delete()
                response = Response({'message': '좋아요가 취소되었습니다. 쿠키가 삭제되었습니다.'})
                response.delete_cookie(booth_id, secure=DEPLOY)
                return response
            else:
                return Response({'error': '해당 부스에 대한 좋아요를 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Comment.objects.filter(
            booth__id=self.kwargs.get("id")
        )
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        password = request.data.get('password')
        if password == instance.password:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=400)