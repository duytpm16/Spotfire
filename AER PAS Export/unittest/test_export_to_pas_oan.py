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
        mnemonics = {
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
            "VERS.": {"optional": False, "allow_zero": False, "allow_neg": True}} | {
                "DVL%s.FRAC" % (i): {"optional": True, "allow_zero": False, "allow_neg": True} for i in range(1, 21)}
        
        for mnemonic, config in mnemonics.items():
            self.pas.check_null(mnemonic, config)
            self.pas.check_zero(mnemonic, config)
            self.pas.check_negative(mnemonic, config, 1, 100)
            self.pas.check_within_range(mnemonic, -1e6, 1e6)


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
            "CRKBP.DEGC": {"optional": True, "allow_zero": False, "allow_neg": True},
            "FBP.DEGC": {"optional": True, "allow_zero": False, "allow_neg": True},
            "IBP.DEGC": {"optional": True, "allow_zero": False, "allow_neg": True},            
            "PPTASTM.DEGC": {"optional": True, "allow_zero": True, "allow_neg": True},
            "PPTUSBM.DEGC": {"optional": True, "allow_zero": True, "allow_neg": True},
            "RTEMP.DEGC": {"optional": True, "allow_zero": True, "allow_neg": True},
            "STEMP.DEGC": {"optional": True, "allow_zero": True, "allow_neg": True}} | {
                "DTP%s.DEGC" % (i): {"optional": True, "allow_zero": False, "allow_neg": True} for i in range(1, 21) }

        for mnemonic, config in mnemonics.items():
            self.pas.check_null(mnemonic, config)
            self.pas.check_zero(mnemonic, config)
            self.pas.check_negative(mnemonic, config, 0.001, 100, 100, 500)
            self.pas.check_out_of_range(mnemonic, 1000, 1500)
            self.pas.check_within_range(mnemonic, -100, 1000)
    

    def test_unit_kPa(self):
        mnemonics = {
            "PBARA.KPAA": {"optional": True, "allow_zero": False, "allow_neg": True},
            "RPRES.KPAA": {"optional": True, "allow_zero": False, "allow_neg": True},
            "RVP.KPAA": {"optional": True, "allow_zero": True, "allow_neg": True},
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
                

    def test_troom_degC(self):
        mnemonics = {  
            "TROOM.DEGC": {"optional": True, "allow_zero": False, "allow_neg": False}}
        
        for mnemonic, config in mnemonics.items():
            self.pas.check_null(mnemonic, config)
            self.pas.check_zero(mnemonic, config)
            self.pas.check_negative(mnemonic, config, 0.001, 100)
            self.pas.check_out_of_range(mnemonic, 45.001, 1000)
            self.pas.check_within_range(mnemonic, 0.001, 45)


    def test_tsul(self):
        mnemonic1 = "TSUL.FRAC"
        mnemonic2 = "TSUL.GM/KG"
        
        self.pas.pas.data[mnemonic1] = None
        self.pas.pas.data[mnemonic2] = None
        self.pas.check_assert_raised()

        self.pas.pas.data[mnemonic1] = random.uniform(-1e6, 1e6)
        self.pas.pas.data[mnemonic2] = None
        self.pas.check_null(mnemonic1, {"optional": False})
        self.pas.check_zero(mnemonic1, {"allow_zero": True})
        self.pas.check_negative(mnemonic1, {"allow_neg": True}, 0.001, 100)
        self.pas.check_within_range(mnemonic1, -1e6, 1e6)

        self.pas.pas.data[mnemonic1] = None
        self.pas.pas.data[mnemonic2] = random.uniform(-1e6, 1e6)
        self.pas.check_null(mnemonic2, {"optional": False})
        self.pas.check_zero(mnemonic2, {"allow_zero": True})
        self.pas.check_negative(mnemonic2, {"allow_neg": True}, 0.001, 100)
        self.pas.check_within_range(mnemonic2, -1e6, 1e6)

    
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

    
    def test_ukin(self):
        mnemonics = {"UKIN1.MM2/S": {"optional": False, "allow_zero": False, "allow_neg": False}} | {
                "UKIN%s.MM2/S" % (i): {"optional": True, "allow_zero": False, "allow_neg": False} for i in range(2, 7)}
        
        for mnemonic, config in mnemonics.items():
            self.pas.check_null(mnemonic, config)
            self.pas.check_zero(mnemonic, config)
            self.pas.check_negative(mnemonic, config, 1, 100)
            self.pas.check_within_range(mnemonic, 0.001, 1e6)

    def test_uab(self):
        mnemonics = {
            "UAB1.MPA'S": {"optional": False, "allow_zero": False, "allow_neg": False} } | {
                "UAB%s.MPA'S" % (i): {"optional": True, "allow_zero": False, "allow_neg": False} for i in range(2, 7)}

        for mnemonic, config in mnemonics.items():
            self.pas.check_null(mnemonic, config)
            self.pas.check_zero(mnemonic, config)
            self.pas.check_negative(mnemonic, config, 1, 100)
            self.pas.check_out_of_range(mnemonic, 150, 1500)
            self.pas.check_within_range(mnemonic, 0.001, 150)

    def test_ut_degC(self):
        mnemonics = {"UT1.DEGC": {"optional": False, "allow_zero": False, "allow_neg": False}} | {
                "UT%s.DEGC" % (i): {"optional": True, "allow_zero": False, "allow_neg": False} for i in range(2, 7)}

        for mnemonic, config in mnemonics.items():
            self.pas.check_null(mnemonic, config)
            self.pas.check_zero(mnemonic, config)
            self.pas.check_negative(mnemonic, config, 0.001, 100, 100, 500)
            self.pas.check_out_of_range(mnemonic, 1000, 1500)
            self.pas.check_within_range(mnemonic, 0.001, 1000)

if __name__ == "__main__":
    unittest.main()