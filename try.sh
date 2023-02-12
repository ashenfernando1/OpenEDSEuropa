#!/bin/bash

#VAR=$1

#mkdir "${VAR}_try"
VAR=$1

#if not exist "proc_vid" mkdir "proc_vid"

#dastring=$(ffmpeg -i VAR)
#dastring=$(ffmpeg -i VAR 2>&1 | grep "Duration" | cut -d ' ' -f 4 | sed s/,// | sed 's@\..*@@g' | awk '{ split($1, A, ":"); split(A[3], B, "."); print A[2]+1 }')



#echo "$(ffmpeg -i $VAR 2>&1 | grep "Duration" | cut -d ' ' -f 4 | sed s/,// | sed 's@\..*@@g' | awk '{ split($1, A, ":"); split(A[3], B, "."); print A[2]+1 }')"
#num_nodes=$(ffmpeg -i $VAR 2>&1 | grep "Duration" | cut -d ' ' -f 4 | sed s/,// | sed 's@\..*@@g' | awk '{ split($1, A, ":"); split(A[3], B, "."); print A[2]+1 }')

ffmpeg -i videos/$VAR -c copy -map 0 -segment_time 00:01:00 -f segment videos/proc_video/output%03d_$VAR

#echo "$num_nodes"

#cmnd = ffmpeg -i VAR 2>&1 | grep "Duration"
#eval dastring=\`${cmnd}$\`
#| cut -d ' ' -f 4 | sed s/,// | sed 's@\..*@@g' | awk '{ split($1, A, ":"); split(A[3], B, "."); print A[2]+1 }'	
