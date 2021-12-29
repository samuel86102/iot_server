from flask import Flask, jsonify, request
from flask import render_template
import pandas as pd
import random
import authorization
import numpy as np
from numpy.linalg import norm

# add table to html
from pandas import DataFrame, read_csv

df = pd.read_csv("valence_arousal_dataset.csv")
# print(df.shape)
df.head()


# mood
df["mood_vec"] = df[["valence", "energy"]].values.tolist()
df["mood_vec"].head()

# generate token
sp = authorization.authorize() 

def calsp(track_id, invalence, inenergy, ref_df, sp, n_recs = 5):
    track_moodvec = np.array([invalence, inenergy])
    ref_df["distances"] = ref_df["mood_vec"].apply(lambda x: norm(track_moodvec-np.array(x)))
    ref_df_sorted = ref_df.sort_values(by = "distances", ascending = True)
    ref_df_sorted = ref_df_sorted[ref_df_sorted["id"] != track_id]
    return ref_df_sorted.iloc[:n_recs]

# Flask
app = Flask(__name__)
#app.config['DEBUG'] = True

@app.route("/")
def index():

    #test = request.args.get("test")
    
    return render_template('index.html')


# add submit POST
@app.route("/post_submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':

        username=request.values.get('username')
        id1=int(request.values.get('id'))
        val1=float(request.values.get('valence'))
        en1=float(request.values.get('energy'))

        new_df = df.append({
            "id": id1,
            "valence": val1,
            "energy": en1
        }, ignore_index=True)


        resdf = (calsp(track_id = id1, invalence = val1, inenergy = en1, ref_df = new_df, sp = sp, n_recs = 5))
        resdf = resdf.to_numpy().tolist()

        print((resdf))

    #return render_template('index.html',username=username, id1=id1, val1=val1, en1=en1, tables=[df.to_html(classes='data', header="true")])
    return render_template('index.html',username=username, id1=id1, val1=val1, en1=en1, tables=resdf)


# add submit POST
@app.route("/pass", methods=['GET', 'POST'])
def pass_value():
    if request.method == 'GET':

        username=(request.args.get('uname'))
        #id1=float(request.args.get('id'))
        id1=1234
        val1=float(request.args.get('val'))
        en1=float(request.args.get('en'))

        print(val1)
        print(en1)


        new_df = df.append({
            "id": id1,
            "valence": val1,
            "energy": en1
        }, ignore_index=True)


        resdf = (calsp(track_id = id1, invalence = val1, inenergy = en1, ref_df = new_df, sp = sp, n_recs = 5))
        resdf = resdf.to_numpy().tolist()

        print((resdf))

    #return render_template('index.html',username=username, id1=id1, val1=val1, en1=en1, tables=[df.to_html(classes='data', header="true")])
    return render_template('index.html',username=username, id1=id1, val1=val1, en1=en1, tables=resdf)







if __name__ == "__main__":
    app.run( host='0.0.0.0', port=5000,debug=True)

