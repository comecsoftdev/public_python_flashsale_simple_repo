from django.db import migrations, transaction
from django.conf import settings

from flashsale.models.basic_data import Category


def insertCategory(apps, schema_editor):
    with transaction.atomic():
        Category.objects.create(name='음식점', abbr='음식점', items='한식, 중식, 일식, 분식 등')
        Category.objects.create(name='주점/음료', abbr='주점/음료', items='일반주점, 커피전문점 등')
        Category.objects.create(name='종합소매업', abbr='종합소매업', items='슈퍼마켓, 편의점 등')
        Category.objects.create(name='오락시설', abbr='오락시설', items='PC방, 당구장, 노래연습장, 스포츠시설, 테마파크 등')
        Category.objects.create(name='개인서비스업', abbr='서비스업', items='미용, 헤어샵, 찜질방, 세탁 등')
        Category.objects.create(name='의류/신발/가방/액세서리', abbr='의류/신발', items='의류, 신발, 가방, 액세서리 등')
        Category.objects.create(name='화장품', abbr='화장품', items='화장품, 비누, 방향제 등')
        Category.objects.create(name='영화/공연', abbr='영화/공연', items='영화, 연극, 콘서트 등')
        Category.objects.create(name='문화/오락/여가 용품', abbr='문화생활', items='서적, 음반, 문구, 스포츠용품, 게임용품, 장난감 등')
        Category.objects.create(name='컴퓨터/통신기기', abbr='정보통신', items='컴퓨터 및 주변장치, 소프트웨어, 통신기기 등')


class Migration(migrations.Migration):
    dependencies = [
        ('flashsale', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insertCategory),
    ]
