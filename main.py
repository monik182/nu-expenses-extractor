import pandas as pd
import camelot
import sys

from utils import format_table_data


def extract_and_format_table(pdf_path):
    tables = camelot.read_pdf(pdf_path, pages='2-end', flavor='stream')

    if len(tables) == 0:
        print("No tables found in the PDF.")
        return None

    combined_data = []
    for table in tables:
        df = table.df
        combined_data.append(df)

    full_table = pd.concat(combined_data, ignore_index=True)
    formatted_table = format_table_data(full_table)
    return formatted_table


def main(file_name, output_csv):
    try:
        formatted_data = extract_and_format_table(file_name)
        if formatted_data is not None:
            formatted_data.to_csv(output_csv, index=False)
            print(f"Table data successfully formatted and saved to {output_csv}")
        else:
            print("No table data extracted or formatted.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    file_name = sys.argv[1]
    if file_name == "":
        print("Please provide the file name")

    output_csv = "output.csv"
    if len(sys.argv) > 2 and sys.argv[2] != "":
        output_csv = sys.argv[2]

    if ".csv" not in output_csv:
        output_csv = output_csv + ".csv"

    main(file_name, output_csv)
