import pandas as pd
import math


def format_amount(amount):
    print(amount)
    if not amount:
        return amount
    if amount != amount:
        return amount
    if not isinstance(amount, str) and (math.isnan(amount) or amount.isnumeric()):
        return amount
    return amount.replace("$", "").replace(" ", "").replace(".", "").replace(",", ".")


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
        if isinstance(first_cell, str) and len(first_cell.split()) >= 2:
            amount_cell = row.iloc[-2]
            formatted_amount = format_amount(amount_cell)
            row.iloc[-2] = formatted_amount
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
