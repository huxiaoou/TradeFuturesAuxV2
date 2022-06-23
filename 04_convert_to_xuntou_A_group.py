from setup import *
from configure import strategy_config_table

"""
created @ 2022-06-23
"""

print(SEP_LINE_EQ)

sig_date = sys.argv[1]
factor_lbl = sys.argv[2]  # "RSW252HL063"
factor_config = strategy_config_table[factor_lbl]

# load raw calendar
calendar_cne = CCalendar(SKYRIM_CONST_CALENDAR_PATH)
exe_date = calendar_cne.get_next_date(sig_date, 1)

# load signal calendar
signal_calendar_file = "signal_calendar.{}.csv".format(factor_lbl)
signal_calendar_path = os.path.join(signal_calendar_dir, signal_calendar_file)
signal_calendar_df = pd.read_csv(signal_calendar_path, dtype={"trade_date": str}).set_index("trade_date")

for gid in factor_config.m_gid_list:
    if signal_calendar_df.at[sig_date, gid] > 0:
        src_dir = os.path.join(signals_dir, sig_date[0:4], sig_date)
        src_file = "raw_signals.{}.sig_{}.exe_{}.{}.revised.2.csv".format(factor_lbl, sig_date, exe_date, gid)
        src_path = os.path.join(src_dir, src_file)
        df = pd.read_csv(src_path)

        # reformat
        df["代码"], df["市场"] = zip(*df.apply(lambda z: z["contract"].split("."), axis=1))
        df["市场"] = df["市场"].map(convert_mkt_code)
        df["代码"] = df[["市场", "代码"]].apply(convert_contract_code, axis=1)
        df["数量"] = np.abs(df["trade_quantity"])
        df["相对权重"] = 1
        df_lng = df[["代码", "市场", "数量", "相对权重", "direction"]].copy()  # type:pd.DataFrame
        df_srt = df[["代码", "市场", "数量", "相对权重", "direction"]].copy()  # type:pd.DataFrame
        df_lng["方向"] = 0  # in xuntou system, 0 for long
        df_srt["方向"] = 1  # in xuntou system, 1 for short
        df_lng.loc[df_lng["direction"] <= 0, "数量"] = 0
        df_srt.loc[df_srt["direction"] >= 0, "数量"] = 0
        df_lng = df_lng.drop(labels="direction", axis=1)
        df_srt = df_srt.drop(labels="direction", axis=1)
        lng_file = "{}_{}_买入开仓_exe_{}.csv".format(factor_lbl, gid, exe_date)
        srt_file = "{}_{}_卖出开仓_exe_{}.csv".format(factor_lbl, gid, exe_date)
        lng_path = os.path.join(signals_dir, sig_date[0:4], sig_date, lng_file)
        srt_path = os.path.join(signals_dir, sig_date[0:4], sig_date, srt_file)
        df_lng.to_csv(lng_path, index=False)
        df_srt.to_csv(srt_path, index=False)

        if os.path.exists(OPERATION_XUNTOU_U_DISK_DIR):
            u_disk_srt_path = os.path.join(OPERATION_XUNTOU_U_DISK_DIR, srt_file)
            u_disk_lng_path = os.path.join(OPERATION_XUNTOU_U_DISK_DIR, lng_file)
            df_lng.to_csv(u_disk_lng_path, index=False)
            df_srt.to_csv(u_disk_srt_path, index=False)
        else:
            print("| {} | U disk is not ready! Please check again.|".format(dt.datetime.now()))
