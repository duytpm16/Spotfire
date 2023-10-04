import re
import sys
import random
import string
import unittest
import pandas as pd

sys.path.insert(1, "../")
from export_to_pas import PAS


class TestPAS(unittest.TestCase):
    file = pd.read_csv("pas_lookup.csv", sep=",", header=0)
    pas = PAS(file)
    ppt = pas.pt
    field = None
    mn = "MNEMONIC NAME"
    fs = "FIELD SIZE"
    br = "BUSINESS RULES AND EDITS"

    def subset_pas(self, analysis):
        self.pas.subset(analysis)
        self.ppt = self.pas.pt


    def check_assert_raised(self):
        self.pas.pt = self.ppt[self.ppt[self.mn].isin(self.pas.data)]

        if self.field is not None:
            self.pas.pt = self.pas.pt.groupby(self.mn, group_keys=True).apply(
                lambda x: x if len(x) == 1 else x.loc[x["FIELD"].eq(self.field)]
            )

        self.assertTrue(
            set(self.pas.data).issubset(self.pas.pt[self.mn]),
            "Not all mnemonic exists.",
        )
        self.pas.pt_zip = zip(self.pas.pt[self.mn], self.pas.pt["FIELD"], self.pas.pt[self.fs], self.pas.pt[self.br])

        with self.assertRaises(SystemExit):
            self.pas.check_pas_data()


    def check_not_assert_raised(self):
        self.pas.pt = self.ppt[self.ppt[self.mn].isin(self.pas.data)]

        if self.field is not None:
            self.pas.pt = self.pas.pt.groupby(self.mn, group_keys=True).apply(
                lambda x: x if len(x) == 1 else x.loc[x["FIELD"].eq(self.field)]
            )

        self.assertTrue(
            set(self.pas.data).issubset(self.pas.pt[self.mn]),
            "Not all mnemonic can be tested.",
        )
        self.pas.pt_zip = zip(self.pas.pt[self.mn], self.pas.pt["FIELD"], self.pas.pt[self.fs], self.pas.pt[self.br])

        self.pas.check_pas_data()


    def check_null(self, mnemonic, config):
        self.pas.data[mnemonic] = None
        if config["optional"]:
            self.check_not_assert_raised()
        else:
            self.check_assert_raised()


    def check_zero(self, mnemonic, config):
        self.pas.data[mnemonic] = "0.0"
        if config["allow_zero"]:
            self.check_not_assert_raised()
        else:
            self.check_assert_raised()


    def check_negative(self, mnemonic, config, rmin, rmax):
        self.pas.data[mnemonic] = random.uniform(rmin, rmax)
        if config["allow_neg"]:
            self.check_not_assert_raised()
        else:
            self.check_assert_raised()


    def check_out_of_range(self, mnemonic, rmin, rmax):
        self.pas.data[mnemonic] = random.uniform(rmin, rmax)
        self.check_assert_raised()


    def check_within_range(self, mnemonic, rmin, rmax):
        self.pas.data[mnemonic] = random.uniform(rmin, rmax)
        self.check_not_assert_raised()


    def check_char_out_of_range(self, mnemonic, field_size):
        alphanumeric = string.ascii_uppercase + string.digits
        k = random.choice(list(range(field_size + 1, field_size + 500)))
        self.pas.data[mnemonic] = "".join(random.choices(alphanumeric, k=k))
        self.check_assert_raised()


    def check_char_within_range(self, mnemonic, field_size):
        alphanum = string.ascii_uppercase + string.digits
        k = random.choice(list(range(1, field_size + 1)))
        self.pas.data[mnemonic] = "".join(random.choices(alphanum, k=k))
        self.check_not_assert_raised()


    def check_char_code_out_of_range(self, mnemonic):
        alphanum = string.ascii_uppercase + string.digits
        excluded = re.sub(r"|".join(self.pas.codes[mnemonic]), "", alphanum)
        self.pas.data[mnemonic] = random.choice(excluded)
        self.check_assert_raised()


    def check_numb_code_out_of_range(self, mnemonic):
        ints = list(set(range(0, 100)) - set(self.pas.codes[mnemonic]))
        self.pas.data[mnemonic] = random.choice(ints)
        self.check_assert_raised()


    def check_code_within_range(self, mnemonic):
        self.pas.data[mnemonic] = random.choice(self.pas.codes[mnemonic])
        self.check_not_assert_raised()


    def get_char_size(self, mnemonic):
        field_size = self.ppt[self.ppt[self.mn].isin([mnemonic])][self.fs].to_list()
        if len(set(field_size)) != 1:
            sys.exit("ERROR: Multiple rows for mnemonic [%s]." % (mnemonic))
        return int(field_size[0].split(" ")[1])
    

    def char_test_sequence(self, mnemonic, config):
        field_size = self.get_char_size(mnemonic)
            
        self.check_null(mnemonic, config)
        self.check_char_out_of_range(mnemonic, field_size)
        self.check_char_within_range(mnemonic, field_size)


    def char_code_test_sequence(self, mnemonic, config):
        field_size = self.get_char_size(mnemonic)
        
        self.check_null(mnemonic, config)
        self.check_char_out_of_range(mnemonic, field_size)
        self.check_char_code_out_of_range(mnemonic)
        self.check_code_within_range(mnemonic)


    def numb_test_sequence(self, mnemonic, config):
        self.check_null(mnemonic, config)
        self.check_zero(mnemonic, config)
        self.check_negative(mnemonic, config, -1e6, 0)

        if config['allow_neg']:
            self.check_within_range(mnemonic, -1e6, 0)
        self.check_within_range(mnemonic, 0, 1e6)


    def numb_code_test_sequence(self, mnemonic, config):
        self.check_null(mnemonic, config)
        self.check_numb_code_out_of_range(mnemonic)
        self.check_code_within_range(mnemonic)

    
    def unit_degC_test_sequence(self, mnemonic, config):
        self.check_null(mnemonic, config)
        self.check_zero(mnemonic, config)
        self.check_negative(mnemonic, config, -99.99, 0)
        self.check_out_of_range(mnemonic, 1000, 1500)
        self.check_out_of_range(mnemonic, -1e6, -100)
        self.check_within_range(mnemonic, 0.001, 1000)


    def unit_degK_test_sequence(self, mnemonic, config):
        self.check_null(mnemonic, config)
        self.check_zero(mnemonic, config)
        self.check_negative(mnemonic, config, -1e6, 0)
        self.check_out_of_range(mnemonic, 0.001, 173.15)
        self.check_out_of_range(mnemonic, 1273.15, 1500)
        self.check_within_range(mnemonic, 173.15, 1273.15)


    def unit_kPa_test_sequence(self, mnemonic, config):
        self.check_null(mnemonic, config)
        self.check_zero(mnemonic, config)
        self.check_negative(mnemonic, config, -1e6, 0)
        self.check_out_of_range(mnemonic, 150000, 1e6)
        self.check_within_range(mnemonic, 0.001, 150000)


    def unit_mPa_test_sequence(self, mnemonic, config):
        self.check_null(mnemonic, config)
        self.check_zero(mnemonic, config)
        self.check_negative(mnemonic, config, -1e6, 0)
        self.check_out_of_range(mnemonic, 150, 1e6)
        self.check_within_range(mnemonic, 0.001, 150)


    def numb_null_only_test_sequence(self, mnemonic):
        self.check_out_of_range(mnemonic, -1e6, 0)
        self.check_out_of_range(mnemonic, 0.001, 1e6)
        self.check_zero(mnemonic, {"allow_zero": False})
        self.check_null(mnemonic, {"optional": True})

    
    def numb_code_null_only_test_sequence(self, mnemonic):
        self.pas.data[mnemonic] = random.randint(0, 100)
        self.check_assert_raised()
        self.check_null(mnemonic, {"optional": True})


    def char_null_only_test_sequence(self, mnemonic):
        self.check_char_out_of_range(mnemonic, 1)
        self.check_null(mnemonic, {"optional": True})


    def char_code_null_only_test_sequence(self, mnemonic):
        self.pas.data[mnemonic] = random.choice(string.ascii_uppercase)
        self.check_assert_raised()
        self.check_null(mnemonic, {"optional": True})

