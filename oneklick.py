from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)


region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'users'


@app.route("/", methods=['GET', 'POST'])
def home():
	return render_template('index.html')


#@app.route("/about", methods=['POST'])
#def about():
#    return render_template('www.intellipaat.com')


@app.route("/", methods=['POST'])
def Addmenu():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    address = request.form['street_address']
    postcode = request.form['postcode']
    city = request.files['city']
    state = request.files['state']
    phone_number = request.files['phone_number']
    email_address = request.files['email_address']
    

    insert_sql = "INSERT INTO users VALUES (%s, %s, %s, %s,%s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if image.filename == "":
        return "Please select a file"

    try:

        cursor.execute(insert_sql, (first_name,last_name,address,postcode,city,state,phone_number,address))
        db_conn.commit()
        name = "" + first_name + " " + last_name
        Upload image file in S3 
        image_name_in_s3 = "Menu of_" + str(center_name) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...!!!")
            s3.Bucket(custombucket).put_object(Key=image_name_in_s3, Body=image)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                image_name_in_s3)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('Output.html', name=name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
