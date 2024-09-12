def sendMongo(data):
    print("\n==> Sending data to MONGO", str(data),"\n")

currentUsers= {}
class User:
    imei= 0
    battery= 0
    lat= 0
    lng= 0
    time= ""
    speed= 0
    signal= 0

    def __init__(self, imei) -> None:
        self.imei= imei
    
    def __str__(self) -> str:
        return ("IMEI:"+str(self.imei)+"\nbattery"+str(self.battery)+"\lat"+str(self.lat)+"\lng"+str(self.lng)+"\signal"+str(self.signal))


while True:
    typ= int(input("1. Login\n2. Battery\n3. GPS/LBS data"))
    if typ==1:
        imei= input("Enter imei: ")
        if imei not in currentUsers:
            newUser= User(imei)
            currentUsers[imei]= newUser
        else:
            print("User already in progress. Not possible")
    
    elif typ==2:
        imei= input("Enter Imei: ")
        bat= int(input("ENter battery: "))
        sign= int(input("ENter signal str.: "))

        if imei in currentUsers:
            currentUsers[imei].battery= bat
            currentUsers[imei].signal= sign
    
    elif typ==3:
        imei= input("Enter Imei: ")
        lat= input("Enter lat: ")
        lng= input("Enter lng: ")
        # speed= input("Enter Imei: ")

        if imei in currentUsers:
            currentUsers[imei].lat= lat
            currentUsers[imei].lng= lng
        
            sendMongo(currentUsers[imei])
