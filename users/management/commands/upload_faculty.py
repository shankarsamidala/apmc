import pandas as pd
from django.core.management.base import BaseCommand
from users.models import Faculty
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = "Upload faculty details from an Excel file"

    def handle(self, *args, **kwargs):
        file_path = "/Users/shankarsamidala/Documents/WORK/ORGS/ASCS/apmc/users/management/commands/staff.xlsx"  # Update the file path if needed
        df = pd.read_excel(file_path,skiprows=1)
        print(df.head())

        for _, row in df.iterrows():
            emp_id = str(row['EMP ID']).strip()
            full_name = row['NAME OF THE FACULTY'].strip()
            department = row['DEPARTMENT'].strip()
            phone = str(row['PHONE NUMBER']).strip() if not pd.isna(row['PHONE NUMBER']) else None
            if phone:
                phone = phone.split("\n")[0]
                
            # Assign default role as 'staff' unless otherwise specified
            role = 'staff'

            # Create faculty entry
            Faculty.objects.update_or_create(
                emp_id=emp_id,
                defaults={
                    'full_name': full_name,
                    'department': department,
                    'phone': phone,
                    'role': role,
                    'username': emp_id,  # Using emp_id as the username
                    'password': make_password('Aditya@1234')  # Set a default password
                }
            )

        self.stdout.write(self.style.SUCCESS("Faculty data uploaded successfully!"))
