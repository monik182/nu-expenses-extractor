import pdfplumber
import pandas as pd
import camelot
import re

# Path to your PDF file
pdf_path = "./file.pdf"
output_csv = "formatted_table_4.csv"



# Function to extract tables from the PDF
# def extract_table_from_pdf(pdf_path):
#     data = []
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             if page == 0:
#                 continue
#             # Extract table data from the current page
#             print(f"Extracting tables from page {page.page_number}...")
#             # print(page)
#             print(page.extract_tables())
#             if page.extract_tables():
#                 for table in page.extract_tables():
#                     data.extend(table)  # Append all rows from the table

#     # Convert extracted data into a pandas DataFrame
#     df = pd.DataFrame(data[1:], columns=data[0])  # Assuming first row as headers
#     return df



# def extract_table_with_camelot(pdf_path):
#     # Parsing the PDF for tables
#     tables = camelot.read_pdf(pdf_path, pages='2-end', flavor='stream')

#     # Check if tables are detected
#     if len(tables) == 0:
#         print("No tables found in the PDF.")
#         return None

#     # Combine all detected tables into one DataFrame
#     combined_data = []
#     for table in tables:
#         # Convert each table into a DataFrame
#         df = table.df
#         combined_data.append(df)

#     # Concatenate all tables
#     full_table = pd.concat(combined_data, ignore_index=True)
#     return full_table


def extract_and_format_table(pdf_path):
    # Extract tables using Camelot, skipping the first page
    tables = camelot.read_pdf(pdf_path, pages='2-end', flavor='stream')

    # Check if tables are detected
    if len(tables) == 0:
        print("No tables found in the PDF.")
        return None

    # Combine all detected tables into one DataFrame
    combined_data = []
    for table in tables:
        df = table.df
        combined_data.append(df)

    # Concatenate all tables into a single DataFrame
    full_table = pd.concat(combined_data, ignore_index=True)

    # Format the table according to the rules
    # full_table.dropna(axis=1, how='all', inplace=True)
    # Drop the index
    # full_table = full_table.reset_index(drop=True, inplace=True)
    # full_table = full_table.set_index(0)
    # formatted_table = format_table(full_table)
    formatted_table = format_table_data(full_table)
    return formatted_table


# def format_table_0(df):
#     # Step 1: Remove the first row if it's numeric
#     # print(df.head(5))
#     # if df.iloc[0].apply(lambda x: isinstance(x, (int, float))).all():
#     #     df = df.drop(0).reset_index(drop=True)

#     # Step 2: Combine the second and third rows into one header row
#     if len(df) > 2:
#         header_row = df.iloc[0] + ' ' + df.iloc[1]
#         df.columns = header_row
#         df = df.drop([0, 1]).reset_index(drop=True)

#     # Step 3: Remove any subsequent rows matching the combined header row
#     df = df[~df.apply(lambda row: row.equals(header_row), axis=1)]

#     # Step 4: Merge records (rows) based on the logic
#     merged_records = []
#     current_record = []
#     previous_cell = None
#     for index, row in df.iterrows():
#         first_cell = str(row[0])
#         print(first_cell)
#         if first_cell == 'Fecha':
#             previous_cell = first_cell
#             continue

#         if previous_cell == 'Fecha':
#             previous_cell = None
#             continue
        

#         # Check if the row is the start of a new record (DD MMM pattern)
#         if re.match(r'^\d{2} \w{3}$', first_cell):
#             if current_record:
#                 merged_records.append(' '.join(current_record))
#             current_record = [first_cell]  # Start a new record
#         else:
#             current_record.append(' '.join(row.dropna().astype(str)))  # Merge the row into current record

#         # Check if the row contains "Pago mínimo", marking the end of the table
#         if 'Pago mínimo' in first_cell:
#             if current_record:
#                 merged_records.append(' '.join(current_record))
#             break

#     # Create a DataFrame from the merged records
#     formatted_df = pd.DataFrame(merged_records, columns=df.columns)
    # return formatted_df

def format_table_data(df):
    # Step 1: Remove the first row if it’s numeric
    if df.iloc[0].apply(lambda x: x.isnumeric()).any():
        df = df.iloc[1:]

    # Step 2: Combine 2nd and 3rd rows to create a header
    header_row = df.iloc[0] + " " + df.iloc[1]
    df.columns = header_row
    df = df.iloc[2:]  # Remove the original 2nd and 3rd rows

    # Step 3: Remove duplicate headers if any
    df = df.loc[~(df.iloc[:, 0] == header_row[0])]

    # Step 4: Identify records to merge
    merged_records = []
    current_record = []
    previous_cell = None
    for _, row in df.iterrows():
        # Check if the row starts a new record
        first_cell = row.iloc[0]
        if isinstance(first_cell, str) and len(first_cell.split()) == 2:
            if current_record:  # Add the previous record
                merged_records.append(current_record)
            current_record = [row]
        else:
                        # print(first_cell)
            if first_cell == 'Fecha':
                previous_cell = first_cell
                continue

            if previous_cell == 'Fecha':
                previous_cell = None
                continue
            current_record.append(row)  # Append to the current record

        # Check for the end marker
        if "Pago mínimo" in row.to_string():
            break

    if current_record:  # Add the last record
        merged_records.append(current_record)

    # Step 5: Merge rows for each record
    formatted_data = []
    for record in merged_records:
        # Merge rows by combining text from all cells
        merged_row = record[0].copy()
        for additional_row in record[1:]:
            merged_row = merged_row.fillna("") + " " + additional_row.fillna("")
        formatted_data.append(merged_row)

    # Create a new DataFrame with formatted records
    formatted_df = pd.DataFrame(formatted_data)
    return formatted_df

try:
    formatted_data = extract_and_format_table(pdf_path)
    if formatted_data is not None:
        # Save to CSV
        formatted_data.to_csv(output_csv, index=False)
        print(f"Table data successfully formatted and saved to {output_csv}")
    else:
        print("No table data extracted or formatted.")
except Exception as e:
    print(f"Error: {e}")

# Main code THIS WORKS
# try:
#     extracted_data = extract_table_with_camelot(pdf_path)
#     if extracted_data is not None:
#         # Save to CSV
#         output_csv = "extracted_table_camelot2.csv"
#         extracted_data.to_csv(output_csv, index=False)
#         print(f"Table data successfully extracted and saved to {output_csv}")
#     else:
#         print("No table data extracted.")
# except Exception as e:
#     print(f"Error: {e}")

# # Extract and save the table
# try:
#     df = extract_table_from_pdf(pdf_path)
#     output_csv = "extracted_table.csv"
#     df.to_csv(output_csv, index=False)
#     print(f"Table data successfully extracted to {output_csv}")
# except Exception as e:
#     print(f"Error: {e}")
