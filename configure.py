from typing import Dict

universe_options = {
    "U21": [
        "RU.SHF",  # "19950516"
        "BU.SHF",  # "20131009"
        "A.DCE",  # "19990104"
        "M.DCE",  # "20000717"
        "Y.DCE",  # "20060109"
        "C.DCE",  # "20040922"
        "CS.DCE",  # "20141219"
        "L.DCE",  # "20070731"
        "P.DCE",  # "20071029"
        "V.DCE",  # "20090525"
        "J.DCE",  # "20110415"
        "JM.DCE",  # "20130322"
        "I.DCE",  # "20131018"
        "PP.DCE",  # "20140228"
        "CF.CZC",  # "20040601"
        "SR.CZC",  # "20060106"
        "OI.CZC",  # "20130423"
        "RM.CZC",  # "20121228"
        "TA.CZC",  # "20061218"
        "MA.CZC",  # "20141224"
        "FG.CZC",  # "20121203"
    ],
    "U29": [
        "CU.SHF",  # "19950417"
        "AL.SHF",  # "19950417"
        "PB.SHF",  # "20140801"
        "ZN.SHF",  # "20070326"
        "SN.SHF",  # "20151102"
        "NI.SHF",  # "20150327"
        "RB.SHF",  # "20090327"
        "HC.SHF",  # "20140321"
        "J.DCE",  # "20110415"
        "JM.DCE",  # "20130322"
        "I.DCE",  # "20131018"
        "FG.CZC",  # "20121203"
        "Y.DCE",  # "20060109"
        "P.DCE",  # "20071029"
        "OI.CZC",  # "20130423"
        "M.DCE",  # "20000717"
        "RM.CZC",  # "20121228"
        "A.DCE",  # "19990104"
        "RU.SHF",  # "19950516"
        "BU.SHF",  # "20131009"
        "L.DCE",  # "20070731"
        "V.DCE",  # "20090525"
        "PP.DCE",  # "20140228"
        "TA.CZC",  # "20061218"
        "MA.CZC",  # "20141224"
        "CF.CZC",  # "20040601"
        "SR.CZC",  # "20060106"
        "C.DCE",  # "20040922"
        "CS.DCE",  # "20141219"
    ],  # size = 29
}
WANYUAN = 1e4


class CConfigTable(object):
    def __init__(self, t_bgn_date: str, t_gid_list: list, t_gid_delay: dict, t_hold_period_n: int, t_single_hold_prop: float, t_uid: str, t_available_amt_dict: Dict[str, float]):
        """

        :param t_bgn_date: signal begin date,  format = "YYYYMMDD"
        :param t_gid_list: list of gid
        :param t_gid_delay: start delay of each gid, consider its co-work with hold_period_n
        :param t_hold_period_n:
        :param t_single_hold_prop:
        :param t_uid: universe id
        :param t_available_amt_dict: total amount money for each gid. Make sure its KEYS are sorted as DESCENDING
        """
        self.m_bgn_date = t_bgn_date
        self.m_gid_list = t_gid_list
        self.m_gid_delay = t_gid_delay
        self.m_hold_period_n = t_hold_period_n
        self.m_single_hold_prop = t_single_hold_prop
        self.m_uid = t_uid
        self.m_available_amt_dict = t_available_amt_dict

    def get_available_amt_dict(self, t_sig_date: str):
        for key_date, val_amt in self.m_available_amt_dict.items():
            if t_sig_date >= key_date:
                return val_amt
        return 0


strategy_config_table: Dict[str, CConfigTable] = {
    "TS": CConfigTable(
        t_bgn_date="20220512",
        t_gid_list=["G_TS04", "G_TS05", "G_TS06"],
        t_gid_delay={"G_TS04": 0, "G_TS05": 7, "G_TS06": 14},
        t_hold_period_n=20,
        t_single_hold_prop=0.4,
        t_uid="U21",
        t_available_amt_dict={
            # Make sure its KEYS are sorted as DESCENDING
            "20230103": 3600 * WANYUAN,
            "20220512": 1800 * WANYUAN,
        }
    ),

    "RSW252HL063": CConfigTable(
        t_bgn_date="20230131",
        t_gid_list=["G_RS00"],
        t_gid_delay={"G_RS00": 0},
        t_hold_period_n=5,
        t_single_hold_prop=0.2,
        t_uid="U29",
        t_available_amt_dict={
            # Make sure its KEYS are sorted as DESCENDING
            "20230130": 6000 * WANYUAN,
            "20220623": 800 * WANYUAN,
        },
    ),
}
