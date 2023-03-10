import requests
userinput = input("User input here: ")
fstring_payload_example = f"XML-Payload Stuff {userinput} more payload stuff"

payload = f'<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  xmlns:tns="http://tempuri.org/" xmlns:tm="http://microsoft.com/wsdl/mime/textMatching/"><soap:Body><LoginRequest xmlns="http://tempuri.org/"><username>{userinput}</username><password></password></LoginRequest></soap:Body></soap:Envelope>'

print(requests.post("http://10.129.202.133:3002/wsdl", data=payload, headers={"SOAPAction":'"Login"'}).content)
