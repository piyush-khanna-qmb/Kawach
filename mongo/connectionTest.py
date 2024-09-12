import mongoengine as me
from mongoengine import Document, fields, StringField, LongField, EmbeddedDocument, EmbeddedDocumentField, ListField

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

# Example usage
# data= [
#     Data(latitude= 23.77788, longitude= 77.88856002, altitude= 0, timestamp= "2024/08/23 11:15:29", battery= 33.3, speed= 36),
#     Data(latitude= 53.77788, longitude= 67.88856002, altitude= 10, timestamp= "2024/08/23 11:15:29", battery= 32.3, speed= 36.7)
# ]
data= [
    Data(latitude= 30.73609, longitude= 76.7755, altitude= 0, timestamp= "2024/08/23 11:15:24", battery= 33.3, speed= 36, signalStrength= 53.3)
]
user = User(imei= 123, kawachId= "test102", accountDob= "2024/12/06", last50kData= data)
user.save()

found_user = User.objects(imei=1234567)
print(found_user)

