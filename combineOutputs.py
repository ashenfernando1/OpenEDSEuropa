import pandas as pd
import os

final_df = pd.DataFrame()
output_full_path = sorted(['outputs/eyesstream_20210526T05/'+i for i in os.listdir('outputs/eyesstream_20210526T05')])
for i in output_full_path:
   final_df = pd.concat([final_df, pd.read_csv(i)])
final_df.to_csv('outputs/eyesstream_20210526T05/combined_eyesstream_20210526T05.csv')