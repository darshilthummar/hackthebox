FOOTPRINTING 

¬¬Lab-1	

Summary

The FTP proxy server on host 10.129.45.17 is allowing unauthenticated access to the FTP service on port 2121. This vulnerability allows unauthorized access to the server's files and data, potentially exposing sensitive information to attackers.

Steps: 

Host : 10.129.45.17

Let’s start dig which ports are open and what we got form it.

	Sudo nmap -sCV -p- 10.129.45.17
		-sCV is for default script and dig version information.
		-p- is for scan all port.

![Picture 1](https://user-images.githubusercontent.com/49148722/234991260-eb9c1e13-6502-41ed-918c-c2b28f0984e8.png)

As we can see form scan results, here four ports are open. 21,22,53,2121
Two FTP ports are open in the system. One is proftpd and another one Is proxy ftp.


Let’s enumerate more for ftp port by using script FTP.
 	As we can see there is no more information, we got by using script.

Let enumerate manually. 
	I use wget to see what inside of proxy port. 
	wget ftp://10.129.45.17:2121/
  
  ![Picture 2](https://user-images.githubusercontent.com/49148722/234991302-e4764aac-cd3a-467f-83f9-de2657ab0400.png)
  

As we can see it can connect with 2121 but login cred is wrong let use "ceil:qwer1234" which is given in hint. 


As we can see that connection has been establish with cred. 
And the file has been saved in INDEX.HTML, in that file there is list of other directory we can found on ftp server

![Picture 3](https://user-images.githubusercontent.com/49148722/234991348-d09df11f-2bad-4a9d-ab48-68e9b928e35b.png)


Jump into ssh directory and see what we got.

![Picture 4](https://user-images.githubusercontent.com/49148722/234991385-bab33abd-616f-4982-a232-2df24814c970.png)



as we found in ssh directory, there are three file which can help to login into ssh port.
 id_rsa is a public key, which can help to get into ssh server.

For that we need to change permission of id_rsa.

	Chmod 600 id_rsa
Let connect by using public key with username and host name.
	
ssh -i id_rsa ceil@10.129.45.17

![Picture 5](https://user-images.githubusercontent.com/49148722/234991437-baca3b3c-838f-4423-ad68-fa5393912e1c.png)


hola we are in 

![Picture 6](https://user-images.githubusercontent.com/49148722/234991468-5b1ee4db-4531-4aed-8ef1-11fa9dcc8286.png)

Expected Results:
The FTP service on the target host should require authentication to access the server's files and data. The public key file id_rsa should have restricted permissions to prevent unauthorized access.

Impact:
The vulnerability described above could potentially allow unauthorized users to access sensitive data and files on the target host, including personally identifiable information (PII) and confidential data. Attackers could leverage this vulnerability to escalate their privileges and gain unauthorized access to additional resources on the target network.

