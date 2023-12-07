import math
import pandas as pd
from scipy.optimize import minimize, curve_fit


def corey_rss(i, swn, kr, kr_max):
    return sum([(((s**i) * kr_max - k) ** 2) / k for s, k in zip(swn, kr)])


def sm_rss(i, swn, kr, kr_max, n):
    return sum(
        [
            (((kr_max * (s**n + i * s) / (1 + i)) - k) ** 2) / k
            for s, k in zip(swn, kr)
        ]
    )


class RelPerm:
    def __init__(self, data):
        data.columns = data.columns.str.lower()

        self.kro = data["kro"]
        self.krw = data["krw"]
        self.kro_max = max(data["kro"])
        self.krw_max = max(data["krw"])

        self.swi = min(data["sw"])
        self.sor = 1 - max(data["sw"])
        self.swn = [(sw - self.swi) / (1 - self.swi - self.sor) for sw in data["sw"]]
        self.swc = [1 - swn for swn in self.swn]

        self.corey = {"no": None, "nw": None}
        self.sm = {"A": None, "B": None}
        self.let = {
            "lo": None,
            "eo": None,
            "to": None,
            "lw": None,
            "ew": None,
            "tw": None,
        }

    def calc_let_kro(self, swn, l, e, t):
        return self.kro_max * (swn ** l / (swn ** l + e * (1 - swn) ** t))

    def calc_let_krw(self, swn, l, e, t):
        return self.krw_max * (swn ** l / (swn ** l + e * (1 - swn) ** t))

    def call_minimize(self, fun, x0, args, bounds):
        return minimize(fun=fun, x0=x0, args=args, bounds=bounds)["x"][0]

    def call_curve_fit(self, f, xdata, ydata, p0, bounds):
        return curve_fit(f=f, xdata=xdata, ydata=ydata, p0=p0, bounds=bounds)[0]

    def corey_fit(self):
        kro_args = (self.swc[1:], self.kro[1:], self.kro_max)
        krw_args = (self.swn[1:], self.krw[1:], self.krw_max)

        self.corey["no"] = self.call_minimize(corey_rss, 1, kro_args, [[None, None]])
        self.corey["nw"] = self.call_minimize(corey_rss, 1, krw_args, [[None, None]])

    def sm_fit(self):
        if self.corey["nw"] is None or self.corey["no"] is None:
            self.corey_fit()

        kro_args = (self.swc[1:], self.kro[1:], self.kro_max, self.corey["no"])
        krw_args = (self.swn[1:], self.krw[1:], self.krw_max, self.corey["nw"])

        self.sm["B"] = self.call_minimize(sm_rss, 0, kro_args, [[0, None]])
        self.sm["A"] = self.call_minimize(sm_rss, 0, krw_args, [[0, None]])

    def let_fit(self):
        p0 = [1, 0.5, 0.5]
        bounds = ((1, 0.5, 0.5), (math.inf, math.inf, math.inf))

        kro_let = self.call_curve_fit(self.calc_let_kro, self.swc, self.kro, p0, bounds)
        self.let["lo"], self.let["eo"], self.let["to"] = kro_let

        krw_let = self.call_curve_fit(self.calc_let_krw, self.swn, self.krw, p0, bounds)
        self.let["lw"], self.let["ew"], self.let["tw"] = krw_let

    def fit_models(self):
        self.corey_fit()
        self.sm_fit()
        self.let_fit()

        A, B = self.sm["A"], self.sm["B"]
        no, nw = self.corey["no"], self.corey["nw"]
        kro_max, krw_max = self.kro_max, self.krw_max
        lo, eo, to = (self.let["lo"], self.let["eo"], self.let["to"])
        lw, ew, tw = (self.let["lw"], self.let["ew"], self.let["tw"])

        swn = [x / 1000.0 for x in range(0, 1001, 25)]
        swc = [1 - s for s in swn]
        sw = [s * (1 - self.swi - self.sor) + self.swi for s in swn]

        corey_kro = [(s**no) * kro_max for s in swc]
        corey_krw = [(s**nw) * krw_max for s in swn]

        sm_kro = [kro_max * (s**no + B * s) / (1 + B) for s in swc]
        sm_krw = [krw_max * (s**nw + A * s) / (1 + A) for s in swn]

        let_kro = [self.calc_let_kro(s, lo, eo, to) for s in swc]
        let_krw = [self.calc_let_krw(s, lw, ew, tw) for s in swn]

        return pd.DataFrame(
            {
                "Swn": swn,
                "Sw": sw,
                "Corey Kro": corey_kro,
                "Corey Krw": corey_krw,
                "SM Kro": sm_kro,
                "SM Krw": sm_krw,
                "LET Kro": let_kro,
                "LET Krw": let_krw,
            }
        )


if __name__ == "__main__":
    df = pd.read_excel("relperm_curvefit_testdata.xlsx")
    rp = RelPerm(df)
    output = rp.fit_models()
    params = pd.DataFrame(
        {
            "No": [rp.corey["no"]],
            "Nw": [rp.corey["nw"]],
            "A": [rp.sm["A"]],
            "B": [rp.sm["B"]],
            "Lo": [rp.let['lo']],
            "Eo": [rp.let['eo']],
            "To": [rp.let['to']],
            "Lw": [rp.let['lw']],
            "Ew": [rp.let['ew']],
            "Tw": [rp.let['tw']]
        }
    )
    print(params)
