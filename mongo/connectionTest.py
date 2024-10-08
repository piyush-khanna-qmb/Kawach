import mongoengine as me
from mongoengine import Document, fields, StringField, LongField, EmbeddedDocument, EmbeddedDocumentField, ListField

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
        print(f"IMEI {imei} not linked with a user.")
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

    user.save()
    print(f"New data added to user with IMEI: {imei}")

############################ 
#endregion


if __name__ == "__main__":
    
    insData= {'imei': '12345', 'lat': '+28.615685', 'lng': '+77.3744148', 'speed': 0, 'time': '2024/10/04 11:47:50', 'battery': 68, 'signal': 20}

    insert_data_for_user(insData)