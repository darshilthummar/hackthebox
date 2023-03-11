Challenge Lab: Forensics
   
   Difficulty: Easy
   
   CHALLENGE DESCRIPTION
      "A Junior Developer just switched to a new source control platform. Can you find the secret token?"
   

   Zip Password: hackthebox
    
   Start by Downloading file and unzip with the password.
      
                  total 20
            drwxr-xr-x 3 kali kali 4096 May 30  2019 .
            drwxr-xr-x 3 kali kali 4096 Mar 11 13:58 ..
            -rw-r--r-- 1 kali kali 2635 May 30  2019 bot.js
            -rw-r--r-- 1 kali kali  199 May 30  2019 config.json
            drwxr-xr-x 7 kali kali 4096 May 30  2019 .git

   you can see there is hiddent file .get 
   lets go in and check what we have..
       
                       $ git log 
                  commit edc5aabf933f6bb161ceca6cf7d0d2160ce333ec (HEAD -> master)
                  Author: SherlockSec <dan@lights.htb>
                  Date:   Fri May 31 14:16:43 2019 +0100

                      Added some whitespace for readability!

                  commit 47241a47f62ada864ec74bd6dedc4d33f4374699
                  Author: SherlockSec <dan@lights.htb>
                  Date:   Fri May 31 12:00:54 2019 +0100

                      Thanks to contributors, I removed the unique token as it was a security risk. Thanks for reporting responsibly!

                  commit ddc606f8fa05c363ea4de20f31834e97dd527381
                  Author: SherlockSec <dan@lights.htb>
                  Date:   Fri May 31 09:14:04 2019 +0100

                      Added some more comments for the lovely contributors! Thanks for helping out!

                  commit 335d6cfe3cdc25b89cae81c50ffb957b86bf5a4a
                  Author: SherlockSec <dan@lights.htb>
                  Date:   Thu May 30 22:16:02 2019 +0100

                      Moving to Git, first time using it. First Commit!


   log directory has history of chnages from the junior develoer.
   Let’s focus on the one where the tokens were removed:
      
                     git show 47241a47f62ada864ec74bd6dedc4d33f4374699
               commit 47241a47f62ada864ec74bd6dedc4d33f4374699
               Author: SherlockSec <dan@lights.htb>
               Date:   Fri May 31 12:00:54 2019 +0100

                   Thanks to contributors, I removed the unique token as it was a security risk. Thanks for reporting responsibly!

               diff --git a/config.json b/config.json
               index 316dc21..6735aa6 100644
               --- a/config.json
               +++ b/config.json
               @@ -1,6 +1,6 @@
                {

               -       "token": "SFRCe3YzcnNpMG5fYzBudHIwbF9hbV9JX3JpZ2h0P30=",
               +       "token": "Replace me with token when in use! Security Risk!",
                       "prefix": "~",
                       "lightNum": "1337",
                       "username": "UmVkIEhlcnJpbmcsIHJlYWQgdGhlIEpTIGNhcmVmdWxseQ==",
                                                                            
   decode it into base64 
      
      
      echo "SFRCe3YzcnNpMG5fYzBudHIwbF9hbV9JX3JpZ2h0P30=" | base64 -d
      
          HTB{v3rsi0n_c0ntr0l_am_I_right?}    
