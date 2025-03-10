import pandas as pd

# Load faculty details
faculty_file_path = "/Users/shankarsamidala/Documents/WORK/ORGS/ASCS/apmc/users/management/commands/staff.xlsx"
df_faculty = pd.read_excel(faculty_file_path, skiprows=1)

# Load student call data
calls_file_path = "/Users/shankarsamidala/Documents/WORK/ORGS/ASCS/apmc/users/management/commands/calls.csv"
df_calls = pd.read_csv(calls_file_path, skiprows=2)

# Standardize column names (strip spaces, lowercase)
df_faculty.columns = df_faculty.columns.str.strip().str.lower()
df_calls.columns = df_calls.columns.str.strip().str.lower()

# Identify faculty name columns
faculty_name_col_faculty = [col for col in df_faculty.columns if "faculty" in col or "name" in col][0]
faculty_name_col_calls = [col for col in df_calls.columns if "faculty" in col or "name" in col][0]

# Convert faculty names to strings & trim spaces
df_faculty[faculty_name_col_faculty] = df_faculty[faculty_name_col_faculty].astype(str).str.strip()
df_calls[faculty_name_col_calls] = df_calls[faculty_name_col_calls].astype(str).str.strip()



# Save cleaned data
df_faculty.to_csv("cleaned_faculty_data.csv", index=False)
df_calls.to_csv("cleaned_calls_data.csv", index=False)

print("✅ Data cleaned and saved! Ready for merging.")
