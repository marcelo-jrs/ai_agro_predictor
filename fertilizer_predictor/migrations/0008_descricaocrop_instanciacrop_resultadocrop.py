# Generated by Django 4.1.3 on 2023-10-10 14:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fertilizer_predictor', '0007_instancia_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='DescricaoCrop',
            fields=[
                ('id_descricao', models.AutoField(primary_key=True, serialize=False)),
                ('id_fertilizante', models.IntegerField()),
                ('descricao', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='InstanciaCrop',
            fields=[
                ('id_instancia', models.AutoField(primary_key=True, serialize=False)),
                ('nome_instancia', models.TextField()),
                ('temperatura', models.FloatField()),
                ('umidade', models.FloatField()),
                ('nitrogenio', models.IntegerField()),
                ('potassio', models.IntegerField()),
                ('fosforo', models.IntegerField()),
                ('ph', models.FloatField()),
                ('chuva', models.FloatField()),
                ('data', models.DateField(default=datetime.date.today)),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ResultadoCrop',
            fields=[
                ('id_resultado', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_fertilizante', models.TextField()),
                ('data', models.DateField(default=datetime.date.today)),
                ('id_descricao', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fertilizer_predictor.descricaocrop')),
                ('id_instancia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fertilizer_predictor.instanciacrop')),
            ],
        ),
    ]
