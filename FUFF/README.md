Target: 178.128.173.79:31149

first save the host in /etc/hosts


Run a sub-domain/vhost fuzzing scan on '*.academy.htb' for the IP shown above. What are all the sub-domains you can identify? (Only write the sub-domain name)

	ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -u http://178.128.173.79:31149 -H "HOST: FUZZ.academy.htb" -fs 612 2>/dev/null

		Found: test.academy.htb:31149 (Status: 200) [Size: 0]
		Found: archive.academy.htb:31149 (Status: 200) [Size: 0]
		Found: faculty.academy.htb:31149 (Status: 200) [Size: 0]

 Before you run your page fuzzing scan, you should first run an extension fuzzing scan. What are the different extensions accepted by the domains?

 first i find the directory of domains

 		ffuf - http://faculty.academy.htb:31731/FUZZ -w /usr/share/seclists/Discovery/directory-list-2.3-small.txt


 		/courses

 		ffuf -u http://faculty.academy.htb:31731/courses/indexFUZZ -w /usr/share/seclists/Discovery/Web-Content/web-extensions.txt:FUZZ

 		php
 		phps
 		php7

One of the pages you will identify should say 'You don't have access!'. What is the full page URL?

		ffuf - http://faculty.academy.htb:31731/courses/FUZZ.php7 -w /usr/share/seclists/Discovery/directory-list-2.3-small.txt

		linux-security

In the page from the previous question, you should be able to find multiple parameters that are accepted by the page. What are they?

		fuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u http://faculty.academy.htb:31731/courses/linux-security.php7 -X POST -d 'FUZZ=key' -H 'Content-Type: application/x-www-form-urlencoded' -ms 780 2>/dev/null
user                    [Status: 200, Size: 780, Words: 223, Lines: 53, Duration: 82ms]

lets find anotherone 

ffuf -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt:FUZZ -u http://faculty.academy.htb:31731/courses/linux-security.php7 -X POST -d 'FUZZ=key' -H 'Content-Type: application/x-www-form-urlencoded' -fs 900 2>/dev/null

username                [Status: 200, Size: 781, Words: 223, Lines: 53, Duration: 89ms]

 Try fuzzing the parameters you identified for working values. One of them should return a flag. What is the content of the flag?

 		ffuf -w /usr/share/seclists/Usernames/Names/names.txt:FUZZ -u http://faculty.academy.htb:31149/courses/linux-security.php7 -X POST -d 'username=FUZZ' -H 'Content-Type: application/x-www-form-urlencoded' -ms 773 2>/dev/null
 		harry                   [Status: 200, Size: 773, Words: 218, Lines: 53, Duration: 41ms]

lets run in curl 
		curl -s http://faculty.academy.htb:31149/courses/linux-security.php7 -X POST -d 'username=harry' -H 'Content-Type: application/x-www-form-urlencoded'
