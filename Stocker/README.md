
STOCKER

IP 10.10.11.196

My first step is to start collecting the information about the machine.
As usual, I start with namp to find open port.

![Screenshot 2023-06-04 at 14 06 13](https://github.com/darshilthummar/hackthebox/assets/49148722/c15be363-be38-4ec9-bd50-0a37a443d016)

as we can see two ports are open 80 HTTP and 22 SSH 

I used the -sCV flag to get more resources about the found ports.

I search IP in the browser but It shows nothing. 

I add the hostname and the IP on the system hosts config file.
After this step, we can able to browse the page.


It’s a basic web page which has nothing in the backend, no Hint.

![Screenshot 2023-06-06 at 07 07 06](https://github.com/darshilthummar/hackthebox/assets/49148722/72441814-765c-4c48-95a6-e6eb2a3b399c)

Let’s check the other directory and virtual hots. For that, we can use ffuf and gobuster. 
I used gobuster to after a known directory by using a common directory file. Noting have found on http://stocker.htb

![Screenshot 2023-06-06 at 07 13 29](https://github.com/darshilthummar/hackthebox/assets/49148722/b6e609d2-8e94-455e-b322-0a7fb47fde68)

Let’s go for vhost. As we see there is only one vhost “dev.stocker.htb”

Add to system hosts 

![Screenshot 2023-06-06 at 07 13 55](https://github.com/darshilthummar/hackthebox/assets/49148722/195efe20-f40e-4e41-b076-4d396c6e5ce6)

Search found vhost on the browser and let's see what we got.
Dev.stocker.htb has a login page.

I tried SQL injection with the help of https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master
But no luck. Also, check negix known vulnerability but nothing has been found. 

Let’s explore the web request and how it works by using the burp suite. As we send the login request with credentials, it gives an error redirecting /login?error=login-error.

![Screenshot 2023-06-04 at 14 32 39](https://github.com/darshilthummar/hackthebox/assets/49148722/6f69cac5-9f47-45a5-ac7d-aaee66b7ea45)

I change the application type to JSON to see If it gets JSON error or not. After detecting that JSON has been used in the background, I change the login credentials to JSON format. 

![Screenshot 2023-06-06 at 07 25 17](https://github.com/darshilthummar/hackthebox/assets/49148722/daba7b4e-fd95-425b-ab38-74b9bbffda9f)

{“username”:{“$ne”:”admin”}, “password”:{“$ne”:”pass”}}

![Screenshot 2023-06-04 at 14 35 15](https://github.com/darshilthummar/hackthebox/assets/49148722/65d0bc0d-7080-4faa-b6c0-be0f8fb4a55a)

It redirects to /stock page. 

It’s a basic stock page which has some products on it. When we add the product in the bag and click on the purchase it sends us to another page, which is an invoice. Here we can use the payload to find a vulnerability. 


Let’s modify the request to see any xxe vulnerability. I use PayloadsAllTheThings to check each payload in the request. 

I used <iframe src=/etc/passwd></iframe>

![Screenshot 2023-06-06 at 07 35 59](https://github.com/darshilthummar/hackthebox/assets/49148722/e3f73653-25e4-4db7-b6cd-4e11b671d1c8)


As we can see we got a passwd file in the response. Let’s ass height and width and /var/www/html/index.js

<iframe src=file:///var/www/dev/index.js height=1000px width=1000px></iframe>

![Screenshot 2023-06-04 at 15 06 17](https://github.com/darshilthummar/hackthebox/assets/49148722/eb6bf6f9-b1db-45e9-9403-eeb7f0ec2ef9)

When scan carefully the opening file we got the credential.

Now we have a username and password
Username angoose
Password: *******

Let’s use ssh and connect the server.

ssh angoose@10.10.11.196

![Screenshot 2023-06-04 at 15 08 32](https://github.com/darshilthummar/hackthebox/assets/49148722/f6d02513-47b3-4237-a188-ce2057cb1fef)

we have user.txt in the angoose directory.

For the root flag, we need to find the root privilege 
sudo -l

![Screenshot 2023-06-06 at 07 40 29](https://github.com/darshilthummar/hackthebox/assets/49148722/6bcb54b0-87ba-43a4-899d-d9550eaab5f4)

We can run any .js file under the /usr/local/scripts/ file as we see node.

I ask to ChatGPT to write a script in node.js to read /root/root/txt file.

![Screenshot 2023-06-06 at 07 43 06](https://github.com/darshilthummar/hackthebox/assets/49148722/95521f9f-4a64-4742-8b7d-d5e9f6356394)

I save code in .js format and run it under node /usr/local/script/.

![Screenshot 2023-06-06 at 07 42 48](https://github.com/darshilthummar/hackthebox/assets/49148722/da461ef4-70d7-42dc-9b1f-fab84a1b702b)

We got a root flag without the privilege to root.
