import pandas as pd
import camelot

pdf_path = "./file.pdf"
output_csv = "formatted_table_4.csv"


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


def format_table_data(df):
    if df.iloc[0].apply(lambda x: x.isnumeric()).any():
        df = df.iloc[1:]

    header_row = df.iloc[0] + " " + df.iloc[1]
    df.columns = header_row
    df = df.iloc[2:]

    df = df.loc[~(df.iloc[:, 0] == header_row[0])]

    merged_records = []
    current_record = []
    previous_cell = None
    for _, row in df.iterrows():
        first_cell = row.iloc[0]
        if isinstance(first_cell, str) and len(first_cell.split()) == 2:
            if current_record:
                merged_records.append(current_record)
            current_record = [row]
        else:
            if first_cell == 'Fecha':
                previous_cell = first_cell
                continue

            if previous_cell == 'Fecha':
                previous_cell = None
                continue
            current_record.append(row)

        if "Pago mínimo" in row.to_string():
            break

    if current_record:
        merged_records.append(current_record)

    formatted_data = []
    for record in merged_records:
        merged_row = record[0].copy()
        for additional_row in record[1:]:
            merged_row = merged_row.fillna("") + " " + additional_row.fillna("")
        formatted_data.append(merged_row)

    formatted_df = pd.DataFrame(formatted_data)
    return formatted_df

try:
    formatted_data = extract_and_format_table(pdf_path)
    if formatted_data is not None:
        formatted_data.to_csv(output_csv, index=False)
        print(f"Table data successfully formatted and saved to {output_csv}")
    else:
        print("No table data extracted or formatted.")
except Exception as e:
    print(f"Error: {e}")
