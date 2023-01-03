from setup import *
from configure import strategy_config_table

# arguments
sig_date = sys.argv[1]
factor_lbl = sys.argv[2].upper()  # ["RSW252HL063", "TS"]
factor_config = strategy_config_table[factor_lbl]

# --- load raw calendar
calendar_cne = CCalendar(SKYRIM_CONST_CALENDAR_PATH)
exe_date = calendar_cne.get_next_date(t_this_date=sig_date, t_shift=1)

# --- instrument info
instrument_info_table = CInstrumentInfoTable(t_path=SKYRIM_CONST_INSTRUMENT_INFO_PATH, t_index_label="windCode")

# --- load signal calendar
signal_calendar_file = "signal_calendar.{}.csv".format(factor_lbl)
signal_calendar_path = os.path.join(signal_calendar_dir, signal_calendar_file)
signal_calendar_df = pd.read_csv(signal_calendar_path, dtype={"trade_date": str}).set_index("trade_date")

for gid in factor_config.m_gid_list:
    if signal_calendar_df.at[sig_date, gid] > 0:
        raw_signals_file = "raw_signals.{}.sig_{}.exe_{}.{}.revised.csv".format(factor_lbl, sig_date, exe_date, gid)
        raw_signals_path = os.path.join(signals_dir, sig_date[0:4], sig_date, raw_signals_file)

        revised_df = pd.read_csv(raw_signals_path)
        revised_df["contract_multiplier"] = revised_df["instrument"].map(lambda z: instrument_info_table.get_multiplier(z))
        revised_df["weight"] = 1
        revised_df["available_amt"] = factor_config.get_available_amt_dict(t_sig_date=sig_date) / revised_df["weight"].sum()
        revised_df["close"] = revised_df["contract"].map(lambda z: get_contract_price(z, sig_date, futures_instrument_mkt_data_dir, "close"))
        revised_df["quantity"] = revised_df["available_amt"] / revised_df["close"] / revised_df["contract_multiplier"]
        revised_df["trade_quantity"] = revised_df["quantity"].map(lambda z: int(np.round(z)))
        revised_df = revised_df[[
            "instrument", factor_lbl,
            "contract_multiplier", "weight", "available_amt", "close", "quantity",
            "contract", "direction", "trade_quantity"]]

        revised_path = raw_signals_path.replace(".csv", ".2.csv")
        revised_df.to_csv(revised_path, index=False, float_format="%.2f")
        print(revised_df)
