import mongoengine as me
from mongoengine import Document, fields, StringField, LongField, EmbeddedDocument, EmbeddedDocumentField, ListField
import os

#region DATABASE SETUP
############################
connection_string = "mongodb+srv://piyush:piyushStudent@kawachtest.kglue.mongodb.net/?retryWrites=true&w=majority&appName=KawachTest"

me.connect(
    db='deviceDB',
    host=connection_string
)

class Data(EmbeddedDocument):
    latitude= fields.FloatField()
    longitude= fields.FloatField()
    altitude= fields.FloatField()
    timestamp= StringField()
    battery= fields.FloatField()
    speed= fields.FloatField()
    signalStrength= fields.FloatField()

class User(Document):
    imei= LongField()
    kawachId= StringField()
    accountDob= StringField()
    last50kData= ListField(EmbeddedDocumentField(Data))

    def __str__(self):
        return f"{{\nimei={self.imei!r}, \nkawach={self.kawachId!r}}}"
    
############################ 
#endregion

#region FUNCTIONS
############################ 
def insert_data_for_user(insertable_data):
    imei = insertable_data['imei']
    print(f"Searching for user with IMEI: {imei}")
    user = User.objects(imei=imei).first()

    if not user:
        print(f"IMEI {imei} not linked with a user yet.")
        return
    print(f"User found with IMEI: {imei}")

    new_data = Data(
        latitude=float(insertable_data['lat']),
        longitude=float(insertable_data['lng']),
        altitude=0,  # Baad ke version updates me dekha jayega
        timestamp=insertable_data['time'],
        battery=float(insertable_data['battery']),
        speed=float(insertable_data['speed']),
        signalStrength=float(insertable_data['signal'])
    )

    user.last50kData.insert(0, new_data)
    if len(user.last50kData) > 5:
        user.last50kData.pop() 
    user.save()
    print(f"New data added to user with IMEI: {imei}")
    
    date_str = insertable_data['time'].split(' ')[0].strip() 
    year, month, day = date_str.split('/') 
    folder_path = f"D:/ManoJava/Kawach/final_logs/{year}/{monthDict[month]}/" 

    # Create the directories if they do not exist
    os.makedirs(folder_path, exist_ok=True)

    # Create the full file path
    file_path = os.path.join(folder_path, f"{day}.txt")

    # Write the log data
    with open(file_path, 'a') as log_file:
        log_file.write(f"{insertable_data}\n")

    print(f"Data logged to {file_path}")

############################ 
#endregion


if __name__ == "__main__":
    
    insData= {'imei': '201202', 'lat': '+69.615685', 'lng': '+77.3744148', 'speed': 0, 'time': '2024/10/04 11:47:50', 'battery': 68, 'signal': 20}

    monthDict = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December'
}

    insert_data_for_user(insData)