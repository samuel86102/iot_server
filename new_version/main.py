from flask import Flask, jsonify, request, send_from_directory
from flask import render_template
import pandas as pd
import random
import authorization
import numpy as np
from numpy.linalg import norm
import socket
import time
import threading

global rawCamData 
global rawGsrData

reData = "None"

#rawCamData = "b'Angry'"


class Worker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        '''
        #get value via consumer class 12/30
        my_comsumer = Comsumer()
        my_comsumer.start()
        '''
        
    def run(self):
        
        receiverServer = ReceiverServer()
        receive_ip = receiverServer.socket_accept()

        #global reData

        #while True:

        '''    
        global rawCamData
        global rawGsrData
        ''' 

        for i in range(20):
            reData = receiverServer.socket_read()
            with open("./reData","w") as file:
                file.write(reData)
            '''
            if receive_ip == '192.168.50.165':
                if reData != None and reData1 !=b'':
                    print('     Receiver Data:%s' % reData)

                    #There no effect
                    global rawGsrData
                    self.reData=reData
                    rawGsrData=str(self.reData)
                    #---nonono
                    #time.sleep(1)
            '''      
            if receive_ip == '127.0.0.1':
                print("Received data from client: %s" % reData)
                '''

                if reData != None and reData1 !=b'':
                    print('     Receiver Data:%s' % reData)

                    #There no effect
                    global rawCamData
                    self.reData=reData
                    rawCamData=str(self.reData)
                    #---nonono
                    #time.sleep(0.1)
                '''
            else:
                print("no")






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
        self.connection, acpt_data = self.server_socket.accept()
        addr = acpt_data[0]
        print('connected by client address: %s' % (addr))

        return addr

    def socket_send(self, content):
        self.connection.write(bytes(content, encoding='utf-8'))
        
    def socket_read(self):
        return self.connection.recv(1024).decode()

        '''
        #add try 12/31
        global rawCamData
        print("rawCamData before write is :" + rawCamData + "hahaha")
        rawCamData=str(content)
        print("rawCamData now is: " + rawCamData + "hahaha")
        #--end of try---
        ''' 


# add table to html
from pandas import DataFrame, read_csv

df = pd.read_csv("valence_arousal_dataset.csv")
# print(df.shape)
df.head()


# mood
df["mood_vec"] = df[["valence", "energy"]].values.tolist()
df["mood_vec"].head()

# Generate API token
sp = authorization.authorize() 

# Calculation
def calsp(track_id, invalence, inenergy, ref_df, sp, n_recs = 5):
    track_moodvec = np.array([invalence, inenergy])
    ref_df["distances"] = ref_df["mood_vec"].apply(lambda x: norm(track_moodvec-np.array(x)))
    ref_df_sorted = ref_df.sort_values(by = "distances", ascending = True)
    ref_df_sorted = ref_df_sorted[ref_df_sorted["id"] != track_id]
    return ref_df_sorted.iloc[:n_recs]




def ConvertData(reData):

    username="tester"
    id1=random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()')
    
    if reData == "Angry":
        val1=random.uniform(0.4,0.5)
        en1=random.uniform(0.85,1)

    elif reData == "Sad":
        val1=random.uniform(0,0.5)
        en1=random.uniform(0.01,0.5)

    elif reData == "Neutral":
        val1=random.uniform(0.45,0.55)
        en1=random.uniform(0.45,0.55)

    elif reData == "Disgust":
        val1=random.uniform(0,0.25)
        en1=random.uniform(0.5,0.75)

    elif reData == "Surprise":
        val1=random.uniform(0.5,0.75)
        en1=random.uniform(0.75,1)

    elif reData == "Scared":
        val1=random.uniform(0.3,0.5)
        en1=random.uniform(0.75,1)

    elif reData == "Happy":
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

    return resdf




# Flask
app = Flask(__name__)
#app.config['DEBUG'] = True


@app.route("/")
def index():
    return render_template('index.html')
    #return app.send_static_file('index.html')
    #return send_from_directory('templates','index.html')


@app.route("/fetch_data",methods=[ "GET",'POST'])
def fetch_data():

    with open("reData","r") as file:
        reData = file.read()
    
    resdf = ConvertData(reData)
    #return render_template('index.html',data=jsonify(a))
    return jsonify(resdf)





# Following is the major method of submit POST
@app.route("/post_submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':

        with open("./reData","r") as file:
            reData = file.read()

    resdf = ConvertData(reData)


    
    #return render_template('index.html',redata=reData, username=username, id1=id1, val1=val1, en1=en1, tables=resdf)
    return render_template('index.html',redata=reData, tables=resdf)



if __name__ == "__main__":
    

    #build worker instance
    my_worker = Worker()
    my_worker.start()    
    
    app.run( host='0.0.0.0', port=8787, debug=True)
