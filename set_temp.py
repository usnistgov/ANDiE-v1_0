import sys
from scantools.scripting import *
from scantools.ScanTools.util import getPvValue
import time

temperature = float(sys.argv[1])
count_time = sys.argv[2]
current_temperature=getPvValue("HB2C:SE:SampleTemp")

delay = 60 * abs(temperature-current_temperature)
if delay>900:
    delay = 900
Set("HB2C:SE:LS:SETP_S3", temperature, completion=False, tolerance=1.0)
Set("HB2C:SE:LS:SETP_S2", temperature, completion=True, tolerance=1.0)

Delay(delay)
Set("HB2C:SMS:RunInfo:RunTitle","MnO T = {} K".format(temperature))
Set("HB2C:SMS:Marker:NotesComment","powder")
Start()
Delay(count_time)
Stop()
Submit("MnO T = {} K".format(temperature))
Set("HB2C:SMS:RunInfo:RunTitle","Done {}".format(temperature))
Submit("Done")
while ''.join([chr(i) for i in getPvValue("HB2C:SMS:RunInfo:RunTitle")]).replace('\x00','') != "Done {}".format(temperature):
    time.sleep(10)
