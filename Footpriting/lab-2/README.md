FOOTPRINTING LAB-2 HTB	

This second server is a server that everyone on the internal network has access to. In our discussion with our client, we pointed out that these servers are often one of the main targets for attackers and that this server should be added to the scope.
Our customer agreed to this and added this server to our scope. Here, too, the goal remains the same. We need to find out as much information as possible about this server and find ways to use it against the server itself. For the proof and protection of customer data, a user named HTB has been created. Accordingly, we need to obtain the credentials of this user as proof.

Machine ip : 10.129.202.41

Let get started:
	
Stapes:
Start with nmap 
		sudo nmap -sCV 10.129.202.41 -p- 
	
  ![Screenshot 2023-04-30 at 13 14 56](https://user-images.githubusercontent.com/49148722/235354530-66910fd9-ceab-44d9-a945-af12f2ebd856.png)

	
as we can see on nmap result there are list of ports are open at the movement. The first port is 111 which is rpcbind (NFS). This port work as as SMB. 
	
Let’s dig deep and find what we get from it. For that we use –script nfs* 
	sudo nmap -p111,2049 10.129.202.41 –script nfs*
	
  ![Screenshot 2023-04-30 at 13 22 05](https://user-images.githubusercontent.com/49148722/235354535-c614b028-dcbb-4d6e-a08c-1f96ad11431f.png)

as we can see we have discovered such as nfs service. Now let mount in our local machine. For that we need to create empty folder and month nfs service into local machine. Once we mount, we can navigate it view it just like server local machine.
	Showmount -e 10.129.202.41

![Screenshot 2023-04-30 at 13 27 12](https://user-images.githubusercontent.com/49148722/235354550-f28642b8-1569-4337-a0d2-431153295fce.png)

Create empty folder 
	mkdir Target-nfs
	sudo -t nfs 10.129.202.41:/ ./Target-nfs/ -o nolock
	
once we mount the nfs service we can navigate all file.

![Screenshot 2023-04-30 at 13 28 34](https://user-images.githubusercontent.com/49148722/235354571-ad02ac20-41f7-4a14-870b-c1effcac925b.png)

As we can see it not allow to move into directory 
For that we should change root user 

![Screenshot 2023-04-30 at 13 29 14](https://user-images.githubusercontent.com/49148722/235354591-830e79c2-677b-4f71-b358-56e5ac92714a.png)

As we can see there is only one file which is content data let see what we can get from it. 
	
As we can see it is a conversation between alex and operator, and alex shared their password. 

![Screenshot 2023-04-30 at 13 32 09](https://user-images.githubusercontent.com/49148722/235354624-c24d4271-735b-44d8-9cc4-785019fa2cf3.png)


Let’s use it over rdp which is open port as discovered on nmap result. 
I am using xfreerdp 
	sudo xfreerdp /u:alex /v:10.129.202.41 /p:’PASSWORD’

![Screenshot 2023-04-30 at 13 36 33](https://user-images.githubusercontent.com/49148722/235354685-3821a03a-8415-452c-bcb9-9a0c1d35a07b.png)


I tried to connect sql server management studio with alex credential. But no luck so, I dig deep search all file for credential and I got form alex file profile. 

![Screenshot 2023-04-30 at 13 37 33](https://user-images.githubusercontent.com/49148722/235354773-57ed6a3b-29bf-4b45-85c5-f653c3ee1b9c.png)


I tried this credential on sql server as well but no luck. 

I think it’s for new user such as administration. So I try to logging with this by using RDP.
	sudo xfreerdp /u:administration /v:10.129.202.41 /p:’PASSWORD’
no luck lets user administrator.

  sudo xfreerdp /u:administrator /v:10.129.202.41 /p:’PASSWORD’
I got access of admin user. 

![Screenshot 2023-04-30 at 13 44 53](https://user-images.githubusercontent.com/49148722/235354782-5685c613-8a4a-45a1-8c60-77ee4a4be678.png)

Let open sql manager studio and find out the HTB user’s password. 

![Screenshot 2023-04-30 at 13 45 25](https://user-images.githubusercontent.com/49148722/235354815-3cbcd5f2-9728-4b5e-92ee-b1d2c4569dfc.png)

First let’s see how mane databases are in the server.
As we can see list of databases can find.

![Screenshot 2023-04-30 at 13 53 16](https://user-images.githubusercontent.com/49148722/235354818-3c7ae77d-0806-4d02-97e2-1ec2f991eece.png)

Dig deep and use where query to find same username of table.

![Screenshot 2023-04-30 at 13 53 52](https://user-images.githubusercontent.com/49148722/235354820-8c283d2e-8d12-4a57-985b-d08963342b53.png)

    select * from accounts.dbo.devsacc where name = ‘htb’;
    
![Screenshot 2023-04-30 at 13 54 24](https://user-images.githubusercontent.com/49148722/235354964-96ab6e96-7947-4347-b214-a4a444509c81.png)

