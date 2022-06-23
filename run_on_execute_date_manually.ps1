Write-Host "Begin to run operation for TS factors"
$trade_date = Read-Host -Prompt "Please Input the trade_date [format = YYYYMMDD], which should be a signal date"
$factor = Read-Host -Prompt "Please Input the factor, available options = [RSW252HL063, TS]"
python 02_revised_position.py $trade_date $factor >> .\log\$trade_date.manual.log
python 03_position_diff.py $trade_date $factor >> .\log\$trade_date.manual.log
python 04_convert_to_xuntou_A_group.py $trade_date $factor >> .\log\$trade_date.manual.log
python 05_convert_to_xuntou_B_diff.py $trade_date $factor 2 >> .\log\$trade_date.manual.log
Pause
