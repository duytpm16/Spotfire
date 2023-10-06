import re
import pandas as pd
import numpy as np


def format_pas_analysis(xls, analysis):
    df = pd.read_excel(
        io=xls,
        sheet_name=analysis,
        header=None,
        dtype=str,
        names=[
            "MNEMONIC NAME",
            "FIELD SIZE",
            "DATA ELEMENT DESCRIPTION",
            "BUSINESS RULES AND EDITS",
            "CLARIFICATION / EXPLANATION OF MNEMONIC",
        ],
    )

    # Replace values in the entire DataFrame
    df.replace(
        {
            r"^\s*$": np.nan,
            "^\s": "",
            "–": "-",
            "’": "'",
            "\n": " ",
            ".DGEK": ".DEGK",
        },
        regex=True,
        inplace=True,
    )

    # Drop rows with all NaN values and with "#" or "~ (DT" (These are comments).
    df.dropna(axis=0, how="all", inplace=True)
    df = df[~df["MNEMONIC NAME"].str.startswith("#", na=False)]
    df = df[~df["MNEMONIC NAME"].str.startswith("~ (DT", na=False)]

    # Find and filter specific rows by their "MNEMONIC NAME"
    filter_rows = [
        "Sample Point Codes (SPNT)",
        "Recovery Type Codes (RXXC):…",
        "Test Type Codes: (TTYP)",
        "Test Type Codes:",
        "GENERAL EDITS",
    ]

    for row in filter_rows:
        index = df[df["MNEMONIC NAME"] == row].index
        if len(index) > 0:
            df = df.loc[: index[0] - 1, :]
            break

    # Add new section column.
    info = ""
    info_list = []
    for _, row in df.iterrows():
        if row["MNEMONIC NAME"].startswith("~"):
            info = row["MNEMONIC NAME"]
        else:
            info_list.append(info)

    # Remove rows starting with "~" in MNEMONIC NAME
    df = df[~df["MNEMONIC NAME"].str.startswith("~")]
    df["MNEMONIC NAME"] = df["MNEMONIC NAME"].str.replace(" ", "", regex=True)
    df["MNEMONIC NAME"] = [s + "." if s.count(".") == 0 else s for s in df["MNEMONIC NAME"]]

    # Add new column FIELD
    # Remove ~ FILE VERIFICATION. This is for AER
    # Remove rows starting with ~ DT or ~DT in FIELD
    df["FIELD"] = info_list
    df = df[~df["FIELD"].str.startswith("~ FILE VERIFICATION")]
    df = df[~df["FIELD"].str.startswith("~ DT")]
    df = df[~df["FIELD"].str.startswith("~DT")]
    df["FIELD"] = df["FIELD"].str.replace(r"^ +| +$", r"", regex=True)

    # Lower case this column
    df["BUSINESS RULES AND EDITS"] = df["BUSINESS RULES AND EDITS"].str.casefold()
    df["BUSINESS RULES AND EDITS"] = [re.sub(' +', ' ', str(s)) for s in df["BUSINESS RULES AND EDITS"]]

    # Remove brackets in FIELD SIZE
    df["FIELD SIZE"] = df["FIELD SIZE"].str.replace("[", "", regex=True)
    df["FIELD SIZE"] = df["FIELD SIZE"].str.replace("]", "", regex=True)

    # Add new column of the PAS type.
    df["ANALYSIS"] = analysis

    return df


if __name__ == "__main__":
    pas_file = "PASFileFormats.xls"
    pas_type = ["OAN", "WAN", "DST", "PRD", "GAN", "GRD", "TRG"]

    all_pas = [format_pas_analysis(pas_file, pas) for pas in pas_type]

    combined_pas = pd.concat(all_pas, ignore_index=True)
    combined_pas.to_csv("pas_lookup.csv", index=False, header=True, sep=",")
