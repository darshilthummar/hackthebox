machin ip :: 10.129.101.28

start wich Nmap to see which port are rinning.


	sudo nmap -sCV -T5 10.129.101.28 
	
	Starting Nmap 7.92 ( https://nmap.org ) at 2022-10-23 14:42 EDT
	Nmap scan report for 10.129.101.28
	Host is up (0.16s latency).
	Not shown: 999 closed tcp ports (reset)
	PORT   STATE SERVICE VERSION
	80/tcp open  http    Apache httpd 2.4.38 ((Debian))
	|_http-server-header: Apache/2.4.38 (Debian)
	|_http-title: Login

	Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
	Nmap done: 1 IP address (1 host up) scanned in 10.73 seconds

Here we can see only one port is open {80}

let hit the url in browser

		it login page I check source page but nothing usal I get
		

		I use gobuster to look other dircetoy 

		gobuster dir -u http://10.129.101.28/ -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt -t 50
		===============================================================
		Gobuster v3.1.0
		by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
		===============================================================
		[+] Url:                     http://10.129.101.28/
		[+] Method:                  GET
		[+] Threads:                 50
		[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-small.txt
		[+] Negative Status codes:   404
		[+] User Agent:              gobuster/3.1.0
		[+] Timeout:                 10s
		===============================================================
		2022/10/23 14:46:32 Starting gobuster in directory enumeration mode
		===============================================================
		/images               (Status: 301) [Size: 315] [--> http://10.129.101.28/images/]
		/css                  (Status: 301) [Size: 312] [--> http://10.129.101.28/css/]   
		Progress: 681 / 81644 (0.83%)                                                    [ERROR] 2022/10/23 14:46:53 [!] Get "http://10.129.101.28/wp-login": context deadline exceeded (Client.Timeout exceeded while awaiting headers)
		/js                   (Status: 301) [Size: 311] [--> http://10.129.101.28/js/]    
		/vendor               (Status: 301) [Size: 315] [--> http://10.129.101.28/vendor/]
		/fonts                (Status: 301) [Size: 314] [--> http://10.129.101.28/fonts/] 

noting Intresting I get 

let hit SQl Sequence injection to bypass login page 
	I use admin'-- to by pass true condition and success fuly login into websit.


Congratulations!

Your flag is: e3d0796d002a446c0e622226f42e9672
