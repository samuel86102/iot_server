import pandas as pd
import random
import authorization
import numpy as np
from numpy.linalg import norm
import os
df = pd.read_csv("valence_arousal_dataset.csv")
print(df.shape)
df.head()


#mood
df["mood_vec"] = df[["valence", "energy"]].values.tolist()
df["mood_vec"].head()

#generate token
sp = authorization.authorize() 

def calsp(track_id, invalence, inenergy, ref_df, sp, n_recs = 5):
    track_moodvec = np.array([invalence, inenergy])
    ref_df["distances"] = ref_df["mood_vec"].apply(lambda x: norm(track_moodvec-np.array(x)))
    ref_df_sorted = ref_df.sort_values(by = "distances", ascending = True)
    ref_df_sorted = ref_df_sorted[ref_df_sorted["id"] != track_id]
    result = (ref_df_sorted["track_name"] + "  " + ref_df_sorted["artist_name"])
    return result


def execute():

    test = "abcdefg"
    val = 0.5
    en = 0.1

    new_df = df.append({
        "id": test,
        "valence": val,
        "energy": en
    }, ignore_index=True)

    result = calsp(track_id = test, invalence=val, inenergy=en,ref_df=new_df , sp=sp, n_recs = 5)
    return result
    '''
    with open("data","w") as file:
        i = 1
        for line in result:
            file.write(str(i)+" "+str(line) + os.linesep)
            i+=1
    for e in result:
        print(e)

    '''
