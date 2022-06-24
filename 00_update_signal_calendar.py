from setup import *
from configure import strategy_config_table

print(SEP_LINE_EQ)

factor_lbl = sys.argv[1].upper()  # ["RSW252HL063", "TS"]
factor_config = strategy_config_table[factor_lbl]

check_and_mkdir(signal_calendar_dir)

# load raw calendar
calendar_cne = CCalendar(SKYRIM_CONST_CALENDAR_PATH)
stp_date = (dt.datetime.now() + dt.timedelta(days=31)).strftime("%Y%m%d")
trade_dates_list = calendar_cne.get_iter_list(
    t_bgn_date=factor_config.m_bgn_date,
    t_stp_date=stp_date,
    t_ascending=True
)
weekday_list = [str(dt.datetime.strptime(z, "%Y%m%d").weekday() + 1) for z in trade_dates_list]
signal_calendar_df = pd.DataFrame({
    "trade_date": trade_dates_list,
    "week_date": weekday_list,
})

for gi, gid in enumerate(factor_config.m_gid_list):
    signal_calendar_df[gid] = 0
    signal_calendar_df.loc[factor_config.m_gid_delay[gid]::factor_config.m_hold_period_n, gid] = 1

signal_calendar_file = "signal_calendar.{}.csv".format(factor_lbl)
signal_calendar_path = os.path.join(signal_calendar_dir, signal_calendar_file)
signal_calendar_df.to_csv(signal_calendar_path, index=False)

print(signal_calendar_df.tail(60))
print(SEP_LINE_EQ)
