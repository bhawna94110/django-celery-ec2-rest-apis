# Generated by Django 4.2.2 on 2023-07-04 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_customer_options_remove_customer_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can can cancel order')]},
        ),
    ]
