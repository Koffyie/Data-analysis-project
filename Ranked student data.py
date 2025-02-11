import pandas as pd
import glob

#Checking for all the csv files.
file_list = ["CNG202.csv", "BAT101.csv", "ENG401.csv"]
data_frames = []

#Required columns for validation.
required_columns = {'Student ID', 'Firstname', 'Last name', 'CA Score', 'Exam Score'}

for file in file_list:
    try:
#Reading the file.        
       df = pd.read_csv(file)
    
#Validate columns.
       if not required_columns.issubset(df.columns):
            print(f"Error: {file} is missing required columns.")
            continue
        
#Handle missing values
       df['CA Score'] = df['CA Score'].fillna(0)
       df['Exam Score'] = df['Exam Score'].fillna(0)
        
    
       df['Total Score'] = df['CA Score'] + df['Exam Score']

#Drop the duplicates and handle missing Student IDs.
       df = df.drop_duplicates(subset=['Student ID'])
       if df['Student ID'].isnull().any():
           print(f"Warning: Missing Student IDs in {file}. These rows were ignored.")
       data_frames.append(df)
    except FileNotFoundError:
        print(f"File not found: {file}")
    except pd.errors.EmptyDataError:
        print(f"File is empty or corrupted: {file}")
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Combine all dataframes
if not data_frames:
    print("No valid data files were processed.")
else:
#Combining all the data into one dataframe with concatenation-adding the rows.
    combined_df = pd.concat(data_frames)

#Creating full name column.
    combined_df['Full_Name'] = combined_df['Firstname'] + " " + combined_df['Last name']
	
#Calculating total and average scores for each student across all files.
    student_data = combined_df.groupby('Student ID').agg(
     Full_Name=('Full_Name', 'first'), #To avoid repetition.
    Total_Score=('Total Score', 'sum')
)

student_data['Average Score'] = student_data['Total_Score'] / 3

#Ranking students based on their average scores.
student_data['Rank'] = student_data['Average Score'].rank(ascending=False, method='dense').astype(int)

#Saving the results to a new CSV file.
student_data = student_data.reset_index()
student_data = student_data[['Student ID', 'Full_Name', 'Average Score', 'Rank']]
student_data.to_csv("Ranked_student_data.csv", index=False)

print("Student rankings have been saved to 'Ranked_student_data.csv'.")
	
