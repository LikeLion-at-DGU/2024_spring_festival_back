from datetime import datetime
from rest_framework import serializers
from django.core.validators import RegexValidator

from.models import Booth, BoothImage, BoothLike, Comment, BoothLocationOperationTime
from datetime import datetime, date
from django.core.exceptions import ObjectDoesNotExist


def trans_datetime_to_str(self, instance):
    operation_times = instance.location_operation_times.all()
    if not operation_times:
        return ""

    # 요일 문자열로 변환
    # 요일을 숫자로 매핑
    days_map = ['월', '화', '수', '목', '금', '토', '일']

    # 요일별로 중복 없이 저장
    days_set = set()
    for op_time in operation_times:
        day = days_map[op_time.date.weekday()]
        days_set.add(day)

    sorted_days = sorted(days_set, key=lambda x: days_map.index(x))
    days_str = ', '.join(sorted_days)

    # date = self.context.get('date')
    date_param = self.context.get('request').query_params.get('date')
    # 운영시간 문자열로 변환
    # 파라미터로 전달된 date 값으로 운영시간을 찾음
    # date 파라미터를 받지 못했다면 오늘 날짜로 탐색
    if date_param:
        target_date = int(date_param)
    else:
        target_date = int(datetime.today().day)

    # 입력된 날짜로 운영시간 탐색
    try:
        target_operation_time = operation_times.get(date__day=target_date)
    except ValueError:
        target_operation_time = None
    except ObjectDoesNotExist:
        target_operation_time = None

    # 문자열로 변환
    if target_operation_time is not None:
        start_time_str = target_operation_time.start_time.strftime('%H:%M')
        end_time_str = target_operation_time.end_time.strftime('%H:%M')
        times_str = f"{start_time_str} ~ {end_time_str}"

    else:
        times_str = "오늘은 운영하지 않습니다."

    return f"({days_str}) {times_str}"

class BoothImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = BoothImage
        fields = ['image']

class BoothLocationOperationTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoothLocationOperationTime
        fields = ['location', 'latitude', 'longitude']

class BoothListSerializer(serializers.ModelSerializer):
    like_cnt = serializers.IntegerField()
    thumbnail = serializers.SerializerMethodField()
    during = serializers.SerializerMethodField()
    location_info = serializers.SerializerMethodField()

    def get_thumbnail(self, instance):
        request = self.context.get('request')
        first_image = instance.boothimages.first()
        if first_image:
            thumbnail_url = request.build_absolute_uri(first_image.image.url)
            return thumbnail_url
        return None
    
    def get_during(self, instance):
        print(self.context.get('date'))
        return trans_datetime_to_str(self, instance)

    def get_location_info(self, instance):
        date_param = self.context.get('request').query_params.get('date')
        if date_param:
            target_date = int(date_param)
        else:
            target_date = int(datetime.today().day)

        location_operation_time = instance.location_operation_times.get(date__day=target_date)
        if location_operation_time:
            return BoothLocationOperationTimeSerializer(location_operation_time).data
        return None

    class Meta:
        model = Booth
        fields = [
            'id',
            'name',
            'thumbnail',
            'description',
            'operator',
            'location_info',
            'like_cnt',
            'during',
        ]

class BoothSerializer(serializers.ModelSerializer):
    like_cnt = serializers.IntegerField()
    is_liked = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    during = serializers.SerializerMethodField()
    location_info = serializers.SerializerMethodField()

    def get_is_liked(self, instance):
        request = self.context.get('request')
        if request:
            booth_id = str(instance.id)
            return booth_id in request.COOKIES.keys()
        return False

    def get_during(self, instance):
        return trans_datetime_to_str(self, instance)
    
    def get_images(self, instance):
        request=self.context.get('request')
        boothimage=instance.boothimages.all().order_by('id')
        try:
            booth_image_serializer=BoothImageSerializer(boothimage, many=True)
            outcome = []
            for data in booth_image_serializer.data:
                image_url = request.build_absolute_uri(data["image"])
                outcome.append(image_url)
            return outcome
        
        except:
            return None
        
    def get_location_info(self, instance):
        date_param = self.context.get('request').query_params.get('date')
        if date_param:
            target_date = int(date_param)
        else:
            target_date = int(datetime.today().day)

        location_operation_time = instance.location_operation_times.get(date__day=target_date)
        if location_operation_time:
            return BoothLocationOperationTimeSerializer(location_operation_time).data
        return None

    class Meta:
        model = Booth
        fields = [
            'id',
            'name',
            'description',
            'operator',
            'location_info',
            'during',
            'like_cnt',
            'is_liked',
            'images',
        ]

# class BoothLocationSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Booth
#         fields = [
#             'id',
#             'name',
#             'location',
#             'latitude',
#             'longitude'
#         ]

class LikeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BoothLike
        fields = [
                    'id',
                    'booth', 
                    'key'
                ]

class CommentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=4,
        validators=[RegexValidator(regex='^\d{4}$', message='Error : Password must be a 4-digit number')]
    , write_only=True)
    content = serializers.CharField()

    def create(self, validated_data):
        booth = Booth.objects.get(id=self.context.get("view").kwargs.get("id"))
        validated_data["booth"] = booth
        return super().create(validated_data)
    
    class Meta:
        model = Comment
        fields = ['id', 'password','content', 'created_at']
        read_only_fields = ['created_at']

