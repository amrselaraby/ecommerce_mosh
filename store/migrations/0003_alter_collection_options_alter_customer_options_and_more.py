# Generated by Django 5.0 on 2023-12-09 15:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0002_rename_price_product_unit_price"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="collection",
            options={"ordering": ["title"]},
        ),
        migrations.AlterModelOptions(
            name="customer",
            options={"ordering": ["first_name", "last_name"]},
        ),
        migrations.AlterModelOptions(
            name="product",
            options={"ordering": ["title"]},
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(null=True),
        ),
    ]
