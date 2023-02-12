import subprocess
import argparse
import ffmpeg
import numpy as np
import os

parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()
filename = args.file.split('.')[0]
#print(args.file)

#video = ffmpeg.probe("videos/"+args.file)
#num_nodes = (int(np.ceil(float(video['streams'][0]['duration'])/60)))

#subprocess.run(["cp","videos/"+args.file,"videos/proc_video/"])
subprocess.run(["./videos/try.sh",args.file])
#subprocess.run(["rm","videos/proc_video/"+args.file])
#subprocess.run(["mkdir","scripts/"+filename])
os.makedirs("scripts/"+filename, exist_ok=True)
os.makedirs("logs/"+filename, exist_ok=True)
os.makedirs("outputs/"+filename, exist_ok=True)

for i in os.listdir("videos/proc_video/"):
    if "output" in i and args.file in i:
        slurm_file = i.split('.')[0]+".slurm"
        with open(f"scripts/{filename}/{slurm_file}", "w") as f:
            f.write("#!/bin/bash\n")
            f.write("\n")
            f.write(f"#SBATCH --nodes=1\n")
            f.write("#SBATCH --ntasks=1\n")
            f.write("#SBATCH --partition=normal\n")
            f.write(f"#SBATCH --output='logs/'{filename}/%j.out")
            f.write("#SBATCH --mail-user=aaf170130@utdallas.edu\n")
            f.write("\n")
            f.write(f"python inference.py videos/proc_video/{i}\n")

with open("run-all.sh","w") as g:
    g.write("#!/bin/bash\n")
    g.write("\n")
    g.write(f"for script in $(ls scripts/{filename}/*.slurm)\n")
    g.write("do\n")
    g.write("   sbatch $script\n")
    g.write("done\n")

with open("combineOutputs.py","w") as h:
    h.write("import pandas as pd\n")
    h.write("import os\n")
    h.write("\n")
    h.write("final_df = pd.DataFrame()\n")
    h.write(f"output_full_path = sorted(['outputs/{filename}/'+i for i in os.listdir('outputs/{filename}')])\n")
    h.write("for i in output_full_path:\n")
    h.write("   final_df = pd.concat([final_df, pd.read_csv(i)])\n")
    h.write(f"final_df.to_csv('outputs/{filename}/combined_{filename}.csv')")

subprocess.run(["chmod","u+x","combineOutputs.py"]),
