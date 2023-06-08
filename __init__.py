from flask import Flask, request, jsonify, json
import numpy as np
from pyzbar.pyzbar import decode
# import pytesseract
from nanonets import NANONETSOCR
import os
import cv2
import numpy as np
from flask import Flask, request
from typing import Final
import pymysql
from flask import jsonify
from flask import flash, request
from flask import Flask
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL
# import cv2
import numpy as np
# from pyzbar.pyzbar import decode
import pytesseract
from nanonets import NANONETSOCR
import os
import re

model = NANONETSOCR()
app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey123"
model.set_token('5ed18a44-eb16-11ed-9413-8ed029f0ba74')
net = cv2.dnn.readNet('/root/pod/yolov3_testing.cfg', '/root/pod/yolov3_training_lastround.weights')
net2 = cv2.dnn.readNet('/root/pod/yolov3_testing.cfg', '/root/pod/yolov3_training_lastsquare.weights')
#net1 = cv2.dnn.readNet('/root/pod/yolov3_testing.cfg', '/root/pod/yolov3_training_lastpod.weights')
CORS(app)
mysql = MySQL()
app.config['SECRET_KEY']= 'bonapatito'
app.config['MYSQL_DATABASE_USER'] = 'test'
app.config['MYSQL_DATABASE_PASSWORD'] = '@Test123@'
app.config['MYSQL_DATABASE_DB'] = 'production'
app.config['MYSQL_DATABASE_HOST'] = '103.109.78.141'
mysql.init_app(app)

    
@app.route('/pod_stamp_round', methods=['POST'])
def apii():
    try:
       if 'pod' not in request.files:
           return 'No image file uploaded', 400
       if 'docket_no' not in request.form:
           return 'No docket_no file uploaded', 400
       
       
       file = request.files['pod']
       docket_no = request.form['docket_no']
       file_path = '/root/pod/image/pics.jpg'
       file.save(file_path)
       image = cv2.imread(file_path, cv2.IMREAD_COLOR)
       #image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
       blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

       net.setInput(blob)
       output_layers = net.getUnconnectedOutLayersNames()
       layer_outputs = net.forward(output_layers)
       conf_threshold = 0.5
       nms_threshold = 0.4
       class_ids = []
       confidences = []
       boxes = []
       for output in layer_outputs:
           for detection in output:
               scores = detection[5:]
               class_id = np.argmax(scores)
               confidence = scores[class_id]       
               if confidence > conf_threshold:
                   center_x = int(detection[0] * image.shape[1])
                   center_y = int(detection[1] * image.shape[0])
                   width = int(detection[2] * image.shape[1])
                   height = int(detection[3] * image.shape[0])
                   left = int(center_x - width / 2)
                   top = int(center_y - height / 2)       
                   class_ids.append(class_id)
                   confidences.append(float(confidence))
                   boxes.append([left, top, width, height])
       indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
       print(len(indices))
       if len(indices) > 0:
           stamp = 'yes'
       else:
           stamp = 'no'
       pic =decode(image)
       if pic:
         qr_code = pic[0]
         qr = qr_code.data.decode('utf-8')
       else:
          text = model.convert_to_txt(
              '/root/pod/image/pics.jpg', output_file_name='/root/pod/image/OUTNAME.TXT')
          file_path = '/root/pod/image/OUTNAME.TXT'
          
          with open(file_path, 'r') as file:
               file_content = file.read()
               file_content = file_content.replace(',', '')
   
          target_text = docket_no
          if target_text in file_content:
              print('yes')
              qr = docket_no
          else:
              qr = 'no'
         

       text = model.convert_to_txt(
            '/root/pod/image/pics.jpg', output_file_name='/root/pod/image/OUTNAME.TXT')
       file_path = '/root/pod/image/OUTNAME.TXT'
       
       with open(file_path, 'r') as file:
            file_content = file.read()
            file_content = file_content.replace(',', '')

       target_text = 'POD/'
       keyword1 = 'ACKNOWLEDGEMENT'
       keyword2='POD/ACKNOWLEDGEMENT'
       if target_text in file_content and keyword1 in file_content or keyword2 in file_content:
           print('yes')
           text2 = 'yes'
       else:
           text2 = 'no' 
       data={'qrcode': qr,'stamp':stamp,'pod':text2}
       return jsonify(data)
              

    except Exception as e:
        print(e)
        return showMessage()

@app.route('/pod_stamp_rec', methods=['POST'])
def api():
    try:
       if 'pod' not in request.files:
           return 'No image file uploaded', 400
       if 'docket_no' not in request.form:
           return 'No docket_no file uploaded', 400
       
       file=request.files['pod']
       docket_no = request.form['docket_no']
       file_path = '/root/pod/image/pics.jpg'
       file.save(file_path)
       
       image = cv2.imread(file_path, cv2.IMREAD_COLOR)
       #image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)
       blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

       net2.setInput(blob)
       output_layers2 = net2.getUnconnectedOutLayersNames()
       layer_outputs2 = net2.forward(output_layers2)
       conf_threshold2 = 0.5
       nms_threshold2 = 0.4
       class_ids2 = []
       confidences2 = []
       boxes2 = []
       for output2 in layer_outputs2:
           for detection2 in output2:
               scores2 = detection2[5:]
               class_id2 = np.argmax(scores2)
               confidence2 = scores2[class_id2]       
               if confidence2 > conf_threshold2:
                   center_x2 = int(detection2[0] * image.shape[1])
                   center_y2 = int(detection2[1] * image.shape[0])
                   width2 = int(detection2[2] * image.shape[1])
                   height2 = int(detection2[3] * image.shape[0])
                   left2 = int(center_x2 - width2 / 2)
                   top2 = int(center_y2 - height2 / 2)       
                   class_ids2.append(class_id2)
                   confidences2.append(float(confidence2))
                   boxes2.append([left2, top2, width2, height2])
       indices2 = cv2.dnn.NMSBoxes(boxes2, confidences2, conf_threshold2, nms_threshold2)
       print(len(indices2))
       if len(indices2) > 0:
           stamp = 'yes'
       else:
           stamp = 'no' 

       pic =decode(image)
       if pic:
         qr_code = pic[0]
         qr = qr_code.data.decode('utf-8')
       else:
           text = model.convert_to_txt(
              '/root/pod/image/pics.jpg', output_file_name='/root/pod/image/OUTNAME.TXT')
           file_path = '/root/pod/image/OUTNAME.TXT'
           
           with open(file_path, 'r') as file:
                file_content = file.read()
                file_content = file_content.replace(',', '')
    
           target_text = docket_no
           if target_text in file_content:
               print('yes')
               qr = docket_no
           else:
               qr = 'no'
       
       text = model.convert_to_txt(
            '/root/pod/image/pics.jpg', output_file_name='/root/pod/image/OUTNAME.TXT')
       file_path = '/root/pod/image/OUTNAME.TXT'
       
       with open(file_path, 'r') as file:
            file_content = file.read()
            file_content = file_content.replace(',', '')

       target_text = 'POD/'
       keyword1 = 'ACKNOWLEDGEMENT'
       keyword2='POD/ACKNOWLEDGEMENT'
       if target_text in file_content and keyword1 in file_content or keyword2 in file_content:
           print('yes')
           text2 = 'yes'
       else:
           text2 = 'no' 
           


       data={'qrcode': qr,'stamp':stamp,'pod': text2 }
       return jsonify(data)
              

    except Exception as e:
        print(e)
        return showMessage()

@app.route('/invoice_amount', methods=['POST'])
def apied():
    try:
        # Check if the request contains an image file
        if 'image' not in request.files:
            return jsonify({'status': 404, 'message': 'Image File  Not Found...'}), 400
        if 'enter_amount' not in request.form:
            return jsonify({'status': 404, 'message': 'Amount Not Found, enter Amount..'}), 400
        files = request.files['image']
        file2 = request.form['enter_amount']
        print(file2)
        files.save('/root/flask_api/invoice_image/pic.jpg')
        print('hii')
        text = model.convert_to_txt(
            '/root/flask_api/invoice_image/pic.jpg', output_file_name='/root/flask_api/invoice_image/OUTNAME.TXT')
        file_path = '/root/flask_api/invoice_image/OUTNAME.TXT'

        with open(file_path, 'r') as file:
            file_content = file.read()
            file_content = file_content.replace(',', '')

        target_text = file2
        if target_text in file_content:
            print('yes')
            text2 = 'yes'
        else:
            text2 = 'no'
        data = {'amount': file2, 'found': text2}

        # os.remove('\invoice_image\pic.jpg')
        return jsonify(data)

    except Exception as e:
        print(e)
        return showMessage()

@app.route('/webhook', methods=['POST'])
def webhook():
    
    data = request.get_json()
    lowercase_text = get_lowercased_text(data)
    response = process_message(lowercase_text)
    return response
    

def get_lowercased_text(data):
    if 'payload' in data and 'type' in data['payload'] and data['payload']['type'] == 'text':
        text = data['payload']['payload']['text']
        lowercase_text = text.lower()
        return lowercase_text
    else:
        return ''
    
def process_message(lowercase_text):
    if lowercase_text == 'hi':
        temp='''Hey there
        
_*Welcome to cwl chat boat*_
You can track following information with this chat

1️⃣	Track docket-> *D12345* where   12345=docket number

2️⃣	Track vehicle-> *V12345* where  12345=vehicle number

3️⃣	Track freight-> *F12345* where  12345=docket number

4️⃣	Track outstanding-> *O12345* where  12345=invoice number

5️⃣	Track pincode-> *P12345* where   12345=pincode

Thanks for using cwl chat boat'''
        return temp
    elif lowercase_text == 'my order':
        return 'Enter pincode'
    elif lowercase_text == 'help':
        template='''All you can do
Hey there,
You can check you order, delivery status, Vehical details, any many more thing .

1) For pin-code finder you can write your pin-code number with first letter of word pin-code
Eg : P123456

2) For docket status you can write your docket number with first letter of word docket
Eg : D123456

3) For Truck location you can write your vehicle number with first letter of word truck
Eg : T123456

4) For fright you can write your docket number with first letter of word fright
Eg : F123456

5) For outstanding you can write your invoice number with first letter of word outstanding
Eg : O123456

✈️ 🚇 🚢
Thanks for using Countrywide Logistics India PVT Ltd'''
        return template
    elif re.match(r'^p\s*\d+$', lowercase_text):
        order_number = re.search(r'\d+', lowercase_text).group()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        row= cursor.execute("select bsp.pincode ,b.name ,bsp.distance_km  from branch_serviceable_pincodes bsp  join branches b on b.id = bsp.branch_id where bsp.pincode = {} ".format(order_number)) 
        row = cursor.fetchone()
        if row == None:
            return "Pincode Not Found !"
        else:
            b=dict(row)
            pincode= b['pincode']
            name= b['name'] 
            distance_km= b['distance_km']
            return ("Pincode : %d \nServiceable Branch: %s \nDistance From Branch : %s km"%(pincode,name,distance_km))
        
    elif re.match(r'^d\s*\d+$', lowercase_text):
        docket_number = re.search(r'\d+', lowercase_text).group()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        row2= cursor.execute("call boat_track_shipment({});".format(docket_number)) 
        row2 = cursor.fetchone()
        if row2 == None:
            return ( "deckot not Found !")
        else:
            b2=dict(row2)
            status=b2['status']
            return( "status : %s"%(status))
    else:
        return "Sorry ! I don't understand"
    
    
    


def send_message(recipient, message):
    url = "https://api.gupshup.io/sm/api/v1/msg"
    params = {
        "channel": "whatsapp",  # Change to the desired channel (e.g., "sms", "facebook", etc.)
        "source": "+919265705461",  # Replace with your source name
        "destination": recipient,
        "message": message,
        "header" :'pincode'
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Make a POST request to the Gupshup API to send the message
    response = requests.post(url, data=params, headers=headers)
    # Handle the response as needed
    # ...


@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'something is wrong'
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


if __name__ == '__main__':
    app.run(debug=True)

