import paho.mqtt.client as mqttc

broker="192.168.178.88"
port=1883

def on_publish(client,userdata,result):
    print("data published \n")
    pass

client1= mqttc.Client("command")
client1.on_publish = on_publish
client1.connect(broker,port)
ret= client1.publish("LR/command", "FX5")
