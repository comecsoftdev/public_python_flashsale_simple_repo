# Generated by Django 4.0.2 on 2022-04-11 09:54

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import flashsale.models.product
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Category Name')),
                ('abbr', models.CharField(max_length=12, unique=True, verbose_name='Category Name abbreviation')),
                ('items', models.CharField(max_length=200, verbose_name='Category items example')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='flashsale.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Store Name')),
                ('phone', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+\\d{9,15}$')], verbose_name='Store Phone')),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9)),
                ('lng', models.DecimalField(decimal_places=6, max_digits=9)),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('address_detail', models.CharField(max_length=255, null=True, verbose_name='Address Detail')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store', to='flashsale.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=600)),
                ('rating', models.IntegerField(choices=[(1, 'Poor'), (2, 'Average'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')], null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('parent', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='flashsale.review')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='flashsale.store')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PushMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.JSONField(max_length=2000)),
                ('message_body', models.CharField(max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PushDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, help_text='Inactive devices will not be sent notifications', verbose_name='Is active')),
                ('registration_id', models.TextField(max_length=1000, verbose_name='Registration token')),
                ('type', models.CharField(choices=[('ios', 'ios'), ('android', 'android'), ('web', 'web')], max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='push_device', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=flashsale.models.product.upload_to, verbose_name='Product Image')),
                ('thumbnail', models.ImageField(null=True, upload_to=flashsale.models.product.upload_to, verbose_name='Product Thumbnail')),
                ('name', models.CharField(max_length=50, verbose_name='Product Name')),
                ('comment', models.CharField(max_length=500, null=True, verbose_name='Comment About Product')),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(1000000)], verbose_name='Product Price')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='flashsale.store')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
