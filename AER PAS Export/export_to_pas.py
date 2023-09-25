import sys
import math
import pandas as pd
from datetime import datetime


def check_valid_day_format(mnemonic, day):
    if len(day) != 3 and len(day[0]) != 4 and len(day[1]) != 2 and len(day[2]) != 2:
        sys.exit("ERROR: %s must be in [YYYY MM DD] format." % (mnemonic))


def check_char_size(mnemonic, value, size):
    if len(value) > size:
        sys.exit("ERROR: %s size is greater than %s." % (mnemonic, size))


def check_required_null(mnemonic, value):
    if value is not None:
        sys.exit("ERROR: %s must be null." % (mnemonic))


def check_required(mnemonic, value):
    if value is None:
        sys.exit("ERROR: %s must not be null." % (mnemonic))


def check_zero(mnemonic, value):
    if value == 0:
        sys.exit("ERROR: %s must not be 0." % (mnemonic))


def check_negative(mnemonic, value):
    if value < 0:
        sys.exit("ERROR: %s must not be negative." % (mnemonic))


def check_num_range(mnemonic, value, rmin, rmax):
    if not (rmin < value and value < rmax):
        sys.exit("ERROR: %s must be in valid range." % (mnemonic))


def check_code(mnemonic, value, codes):
    if value not in codes:
        msg = ", ".join([c if isinstance(c, str) else str(c) for c in codes])
        sys.exit("ERROR: %s must be any of: %s." % (mnemonic, msg))


def check_num_equal(mnemonic, value, expected):
    if value != expected:
        sys.exit("ERROR: %s must be %d." % (mnemonic, expected))


def check_less_than(m1, m2, value1, value2):
    if value1 >= value2:
        sys.exit("ERROR: %s must be less than %s." % (m1, m2))


def check_units_range(mnemonic, value, ranges):
    check_num_range(mnemonic, value, ranges[0], ranges[1])


def check_required_two(mnemonics, data):
    value1 = data[mnemonics[0]]
    value2 = data[mnemonics[1]]
    if value1 is None and value2 is None:
        sys.exit("ERROR: %s and %s must not both be null." % mnemonics)


def check_depths(depths, data):
    check_less_than(depths[0], depths[1], data[depths[0]], data[depths[1]])


def check_dstloc(mnemonic, value, spnt_value):
    if spnt_value is None or spnt_value != "50":
        check_required_null(mnemonic, value)
    else:
        check_required(mnemonic, value)


def is_date_greater(day, min_day):
    return datetime.strptime(day, "%Y %m %d").date() > min_day


class PAS:
    def __init__(self, pas_spec):
        self.version = 4.0

        self.pt = pas_spec
        self.data = {}
        self.pas_format = []
        self.pas_type = ""
        self.pastype_column = "PASTYPE."
        self.field_char = "CHAR"
        self.field_numb = "NUMB"
        self.field_day = "YYYY MM DD"
        self.field_hr = "YYYY MM DD HHHH"
        self.field_day_hr_sec = "YYYY MM DD HHHH:SS"
        self.delim = " "
        self.units_range = {
            "DEGC": (-100.00, 1000.00),
            "DEGK": (173.15, 1273.15),
            "KPA": (-math.inf, 150000.00),
            "KPAA": (-math.inf, 150000.00),
            "MPA'S": (-math.inf, 150.00),
            "M": (-math.inf, 7000.00),
            "TROOM.DEGC": (0.0, 45.0),
            "RELMM.": (80.0, 250.0),
            "RDLIQ.": (-math.inf, 1.0),
        }
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
        self.depths = ("TTOPL.M", "TBASL.M")
        self.pairs = {
            "TSUL.FRAC": ("TSUL.FRAC", "TSUL.GM/KG"),
            "TSUL.GM/KG": ("TSUL.FRAC", "TSUL.GM/KG"),
        }
        self.min_day = datetime.strptime("2004 09 30", "%Y %m %d").date()
        self.date_dependent = {
            "FS-SPRES.KPAA": "FS-SDAT.DAY",
            "FS-STEMP.DEGC": "FS-SDAT.DAY",
            "SS-SPRES.KPAA": "SS-SDAT.DAY",
            "SS-STEMP.DEGC": "SS-SDAT.DAY",
            "CL-SPRES.KPAA": "CL-SDAT.DAY",
            "CL-STEMP.DEGC": "CL-SDAT.DAY",
        }
        self.test_negative = ["> 0", ">= 0", "> = 0", "> zero"]
        self.test_null = [
            "optional",
            "mandatory, if",
            "then",
            "can be blank",
            "can be null",
            "can be zero or null",
        ]
        self.test_zero = [
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

            self.pt_zip = zip(
                self.pt["MNEMONIC NAME"],
                self.pt["FIELD"],
                self.pt["FIELD SIZE"],
                self.pt["BUSINESS RULES AND EDITS"],
            )
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
        if mnemonic in self.pairs:
            check_required_two(self.pairs[mnemonic], self.data)

        if mnemonic in self.date_dependent:
            if is_date_greater(self.data[self.date_dependent[mnemonic]], self.min_day):
                check_required(mnemonic, value)

        if rule is None or all([r not in rule for r in self.test_null]):
            check_required(mnemonic, value)

        if value is not None and not pd.isnull(value):
            if self.field_day in size:
                check_valid_day_format(mnemonic, value.split(self.delim))

            elif self.field_char in size:
                check_char_size(mnemonic, value, int(size.split(self.delim)[1]))

                if mnemonic in self.codes:
                    check_code(mnemonic, value, self.codes[mnemonic])

            else:
                value = float(value)
                units = mnemonic.split(".")
                units = units[1] if len(units) == 2 else None

                if rule is None or all([r not in rule for r in self.test_zero]):
                    check_zero(mnemonic, value)

                if rule is not None and any([r in rule for r in self.test_negative]):
                    check_negative(mnemonic, value)

                if mnemonic in self.codes:
                    check_code(mnemonic, int(value), self.codes[mnemonic])

                if units in self.units_range:
                    check_units_range(mnemonic, value, self.units_range[units])

                    if mnemonic in self.depths:
                        check_depths(self.depths, self.data)

                if mnemonic in self.units_range:
                    check_units_range(mnemonic, value, self.units_range[mnemonic])

    def check_oan_wan_data(self):
        for mnemonic, _, size, rule in self.pt_zip:
            if mnemonic == "DSTLOC.":
                check_dstloc(mnemonic, self.data[mnemonic], self.data["SPNT."])

            self.check_value(mnemonic, self.data[mnemonic], size, rule)

    def check_gan_data(self):
        for mnemonic, field, size, rule in self.pt_zip:
            value = self.data[mnemonic]

            if field in {
                "~ HEADER DATA - FIRST STAGE SEPARATOR GAS ANALYSIS",
                "~ DATA TABLE - FIRST STAGE SEPARATOR GAS ANALYSIS",
            }:
                if self.data["STYP."] == "C":
                    check_required_null(mnemonic, value)
                else:
                    self.check_value(mnemonic, value, size, rule)

            elif field == "~ HEADER DATA - SECOND STAGE SEPARATOR - GAS ANALYSIS":
                if self.data["FS-SPNT."] is None:
                    check_required_null(mnemonic, value)
                else:
                    if self.data["SEPCOND."] == "B":
                        self.check_value(mnemonic, value, size, rule)
                    else:
                        if value is not None:
                            self.check_value(mnemonic, value, size, rule)

            elif field == "~ SECOND STAGE SEPARATOR - GAS ANALYSIS":
                if self.data["SEPCOND."] == "B" and self.data["STYP."] == "R":
                    check_required(mnemonic, value)
                self.check_value(mnemonic, value, size, rule)

            elif field in {
                "~ HEADER DATA - CONDENSATE / LIQUID ANALYSIS",
                "~ DATA TABLE - CONDENSATE / LIQUID ANALYSIS",
                "~ CONDENSATE / LIQUID ANALYSIS - DATA PROPERTIES",
                "~ DATA TABLE - CONDENSATE / LIQUID FRACTION DISTILLATION",
            }:
                if self.data["HYDLP."] == "N":
                    check_required_null(mnemonic, value)
                else:
                    if field == "~ DATA TABLE - CONDENSATE / LIQUID FRACTION DISTILLATION":
                        if mnemonic in {"MOLL.FRAC", "MASS.FRAC", "VOL.FRAC", "RDLIQ."}:
                            if value is not None:
                                check_num_range(mnemonic, float(value), -math.inf, 1)
                    else:
                        if mnemonic == "H2SLP.":
                            check_required(mnemonic, value)
                        elif mnemonic == "LIQRDN.":
                            check_required(mnemonic, value)
                            check_num_range(mnemonic, float(value), -math.inf, 1)
                    self.check_value(mnemonic, value, size, rule)

            elif field in {
                "~ RECOMBINED GAS ANALYSIS - DATA PROPERTIES",
                "~ RECOMBINED GAS PROPERTIES",
            }:
                if self.data["STYP."] != "R":
                    check_required_null(mnemonic, value)
                else:
                    if mnemonic == "SS-GAS.E3M3/D" and self.data["SEPCOND."] != "B":
                        self.check_value(mnemonic, value, size, rule)
                    elif mnemonic in ["R-PPC.KPAA", "R-PTC.DEGK"]:
                        self.check_value(mnemonic, value, size, rule)
                    else:
                        check_required(mnemonic, value)
                        self.check_value(mnemonic, value, size, rule)

            elif field == "~ RECOMBINED GAS COMPOSITION":
                if self.data["STYP."] == "R":
                    check_required(mnemonic, value)
                self.check_value(mnemonic, value, size, rule)

            else:
                if mnemonic == "DSTLOC.":
                    check_dstloc(mnemonic, value, self.data["FS-SPNT."])

                elif mnemonic == "GLR.M3/M3":
                    if self.data["STYP."] == "R":
                        check_required(mnemonic, value)

                elif mnemonic in {"FLDH2S.PPM", "H2SMT."}:
                    if self.data["H2SLC."] == "L":
                        check_required_null(mnemonic, value)
                    else:
                        check_required(mnemonic, value)

                        if self.data["H2SMT."] == "N" and mnemonic == "FLDH2S.PPM":
                            check_num_equal(mnemonic, float(value), 0)

                elif mnemonic == "HYDLP.":
                    check_required(mnemonic, value)

                elif mnemonic == "LABH2S.FRAC":
                    if self.data["H2SLC."] != "F":
                        check_required(mnemonic, value)

                self.check_value(mnemonic, value, size, rule)

    def check_pas_data(self):
        if self.pas_type in {"OAN", "WAN"}:
            self.check_oan_wan_data()

        elif self.pas_type == "GAN":
            self.check_gan_data()


if __name__ == "__main__":
    dt = pd.read_csv("example/wan_text.txt", sep="\t")
    pt = pd.read_csv("unittest/pas_lookup.csv", sep=",", header=0)

    pas = PAS(pt)
    pas.subset("WAN")
    pas.format_data(dt)
    pas.check_pas_data()
