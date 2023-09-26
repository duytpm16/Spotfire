import sys
import math
import random
import string
import unittest
import pandas as pd

from test_export_to_pas import TestPAS


class TestGAN(unittest.TestCase):

    pas = TestPAS()


    def char_test_sequence(self, mnemonic, config):
        field_size = self.pas.get_char_size(mnemonic)
            
        self.pas.check_null(mnemonic, config)
        self.pas.check_char_out_of_range(mnemonic, field_size)
        self.pas.check_char_within_range(mnemonic, field_size)


    def char_code_test_sequence(self, mnemonic, config):
        field_size = self.pas.get_char_size(mnemonic)
        
        self.pas.check_null(mnemonic, config)
        self.pas.check_char_out_of_range(mnemonic, field_size)
        self.pas.check_char_code_out_of_range(mnemonic)
        self.pas.check_code_within_range(mnemonic)


    def numb_test_sequence(self, mnemonic, config):
        self.pas.check_null(mnemonic, config)
        self.pas.check_zero(mnemonic, config)
        self.pas.check_negative(mnemonic, config, 1, 100)
        self.pas.check_within_range(mnemonic, -1e6, 1e6)


    def numb_code_test_sequence(self, mnemonic, config):
        self.pas.check_null(mnemonic, config)
        self.pas.check_numb_code_out_of_range(mnemonic)
        self.pas.check_code_within_range(mnemonic)

    
    def unit_degC_test_sequence(self, mnemonic, config):
        self.pas.check_null(mnemonic, config)
        self.pas.check_zero(mnemonic, config)
        self.pas.check_negative(mnemonic, config, 0.001, 100, 100, 500)
        self.pas.check_out_of_range(mnemonic, 1000, 1500)
        self.pas.check_within_range(mnemonic, 0.001, 1000)


    def unit_degK_test_sequence(self, mnemonic, config):
        self.pas.check_null(mnemonic, config)
        self.pas.check_zero(mnemonic, config)
        self.pas.check_negative(mnemonic, config, 1, 100)
        self.pas.check_out_of_range(mnemonic, 1273.15, 1500)
        self.pas.check_within_range(mnemonic, 173.15, 1273.15)


    def unit_kPa_test_sequence(self, mnemonic, config):
        self.pas.check_null(mnemonic, config)
        self.pas.check_zero(mnemonic, config)
        self.pas.check_negative(mnemonic, config, 1, 100)
        self.pas.check_out_of_range(mnemonic, 150000, 200000)
        self.pas.check_within_range(mnemonic, 0.001, 150000)


    def numb_null_only_test_sequence(self, mnemonic):
        self.pas.check_out_of_range(mnemonic, -1e6, 0)
        self.pas.check_out_of_range(mnemonic, 0.001, 1e6)
        self.pas.check_zero(mnemonic, {"allow_zero": False})
        self.pas.check_null(mnemonic, {"optional": True})

    
    def numb_code_null_only_test_sequence(self, mnemonic):
        self.pas.pas.data[mnemonic] = random.randint(0, 100)
        self.pas.check_assert_raised()
        self.pas.check_null(mnemonic, {"optional": True})


    def char_null_only_test_sequence(self, mnemonic):
        self.pas.check_out_of_range(mnemonic, -1e6, 0)
        self.pas.check_out_of_range(mnemonic, 0, 1e6)
        self.pas.check_null(mnemonic, {"optional": True})


    def char_code_null_only_test_sequence(self, mnemonic):
        self.pas.pas.data[mnemonic] = random.choice(string.ascii_uppercase)
        self.pas.check_assert_raised()
        self.pas.check_null(mnemonic, {"optional": True})


    def test_a(self):
        self.pas.subset_pas("GAN")


    def test_char(self):
        mnemonics = {
            "FORM.": {"optional": False},
            "GANC.": {"optional": True},
            "LABCO.": {"optional": False},
            "PASTYPE.": {"optional": False},
            "UWI.": {"optional": False},
            "WLIC.": {"optional": False}
        }

        for mnemonic, config in mnemonics.items():
            self.char_test_sequence(mnemonic, config)


    def test_char_code(self):
        mnemonics = {
            "H2SLC.": {"optional": False},
            "HYDLP.": {"optional": False},
            "STYP.": {"optional": False},
            "UNIT.": {"optional": False}
        }

        for mnemonic, config in mnemonics.items():
            self.char_code_test_sequence(mnemonic, config)


    def test_numb(self):
        mnemonics = {
            "C7+DN.": {"optional": True, "allow_zero": False, "allow_neg": True},
            "C7+MW.": {"optional": True, "allow_zero": False, "allow_neg": True},
            "GHV.MJ/M3": {"optional": False, "allow_zero": False, "allow_neg": True},
            "GHVAGF.MJ/M3": {"optional": False, "allow_zero": False, "allow_neg": True},
            "RELDEN.": {"optional": False, "allow_zero": False, "allow_neg": True},
            "TSMW.": {"optional": False, "allow_zero": False, "allow_neg": True},
            "VERS.": {"optional": False, "allow_zero": False, "allow_neg": True}
        }
        
        for mnemonic, config in mnemonics.items():
            self.numb_test_sequence(mnemonic, config)


    def test_numb_code(self):
        mnemonics = {
            "DRILLEG.": {"optional": False},
            "WSFL.": {"optional": False}
        }

        for mnemonic, config in mnemonics.items():
            self.numb_code_test_sequence(mnemonic, config)


    def test_unit_degK(self):
        mnemonics = {
            "FS-PTC.DEGK": {"optional": False, "allow_zero": False, "allow_neg": False},
            "FS-PTCAGF.DEGK": {"optional": False, "allow_zero": False, "allow_neg": False}
        }

        for mnemonic, config in mnemonics.items():
            self.unit_degK_test_sequence(mnemonic, config)
    

    def test_unit_kPa(self):
        mnemonics = {
            "FS-PPC.KPAA": {"optional": False, "allow_zero": False, "allow_neg": True},
            "FS-PPCAGF.KPAA": {"optional":  False, "allow_zero": False, "allow_neg": True},
            "PPVP.KPAA": {"optional": True, "allow_zero": False, "allow_neg": True}}

        for mnemonic, config in mnemonics.items():
            self.unit_kPa_test_sequence(mnemonic, config)


    def test_gas_analysis_data_properties(self):
        mnemonics = {"LFNUM.": {"optional": False},
                     "IDENT.": {"optional": False}}
        self.pas.field = "~ GAS ANALYSIS - DATA PROPERTIES"

        for mnemonic, config in mnemonics.items():
            self.char_test_sequence(mnemonic, config)
            del self.pas.pas.data[mnemonic]
        self.pas.field = None

    
    def test_dstloc(self):
        mnemonics = {"DSTLOC.": {"optional": True}}
        dependent = "FS-SPNT."
        dependent2 = 'STYP.'

        self.pas.pas.data[dependent2] = random.choice([x for x in self.pas.pas.codes[dependent2] if x != 'C'])

        for mnemonic, config in mnemonics.items():
            field_size = self.pas.get_char_size(mnemonic)

            self.pas.pas.data[dependent] = str(random.choice([x for x in self.pas.pas.codes[dependent] if x != 50]))
            self.pas.pas.data[mnemonic] = random.choice(self.pas.pas.codes[mnemonic])
            self.pas.check_assert_raised()
            self.pas.check_null(mnemonic, config)
            
            self.pas.pas.data[dependent] = "50"
            self.char_code_test_sequence(mnemonic, {"optional": False})

            del self.pas.pas.data[mnemonic]
        del self.pas.pas.data[dependent]
        del self.pas.pas.data[dependent2]


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


    def test_glr_m3m3(self):
        mnemonics = {"GLR.M3/M3": {"optional": True, "allow_zero": False, "allow_neg": True}}
        dependent = 'STYP.'

        self.pas.pas.data[dependent] = 'R'
        for mnemonic, config in mnemonics.items():
            config["optional"] = False
            self.numb_test_sequence(mnemonic, config)

        self.pas.pas.data[dependent] = random.choice([x for x in self.pas.pas.codes[dependent] if x != 'R'])
        for mnemonic, config in mnemonics.items():
            config["optional"] = True
            self.numb_test_sequence(mnemonic, config)
        
        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]

    def test_fldh2s(self):
        mnemonic = "FLDH2S.PPM"
        dependent1 = "H2SLC."
        dependent2 = "H2SMT."

        self.pas.pas.data[dependent1] = 'L'
        self.pas.check_null(mnemonic, {"optional": True})
        self.pas.check_zero(mnemonic, {"allow_zero": False})
        self.pas.check_out_of_range(mnemonic, -1e6, 1e6)

        self.pas.pas.data[dependent1] = random.choice([x for x in self.pas.pas.codes[dependent1] if x != 'L'])
        self.pas.pas.data[dependent2] = 'N'
        self.pas.check_null(mnemonic, {"optional": False})
        self.pas.check_zero(mnemonic, {"allow_zero": True})
        self.pas.check_out_of_range(mnemonic, -1e6, 1e6)    

        self.pas.pas.data[dependent1] = random.choice([x for x in self.pas.pas.codes[dependent1] if x != 'L'])
        self.pas.pas.data[dependent2] = random.choice([x for x in self.pas.pas.codes[dependent2] if x != 'N'])
        self.pas.check_null(mnemonic, {"optional": False})
        self.pas.check_zero(mnemonic, {"allow_zero": True})
        self.pas.check_within_range(mnemonic, -1e6, 1e6)    
 
        del self.pas.pas.data[mnemonic]
        del self.pas.pas.data[dependent1]
        del self.pas.pas.data[dependent2]


    def test_h2smt(self):
        mnemonic  = "H2SMT."
        dependent = "H2SLC."


        # H2SLC != 'L', so mnemonic is mandatory. Hence optional=False 
        # Mnemonic must folow its rule in PAS format file.
        self.pas.pas.data[dependent] = random.choice([x for x in self.pas.pas.codes[dependent] if x != 'L'])

        self.char_code_test_sequence(mnemonic, {"optional": False})


        # H2SLC = 'L', so mnemonic is optional. Hence optional=True 
        # Mnemonic must folow its rule in PAS format file.
        self.pas.pas.data[dependent] = 'L'
        
        self.char_code_null_only_test_sequence(mnemonic)


        del self.pas.pas.data[mnemonic]
        del self.pas.pas.data[dependent]


    def test_labh2s(self):
        mnemonic, config = "LABH2S.FRAC", {"optional": True, "allow_zero": True, "allow_neg": True}
        dependent1 = "H2SLC."
 
        # H2SLC = 'F' so mnemonic is optional, hence optional=True.
        # Other dictionary item is based on PAS format file.
        self.pas.pas.data[dependent1] = 'F'

        self.numb_test_sequence(mnemonic, config)    


        # H2SLC != 'F' so mnemonic mandatory, hence optional=True.
        # Other dictionary item is based on PAS format file.
        self.pas.pas.data[dependent1] = random.choice([x for x in self.pas.pas.codes[dependent1] if x != 'F'])

        config["optional"] = False
        self.numb_test_sequence(mnemonic, config)


        del self.pas.pas.data[mnemonic]
        del self.pas.pas.data[dependent1]
  
    
    def test_header_fss_gas_analysis(self):
        mnemonics = ["FS-SPNT.", "FS-SPNTN.", "FS-RPRES.KPAA", "FS-RTEMP.DEGC"]
        char_mnemonics = {"FS-SPNTN.": {"optional": False}}
        numb_code_mnemonics = {"FS-SPNT.": {"optional": False}}
        kpa_mnemonics = {"FS-RPRES.KPAA": {"optional": False, "allow_zero": False, "allow_neg": True}}
        degC_mnemonics = {"FS-RTEMP.DEGC": {"optional": False, "allow_zero": True, "allow_neg": True}}
        dependent = "STYP."


        # STYP is not 'C', so mnemonics must follow its rule in PAS format file.
        # Dictionary is based on rule in PAS format file.
        self.pas.pas.data[dependent] = random.choice([x for x in self.pas.pas.codes[dependent] if x != 'C'])

        for mnemonic, config in char_mnemonics.items():
            self.char_test_sequence(mnemonic, config)

        for mnemonic, config in numb_code_mnemonics.items():
            self.numb_code_test_sequence(mnemonic, config)        
     
        for mnemonic, config in kpa_mnemonics.items():
            self.unit_kPa_test_sequence(mnemonic, config)

        for mnemonic, config in degC_mnemonics.items():
            self.unit_degC_test_sequence(mnemonic, config)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        # STYP is 'C', so mnemonics must be null.
        # Dictionary is based on rule in PAS format file.
        self.pas.pas.data[dependent] = 'C'

        for mnemonic, config in char_mnemonics.items():
            self.char_null_only_test_sequence(mnemonic)

        for mnemonic, config in numb_code_mnemonics.items():
            self.numb_code_null_only_test_sequence(mnemonic)
        
        for mnemonic, config in kpa_mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)

        for mnemonic, config in degC_mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]

        
        del self.pas.pas.data[dependent]


    def test_header_fss_gas_analysis_spres_stemp(self):
        mnemonics = ["FS-SPRES.KPAA", "FS-STEMP.DEGC"]
        kpa_mnemonics  = {"FS-SPRES.KPAA": {"optional": False, "allow_zero": False, "allow_neg": True}}
        degC_mnemonics = {"FS-STEMP.DEGC": {"optional": False, "allow_zero": True, "allow_neg": True}}
        dependent1 = "STYP."
        dependent2 = "FS-SDAT.DAY"


        # STYP != 'C' and Date is > 2004 09 30.
        # Mnemonics must follow its rule in PAS format file.
        # Dictionary is based on rule in PAS format file.
        date = "%04d %02d %02d" % (random.randint(2004, 9999), random.randint(10, 12), random.randint(1, 28))

        self.pas.pas.data[dependent1] = random.choice([x for x in self.pas.pas.codes[dependent1] if x != 'C'])
        self.pas.pas.data[dependent2] = date
 
        for mnemonic, config in kpa_mnemonics.items():
            self.unit_kPa_test_sequence(mnemonic, config)

        for mnemonic, config in degC_mnemonics.items():
            self.unit_degC_test_sequence(mnemonic, config)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        # STYP != 'C' and Date is <= 2004 09 30.
        # Mnemonics are optional, hence optional=True.
        # Other dictionary item is based on rule in PAS format file.
        date = "%04d %02d %02d" % (random.randint(0, 2004), random.randint(1, 9), random.randint(1, 28))

        self.pas.pas.data[dependent1] = random.choice([x for x in self.pas.pas.codes[dependent1] if x != 'C'])
        self.pas.pas.data[dependent2] = date
 
        for mnemonic, config in kpa_mnemonics.items():
            config["optional"] = True
            self.unit_kPa_test_sequence(mnemonic, config)

        for mnemonic, config in degC_mnemonics.items():
            config["optional"] = True
            self.unit_degC_test_sequence(mnemonic, config)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        # STYP = 'C', so date does not matter here.
        # All mnemonics must be null.
        self.pas.pas.data[dependent1] = 'C'
        self.pas.pas.data[dependent2] = None

        for mnemonic, config in kpa_mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)   

        for mnemonic, config in degC_mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)   

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        del self.pas.pas.data[dependent1] 
        del self.pas.pas.data[dependent2]


    def test_dt_fss_gas_analysis(self):
        self.pas.field = "~ DATA TABLE - FIRST STAGE SEPARATOR GAS ANALYSIS"
        mnemonics = ["COMPCOM.", "MOLG.FRAC", "MOLAGF.FRAC", "LIQVOL.ML/M3"]
        char_mnemonics = {"COMPCOM.": {"optional": False}}
        numb_mnemonics = {"MOLG.FRAC": {"optional": False, "allow_zero": True, "allow_neg": True},
                          "MOLAGF.FRAC": {"optional": False, "allow_zero": True, "allow_neg": True},
                          "LIQVOL.ML/M3": {"optional": False, "allow_zero": False, "allow_neg": True}}        
        dependent = "STYP."


        # STYP is not C, so mnemonics must follow its rule. 
        # Dictionary is based on rule in PAS format file.
        self.pas.pas.data[dependent] = random.choice([x for x in self.pas.pas.codes[dependent] if x != 'C'])

        for mnemonic, config in char_mnemonics.items():
            self.char_test_sequence(mnemonic, config)    

        for mnemonic, config in numb_mnemonics.items():
            self.numb_test_sequence(mnemonic, config)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        # STYP is C, so mnemonics must be null.
        # Dictionary is based on rule in PAS format file.
        self.pas.pas.data[dependent] = 'C'

        for mnemonic, config in char_mnemonics.items():
            self.char_null_only_test_sequence(mnemonic)       

        for mnemonic, config in numb_mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)          

        for mnemonics in mnemonics:
            del self.pas.pas.data[mnemonics]


        del self.pas.pas.data[dependent]
        self.pas.field = None  


    def test_header_sss_gas_analysis(self):
        mnemonics = ["SS-SPNT.", "SS-SPNTN.", "SS-RPRES.KPAA", "SS-RTEMP.DEGC"]
        char_mnemonics      = {"SS-SPNTN.": {"optional": False}}
        numb_code_mnemonics = {"SS-SPNT.": {"optional": False}}
        kpa_mnemonics       = {"SS-RPRES.KPAA": {"optional": False, "allow_zero": False, "allow_neg": True}}
        degC_mnemonics      = {"SS-RTEMP.DEGC": {"optional": False, "allow_zero": True, "allow_neg": True}}

        dependent1 = 'STYP.'
        dependent2 = "SEPCOND."
        dependent3 = "FS-SPNT."


        # STYP = 'R' and SEPCOND = 'B'. FS-SPNT must not be null (First Stage Sample exists).
        # All 'mnemonics' should follow its rule. Dictionary are based on PAS rules.
        self.pas.pas.data[dependent1] = 'R'
        self.pas.pas.data[dependent2] = 'B'
        self.pas.pas.data[dependent3] = random.choice(self.pas.pas.codes[dependent3])

        for mnemonic, config in char_mnemonics.items():
            self.char_test_sequence(mnemonic, config)

        for mnemonic, config in numb_code_mnemonics.items():
            self.numb_code_test_sequence(mnemonic, config)        
     
        for mnemonic, config in kpa_mnemonics.items():
            self.unit_kPa_test_sequence(mnemonic, config)

        for mnemonic, config in degC_mnemonics.items():
            self.unit_degC_test_sequence(mnemonic, config)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        # STYP = 'R' and SEPCOND = 'F'. FS-SPNT must not be null (First Stage Sample exists).
        # All 'mnemonics' should follow its rule. Dictionary are based on PAS rules.
        self.pas.pas.data[dependent1] = 'R'
        self.pas.pas.data[dependent2] = 'F'
        self.pas.pas.data[dependent3] = random.choice(self.pas.pas.codes[dependent3])

        for mnemonic, config in char_mnemonics.items():
            self.char_null_only_test_sequence(mnemonic)

        for mnemonic, config in numb_code_mnemonics.items():
            self.numb_code_null_only_test_sequence(mnemonic)
        
        for mnemonic, config in kpa_mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)

        for mnemonic, config in degC_mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        # STYP is not 'R' or 'C', so SEPCOND must be null. FS-SPNT must not be null (First Stage Sample exists).
        # All 'mnemonics' should be null.
        self.pas.pas.data[dependent1] = random.choice([x for x in self.pas.pas.codes[dependent1] if x != 'R' and x != 'C'])
        self.pas.pas.data[dependent2] = None
        self.pas.pas.data[dependent3] = random.choice(self.pas.pas.codes[dependent3])

        for mnemonic, config in char_mnemonics.items():
            self.char_null_only_test_sequence(mnemonic)

        for mnemonic, config in numb_code_mnemonics.items():
            self.numb_code_null_only_test_sequence(mnemonic)
        
        for mnemonic, config in kpa_mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)

        for mnemonic, config in degC_mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        # STYP is 'C', so SEPCOND must be null. FS-SPNT must be null (First Stage Sample exists).
        # All 'mnemonics' should be null.
        self.pas.pas.data[dependent1] = 'C'
        self.pas.pas.data[dependent2] = None
        self.pas.pas.data[dependent3] = None

        for mnemonic, config in char_mnemonics.items():
            self.char_null_only_test_sequence(mnemonic)

        for mnemonic, config in numb_code_mnemonics.items():
            self.numb_code_null_only_test_sequence(mnemonic)
        
        for mnemonic, config in kpa_mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)

        for mnemonic, config in degC_mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        del self.pas.pas.data[dependent1]
        del self.pas.pas.data[dependent2]
        del self.pas.pas.data[dependent3]

    def test_header_sss_gas_analysis_spres_stemp(self):
        mnemonics = ["SS-SPRES.KPAA", "SS-STEMP.DEGC"]
        kpa_mnemonics  = {"SS-SPRES.KPAA": {"optional": False, "allow_zero": False, "allow_neg": True}}
        degC_mnemonics = {"SS-STEMP.DEGC": {"optional": False, "allow_zero": True, "allow_neg": True}}

        dependent1 = 'STYP.'
        dependent2 = "SEPCOND."
        dependent3 = "FS-SPNT."
        dependent4 = "SS-SDAT.DAY"


        # STYP = 'R' and SEPCOND = 'B'. FS-SPNT must not be null (First Stage Sample exists).
        # Date is > 2004 09 30.
        # All 'mnemonics' are mandatory and should follow its rule, hence optional=False.
        date = "%04d %02d %02d" % (random.randint(2004, 9999),  random.randint(10, 12), random.randint(1, 28))
        self.pas.pas.data[dependent1] = 'R'
        self.pas.pas.data[dependent2] = 'B'
        self.pas.pas.data[dependent3] = random.choice(self.pas.pas.codes[dependent3])
        self.pas.pas.data[dependent4] = date

        for mnemonic, config in kpa_mnemonics.items():
            self.unit_kPa_test_sequence(mnemonic, config)

        for mnemonic, config in degC_mnemonics.items():
            self.unit_degC_test_sequence(mnemonic, config)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        # STYP = 'R' and SEPCOND = 'B'. FS-SPNT must not be null (First Stage Sample exists).
        # Date is <= 2004 09 30.
        # All 'mnemonics' are optional, hence optional=True.
        date = "%04d %02d %02d" % (random.randint(0, 2004), random.randint(3, 9), random.randint(1, 30))

        self.pas.pas.data[dependent1] = 'R'
        self.pas.pas.data[dependent2] = 'B'
        self.pas.pas.data[dependent3] = random.choice(self.pas.pas.codes[dependent3])
        self.pas.pas.data[dependent4] = date

        for mnemonic, config in kpa_mnemonics.items():
            config["optional"] = True
            self.unit_kPa_test_sequence(mnemonic, config)

        for mnemonic, config in degC_mnemonics.items():
            config["optional"] = True
            self.unit_degC_test_sequence(mnemonic, config)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        # STYP = 'R' and SEPCOND = 'F'. FS-SPNT must not be null (First Stage Sample exists).
        # Date does not matter since SEPCOND != 'B'. Set to None.
        # All 'mnemonics' must be null.
        self.pas.pas.data[dependent1] = 'R'
        self.pas.pas.data[dependent2] = 'F'
        self.pas.pas.data[dependent3] = random.choice(self.pas.pas.codes[dependent3])
        self.pas.pas.data[dependent4] = None

        for mnemonic, config in kpa_mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)
        
        for mnemonic, config in degC_mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        # STYP is not 'R' or 'C', so SEPCOND must be null. FS-SPNT must not be null (First Stage Sample exists).
        # Date does not matter since SEPCOND != 'B'. Set to None.
        # All 'mnemonics' must be null.
        self.pas.pas.data[dependent1] = random.choice([x for x in self.pas.pas.codes[dependent1] if x != 'R' and x != 'C'])
        self.pas.pas.data[dependent2] = None
        self.pas.pas.data[dependent3] = random.choice(self.pas.pas.codes[dependent3])    
        self.pas.pas.data[dependent4] = None

        for mnemonic, config in kpa_mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)

        for mnemonic, config in degC_mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        # STYP is 'C', so SEPCOND must be null. FS-SPNT must be null (First Stage Sample does not exists).
        # Date does not matter since SEPCOND != 'B'. Set to None.
        # All 'mnemonics' must be null.
        self.pas.pas.data[dependent1] = 'C'
        self.pas.pas.data[dependent2] = None
        self.pas.pas.data[dependent3] = None
        self.pas.pas.data[dependent4] = None

        for mnemonic, config in kpa_mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)

        for mnemonic, config in degC_mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        del self.pas.pas.data[dependent1]
        del self.pas.pas.data[dependent2]
        del self.pas.pas.data[dependent3]
        del self.pas.pas.data[dependent4]

    def test_sss_gas_analysis(self):
        mnemonics = {"SS-%s.FRAC" % (gas): {"optional": False, "allow_zero": False, "allow_neg": True} for gas in ["H2S", "CO2", "N2", "H2", "HE", "C1", "C2", "C3", "IC4", "NC4", "IC5", "NC5", "C6", "C7+"]}
        dependent1 = "STYP."
        dependent2 = "SEPCOND."
        dependent3 = "FS-SPNT."


        # STYP = 'R' and SEPCOND = 'B'. FS-SPNT must not be null (First Stage Sample exists). 
        # All 'mnemonics' are mandatory and should follow its rule, hence optional=False.
        self.pas.pas.data[dependent1] = 'R'
        self.pas.pas.data[dependent2] = 'B'
        self.pas.pas.data[dependent3] = random.choice(self.pas.pas.codes[dependent3])

        for mnemonic, config in mnemonics.items():
            self.numb_test_sequence(mnemonic, config)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        # STYP = 'R' and SEPCOND = 'F'. FS-SPNT must not be null (First Stage Sample exists). 
        # All 'mnemonics' must be null.
        self.pas.pas.data[dependent1] = 'R'
        self.pas.pas.data[dependent2] = 'F'
        self.pas.pas.data[dependent3] = random.choice(self.pas.pas.codes[dependent3])

        for mnemonic, _ in mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        # STYP is not R or C, so SEPCOND must be Null. FS-SPNT must not be null (First Stage Sample exists). 
        # All 'mnemonics' must be null.        
        self.pas.pas.data[dependent1] = random.choice([x for x in self.pas.pas.codes[dependent1] if x != 'R' and x != 'C'])
        self.pas.pas.data[dependent2] = None
        self.pas.pas.data[dependent3] = random.choice(self.pas.pas.codes[dependent3])

        for mnemonic, config in mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        # STYP is C, so SEPCOND must be Null. FS-SPNT must be null (First Stage Sample does not exists). 
        # All 'mnemonics' must be null.    
        self.pas.pas.data[dependent1] = 'C'
        self.pas.pas.data[dependent2] = None
        self.pas.pas.data[dependent3] = None

        for mnemonic, config in mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        del self.pas.pas.data[dependent1]
        del self.pas.pas.data[dependent2]
        del self.pas.pas.data[dependent3]


    def test_header_cl_analysis(self):
        mnemonics = ["CL-SPNT.", 
                     "CL-SPNTN.",
                     "CL-RPRES.KPAA",
                     "CL-RTEMP.DEGC"]
        dependent = "HYDLP."

        self.pas.pas.data[dependent] = 'Y'

        char_mnemonics = {"CL-SPNTN.": {"optional": False}}
        for mnemonic, config in char_mnemonics.items():
            self.char_test_sequence(mnemonic, config)

        numb_code_mnemonics = {"CL-SPNT.": {"optional": False}}
        for mnemonic, config in numb_code_mnemonics.items():
            self.numb_code_test_sequence(mnemonic, config)        
     
        kpa_mnemonics = {"CL-RPRES.KPAA": {"optional": True, "allow_zero": False, "allow_neg": True}}
        for mnemonic, config in kpa_mnemonics.items():
            self.unit_kPa_test_sequence(mnemonic, config)

        degC_mnemonics = {"CL-RTEMP.DEGC": {"optional": True, "allow_zero": True, "allow_neg": True}}
        for mnemonic, config in degC_mnemonics.items():
            self.unit_degC_test_sequence(mnemonic, config)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]

        self.pas.pas.data[dependent] = 'N'

        for mnemonic, config in char_mnemonics.items():
            self.pas.pas.data[mnemonic] = ''.join(random.choices(string.ascii_letters, k = random.randint(1, 1000)))
            self.pas.check_assert_raised()
            self.pas.check_null(mnemonic, {"optional": True})

        for mnemonic, config in numb_code_mnemonics.items():
            self.pas.pas.data[mnemonic] = random.randint(0, 100)
            self.pas.check_assert_raised()
            self.pas.check_null(mnemonic, {"optional": True})
        
        for mnemonic, config in kpa_mnemonics.items():
            self.pas.check_out_of_range(mnemonic, -1e6, 1e6)
            self.pas.check_null(mnemonic, {"optional": True})

        for mnemonic, config in degC_mnemonics.items():
            self.pas.check_out_of_range(mnemonic, -1e6, 1e6)
            self.pas.check_null(mnemonic, {"optional": True})

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


    def test_header_cl_analysis_spres_stemp(self):
        mnemonics = ["CL-SPRES.KPAA",
                     "CL-STEMP.DEGC"]
        dependent1 = "HYDLP."
        dependent2 = "CL-SDAT.DAY"

        date = "%04d %02d %02d" % (random.randint(2004, 9999), random.randint(10, 12), random.randint(1, 28))

        self.pas.pas.data[dependent1] = 'Y'
        self.pas.pas.data[dependent2] = date
 
        kpa_mnemonics = {"CL-SPRES.KPAA": {"optional": False, "allow_zero": False, "allow_neg": True}}
        for mnemonic, config in kpa_mnemonics.items():
            self.unit_kPa_test_sequence(mnemonic, config)

        degC_mnemonics = {"CL-STEMP.DEGC": {"optional": False, "allow_zero": True, "allow_neg": True}}
        for mnemonic, config in degC_mnemonics.items():
            self.unit_degC_test_sequence(mnemonic, config)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]

        date = "%04d %02d %02d" % (random.randint(0, 2004), random.randint(1, 9), random.randint(1, 28))

        self.pas.pas.data[dependent1] = 'Y'
        self.pas.pas.data[dependent2] = date
 
        kpa_mnemonics = {"CL-SPRES.KPAA": {"optional": True, "allow_zero": False, "allow_neg": True}}
        for mnemonic, config in kpa_mnemonics.items():
            self.unit_kPa_test_sequence(mnemonic, config)

        degC_mnemonics = {"CL-STEMP.DEGC": {"optional": True, "allow_zero": True, "allow_neg": True}}
        for mnemonic, config in degC_mnemonics.items():
            self.unit_degC_test_sequence(mnemonic, config)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]

        self.pas.pas.data[dependent1] = 'N'
        self.pas.pas.data[dependent2] = None

        for mnemonic, config in kpa_mnemonics.items():
            self.pas.check_out_of_range(mnemonic, -1e6, 1e6)
            self.pas.check_null(mnemonic, {"optional": True})

        for mnemonic, config in degC_mnemonics.items():
            self.pas.check_out_of_range(mnemonic, -1e6, 1e6)
            self.pas.check_null(mnemonic, {"optional": True})

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]
        del self.pas.pas.data[dependent2]


    def test_dt_cl_analysis(self):
        cl_mnemonics = ["COMPCOM.", 
                        "MOLC.FRAC",
                        "MASS.FRAC",
                        "VOL.FRAC"]
        dependent = "HYDLP."
        self.pas.field = "~ DATA TABLE - CONDENSATE / LIQUID ANALYSIS"
        self.pas.pas.data[dependent] = 'Y'

        mnemonic = cl_mnemonics[0]
        self.char_test_sequence(mnemonic, {"optional": False})

        mnemonics = {cl_mnemonics[1]: {"optional": True, "allow_zero": True, "allow_neg": True},
                     cl_mnemonics[2]: {"optional": True, "allow_zero": True, "allow_neg": True},
                     cl_mnemonics[3]: {"optional": True, "allow_zero": True, "allow_neg": True}}
        for mnemonic, config in mnemonics.items():
            self.numb_test_sequence(mnemonic, config)

        for cl in cl_mnemonics:
            del self.pas.pas.data[cl]
        self.pas.pas.data[dependent] = 'N'

        mnemonic = cl_mnemonics[0]
        field_size = self.pas.get_char_size(mnemonic)
        self.pas.pas.data[mnemonic] = ''.join(random.choices(string.ascii_letters, k=random.choice(list(range(1, field_size)))))
        self.pas.check_assert_raised()
        self.pas.check_null(mnemonic, {"optional": True})

        mnemonics = {cl_mnemonics[1]: {"optional": True, "allow_zero": True, "allow_neg": True},
                     cl_mnemonics[2]: {"optional": True, "allow_zero": True, "allow_neg": True},
                     cl_mnemonics[3]: {"optional": True, "allow_zero": True, "allow_neg": True}}
        for mnemonic, config in mnemonics.items():
            self.pas.pas.data[mnemonic] = random.uniform(-1e6, 1e6)
            self.pas.check_assert_raised()
            self.pas.check_null(mnemonic, config)           

        for cl in cl_mnemonics:
            del self.pas.pas.data[cl]
        self.pas.field = None

    
    def test_cl_data_properties(self):
        self.pas.field = "~ CONDENSATE / LIQUID ANALYSIS - DATA PROPERTIES"
        mnemonics = ["LFNUM.",
                     "IDENT.",
                     "H2SLP.",
                     "LH2S.PPM",
                     "LIQRDN.",
                     "LIQRMW."]
        dependent = 'HYDLP.'

        self.pas.pas.data[dependent] = 'Y'
        char_mnemonics = {"LFNUM.": {"optional": False},
                          "IDENT.": {"optional": False}}

        for mnemonic, config in char_mnemonics.items():
            self.char_test_sequence(mnemonic, config)

        char_code_mnemonics = {"H2SLP.": {"optional": False}}
        for mnemonic, config in char_code_mnemonics.items():
            self.char_code_test_sequence(mnemonic, config)        

        numb_mnemonics = {"LH2S.PPM": {"optional": True, "allow_zero": True, "allow_neg": True},
                          "LIQRMW.": {"optional": False, "allow_zero": False, "allow_neg": True}}
        for mnemonic, config in numb_mnemonics.items():
            self.numb_test_sequence(mnemonic, config)

        numb_rng_mnemonics = {"LIQRDN.": {"optional": False, "allow_zero": False, "allow_neg": True}}
        for mnemonic, config in numb_rng_mnemonics.items():
            self.pas.check_null(mnemonic, config)
            self.pas.check_zero(mnemonic, config)
            self.pas.check_negative(mnemonic, config, 1, 100)
            self.pas.check_out_of_range(mnemonic, 1, 1e6)
            self.pas.check_within_range(mnemonic, 0.001, 1)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]

        self.pas.pas.data[dependent] = 'N'

        for mnemonic, config in char_mnemonics.items():
            self.pas.pas.data[mnemonic] = ''.join(random.choices(string.ascii_letters, k = random.randint(1, 1000)))
            self.pas.check_assert_raised()
            self.pas.check_null(mnemonic, {"optional": True})

        for mnemonic, config in char_code_mnemonics.items():
            self.pas.pas.data[mnemonic] = random.choice(self.pas.pas.codes[mnemonic])
            self.pas.check_assert_raised()
            self.pas.check_char_code_out_of_range(mnemonic)
            self.pas.check_null(mnemonic, {"optional": True})

        for mnemonic, config in numb_mnemonics.items():
            self.pas.check_out_of_range(mnemonic, -1e6, 1e6)
            self.pas.check_null(mnemonic, {"optional": True})

        for mnemonic, config in numb_rng_mnemonics.items():
            self.pas.check_out_of_range(mnemonic, -1e6, 1e6)
            self.pas.check_null(mnemonic, {"optional": True})     
        
        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]

        self.pas.field = None


    def test_dt_cl_fraction_distillation(self):
        self.pas.field = "~ DATA TABLE - CONDENSATE / LIQUID FRACTION DISTILLATION"
        mnemonics = ["LIQCOMP.",
                     "MOLL.FRAC",
                     "MASS.FRAC",
                     "VOL.FRAC",
                     "RDLIQ.",
                     "RELMM."]
        dependent = 'HYDLP.'

        self.pas.pas.data[dependent] = 'Y'

        char_mnemonics = {"LIQCOMP.": {"optional": False}}
        for mnemonic, config in char_mnemonics.items():
            self.char_test_sequence(mnemonic, config)
     
        numb_rng_mnemonics = {"MOLL.FRAC": {"optional": True, "allow_zero": True, "allow_neg": True},
                              "MASS.FRAC": {"optional": True, "allow_zero": True, "allow_neg": True},
                              "VOL.FRAC": {"optional": True, "allow_zero": True, "allow_neg": True},
                              "RDLIQ.": {"optional": True, "allow_zero": False, "allow_neg": True}}
        for mnemonic, config in numb_rng_mnemonics.items():
            self.pas.check_null(mnemonic, config)
            self.pas.check_zero(mnemonic, config)
            self.pas.check_negative(mnemonic, config, 1, 100)
            self.pas.check_out_of_range(mnemonic, 1, 1e6)
            self.pas.check_within_range(mnemonic, 0.001, 1)

        numb_rng_mnemonics2 = {"RELMM.": {"optional": True, "allow_zero": False, "allow_neg": False}}
        for mnemonic, config in numb_rng_mnemonics2.items():
            self.pas.check_null(mnemonic, config)
            self.pas.check_zero(mnemonic, config)
            self.pas.check_negative(mnemonic, config, 80, 250)
            self.pas.check_out_of_range(mnemonic, -1e6, 80)
            self.pas.check_out_of_range(mnemonic, 250.001, 1e6)
            self.pas.check_within_range(mnemonic, 80, 250)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]

        self.pas.pas.data[dependent] = 'N'

        for mnemonic, config in char_mnemonics.items():
            self.pas.pas.data[mnemonic] = ''.join(random.choices(string.ascii_letters, k = random.randint(1, 1000)))
            self.pas.check_assert_raised()
            self.pas.check_null(mnemonic, {"optional": True})

        for mnemonic, config in numb_rng_mnemonics.items():
            self.pas.check_out_of_range(mnemonic, -1e6, 1e6)
            self.pas.check_null(mnemonic, config) 

        for mnemonic, config in numb_rng_mnemonics2.items():
            self.pas.check_out_of_range(mnemonic, -1e6, 1e6)
            self.pas.check_null(mnemonic, config)          
        
        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]

        self.pas.field = None


    def test_rca_data_properties(self):
        self.pas.field = "~ RECOMBINED GAS ANALYSIS - DATA PROPERTIES"
        mnemonics = ["SEPCOND.", "LIQRAT.M3/D", "LIQGPT.", "LIQMM.", "LIQRDN."]
        char_code_mnemonics = {"SEPCOND.": {"optional": False}, "LIQGPT.": {"optional": False}}
        numb_mnemonics = {"LIQRAT.M3/D": {"optional": False, "allow_zero": False, "allow_neg": True},
                          "LIQMM.": {"optional": False, "allow_zero": False, "allow_neg": True},
                          "LIQRDN.": {"optional": False, "allow_zero": False, "allow_neg": True}}        
        dependent = 'STYP.'


        # STYP = 'R', then mnemonics must be mandatory.
        # Dictionary items are based on PAS format file.
        self.pas.pas.data[dependent] = 'R'

        for mnemonic, config in char_code_mnemonics.items():
            self.char_code_test_sequence(mnemonic, config)  

        for mnemonic, config in numb_mnemonics.items():
            self.numb_test_sequence(mnemonic, config)       
        
        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        # STYP != 'R', then mnemonics must be null.
        # Dictionary items are based on PAS format file.
        self.pas.pas.data[dependent] = random.choice([x for x in self.pas.pas.codes[dependent] if x != 'R'])

        for mnemonic, config in char_code_mnemonics.items():
            self.char_code_null_only_test_sequence(mnemonic)

        for mnemonic, config in numb_mnemonics.items():
            self.numb_null_only_test_sequence(mnemonic)
        
        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


        del self.pas.pas.data[dependent]
        self.pas.field = None


    def test_fs_gas_e3m3(self):
        mnemonic, config = "FS-GAS.E3M3/D", {"optional": True, "allow_zero": False, "allow_neg": True}
        dependent1 = 'STYP.'
        dependent2 = 'SEPCOND.'


        # STYP = 'R', so SEPCOND must not be null. SEPCOND can be either 'F' or 'B'.
        # Mnemonic must not be null, hence optional=False.
        # Dictionary is based on PAS format file.
        self.pas.pas.data[dependent1] = 'R'
        self.pas.pas.data[dependent2] = random.choice(self.pas.pas.codes[dependent2])
        config["optional"] = False
        self.numb_test_sequence(mnemonic, config)       
        

        # STYP != 'R', so SEPCOND must be null.
        # Mnemonic must be null, hence optional=False.
        # Dictionary is based on PAS format file.
        self.pas.pas.data[dependent1] = random.choice([x for x in self.pas.pas.codes[dependent1] if x != 'R'])
        self.pas.pas.data[dependent2] = None

        self.numb_null_only_test_sequence(mnemonic)
        

        del self.pas.pas.data[mnemonic]
        del self.pas.pas.data[dependent1]        
        del self.pas.pas.data[dependent2]


    def test_ss_gas_e3m3(self):
        mnemonics = {"SS-GAS.E3M3/D": {"optional": True, "allow_zero": False, "allow_neg": True}}
        dependent1 = 'STYP.'
        dependent2 = 'SEPCOND.'

        self.pas.pas.data[dependent1] = 'R'
        self.pas.pas.data[dependent2] = 'B'
        for mnemonic, config in mnemonics.items():
            config["optional"] = False
            self.numb_test_sequence(mnemonic, config)

        self.pas.pas.data[dependent1] = 'R'
        self.pas.pas.data[dependent2] = 'F'
        for mnemonic, config in mnemonics.items():
            config["optional"] = True
            self.numb_test_sequence(mnemonic, config)        

        self.pas.pas.data[dependent1] = random.choice([x for x in self.pas.pas.codes[dependent1] if x != 'R'])
        self.pas.pas.data[dependent2] = None
        for mnemonic, config in mnemonics.items():
            self.pas.check_out_of_range(mnemonic, -1e6, 1e6)
            self.pas.check_null(mnemonic, {"optional": True})
        
        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]
        del self.pas.pas.data[dependent2]


    def test_rgc(self):
        mnemonics = {"R-%s.FRAC" % (gas): {"optional": True, "allow_zero": False, "allow_neg": True} 
                     for gas in ["H2S", "CO2", "N2", "H2", "HE", "C1", "C2", "C3", "IC4", "NC4", "IC5", "NC5", "C6", "C7+"]}
        dependent = "STYP."

        self.pas.pas.data[dependent] = random.choice([x for x in self.pas.pas.codes[dependent] if x != 'R'])
        for mnemonic, config in mnemonics.items():
            self.numb_test_sequence(mnemonic, config)

        self.pas.pas.data[dependent] = 'R'
        for mnemonic, config in mnemonics.items():
            config["optional"] = False
            self.numb_test_sequence(mnemonic, config)
        
        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]

    
    def test_rgp(self):
        mnemonics = ["RGHV.MJ/M3",
                     "RGHVA.MJ/M3",
                     "RECOFLO.E3M3/D",
                     "RDGAS.",
                     "R-PPC.KPAA",
                     "R-PTC.DEGK"]
        dependent = 'STYP.'

        self.pas.pas.data[dependent] = 'R'
 
        numb_mnemonics = {"RGHV.MJ/M3": {"optional": False, "allow_zero": False, "allow_neg": True},
                          "RGHVA.MJ/M3": {"optional": False, "allow_zero": False, "allow_neg": True},
                          "RECOFLO.E3M3/D": {"optional": False, "allow_zero": False, "allow_neg": True},
                          "RDGAS.": {"optional": False, "allow_zero": False, "allow_neg": True}}
        for mnemonic, config in numb_mnemonics.items():
            self.numb_test_sequence(mnemonic, config)

        kpa_mnemonics = {"R-PPC.KPAA": {"optional": True, "allow_zero": False, "allow_neg": True}}
        for mnemonic, config in kpa_mnemonics.items():
            self.unit_kPa_test_sequence(mnemonic, config)

        degK_mnemonics = {"R-PTC.DEGK": {"optional": True, "allow_zero": False, "allow_neg": False}}
        for mnemonic, config in degK_mnemonics.items():
            self.unit_degK_test_sequence(mnemonic, config)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]

        self.pas.pas.data[dependent] = random.choice([x for x in self.pas.pas.codes[dependent] if x != 'R'])

        for mnemonic, config in numb_mnemonics.items():
            self.pas.check_out_of_range(mnemonic, -1e6, 1e6)
            self.pas.check_null(mnemonic, {"optional": True})
        
        for mnemonic, config in kpa_mnemonics.items():
            self.pas.check_out_of_range(mnemonic, -1e6, 1e6)
            self.pas.check_null(mnemonic, config)

        for mnemonic, config in degK_mnemonics.items():
            self.pas.check_out_of_range(mnemonic, -1e6, 1e6)
            self.pas.check_null(mnemonic, config)

        for mnemonic in mnemonics:
            del self.pas.pas.data[mnemonic]


if __name__ == "__main__":
    unittest.main()





