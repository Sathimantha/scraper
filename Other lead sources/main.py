import pandas as pd

def read_csv_structure(csv_file):
    # Read only the first few rows to get the structure
    df_structure = pd.read_csv(csv_file, nrows=0)
    return df_structure

def filter_and_display_results(csv_file, filter_date):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Convert 'IncorporationDate' column to datetime format
    df['IncorporationDate'] = pd.to_datetime(df['IncorporationDate'], errors='coerce')

    # Filter the DataFrame based on dates after the specified date
    filtered_df = df[df['IncorporationDate'] > filter_date]

    # Display the filtered results in a neat print format
    if not filtered_df.empty:
        print("\nFiltered results:")
        print(filtered_df[['CompanyName', 'IncorporationDate']].to_string(index=False))
    else:
        print("\nNo matching records found.")

if __name__ == "__main__":
    # Replace 'BasicCompanyDataAsOneFile-2023-12-04.csv' with your actual file path
    csv_file_path = 'BasicCompanyDataAsOneFile-2023-12-04.csv'

    try:
        # Read the structure of the CSV file
        df_structure = read_csv_structure(csv_file_path)
        print("Field names:")
        print(df_structure.columns)

        while True:
            filter_date_input = input("Enter the filter date (format: YYYY-MM-DD) or 'exit' to quit: ").strip()

            if filter_date_input.lower() == 'exit':
                break

            try:
                filter_date = pd.to_datetime(filter_date_input)
            except ValueError:
                print("Invalid date format. Please enter a valid date.")
                continue

            # Filter and display results based on user input
            filter_and_display_results(csv_file_path, filter_date)

    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: File '{csv_file_path}' is empty.")
    except Exception as e:
        print(f"An error occurred: {e}")
