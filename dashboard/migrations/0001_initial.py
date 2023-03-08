# Generated by Django 4.1.4 on 2023-03-08 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StrikeSideMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TickerName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('symbol', models.CharField(blank=True, max_length=255, null=True)),
                ('date_of_listing', models.CharField(blank=True, max_length=255, null=True)),
                ('series', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TickerTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker_name', models.CharField(blank=True, max_length=255, null=True)),
                ('entry_price', models.BigIntegerField(blank=True, null=True)),
                ('exit_price', models.BigIntegerField(blank=True, null=True)),
                ('target_price', models.BigIntegerField(blank=True, null=True)),
                ('stop_loss', models.BigIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_sl', models.BooleanField(blank=True, null=True)),
                ('is_target', models.BooleanField(blank=True, null=True)),
                ('is_exit_between', models.BooleanField(blank=True, null=True)),
                ('strike_side', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.strikesidemaster')),
                ('ticker_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.tickertypes')),
            ],
        ),
    ]
