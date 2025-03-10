import pandas as pd
from users.models import Faculty, StudentCall

# Load the cleaned students data
students_df = pd.read_csv(r"/Users/shankarsamidala/Documents/WORK/ORGS/ASCS/apmc/users/management/commands/cleaned_calls.csv")

# Convert faculty_id to integer or string (whichever matches the Faculty model)
students_df['faculty_id'] = students_df['faculty_id'].astype('Int64').astype(str)

# Iterate over the DataFrame and create StudentCall objects
for index, row in students_df.iterrows():
    try:
        faculty_id_str = str(int(float(row['faculty_id']))) if pd.notnull(row['faculty_id']) else None  # Ensures faculty_id is an integer string
        
        # Use the correct field name (update emp_id if necessary)
        faculty = Faculty.objects.get(emp_id=faculty_id_str)  # Adjust field name if necessary

        student_call = StudentCall.objects.create(
            faculty=faculty,
            student_name=row['student_name'],
            phone_1=str(int(float(row['phone_number_1']))) if pd.notnull(row['phone_number_1']) else None,
            phone_2=str(int(float(row['phone_number_2']))) if pd.notnull(row['phone_number_2']) else None,
            inter_group=row.get('inter_group', None),
            inter_marks=row.get('inter_marks', None),
            exam_rank=row.get('exam_rank', None),
            call_1_status='P',  # Default to pending
            # call_2_status='pending',
            # call_3_status='pending'
        )
        print(f"Added: {student_call}")

    except Faculty.DoesNotExist:
        print(f"Faculty not found for {row['faculty_name']} (ID: {faculty_id_str}), skipping...")
    except Exception as e:
        print(f"Error processing {row['student_name']}: {e}")

print("Data import completed!")
