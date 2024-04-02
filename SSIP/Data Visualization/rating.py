import matplotlib.pyplot as plt
import pandas as pd
import time

# Define a function to generate and display the dynamic pie chart
def generate_dynamic_pie_chart(csv_file_path):
    while True:
        if pd.io.common.file_exists(csv_file_path):
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file_path)

            # Count the number of entries for each comment
            comment_counts = df['Comments'].value_counts()

            # Create a pie chart
            plt.pie(comment_counts, labels=comment_counts.index, autopct='%0.1f%%', shadow=True, startangle=140)

            plt.title('Comments Pie Chart')
            plt.show()

        time.sleep(5)  # Check for changes every 5 seconds

# Path to the CSV file
csv_file_path = 'rajkot.csv'

# Generate and display the dynamic pie chart
generate_dynamic_pie_chart(csv_file_path)