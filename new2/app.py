from flask import Flask, jsonify, request
from flask import render_template
import pandas as pd
import random
import authorization
import numpy as np
from numpy.linalg import norm

#add table to html
from pandas import DataFrame, read_csv

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
    return ref_df_sorted.iloc[:n_recs]

#Flask
app = Flask(__name__)
app.config['DEBUG'] = True
@app.route("/")
def index():
    return render_template('1.html', test="Input these data:")


#add submit POST
@app.route("/post_submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        return render_template('1.html',username=request.values.get('username'), id1=request.values.get('xxxx'), val1=request.values.get('valence'), en1=request.values.get('en'), tables=[df.to_html(classes='data', header="true")])



@app.route("/post_submit", methods=['GET', 'POST'])
def html_table():
    '''
    new_df = df.append({
    "id": id1,
    "valence": val1,
    "energy": en1
    }, ignore_index=True)
    '''
    #resdf = df.DataFrame(calsp(track_id = id1, invalence = val1, inenergy = en1, ref_df = new_df, sp = sp, n_recs = 5))
    return render_template('1.html', tables=[df.to_html(classes='data', header="true")])


if __name__ == "__main__":
    app.run( host='0.0.0.0', port=5000,debug=True)
