import math
import random
import unittest
import pandas as pd

from test_export_to_pas import TestPAS


class TestOAN(unittest.TestCase):

    pas = TestPAS()


    def test_a(self):
        self.pas.subset_pas("OAN")


    def test_char(self):
        mnemonics = {
            "CNAM.": {"optional": True},
            "CNUM.": {"optional": True},
            "FORM.": {"optional": False},
            "GCOM.": {"optional": True},
            "IDENT.": {"optional": False},
            "LABCO.": {"optional": False},
            "LFNUM.": {"optional": False},
            "METHD.": {"optional": True},
            "OANC.": {"optional": True},
            "PASTYPE.": {"optional": False},
            "SPNTN.": {"optional": False},
            "UWI.": {"optional": False},
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
                "ADNCL.KG/M3": {"optional": False, "allow_zero": False, "allow_neg": True},
                "ADNRX.KG/M3": {"optional": True, "allow_zero": True, "allow_neg": True},
                "API.": {"optional": True, "allow_zero": True, "allow_neg": True},
                "BSW.FRAC": {"optional": True, "allow_zero": True, "allow_neg": True},
                "BSWS.FRAC": {"optional": True, "allow_zero": True, "allow_neg": True},
                "BSWW.FRAC": {"optional": True, "allow_zero": True, "allow_neg": True},
                "CFACT.": {"optional": True, "allow_zero": True, "allow_neg": True},
                "CONRD.FRAC": {"optional": True, "allow_zero": True, "allow_neg": True},
                "DVLGO.FRAC": {"optional": True, "allow_zero": True, "allow_neg": True},
                "DVLKR.FRAC": {"optional": True, "allow_zero": True, "allow_neg": True},
                "DVLLS.FRAC": {"optional": True, "allow_zero": True, "allow_neg": True},
                "DVLNP.FRAC": {"optional": True, "allow_zero": True, "allow_neg": True},
                "DVLRC.FRAC": {"optional": True, "allow_zero": True, "allow_neg": True},
                "DVLRS.FRAC": {"optional": True, "allow_zero": True, "allow_neg": True},
                "RAMBT.FRAC": {"optional": True, "allow_zero": True, "allow_neg": True},
                "RDNCL.": {"optional": True, "allow_zero": True, "allow_neg": True},
                "RDNRX.": {"optional": True, "allow_zero": True, "allow_neg": True},
                "TSALT.KG/M3": {"optional": True, "allow_zero": True, "allow_neg": True},
                "UKIN1.MM2/S": {"optional": False, "allow_zero": False, "allow_neg": False},
                "VERS.": {"optional": False, "allow_zero": False, "allow_neg": True}
            }
            | {
                "UKIN%s.MM2/S" % (i): {"optional": True, "allow_zero": False, "allow_neg": False} for i in range(2, 7)
            }
            | {
                "DVL%s.FRAC" % (i): {"optional": True, "allow_zero": False, "allow_neg": True} for i in range(1, 21)
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
        mnemonics = (
            {
                "CRKBP.DEGC": {"optional": True, "allow_zero": False, "allow_neg": True},
                "FBP.DEGC": {"optional": True, "allow_zero": False, "allow_neg": True},
                "IBP.DEGC": {"optional": True, "allow_zero": False, "allow_neg": True},
                "PPTASTM.DEGC": {"optional": True, "allow_zero": True, "allow_neg": True},
                "PPTUSBM.DEGC": {"optional": True, "allow_zero": True, "allow_neg": True},
                "RTEMP.DEGC": {"optional": True, "allow_zero": True, "allow_neg": True},
                "STEMP.DEGC": {"optional": True, "allow_zero": True, "allow_neg": True},
                "UT1.DEGC": {"optional": False, "allow_zero": False, "allow_neg": False}
            }
            | {
                "UT%s.DEGC" % (i): {"optional": True, "allow_zero": False, "allow_neg": False} for i in range(2, 7)
            }
            | {
                "DTP%s.DEGC" % (i): {"optional": True, "allow_zero": False, "allow_neg": True} for i in range(1, 21)
            }
        )

        for mnemonic, config in mnemonics.items():
            self.pas.unit_degC_test_sequence(mnemonic, config)


    def test_unit_kPa(self):
        mnemonics = {
            "PBARA.KPAA": {"optional": True, "allow_zero": False, "allow_neg": True},
            "RPRES.KPAA": {"optional": True, "allow_zero": False, "allow_neg": True},
            "RVP.KPAA": {"optional": True, "allow_zero": True, "allow_neg": True},
            "SPRES.KPAA": {"optional": True, "allow_zero": False, "allow_neg": True}
        }

        for mnemonic, config in mnemonics.items():
            self.pas.unit_kPa_test_sequence(mnemonic, config)


    def test_unit_mPa(self):
        mnemonics = (
            {
                "UAB1.MPA'S": {"optional": False, "allow_zero": False, "allow_neg": False}
            } 
            | {
                "UAB%s.MPA'S" % (i): {"optional": True, "allow_zero": False, "allow_neg": False}for i in range(2, 7)
            }
        )

        for mnemonic, config in mnemonics.items():
            self.pas.unit_mPa_test_sequence(mnemonic, config)


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


    def test_troom_degC(self):
        mnemonic = "TROOM.DEGC"
        config = {"optional": True, "allow_zero": False, "allow_neg": False}

        # Test TROOM.DEGC. Value should be > 0 and < 45.
        self.pas.check_null(mnemonic, config)
        self.pas.check_zero(mnemonic, config)
        self.pas.check_negative(mnemonic, config, -99.999, 0)
        self.pas.check_out_of_range(mnemonic, -1e6, 0)
        self.pas.check_out_of_range(mnemonic, 45, 1e6)
        self.pas.check_within_range(mnemonic, 0.001, 45)


    def test_tsul(self):
        mnemonic1 = "TSUL.FRAC"
        mnemonic2 = "TSUL.GM/KG"

        # Either one of TSUL.FRAC or TSUL.GM/KG should be present.
        self.pas.pas.data[mnemonic1] = None
        self.pas.pas.data[mnemonic2] = None
        self.pas.check_assert_raised()

        # Mnemonic2 is null then Mnemonic1 must be present.
        # Hence optional=False for mnemonic1.
        self.pas.pas.data[mnemonic1] = random.uniform(-1e6, 1e6)
        self.pas.pas.data[mnemonic2] = None
        self.pas.check_null(mnemonic1, {"optional": False})
        self.pas.check_zero(mnemonic1, {"allow_zero": True})
        self.pas.check_negative(mnemonic1, {"allow_neg": True}, -1e6, 0)
        self.pas.check_within_range(mnemonic1, -1e6, 1e6)

        # Mnemonic1 is null then Mnemonic2 must be present.
        # Hence optional=False for mnemonic2.
        self.pas.pas.data[mnemonic1] = None
        self.pas.pas.data[mnemonic2] = random.uniform(-1e6, 1e6)
        self.pas.check_null(mnemonic2, {"optional": False})
        self.pas.check_zero(mnemonic2, {"allow_zero": True})
        self.pas.check_negative(mnemonic2, {"allow_neg": True}, -1e6, 0)
        self.pas.check_within_range(mnemonic2, -1e6, 1e6)

        # Both mnemonic1 and mnemonic2 are present.
        self.pas.pas.data[mnemonic1] = random.uniform(-1e6, 1e6)
        self.pas.pas.data[mnemonic2] = random.uniform(-1e6, 1e6)
        config = {"optional": True, "allow_zero": True, "allow_neg": True}
        for mnemonic in {mnemonic1, mnemonic2}:
            self.pas.numb_test_sequence(mnemonic, config)


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
