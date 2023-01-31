from setup import *
from configure import strategy_config_table

this_sig_date = sys.argv[1]
factor_lbl = sys.argv[2].upper()  # ["RSW252HL063", "TS"]
factor_config = strategy_config_table[factor_lbl]

# load raw calendar
calendar_cne = CCalendar(SKYRIM_CONST_CALENDAR_PATH)
prev_sig_date = calendar_cne.get_next_date(this_sig_date, -factor_config.m_hold_period_n)
this_exe_date = calendar_cne.get_next_date(this_sig_date, 1)
prev_exe_date = calendar_cne.get_next_date(prev_sig_date, 1)

# --- load signal calendar
signal_calendar_file = "signal_calendar.{}.csv".format(factor_lbl)
signal_calendar_path = os.path.join(signal_calendar_dir, signal_calendar_file)
signal_calendar_df = pd.read_csv(signal_calendar_path, dtype={"trade_date": str}).set_index("trade_date")

for gid in factor_config.m_gid_list:
    if signal_calendar_df.at[this_sig_date, gid] > 0:
        this_file = "raw_signals.{}.sig_{}.exe_{}.{}.revised.2.csv".format(factor_lbl, this_sig_date, this_exe_date, gid)
        this_path = os.path.join(signals_dir, this_sig_date[0:4], this_sig_date, this_file)
        this_df = pd.read_csv(this_path, dtype={"direction": int, "trade_quantity": int}).set_index("instrument")
        this_df = this_df[["contract", "direction", "trade_quantity"]]

        prev_file = "raw_signals.{}.sig_{}.exe_{}.{}.revised.2.csv".format(factor_lbl, prev_sig_date, prev_exe_date, gid)
        prev_path = os.path.join(signals_dir, prev_sig_date[0:4], prev_sig_date, prev_file)
        try:
            prev_df = pd.read_csv(prev_path, dtype={"direction": int, "trade_quantity": int}).set_index("instrument")
        except FileNotFoundError:
            print("... prev path = '{}' does NOT exist.\n... diff files are not created.".format(prev_path))
            sys.exit()
        prev_df = prev_df[["contract", "direction", "trade_quantity"]]

        # --- save merged
        merge_df: pd.DataFrame = pd.merge(
            left=prev_df,
            right=this_df,
            left_index=True, right_index=True,
            how="outer", suffixes=("_" + prev_sig_date, "_" + this_sig_date)
        )
        merge_file = "merged.{}.sig_{}.exe_{}.{}.csv".format(factor_lbl, this_sig_date, this_exe_date, gid)
        merge_path = os.path.join(signals_dir, this_sig_date[0:4], this_sig_date, merge_file)
        merge_df.to_csv(merge_path, index_label="instrument")

        # --- save diff
        merged_by_key_df = pd.merge(
            left=prev_df.set_index(["contract", "direction"]),
            right=this_df.set_index(["contract", "direction"]),
            left_index=True, right_index=True,
            how="outer", suffixes=("_prev", "_this")
        ).fillna(0)
        operation_data_list = []
        for key in merged_by_key_df.index:
            prev_pos = CPosCell(key, merged_by_key_df.loc[key, "trade_quantity_prev"])
            this_pos = CPosCell(key, merged_by_key_df.loc[key, "trade_quantity_this"])
            operation_data = prev_pos.cal_operation(t_target_pos_cell=this_pos)
            if operation_data is not None:
                operation_data_list.append(operation_data)
        diff_df = pd.DataFrame(operation_data_list)
        diff_df = diff_df.sort_values(by=["operation", "contract", "qty"], ascending=[True, True, False])
        diff_file = "diff.{}.sig_{}.exe_{}.{}.csv".format(factor_lbl, this_sig_date, this_exe_date, gid)
        diff_path = os.path.join(signals_dir, this_sig_date[0:4], this_sig_date, diff_file)
        diff_df.to_csv(diff_path, index=False)

        diff_pivot_df = pd.pivot_table(data=diff_df, index=["operation"], values=["qty"], aggfunc=["count", "sum"])
        diff_pivot_file = "diff_pivot.{}.sig_{}.exe_{}.{}.csv".format(factor_lbl, this_sig_date, this_exe_date, gid)
        diff_pivot_path = os.path.join(signals_dir, this_sig_date[0:4], this_sig_date, diff_pivot_file)
        diff_pivot_df.to_csv(diff_pivot_path)

        print(SEP_LINE_DS)
        print(merge_df)
        print(SEP_LINE_DS)
        print(diff_df)
        print(SEP_LINE_DS)
        print(diff_pivot_df)
        print(SEP_LINE_DS)

        print("| {} | diff-data | {:>12s} | {:>8s} | diff position | this_sig_date = {} | prev_signal_date = {} | calculated |".format(
            dt.datetime.now(), factor_lbl, gid, this_sig_date, prev_sig_date))
