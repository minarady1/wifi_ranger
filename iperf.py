import logging
import os
import io
import time
import subprocess
import sys
from subprocess import check_output


expID = sys.argv[1]
runID = sys.argv[2]
params = sys.argv[3] 
all_params = params.split()
all_params.append("-T")
all_params.append("{}_{}".format(expID,runID))
print (all_params)
log_dir_path = os.path.join(os.path.dirname(__file__), "logs")
log_file_name = "{}_{}.json".format(expID,runID)
file_path = os.path.join(log_dir_path, log_file_name)

out = check_output(all_params).decode("utf-8")
clean_out= out.replace('\r','').replace('\n','')

with open(file_path, 'a') as f:
    f.write('{}\n'.format(clean_out))