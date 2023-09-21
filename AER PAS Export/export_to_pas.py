import sys
import math
import pandas as pd
from datetime import datetime


def check_day(mnemonic, day):
    if len(day) != 3 and len(day[0]) != 4 and len(day[1]) != 2 and len(day[2]) != 2:
        sys.exit("ERROR: %s must be in [YYYY MM DD] format." % (mnemonic))


def check_char_size(mnemonic, value, size):
    if value is not None and len(value) > int(size):
        sys.exit("ERROR: %s size is greater than %s." % (mnemonic, size))


def check_required_null(mnemonic, value):
    if value is not None:
        sys.exit("ERROR: %s must be null." % (mnemonic))


def check_required(mnemonic, value):
    if value is None:
        sys.exit("ERROR: %s must not be null." % (mnemonic))


def check_required_two(m1, m2, value1, value2):
    if value1 is None and value2 is None:
        sys.exit("ERROR: %s and %s must not both be null." % (m1, m2))


def check_zero(mnemonic, value):
    if value is not None and value == 0:
        sys.exit("ERROR: %s must not be 0." % (mnemonic))


def check_negative(mnemonic, value):
    if value is not None and value < 0:
        sys.exit("ERROR: %s must not be negative." % (mnemonic))


def check_num_equal(mnemonic, value, expected):
    if value is not None and float(value) != expected:
        sys.exit("ERROR: %s must be %d." % (mnemonic, expected))


def check_less_than(m1, m2, value1, value2):
    if float(value1) >= float(value2):
        sys.exit("ERROR: %s must be less than %s." % (m1, m2))


def check_code(mnemonic, value, codes):
    if value not in codes:
        msg = ", ".join([c if isinstance(c, str) else str(c) for c in codes])
        sys.exit("ERROR: %s must be any of: %s." % (mnemonic, msg))


def check_num_range(mnemonic, value, rmin, rmax):
    if value is not None and not (rmin < value and value < rmax):
        sys.exit("ERROR: %s must be in valid range." % (mnemonic))


def check_units_range(mnemonic, value, ranges):
    rmin, rmax = ranges
    check_num_range(mnemonic, value, rmin, rmax)


def check_global_depths(global_depths, data):
    depth1, depth2 = global_depths
    check_required(depth1, data[depth1])
    check_required(depth2, data[depth2])
    check_less_than(depth1, depth2, data[depth1], data[depth2])


def check_dstloc(mnemonic, value, spnt_value):
    if spnt_value is None or spnt_value != "50":
        check_required_null(mnemonic, value)
        return False

    check_required(mnemonic, value)
    return True


def sdat_greater(day, min_day):
    return datetime.strptime(day, "%Y %m %d").date() > min_day


class PAS:
    def __init__(self, pas_spec):
        self.pt = pas_spec
        self.data = {}
        self.pas_format = []
        self.pas_type = ""
        self.pastype_column = "PASTYPE."
        self.version = 4.0
        self.field_char = "CHAR"
        self.field_numb = "NUMB"
        self.field_day = "YYYY MM DD"
        self.field_hr = "YYYY MM DD HHHH"
        self.field_day_hr_sec = "YYYY MM DD HHHH:SS"
        self.delim = " "
        self.general_units = {
            "DEGC": (-100.00, 1000.00),
            "DEGK": (173.15, 1273.15),
            "KPA": (-math.inf, 150000.00),
            "KPAA": (-math.inf, 150000.00),
            "MPA'S": (-math.inf, 150.00),
            "M": (-math.inf, 7000.00),
        }
        self.min_day = datetime.strptime("2004 09 30", "%Y %m %d").date()
        self.codes = {
            "AIN.": ["Y", "N"],
            "AFLO.": ["A", "C", "T", "B"],
            "AOFTY.": [1, 2, 31, 32, 41],
            "AWSVAL.": ["Y", "N"],
            "CL-SPNT.": [20, 25, 30, 35, 40, 45, 50, 60, 70],
            "CUTP.": [1, 2, 3, 4, 5],
            "DPTS.": ["Y", "N"],
            "DRILLEG.": [1, 2, 3, 4, 5, 6, 7, 8, 9],
            "DSTLOC.": ["T", "M", "B"],
            "FLEXP.": [1, 2, 6, 17],
            "FS-SPNT.": [20, 25, 30, 35, 40, 45, 50, 60, 70],
            "GPOS.": ["I", "O", "R", "B", "N", "U"],
            "H2SIND.": ["Y", "N"],
            "H2SLC.": ["F", "L", "B"],
            "H2SLP.": ["N", "T", "M"],
            "H2SMT.": ["T", "L", "C", "O", "S", "N"],
            "HYDLP.": ["Y", "N"],
            "INJFL.": [1, 2, 6],
            "INTRP.": ["Y", "N"],
            "LIQGPT.": ["F", "S", "T"],
            "LIQT.": ["O", "C", "W"],
            "LIT.": ["Y", "N"],
            "LQMTYP.": ["T", "L", "V", "O"],
            "MDTYPE.": ["P", "O", "T", "i", "C", "V", "H"],
            "MSRN.": ["Y", "N"],
            "MSRNG.": ["Y", "N"],
            "MTST": ["Y", "N"],
            "MTST.": ["Y", "N"],
            "PACKER.": ["Y", "N"],
            "PLIND.": ["O", "W", "C", "E", "T"],
            "POOL.": ["Y", "N"],
            "PRPS.": ["I", "A", "O"],
            "PRSTY.": [4, 5, 6, 11, 12, 14, 15, 24, 34, 50],
            "PVT": ["Y", "N"],
            "RPXX.": ["V", "H", "N"],
            "RRUN.": ["Y", "N"],
            "RTNUM.": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "E"],
            "SEPCOND.": ["F", "B"],
            "SLIND.": ["O", "W", "C", "E", "T"],
            "SPNT.": [20, 25, 30, 35, 40, 45, 50, 60, 70],
            "SS-SPNT.": [20, 25, 30, 35, 40, 45, 50, 60, 70],
            "STYP.": ["G", "C", "B", "R"],
            "SURBTM.": ["S", "B"],
            "TAP.": ["F", "P"],
            "TAPL.": ["U", "D"],
            "TMEA.": ["I", "C"],
            "TTYP.": ["3", "10", "13", "23", "33", "43"],
            "TULD.": ["Y", "N"],
            "UNIT.": ["M"],
            "WSFL.": [1, 2, 6, 17],
            "WTYP.": ["V", "D", "H"],
        }
        self.global_depths = ("TTOPL.M", "TBASL.M")
        self.test_negative = ["> 0", ">= 0", "> = 0", "> zero"]
        self.ignore_null = [
            "optional",
            "mandatory, if",
            "then",
            "can be blank",
            "can be null",
            "can be zero or null",
        ]
        self.ignore_zero = [
            "> = 0",
            ">= 0",
            "can = zero",
            "can be zero",
            "can  be zero",
            "can be null or zero",
            "can be blank or zero",
            "can be null, negative or zero",
        ]

    def subset(self, pastype):
        if self.pt["ANALYSIS"].eq(pastype).any():
            self.pas_type = pastype

            column = "BUSINESS RULES AND EDITS"
            self.pt[column] = [None if pd.isnull(s) else s for s in self.pt[column]]

            self.pt = self.pt[self.pt["ANALYSIS"].str.match(pastype)]
            self.pas_format = self.pt["FIELD"].unique()
        else:
            sys.exit("ERROR: Cannot find PAS type [%s] does not exists." % pastype)

    def format_data(self, data_table):
        self.data = {
            mnemonic: (
                str(data_table[mnemonic][0])
                if self.field_char in field_size
                else str(data_table[mnemonic][0])
                if self.field_day in field_size
                else "%02d" % (int(data_table[mnemonic][0]))
                if self.field_numb in field_size and "," not in field_size
                else "{:.{}f}".format(
                    float(data_table[mnemonic][0]),
                    int(field_size.split(" ")[1].split(",")[1]),
                )
            )
            if mnemonic in data_table.columns and not pd.isnull(data_table[mnemonic][0])
            else None
            for mnemonic, field_size in zip(
                self.pt["MNEMONIC NAME"], self.pt["FIELD SIZE"]
            )
        }

    def check_value(self, mnemonic, value, size, rule):
        if rule is None or all([r not in rule for r in self.ignore_null]):
            check_required(mnemonic, value)

        if self.field_day in size:
            check_day(mnemonic, value.split(self.delim))

        elif self.field_char in size:
            check_char_size(mnemonic, value, size.split(self.delim)[1])

            if mnemonic in self.codes:
                check_code(mnemonic, value, self.codes[mnemonic])

        else:
            value = None if pd.isnull(value) else float(value)
            units = mnemonic.split(".")[1] if len(mnemonic.split(".")) == 2 else None

            if rule is None or (all([text not in rule for text in self.ignore_zero])):
                check_zero(mnemonic, value)

            if rule is not None and any([text in rule for text in self.test_negative]):
                check_negative(mnemonic, value)

            if mnemonic in self.codes:
                inumb = None if value is None else int(value)
                check_code(mnemonic, inumb, self.codes[mnemonic])

            if units in self.general_units:
                check_units_range(mnemonic, value, self.general_units[units])

    def check_oan_data(self):
        for mnemonic, size, rule in zip(
            self.pt["MNEMONIC NAME"],
            self.pt["FIELD SIZE"],
            self.pt["BUSINESS RULES AND EDITS"],
        ):
            value = self.data[mnemonic]

            if mnemonic == "DSTLOC.":
                if check_dstloc(mnemonic, value, self.data["SPNT."]):
                    self.check_value(mnemonic, value, size, rule)

            elif mnemonic == "TROOM.DEGC":
                if value is not None:
                    check_num_range(mnemonic, float(value), 0.0, 45.0)
                self.check_value(mnemonic, value, size, rule)

            elif mnemonic in ["TSUL.FRAC", "TSUL.GM/KG"]:
                tsul1, tsul2 = ("TSUL.FRAC", "TSUL.GM/KG")
                check_required_two(tsul1, tsul2, self.data[tsul1], self.data[tsul2])
                self.check_value(mnemonic, value, size, rule)

            elif mnemonic in self.global_depths:
                check_global_depths(self.global_depths, self.data)
                self.check_value(mnemonic, value, size, rule)

            else:
                self.check_value(mnemonic, value, size, rule)

    def check_wan_data(self):
        for mnemonic, size, rule in zip(
            self.pt["MNEMONIC NAME"],
            self.pt["FIELD SIZE"],
            self.pt["BUSINESS RULES AND EDITS"],
        ):
            value = self.data[mnemonic]

            if mnemonic == "DSTLOC.":
                if check_dstloc(mnemonic, value, self.data["SPNT."]):
                    self.check_value(mnemonic, value, size, rule)

            elif mnemonic in self.global_depths:
                check_global_depths(self.global_depths, self.data)
                self.check_value(mnemonic, value, size, rule)

            else:
                self.check_value(mnemonic, value, size, rule)

    def check_gan_data(self):
        for mnemonic, field, size, rule in zip(
            self.pt["MNEMONIC NAME"],
            self.pt["FIELD"],
            self.pt["FIELD SIZE"],
            self.pt["BUSINESS RULES AND EDITS"],
        ):
            value = self.data[mnemonic]

            if field == "~ HEADER DATA - FIRST STAGE SEPARATOR GAS ANALYSIS":
                if self.data["STYP."] == "C":
                    check_required_null(mnemonic, value)
                else:
                    if mnemonic in ["FS-SPRES.KPAA", "FS-STEMP.DEGC"]:
                        if sdat_greater(self.data["FS-SDAT.DAY"], self.min_day):
                            check_required(mnemonic, value)

                    self.check_value(mnemonic, value, size, rule)

            elif field == "~ DATA TABLE - FIRST STAGE SEPARATOR GAS ANALYSIS":
                if self.data["STYP."] == "C":
                    check_required_null(mnemonic, value)
                else:
                    self.check_value(mnemonic, value, size, rule)

            elif field == "~ HEADER DATA - SECOND STAGE SEPARATOR - GAS ANALYSIS":
                if self.data["FS-SPNT."] is None:
                    check_required_null(mnemonic, value)
                else:
                    if self.data["SEPCOND."] == "B":
                        if mnemonic in ["SS-SPRES.KPAA", "SS-STEMP.DEGC"]:
                            if sdat_greater(self.data["SS-SDAT.DAY"], self.min_day):
                                check_required(mnemonic, value)

                        self.check_value(mnemonic, value, size, rule)
                    else:
                        if value is not None:
                            self.check_value(mnemonic, value, size, rule)

            elif field == "~ SECOND STAGE SEPARATOR - GAS ANALYSIS":
                if self.data["SEPCOND."] == "B" and self.data["STYP."] == "R":
                    check_required(mnemonic, value)

                self.check_value(mnemonic, value, size, rule)

            elif field == "~ HEADER DATA - CONDENSATE / LIQUID ANALYSIS":
                if self.data["HYDLP."] != "Y":
                    check_required_null(mnemonic, value)

                else:
                    if mnemonic in ["CL-SPRES.KPAA", "CL-STEMP.DEGC"]:
                        if sdat_greater(self.data["CL-SDAT.DAY"], self.min_day):
                            check_required(mnemonic, value)

                    self.check_value(mnemonic, value, size, rule)

            elif field == "~ DATA TABLE - CONDENSATE / LIQUID ANALYSIS":
                if self.data["HYDLP."] != "Y":
                    check_required_null(mnemonic, value)

                else:
                    self.check_value(mnemonic, value, size, rule)

            elif field == "~ CONDENSATE / LIQUID ANALYSIS - DATA PROPERTIES":
                if self.data["HYDLP."] == "N":
                    check_required_null(mnemonic, value)

                else:
                    if mnemonic == "H2SLP.":
                        check_required(mnemonic, value)
                        self.check_value(mnemonic, value, size, rule)

                    elif mnemonic == "LIQRDN.":
                        check_required(mnemonic, value)
                        check_zero(mnemonic, float(value))
                        check_num_range(mnemonic, float(value), -math.inf, 1)

                    else:
                        self.check_value(mnemonic, value, size, rule)

            elif field == "~ DATA TABLE - CONDENSATE / LIQUID FRACTION DISTILLATION":
                if self.data["HYDLP."] == "N":
                    check_required_null(mnemonic, value)

                else:
                    if mnemonic == "LIQCOMP.":
                        self.check_value(mnemonic, value, size, rule)

                    elif mnemonic == "RELMM.":
                        if value is not None:
                            check_zero(mnemonic, float(value))
                            check_negative(mnemonic, float(value))
                            check_num_range(mnemonic, float(value), 80, 250)

                    elif mnemonic == "RDLIQ.":
                        if value is not None:
                            check_zero(mnemonic, float(value))
                            check_num_range(mnemonic, float(value), -math.inf, 1)

                    else:
                        if value is not None:
                            check_num_range(mnemonic, float(value), -math.inf, 1)

            elif field == "~ RECOMBINED GAS ANALYSIS - DATA PROPERTIES":
                if self.data["STYP."] != "R":
                    check_required_null(mnemonic, value)

                else:
                    if mnemonic == "FS-GAS.E3M3/D":
                        if self.data["SEPCOND."] in ["F", "B"]:
                            check_required(mnemonic, value)
                        self.check_value(mnemonic, value, size, rule)

                    elif mnemonic == "SS-GAS.E3M3/D":
                        if self.data["SEPCOND."] == "B":
                            check_required(mnemonic, value)
                        self.check_value(mnemonic, value, size, rule)

                    else:
                        check_required(mnemonic, value)
                        self.check_value(mnemonic, value, size, rule)

            elif field == "~ RECOMBINED GAS COMPOSITION":
                if self.data["STYP."] == "R":
                    check_required(mnemonic, value)

                self.check_value(mnemonic, value, size, rule)

            elif field == "~ RECOMBINED GAS PROPERTIES":
                if self.data["STYP."] != "R":
                    check_required_null(mnemonic, value)

                else:
                    if mnemonic in ["R-PPC.KPAA", "R-PTC.DEGK"]:
                        self.check_value(mnemonic, value, size, rule)

                    else:
                        check_required(mnemonic, value)
                        self.check_value(mnemonic, value, size, rule)

            else:
                if mnemonic == "DSTLOC.":
                    if check_dstloc(mnemonic, value, self.data["FS-SPNT."]):
                        self.check_value(mnemonic, value, size, rule)

                elif mnemonic == "GLR.M3/M3":
                    if self.data["STYP."] == "R":
                        check_required(mnemonic, value)

                    self.check_value(mnemonic, value, size, rule)

                elif mnemonic == "FLDH2S.PPM":
                    if self.data["H2SLC."] not in ["F", "B"]:
                        check_required_null(mnemonic, value)

                    else:
                        if self.data["H2SMT."] == "N":
                            check_required(mnemonic, value)
                            check_num_equal(mnemonic, float(value), 0)

                        else:
                            check_required(mnemonic, value)
                            self.check_value(mnemonic, value, size, rule)

                elif mnemonic == "HYDLP.":
                    check_required(mnemonic, value)
                    self.check_value(mnemonic, value, size, rule)

                elif mnemonic == "H2SMT.":
                    if self.data["H2SLC."] == "L":
                        check_required_null(mnemonic, value)

                    else:
                        check_required(mnemonic, value)
                        self.check_value(mnemonic, value, size, rule)

                elif mnemonic == "LABH2S.FRAC":
                    if self.data["H2SLC."] in ["B", "L"]:
                        check_required(mnemonic, value)

                    self.check_value(mnemonic, value, size, rule)

                elif mnemonic in self.global_depths:
                    check_global_depths(self.global_depths, self.data)
                    self.check_value(mnemonic, value, size, rule)

                else:
                    self.check_value(mnemonic, value, size, rule)

    def check_pas_data(self):
        if self.pas_type == "OAN":
            self.check_oan_data()

        elif self.pas_type == "WAN":
            self.check_wan_data()

        elif self.pas_type == "GAN":
            self.check_gan_data()


if __name__ == "__main__":
    dt = pd.read_csv("example_data/wan_text.txt", sep="\t")
    pt = pd.read_csv("pas_lookup.csv", sep=",", header=0)

    pas = PAS(pt)
    pas.subset("WAN")
    pas.format_data(dt)
    pas.check_pas_data()
