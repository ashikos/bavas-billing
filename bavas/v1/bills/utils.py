
import pandas as pd

def Generate_bill_pdf(request, sponsors):
    """Function to Generate Sponsor logos pdf"""

    elements = []

    return elements


def Check_amount_type(df, row):
    """Function to Generate Sponsor logos pdf"""

    amount, gpay, is_credit_received = None, None, False
    if not pd.isna(df.iloc[row, 6]):
        amount = None if pd.isna(df.iloc[row, 6]) else df.iloc[row, 6]
    elif not pd.isna(df.iloc[row, 7]):
        gpay = None if pd.isna(df.iloc[row, 7]) else df.iloc[row, 7]
        if gpay == None:
            amount = None if pd.isna(df.iloc[row, 13]) else df.iloc[row, 13]
    elif not pd.isna(df.iloc[row, 9]):
        amount = None if pd.isna(df.iloc[row, 9]) else df.iloc[row, 9]
        is_credit_received = True
    elif not pd.isna(df.iloc[row, 10]):
        gpay = None if pd.isna(df.iloc[row, 10]) else df.iloc[row, 10]
        is_credit_received = True
    elif not pd.isna(df.iloc[row, 12]):
        amount = None if pd.isna(df.iloc[row, 12]) else df.iloc[row, 12]
    elif not pd.isna(df.iloc[row, 13]):
        gpay = None if pd.isna(df.iloc[row, 13]) else df.iloc[row, 13]
    elif not pd.isna(df.iloc[row, 15]):
        amount = None if pd.isna(df.iloc[row, 15]) else df.iloc[row, 15]
        is_credit_received = True
    elif not pd.isna(df.iloc[row, 16]):
        gpay = None if pd.isna(df.iloc[row, 16]) else df.iloc[row, 16]
        is_credit_received = True

    print(amount, gpay, is_credit_received)

    return amount, gpay, is_credit_received