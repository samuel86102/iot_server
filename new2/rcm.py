import pandas as pd
import random
import authorization
import numpy as np
from numpy.linalg import norm

df = pd.read_csv("valence_arousal_dataset.csv")
print(df.shape)
df.head()


#mood
df["mood_vec"] = df[["valence", "energy"]].values.tolist()
df["mood_vec"].head()

#generate token
sp = authorization.authorize() 

def recommend(track_id, ref_df, sp, n_recs = 5):
    
    # Crawl valence and arousal of given track from spotify api
    track_features = sp.track_audio_features(track_id)
    track_moodvec = np.array([track_features.valence, track_features.energy])
    print(f"mood_vec for {track_id}: {track_moodvec}")
    
    # Compute distances to all reference tracks
    ref_df["distances"] = ref_df["mood_vec"].apply(lambda x: norm(track_moodvec-np.array(x)))
    
    # Sort distances from lowest to highest
    ref_df_sorted = ref_df.sort_values(by = "distances", ascending = True)
    
    # If the input track is in the reference set, it will have a distance of 0, but should not be recommendet
    ref_df_sorted = ref_df_sorted[ref_df_sorted["id"] != track_id]
    
    print("Song: " + ref_df_sorted["track_name"] +"Artist: " + ref_df_sorted["artist_name"])
    
    #print(ref_df_sorted.iloc[:n_recs])
    
    # Return n recommendations
    return ref_df_sorted.iloc[:n_recs]

def calsp(track_id, invalence, inenergy, ref_df, sp, n_recs = 5):
    track_moodvec = np.array([invalence, inenergy])
    ref_df["distances"] = ref_df["mood_vec"].apply(lambda x: norm(track_moodvec-np.array(x)))
    ref_df_sorted = ref_df.sort_values(by = "distances", ascending = True)
    ref_df_sorted = ref_df_sorted[ref_df_sorted["id"] != track_id]
    result = (ref_df_sorted["track_name"] + "  " + ref_df_sorted["artist_name"])
    return result

"""
track1 = random.choice(df["id"])
recommend(track_id = track1, ref_df = df, sp = sp, n_recs = 5)

mad_world = "3JOVTQ5h8HGFnDdp4VT3MP"
recommend(track_id = mad_world, ref_df = df, sp = sp, n_recs = 5)


zero = "27Ad12p57Wu9nTaQMRD4aR"
recommend(track_id = zero, ref_df = df, sp = sp, n_recs = 5)

rosanna = "37BTh5g05cxBIRYMbw8g2T"
recommend(track_id = rosanna, ref_df = df, sp = sp, n_recs = 5)
"""

#val = float(input())
#en = float(input())

test = "abcdefg"
val = 0.5
en = 0.1

new_df = df.append({
    "id": test,
    "valence": val,
    "energy": en
}, ignore_index=True)

result = calsp(track_id = test, invalence=val, inenergy=en,ref_df=new_df , sp=sp, n_recs = 5)

with open("data","w") as file:
    for line in result:
        file.write(line)


print(result)
