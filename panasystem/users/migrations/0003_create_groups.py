from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    # Create groups
    employee_group, _ = Group.objects.get_or_create(name="Empleado")
    admin_group, _ = Group.objects.get_or_create(name="Administrador")

    # Add permissions to the groups
    # Here you can add specific permissions to each group
    # Example: adding 'add_user' permission to the admin group
    add_user_permission = Permission.objects.get(codename="add_user")
    admin_group.permissions.add(add_user_permission)

    # Save the groups
    employee_group.save()
    admin_group.save()


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
