import secrets

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
    date = filters.CharFilter(method='filter_by_date')

    class Meta:
        model = Booth
        fields = ['location', 'type', 'date']

    def filter_by_date(self, queryset, name, value):
        try:
            # 입력된 날짜를 int로 변환
            day = int(value)

            # 입력된 일자에 해당하는 부스를 필터링
            queryset = queryset.filter(
                operation_times__date__day=day,
            ).distinct()

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
        # elif self.action == 'location':
        #     return BoothLocationSerializer
        return BoothSerializer
    
    def list(self, request, *args, **kwargs):
        date = request.query_params.get('date')
        queryset = self.filter_queryset(self.get_queryset().order_by('-like_cnt'))

        serializer = self.get_serializer(queryset, many=True, context={'request': request, 'date': date})
        return Response(serializer.data)


    def get(self, request, *args, **kwargs):
        date = request.query_params.get('date')
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request, 'date': date})
        return Response(serializer.data)
    
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
                response.delete_cookie(booth_id)
                return response
            else:
                return Response({'error': '해당 부스에 대한 좋아요를 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=True, methods=['GET'], url_path='location')
    # def location(self, request, pk=None):
    #     booth = self.get_object()
    #     serializer = self.get_serializer(booth)
    #     return Response(serializer.data)
    
    @action(detail=False, methods=['GET'], url_path='top3')
    def top3(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        top3 = queryset.order_by('-like_cnt')[:3]
        top3_serializer = BoothListSerializer(top3, many=True, context = {'request': request})
        return Response( top3_serializer.data )

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
