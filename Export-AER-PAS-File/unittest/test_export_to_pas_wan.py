import math
import random
import unittest
import pandas as pd

from test_export_to_pas import TestPAS


class TestWAN(unittest.TestCase):

    pas = TestPAS()


    def test_a(self):
        self.pas.subset_pas("WAN")


    def test_char(self):
        mnemonics = {
            "FORM.": {"optional": False},
            "GCOM.": {"optional": True},
            "IDENT.": {"optional": False},
            "LABCO.": {"optional": False},
            "LFNUM.": {"optional": False},
            "PASTYPE.": {"optional": False},
            "SPNTN.": {"optional": False},
            "UWI.": {"optional": False},
            "WANC.": {"optional": True},
            "WLIC.": {"optional": False}
        }

        for mnemonic, config in mnemonics.items():
            self.pas.char_test_sequence(mnemonic, config)


    def test_char_code(self):
        mnemonics = {"UNIT.": {"optional": False}}

        for mnemonic, config in mnemonics.items():
            self.pas.char_code_test_sequence(mnemonic, config)


    def test_numb(self):
        mnemonics = (
            {
                "DSCAL.MG/L": {"optional": False, "allow_zero": False, "allow_neg": False},
                "PEOHM.": {"optional": True, "allow_zero": True, "allow_neg": True},
                "PHOBS.": {"optional": False, "allow_zero": False, "allow_neg": False},
                "RDWTR.": {"optional": True, "allow_zero": True, "allow_neg": True},
                "RFIDX.": {"optional": True, "allow_zero": True, "allow_neg": True},
                "SALT.PCT": {"optional": True, "allow_zero": True, "allow_neg": True},
                "VERS.": {"optional": False, "allow_zero": False, "allow_neg": True}
            }
            | {
                "%s.MG/L" % (ion): {"optional": False, "allow_zero": True, "allow_neg": True} for ion in ["NA", "K", "CA", "MG", "CL", "HCO3", "SO4", "CO3", "OH", "H2S"]
            }
            | {
                "%s.MEQ/L" % (ion): {"optional": False, "allow_zero": True, "allow_neg": True} for ion in ["NA", "K", "CA", "MG", "CL", "HCO3", "SO4", "CO3", "OH"]
            }
            | {
                "%s.MG/L" % (ion): {"optional": True, "allow_zero": True, "allow_neg": True} for ion in ["BA", "SR", "FE", "MN", "B", "BR", "I", "DS110", "DS180", "DSING"]
            }
            | {
                "%s.MEQ/L" % (ion): {"optional": True, "allow_zero": True, "allow_neg": True} for ion in ["BA", "SR", "FE", "MN", "B", "BR", "I"]
            }
        )

        for mnemonic, config in mnemonics.items():
            self.pas.numb_test_sequence(mnemonic, config)


    def test_numb_code(self):
        mnemonics = {
            "DRILLEG.": {"optional": False},
            "SPNT.": {"optional": False},
            "WSFL.": {"optional": False}
        }

        for mnemonic, config in mnemonics.items():
            self.pas.numb_code_test_sequence(mnemonic, config)


    def test_unit_degC(self):
        mnemonics = {
            "PETMP.DEGC": {"optional": True, "allow_zero": True, "allow_neg": True},
            "PHTMP.DEGC": {"optional": False, "allow_zero": False, "allow_neg": False},
            "RDTMP.DEGC": {"optional": True, "allow_zero": True, "allow_neg": True},
            "RFTMP.DEGC": {"optional": True, "allow_zero": True, "allow_neg": True},
            "RTEMP.DEGC": {"optional": True, "allow_zero": False, "allow_neg": True},
            "STEMP.DEGC": {"optional": True, "allow_zero": False, "allow_neg": True}
        }

        for mnemonic, config in mnemonics.items():
            self.pas.unit_degC_test_sequence(mnemonic, config)


    def test_unit_kPa(self):
        mnemonics = {
            "RPRES.KPAA": {"optional": True, "allow_zero": False, "allow_neg": True},
            "SPRES.KPAA": {"optional": True, "allow_zero": False, "allow_neg": True}
        }

        for mnemonic, config in mnemonics.items():
            self.pas.unit_kPa_test_sequence(mnemonic, config)


    def test_dstloc(self):
        mnemonic = "DSTLOC."
        dependent1 = "SPNT."

        # SPNT is required. Set SPNT to '50'.
        # Mnemonic is required and must be a valid code, hence optional=False.
        # See DSTLOC codes in PAS format file.
        self.pas.pas.data[dependent1] = 50
        self.pas.char_code_test_sequence(mnemonic, {"optional": False})

        # SPNT is required. Set SPNT != '50'.
        # Mnemonic must be null.
        self.pas.pas.data[dependent1] = random.choice([x for x in self.pas.pas.codes[dependent1] if x != 50])
        self.pas.char_code_null_only_test_sequence(mnemonic)

        del self.pas.pas.data[mnemonic]
        del self.pas.pas.data[dependent1]


    def test_depths(self):
        # Both depths are required. The program should exit with error.
        self.pas.pas.data["TTOPL.M"] = None
        self.pas.pas.data["TBASL.M"] = None
        self.pas.check_assert_raised()

        # Depths cannot be 0. The program should exit with error for both cases.
        self.pas.pas.data["TTOPL.M"] = 0
        self.pas.pas.data["TBASL.M"] = random.uniform(0.001, 7000)
        self.pas.check_assert_raised()

        self.pas.pas.data["TTOPL.M"] = random.uniform(0.001, 7000)
        self.pas.pas.data["TBASL.M"] = 0
        self.pas.check_assert_raised()

        # Depths cannot be negative. The program should exit with error for both cases.
        self.pas.pas.data["TTOPL.M"] = -random.uniform(0.001, 7000)
        self.pas.pas.data["TBASL.M"] = random.uniform(0.001, 7000)
        self.pas.check_assert_raised()

        self.pas.pas.data["TTOPL.M"] = random.uniform(0.001, 7000)
        self.pas.pas.data["TBASL.M"] = -random.uniform(0.001, 7000)
        self.pas.check_assert_raised()

        # TTOPL.M should be < TBASL.M. The program should exit with error.
        self.pas.pas.data["TTOPL.M"] = random.uniform(0.001, 7000)
        self.pas.pas.data["TBASL.M"] = random.uniform(0.001, self.pas.pas.data["TTOPL.M"])
        self.pas.check_assert_raised()

        # Depths are in valid range and TTOPL < TBASL. Program should not exit with error.
        self.pas.pas.data["TBASL.M"] = random.uniform(0.001, 7000)
        self.pas.pas.data["TTOPL.M"] = random.uniform(0.0001, self.pas.pas.data["TBASL.M"])
        self.pas.check_not_assert_raised()


if __name__ == "__main__":
    unittest.main()
