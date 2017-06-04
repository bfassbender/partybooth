date >> ~/cputemp.log
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq >> ~/cputemp.log
/opt/vc/bin/vcgencmd measure_temp >> ~/cputemp.log
echo "-------------------" >> ~/cputemp.log
