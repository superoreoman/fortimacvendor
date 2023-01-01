from flask import Flask, render_template, url_for, request
import urllib.request as urllib2
import json
import codecs
import paramiko
app = Flask(__name__)

 

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/result',methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    # print(output)
    # print(output)
   
    name = output["name"]
    ipForti = output["ip"]
    if ipForti != "":
    # Set the IP address and port of the Fortigate device
        device_ip = ipForti
        port = 22

        # Set the username and password for the device
        username = 'admin'
        password = 'admin'

        # Create an SSH client
        client = paramiko.SSHClient()

        # Set the missing host key policy to automatically add any unknown host keys
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the Fortigate device
        client.connect(device_ip, port=port, username=username, password=password)

        # Run a command on the device
        stdin, stdout, stderr = client.exec_command('get system arp')

        # Print the output of the command
        print("PRINETR")
        print( )
        name =str(stdout.read().decode('UTF-8'))
        
        # Disconnect from the device
        client.close()
        ipForti==""
    print(name+ "NAME")
    
    if name  == ipForti =="":
        return render_template("index.html")
    
    ip = None
    mac = None
    data = []
    
    # Iterate through each line in the input string
    for line in name.split():
        # If the line contains 5 colons, it is a MAC address
        if line.count(":") == 5:
            mac = line
        # If the line contains 3 dots, it is an IP address
        elif line.count(".") == 3:
            ip = line
            
        # If both the IP and MAC variables are not None, add them to the data list
        if ip and mac:
            data.append((ip, mac))
            # Reset the IP and MAC variables to None
            ip = None
            mac = None

    print(data)

    #33221321321321321231
    listEX = name
    url = "http://macvendors.co/api/"
    #Mac address to lookup vendor from
    print("STARTING")
    name =""
    for first, second in data:
        
        name+=first #+"|"+second
        mac_address = second
        request2 = urllib2.Request(url+mac_address, headers={'User-Agent' : "API Browser"}) 
        response = urllib2.urlopen( request2 )
        #Fix: json object must be str, not 'bytes'
        reader = codecs.getreader("utf-8")
        obj = json.load(reader(response))

        #Print company name
        try:
            name +="| "+obj['result']['company']
        except:
            name +="| "+" | "+"Not Found ):"  
        name +="\n"
        
   
    print("DONE")
    print(name)
    return render_template('index.html', name = name , ip =ipForti)
    




if __name__ == "__main__":
    app.run(host='192.168.1.110')
