now=$(date +%Y-%m-%d_%H:%M:%S)
freq=$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq)
temp=$(/opt/vc/bin/vcgencmd measure_temp)
echo "$now;$freq;$temp" >> ~/cputemp.log
