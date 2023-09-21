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

    def check_negative(
        self, mnemonic, config, in_rmin, in_rmax, out_rmin=None, out_rmax=None
    ):
        self.pas.data[mnemonic] = -random.uniform(in_rmin, in_rmax)
        if config["allow_neg"]:
            self.check_not_assert_raised()
            if out_rmin is not None and out_rmax is not None:
                self.pas.data[mnemonic] = -random.uniform(out_rmin, out_rmax)
                self.check_assert_raised()
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

