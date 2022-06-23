Write-Host "begin to run daily signal calculation for factors"
$trade_date = Read-Host -Prompt "Please input the trade_date to calcualte, format = [YYYYMMDD]"
python 00_update_signal_calendar.py TS > .\log\$trade_date.log
#python 00_update_signal_calendar.py RSW252HL063 >> .\log\$trade_date.log
python 01_raw_signals.py $trade_date TS >> .\log\$trade_date.log
#python 01_raw_signals.py $trade_date RSW252HL063 >> .\log\$trade_date.log
Pause
