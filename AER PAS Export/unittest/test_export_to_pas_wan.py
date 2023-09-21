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
            field_size = self.pas.get_char_size(mnemonic)

            self.pas.check_null(mnemonic, config)
            self.pas.check_char_out_of_range(mnemonic, field_size)
            self.pas.check_char_within_range(mnemonic, field_size)


    def test_char_code(self):
        mnemonics = {
            "UNIT.": {"optional": False}
        }

        for mnemonic, config in mnemonics.items():
            field_size = self.pas.get_char_size(mnemonic)
            self.pas.check_null(mnemonic, config)
            self.pas.check_char_out_of_range(mnemonic, field_size)
            self.pas.check_char_code_out_of_range(mnemonic)
            self.pas.check_code_within_range(mnemonic)


    def test_numb(self):
        mnemonics = {"DSCAL.MG/L": {"optional": False, "allow_zero": False, "allow_neg": False},
            "PEOHM.": {"optional": True, "allow_zero": True, "allow_neg": True},
            "PHOBS.": {"optional": False, "allow_zero": False, "allow_neg": False},
            "RDWTR.": {"optional": True, "allow_zero": True, "allow_neg": True},            
            "RFIDX.": {"optional": True, "allow_zero": True, "allow_neg": True},
            "SALT.PCT": {"optional": True, "allow_zero": True, "allow_neg": True},
            "VERS.": {"optional": False, "allow_zero": False, "allow_neg": True}} | {
                "%s.MG/L" % (ion): {"optional": False, "allow_zero": True, "allow_neg": True} for ion in ["NA", "K", "CA", "MG", "CL", "HCO3", "SO4", "CO3", "OH", "H2S"]} | {
                "%s.MEQ/L" % (ion): {"optional": False, "allow_zero": True, "allow_neg": True} for ion in ["NA", "K", "CA", "MG", "CL", "HCO3", "SO4", "CO3", "OH"]} | {
                "%s.MG/L" % (ion): {"optional": True, "allow_zero": True, "allow_neg": True} for ion in ["BA", "SR", "FE", "MN", "B", "BR", "I", "DS110", "DS180", "DSING"]} | {
                "%s.MEQ/L" % (ion): {"optional": True, "allow_zero": True, "allow_neg": True} for ion in ["BA", "SR", "FE", "MN", "B", "BR", "I"]}
        
        
        for mnemonic, config in mnemonics.items():
            self.pas.check_null(mnemonic, config)
            self.pas.check_zero(mnemonic, config)
            self.pas.check_negative(mnemonic, config, 1, 100)
            self.pas.check_within_range(mnemonic, -math.inf, math.inf)


    def test_numb_code(self):
        mnemonics = {
            "DRILLEG.": {"optional": False},
            "SPNT.": {"optional": False},
            "WSFL.": {"optional": False}
        }

        for mnemonic, config in mnemonics.items():
            self.pas.check_null(mnemonic, config)
            self.pas.check_numb_code_out_of_range(mnemonic)
            self.pas.check_code_within_range(mnemonic)


    def test_unit_degC(self):
        mnemonics = {        
            "PETMP.DEGC": {"optional": True, "allow_zero": True, "allow_neg": True},
            "PHTMP.DEGC": {"optional": False, "allow_zero": False, "allow_neg": False},
            "RDTMP.DEGC": {"optional": True, "allow_zero": True, "allow_neg": True},
            "RFTMP.DEGC": {"optional": True, "allow_zero": True, "allow_neg": True},
            "RTEMP.DEGC": {"optional": True, "allow_zero": False, "allow_neg": True},
            "STEMP.DEGC": {"optional": True, "allow_zero": False, "allow_neg": True}}

        for mnemonic, config in mnemonics.items():
            self.pas.check_null(mnemonic, config)
            self.pas.check_zero(mnemonic, config)
            self.pas.check_negative(mnemonic, config, 0.001, 100, 100, 500)
            self.pas.check_out_of_range(mnemonic, 1000, 1500)
            self.pas.check_within_range(mnemonic, 0.001, 1000)
    

    def test_unit_kPa(self):
        mnemonics = {
            "RPRES.KPAA": {"optional": True, "allow_zero": False, "allow_neg": True},
            "SPRES.KPAA": {"optional": True, "allow_zero": False, "allow_neg": True}}

        for mnemonic, config in mnemonics.items():
            self.pas.check_null(mnemonic, config)
            self.pas.check_zero(mnemonic, config)
            self.pas.check_negative(mnemonic, config, 1, 100)
            self.pas.check_out_of_range(mnemonic, 150000, 200000)
            self.pas.check_within_range(mnemonic, 0.001, 150000)


    def test_dstloc(self):
        mnemonics = {"DSTLOC.": {"optional": True}}
        dependent = "SPNT."

        for mnemonic, config in mnemonics.items():
            field_size = self.pas.get_char_size(mnemonic)

            self.pas.pas.data[dependent] = str(random.choice([x for x in self.pas.pas.codes[dependent] if x != 50]))
            self.pas.pas.data[mnemonic] = random.choice(self.pas.pas.codes[mnemonic])
            self.pas.check_assert_raised()
            self.pas.check_null(mnemonic, config)
            
            self.pas.pas.data[dependent] = "50"
            self.pas.check_null(mnemonic, {"optional": False})
            self.pas.check_char_out_of_range(mnemonic, field_size)
            self.pas.check_char_code_out_of_range(mnemonic)
            self.pas.check_code_within_range(mnemonic)

            del self.pas.pas.data[mnemonic]
                

    def test_global_depths(self):
        mnemonics = {  
            "TTOPL.M": {"optional": False, "allow_zero": False, "allow_neg": False},
            "TBASL.M": {"optional": False, "allow_zero": False, "allow_neg": False}}
    
        self.pas.pas.data["TTOPL.M"] = None
        self.pas.pas.data["TBASL.M"] = None
        self.pas.check_assert_raised()

        self.pas.pas.data["TTOPL.M"] = 0
        self.pas.pas.data["TBASL.M"] = random.uniform(0.001, 7000)
        self.pas.check_assert_raised()

        self.pas.pas.data["TTOPL.M"] = random.uniform(0.001, 7000)
        self.pas.pas.data["TBASL.M"] = 0
        self.pas.check_assert_raised()

        self.pas.pas.data["TTOPL.M"] = -random.uniform(0.001, 7000)
        self.pas.pas.data["TBASL.M"] = random.uniform(0.001, 7000)
        self.pas.check_assert_raised()

        self.pas.pas.data["TTOPL.M"] = random.uniform(0.001, 7000)
        self.pas.pas.data["TBASL.M"] = -random.uniform(0.001, 7000)
        self.pas.check_assert_raised()

        self.pas.pas.data["TTOPL.M"] = random.uniform(0.001, 7000)
        self.pas.pas.data["TBASL.M"] = random.uniform(0.001, self.pas.pas.data["TTOPL.M"])
        self.pas.check_assert_raised()

        self.pas.pas.data["TBASL.M"] = random.uniform(0.001, 7000)
        self.pas.pas.data["TTOPL.M"] = random.uniform(0.0001, self.pas.pas.data["TBASL.M"])
        self.pas.check_not_assert_raised()


if __name__ == "__main__":
    unittest.main()