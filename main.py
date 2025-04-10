import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("Key_Code")

# Function to check logs using GPT-4
def check_logs_with_gpt(log_file_path, output_file_path):

    # Reading the input log file
    try:
        with open(log_file_path, 'r') as log_file:
            logs = log_file.read()
    except Exception as e:
        print(f"Error reading file {log_file_path}: {e}")
        return

    # Using GPT-4 model to analyze the logs
    try:
        response = openai.Completion.create(
            model="gpt-4",
            prompt=f"Check these logs for any errors or anomalies:\n{logs}",
            max_tokens=1000,
            temperature=0.5,
        )
    except Exception as e:
        print(f"Error while making request to OpenAI: {e}")
        return

    # Getting the response from the model
    result = response.choices[0].text.strip()

    # Writing the result to a file
    try:
        with open(output_file_path, 'w') as output_file:
            output_file.write(result)
        print(f"Result written to file {output_file_path}")
    except Exception as e:
        print(f"Error writing to file {output_file_path}: {e}")

# Main logic to process all files in the input_logs folder
def process_all_logs(input_folder, output_folder):
    # Check if input_logs folder exists
    if not os.path.exists(input_folder):
        print(f"Folder {input_folder} does not exist. Creating folder.")
        os.makedirs(input_folder)  # Create input_logs folder if it doesn't exist

    # Check if output_results folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Check the contents of input_logs folder
    log_files = os.listdir(input_folder)
    if not log_files:
        print(f"No files found in folder {input_folder}. Creating test log file.")
        test_log_path = os.path.join(input_folder, 'log_file.txt')
        try:
            with open(test_log_path, 'w') as f:
                f.write("2025-03-01 12:00:00 Error: Connection lost\n")
                f.write("2025-03-01 12:05:00 Warning: High memory usage\n")
                f.write("2025-03-01 12:10:00 Info: Service restarted successfully\n")
            print(f"Test file created at {test_log_path}")
            log_files = ['log_file.txt']  # Add the created file to the list
        except Exception as e:
            print(f"Error creating test file: {e}")
            return

    # Process each file in the input_logs folder
    for log_file in log_files:
        log_file_path = os.path.join(input_folder, log_file)
        if os.path.isfile(log_file_path):
            output_file_path = os.path.join(output_folder, f"output_{log_file}")
            print(f"Processing file: {log_file}")
            check_logs_with_gpt(log_file_path, output_file_path)

# Call the function to process all logs
input_folder = 'input_logs'  # Folder containing input logs
output_folder = 'output_results'  # Folder for results

process_all_logs(input_folder, output_folder)
