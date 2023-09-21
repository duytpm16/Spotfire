import pandas as pd
import numpy as np

def format_pas_analysis(xls, analysis):
    df = pd.read_excel(
        io=xls,
        sheet_name=analysis,
        header=None,
        dtype=str,
        names=["MNEMONIC NAME", "FIELD SIZE", "DATA ELEMENT DESCRIPTION", "BUSINESS RULES AND EDITS", "CLARIFICATION / EXPLANATION OF MNEMONIC"],
    )
    
    # Replace values in the entire DataFrame
    df.replace({
        r"^\s*$": np.nan,
        "^\s": "",
        "–": "-",
        "’": "'",
        "\n": " ",
        ".DGEK": ".DEGK",
    }, regex=True, inplace=True)

    # Drop rows with all NaN values
    df.dropna(axis=0, how="all", inplace=True)

    # Filter out rows starting with "#"
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
            df = df.loc[:index[0] - 1, :]

    info = ""
    info_list = []

    # Process rows with "~" and "~ DT" or "~DT"
    for _, row in df.iterrows():
        if row["MNEMONIC NAME"].startswith("~"):
            info = row["MNEMONIC NAME"]
        else:
            if info.startswith("~ DT") or info.startswith("~DT"):
                info_list.append("Remove")
            else:
                info_list.append(info)

    # Remove rows starting with "~"
    df = df[~df["MNEMONIC NAME"].str.startswith("~")]

    # Add new columns and transformations
    df["FIELD"] = info_list
    df["FIELD"] = df["FIELD"].str.replace(r"^ +| +$", r"", regex=True)
    df["ANALYSIS"] = analysis
    df["BUSINESS RULES AND EDITS"] = df["BUSINESS RULES AND EDITS"].str.casefold()
    df = df[~df.FIELD.str.startswith("~ FILE VERIFICATION")]
    df = df[~df.FIELD.str.startswith("Remove")]
    df['MNEMONIC NAME'] = df['MNEMONIC NAME'].str.replace(" ", "", regex=True)
    df['MNEMONIC NAME'] = [s + "." if s.count('.') == 0 else s for s in df['MNEMONIC NAME']]
    df['FIELD SIZE'] = df['FIELD SIZE'].str.replace("[", "", regex=True)
    df['FIELD SIZE'] = df['FIELD SIZE'].str.replace(']', "", regex=True)

    return df

if __name__ == "__main__":
    xls = "PASFileFormats.xls"
    analysis_list = ["OAN", "WAN", "DST", "PRD", "GAN", "GRD", "TRG"]
    
    all_dfs = [format_pas_analysis(xls, analysis) for analysis in analysis_list]
    
    combined_df = pd.concat(all_dfs, ignore_index=True)
    combined_df.to_csv("pas_lookup.csv", index=False, header=True, sep=",")