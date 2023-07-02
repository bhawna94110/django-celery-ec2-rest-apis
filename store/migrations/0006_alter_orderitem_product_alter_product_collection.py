# Generated by Django 4.2.2 on 2023-06-29 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_product_inventory_alter_product_promotions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orderitems', to='store.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='store.collection'),
        ),
    ]