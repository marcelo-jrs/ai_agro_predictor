# Generated by Django 4.1.3 on 2023-10-27 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fertilizer_predictor', '0009_resultado_id_usuario_resultadocrop_id_usuario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resultadocrop',
            old_name='tipo_fertilizante',
            new_name='cultura',
        ),
    ]
