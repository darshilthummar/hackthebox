Challenge Lab: Forensics
   
   Difficulty: Easy
   
    CHALLENGE DESCRIPTION
      "A Junior Developer just switched to a new source control platform. Can you find the secret token?"
      
    Zip Password: hackthebox
    
      Start by Downloading file and unzip with the password.
      
      ![Screenshot 2023-03-11 at 19 11 38](https://user-images.githubusercontent.com/49148722/224507268-b2578467-a1aa-4944-9853-1d7f1ab095f0.png)
      
       you can see there is hiddent file .get 
       lets go in and check what we have..
       
       ![Screenshot 2023-03-11 at 19 13 15](https://user-images.githubusercontent.com/49148722/224507338-5a95a43a-26b5-4712-ae99-f43096b502f0.png)

      log directory has history of chnages from the junior develoer.
      
      Let’s focus on the one where the tokens were removed:
      
      ![Screenshot 2023-03-11 at 19 14 33](https://user-images.githubusercontent.com/49148722/224507390-39e6ca25-6a68-4e85-b896-0dbd8daeca0b.png)

      decode it into base64 
      
      
      echo "SFRCe3YzcnNpMG5fYzBudHIwbF9hbV9JX3JpZ2h0P30=" | base64 -d
      
      ![Screenshot 2023-03-11 at 19 15 29](https://user-images.githubusercontent.com/49148722/224507428-42163a2a-42e5-4cd1-a55b-6e86e392eff8.png)
