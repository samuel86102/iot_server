from flask import Flask, jsonify, request
from flask import render_template
import pandas as pd
import random
import authorization
import numpy as np
from numpy.linalg import norm
import socket
import time
import threading

global reData 

class Worker(threading.Thread):
    def __init__(self):
        
        threading.Thread.__init__(self)

    def run(self):
        receiverServer = ReceiverServer()
        while True:
            receive_ip = receiverServer.socket_accept()
            for i in range(20):
                reData1 = receiverServer.socket_read()
                
                gsrData = receiverServer.socket_read()
                
                if receive_ip == '192.168.43.230':
                    if reData1 != None and reData1 !=b'':
                        print('     Receiver Data:%s' % gsrData)
                        time.sleep(1)
                if receive_ip == '192.168.43.174':
                    if reData1 != None and reData1 !=b'':
                        print('     Receiver Data:%s' % reData1)
                        global reData 
                        reData = str(reData1)

                        time.sleep(0.1)


class ReceiverServer:
    def __init__(self):
        host_ip = "0.0.0.0"
        listen_port = 8124

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host_ip, listen_port))  # ADD IP HERE
        self.server_socket.listen(5)

        print('server start at: %s:%s' % (host_ip, listen_port))
        print('wait for connection...') 


    def socket_accept(self):
        self.connection, addr = self.server_socket.accept()
        addr = str(addr)
        print('connected by client address: %s' % (addr))

        return addr

    def socket_send(self, content):
        self.connection.write(bytes(content, encoding='utf-8'))
        
    def socket_read(self):
        content = self.connection.recv(1024)
        #reData=str(content)
        if content != None and content !=b'':
            print("receive time from client: " + str(content))
        return content


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
    return render_template('index.html')


# add submit POST
@app.route("/post_submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':

        username=request.values.get('username')
        id1=random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()')
        #val1=float(request.values.get('valence'))
        #en1=float(request.values.get('energy'))
        
        

        if reData ==b'Angry':
            
            val1=random.uniform(0.4,0.5)
            en1=random.uniform(0.85,1)
            
        elif reData == b'Sad':
            val1=random.uniform(0,0.5)
            en1=random.uniform(0.01,0.5)
        elif reData=="Neutral":
            val1=random.uniform(0.45,0.55)
            en1=random.uniform(0.45,0.55)
        elif reData=="Disgust":
            val1=random.uniform(0,0.25)
            en1=random.uniform(0.5,0.75)
        elif reData=="Surprise":
            val1=random.uniform(0.5,0.75)
            en1=random.uniform(0.75,1)
        elif reData=="Fear":
            val1=random.uniform(0.3,0.5)
            en1=random.uniform(0.75,1)
        elif reData=="Happy":
            val1=random.uniform(0.8,1)
            en1=random.uniform(0.4,0.6)
        else:
            val1=random.uniform(0,1)
            en1=random.uniform(0,1)

        new_df = df.append({
            "id": id1,
            "valence": val1,
            "energy": en1
        }, ignore_index=True)



        resdf = (calsp(track_id = id1, invalence = val1, inenergy = en1, ref_df = new_df, sp = sp, n_recs = 5))
        resdf = resdf.to_numpy().tolist()

        print((resdf))


    #return render_template('index.html',username=username, id1=id1, val1=val1, en1=en1, tables=[df.to_html(classes='data', header="true")])
    return render_template('index.html',redata=reData, username=username, id1=id1, val1=val1, en1=en1, tables=resdf)



if __name__ == "__main__":
    #app.run( host='0.0.0.0', port=8787, debug=True)
    
    #build worker instance
    my_worker = Worker()
    my_worker.start()    
    
    app.run( host='0.0.0.0', port=8787, debug=True)


    
