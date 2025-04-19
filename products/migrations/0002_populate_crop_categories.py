from django.db import migrations

def create_initial_categories_and_crops(apps, schema_editor):
    CropCategory = apps.get_model('products', 'CropCategory')
    Crop = apps.get_model('products', 'Crop')
    
    # Create categories
    categories = {
        'cereals': 'Cereals',
        'vegetables': 'Vegetables', 
        'fruits': 'Fruits',
        'roots-tubers': 'Roots & Tubers',
        'legumes': 'Legumes',
        'herbs-spices': 'Herbs & Spices',
        'others': 'Others'
    }
    
    created_categories = {}
    for slug, name in categories.items():
        category = CropCategory.objects.create(name=name, slug=slug)
        created_categories[slug] = category
    
    # Create common crops
    crops_data = [
        ('maize', 'Maize', 'cereals', 'kg, bag'),
        ('rice', 'Rice', 'cereals', 'kg, bag'),
        ('tomato', 'Tomato', 'vegetables', 'kg, crate, box'),
        ('onion', 'Onion', 'vegetables', 'kg, bag'),
        ('mango', 'Mango', 'fruits', 'kg, crate'),
        ('orange', 'Orange', 'fruits', 'kg, bag'),
        ('cassava', 'Cassava', 'roots-tubers', 'kg, bag'),
        ('yam', 'Yam', 'roots-tubers', 'tuber, kg, bag'),
        ('cowpea', 'Cowpea', 'legumes', 'kg, bag'),
        ('groundnut', 'Groundnut', 'legumes', 'kg, bag'),
        ('pepper', 'Pepper', 'herbs-spices', 'kg, bag, basket'),
    ]
    
    for slug, name, category_slug, units in crops_data:
        Crop.objects.create(
            name=name,
            slug=slug,
            category=created_categories[category_slug],
            common_units=units
        )

def reverse_migration(apps, schema_editor):
    CropCategory = apps.get_model('products', 'CropCategory')
    CropCategory.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('products', '0001_initial'),  # Adjust this to your actual migration file
    ]

    operations = [
        migrations.RunPython(create_initial_categories_and_crops, reverse_migration),
    ]