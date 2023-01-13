import os
import sys
import datetime as dt
import numpy as np
import pandas as pd
from skyrim.whiterun import CCalendar, CInstrumentInfoTable, parse_instrument_from_contract_wind
from skyrim.winterhold import check_and_mkdir, remove_files_in_the_dir
from skyrim.windhelm import *
from skyrim.configurationOffice import SKYRIM_CONST_CALENDAR_PATH, SKYRIM_CONST_INSTRUMENT_INFO_PATH

pd.set_option("display.width", 0)
pd.set_option("display.float_format", "{:.2f}".format)
np.set_printoptions(6, suppress=True)

factor_lib = os.path.join("/Works", "2022", "Project_2022_05_Commodity_Factors_Library_V2", "data")
instrument_return_dir = os.path.join(factor_lib, "instruments_return")
factors_by_tm_dir = os.path.join(factor_lib, "factors_by_tm")
available_universe_dir = os.path.join(factor_lib, "available_universe")

# futures_dir = os.path.join("C:\\", "Users", "huxia", "OneDrive", "文档", "Trading", "DataBase", "Futures")
futures_dir = os.path.join("/DataBase", "Futures")
futures_instrument_mkt_data_dir = os.path.join(futures_dir, "instrument_mkt_data")
major_minor_dir = os.path.join(futures_dir, "by_instrument", "major_minor")
md_by_instrument_dir = os.path.join(futures_dir, "by_instrument", "md")


project_data_dir = os.path.join(".", "data")
signal_calendar_dir = os.path.join(project_data_dir, "signal_calendar")
signals_dir = os.path.join(project_data_dir, "signals")
OPERATION_XUNTOU_U_DISK_DIR = os.path.join("H:", "Trade", "xuntou_group")

SEP_LINE_EQ = "=" * 120
SEP_LINE_DS = "-" * 120

if __name__ == "__main__":
    check_and_mkdir(signal_calendar_dir)
    check_and_mkdir(signals_dir)
    check_and_mkdir(OPERATION_XUNTOU_U_DISK_DIR)
