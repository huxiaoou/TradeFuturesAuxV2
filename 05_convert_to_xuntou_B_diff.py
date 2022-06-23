from setup import *
from configure import strategy_config_table


"""
created @ 2022-06-23
"""

sig_date = sys.argv[1]
factor_lbl = sys.argv[2]  # "RSW252HL063"
n_batch = int(sys.argv[3])
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
        diff_file = "diff.{}.sig_{}.exe_{}.{}.csv".format(factor_lbl, sig_date, exe_date, gid)
        diff_path = os.path.join(signals_dir, sig_date[0:4], sig_date, diff_file)
        df = pd.read_csv(diff_path)
        df = df.sort_values(by=["operation", "contract"], ascending=True)

        for op, op_df in df.groupby(by="operation"):
            sub_df: pd.DataFrame = op_df.copy()
            sub_df["代码"], sub_df["市场"] = zip(*sub_df.apply(lambda z: z["contract"].split("."), axis=1))
            sub_df["市场"] = sub_df["市场"].map(convert_mkt_code)
            sub_df["代码"] = sub_df[["市场", "代码"]].apply(convert_contract_code, axis=1)
            sub_df["数量"] = sub_df["qty"].astype(int)
            sub_df["相对权重"] = 1
            sub_df: pd.DataFrame = sub_df[["代码", "市场", "数量", "相对权重"]]
            sub_df["方向"] = 1 if op in ["SellOpen", "SellClose"] else 0
            sub_lbl = {
                "BuyClose": "买入平仓",
                "BuyOpen": "买入开仓",
                "SellClose": "卖出平仓",
                "SellOpen": "卖出开仓",
            }[op]
            sub_file = "{}_{}_diff_{}_exe_{}.csv".format(factor_lbl, gid, sub_lbl, exe_date)

            # save to local
            sub_path = os.path.join(signals_dir, sig_date[0:4], sig_date, sub_file)
            sub_df.to_csv(sub_path, index=False)
            split_xuntou_instruction(t_src_path=sub_path, t_n_batch=n_batch)

            # save to U-disk
            if os.path.exists(OPERATION_XUNTOU_U_DISK_DIR):
                u_disk_sub_path = os.path.join(OPERATION_XUNTOU_U_DISK_DIR, sub_file)
                sub_df.to_csv(u_disk_sub_path, index=False)
                split_xuntou_instruction(t_src_path=u_disk_sub_path, t_n_batch=n_batch)
            else:
                print("| {} | U disk is not ready! Please check again.|".format(dt.datetime.now()))

        print("| {} | split | {:>12s} | {:>8s} | this_sig_date = {} | calculated |".format(
            dt.datetime.now(), factor_lbl, gid, sig_date))