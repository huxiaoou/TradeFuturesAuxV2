from setup import *
from configure import universe_options, strategy_config_table

# arguments
sig_date = sys.argv[1]
factor_lbl = sys.argv[2].upper()  # ["RSW252HL063", "TS"]
factor_config = strategy_config_table[factor_lbl]

# --- load raw calendar
calendar_cne = CCalendar(SKYRIM_CONST_CALENDAR_PATH)
exe_date = calendar_cne.get_next_date(t_this_date=sig_date, t_shift=1)

# --- set mother universe set
mother_universe_set = set(universe_options.get(factor_config.m_uid))

# --- directory check
check_and_mkdir(signals_dir)
check_and_mkdir(os.path.join(signals_dir, sig_date[0:4]))
check_and_mkdir(os.path.join(signals_dir, sig_date[0:4], sig_date))

# --- load signal calendar
signal_calendar_file = "signal_calendar.{}.csv".format(factor_lbl)
signal_calendar_path = os.path.join(signal_calendar_dir, signal_calendar_file)
signal_calendar_df = pd.read_csv(signal_calendar_path, dtype={"trade_date": str}).set_index("trade_date")

for gid in factor_config.m_gid_list:
    if signal_calendar_df.at[sig_date, gid] > 0:
        # --- load available universe
        available_universe_file = "available_universe.{}.csv.gz".format(sig_date)
        available_universe_path = os.path.join(available_universe_dir, sig_date[0:4], sig_date, available_universe_file)
        available_universe_df = pd.read_csv(available_universe_path)
        available_universe_set = set(available_universe_df["instrument"])

        # --- load factors at signal date
        factor_file = "factor.{}.{}.csv.gz".format(sig_date, factor_lbl)
        factor_path = os.path.join(factors_by_tm_dir, sig_date[0:4], sig_date, factor_file)
        factor_df = pd.read_csv(factor_path).set_index("instrument")
        factor_universe_set = set(factor_df.index)

        # --- selected universe
        opt_universe = list(mother_universe_set.intersection(available_universe_set).intersection(factor_universe_set))
        opt_weight_df = factor_df.loc[opt_universe]
        opt_weight_df = opt_weight_df.reset_index()
        opt_weight_df = opt_weight_df.sort_values(by=[factor_lbl, "instrument"], ascending=[False, True])

        # --- calculate weight
        opt_universe_size = len(opt_weight_df)
        k0 = max(min(int(np.ceil(opt_universe_size * factor_config.m_single_hold_prop)), int(opt_universe_size / 2)), 1)
        k1 = opt_universe_size - 2 * k0
        opt_weight_df["direction"] = [1] * k0 + [0] * k1 + [-1] * k0
        raw_signals_df = opt_weight_df.loc[opt_weight_df["direction"].abs() > 0].copy()
        raw_signals_df["contract"] = raw_signals_df["instrument"].map(
            lambda z: get_major_contract(z, sig_date, major_minor_dir, "major.minor.{}.csv.gz"))
        print(raw_signals_df)

        # ---
        raw_signals_file = "raw_signals.{}.sig_{}.exe_{}.{}.csv".format(factor_lbl, sig_date, exe_date, gid)
        raw_signals_path = os.path.join(signals_dir, sig_date[0:4], sig_date, raw_signals_file)
        raw_signals_df.to_csv(raw_signals_path, index=False, float_format="%.2f")

        print(SEP_LINE_DS)
        print("| {} | factor {}-{} at {} is updated |".format(dt.datetime.now(), factor_lbl, gid, sig_date))
        print(SEP_LINE_EQ)
