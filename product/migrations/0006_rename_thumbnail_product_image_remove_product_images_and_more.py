# Generated by Django 4.2.10 on 2024-03-01 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0005_productimage_remove_product_images_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product", old_name="thumbnail", new_name="image",
        ),
        migrations.RemoveField(model_name="product", name="images",),
        migrations.DeleteModel(name="ProductImage",),
    ]
