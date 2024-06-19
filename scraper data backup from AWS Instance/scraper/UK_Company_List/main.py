import pandas as pd

def read_csv_structure(csv_file):
    # Read only the first few rows to get the structure
    df_structure = pd.read_csv(csv_file, nrows=0)
    return df_structure

def filter_and_save_results(csv_file, filter_date, output_file):
    # Specify chunk size based on your system's memory capacity
    chunk_size = 10000

    # Create an empty DataFrame to store the filtered results
    filtered_results = pd.DataFrame()

    # Iterate through chunks of the CSV file
    for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
        # Convert 'IncorporationDate' column to datetime format with UK date format
        chunk['IncorporationDate'] = pd.to_datetime(chunk['IncorporationDate'], format='%d/%m/%Y', errors='coerce')

        # Filter the chunk based on the specified date
        filtered_chunk = chunk[chunk['IncorporationDate'] == filter_date]

        # Append the filtered chunk to the results DataFrame
        filtered_results = pd.concat([filtered_results, filtered_chunk], ignore_index=True)

        # Save the filtered results to the output file in real-time
        filtered_results.to_csv(output_file, index=False)

    print(f"\nFiltered results saved to '{output_file}'.")

if __name__ == "__main__":
    # Replace 'BasicCompanyDataAsOneFile-2023-12-04.csv' with your actual file path
    csv_file_path = 'BasicCompanyDataAsOneFile-2023-12-04.csv'
    
    # Replace 'output.csv' with your desired output file path
    output_file_path = 'output.csv'

    try:
        # Read the structure of the CSV file
        df_structure = read_csv_structure(csv_file_path)
        print("Field names:")
        print(df_structure.columns)

        filter_date = pd.to_datetime('04/12/2023', format='%d/%m/%Y')

        # Filter and save results based on the specified date
        filter_and_save_results(csv_file_path, filter_date, output_file_path)

    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: File '{csv_file_path}' is empty.")
    except Exception as e:
        print(f"An error occurred: {e}")

