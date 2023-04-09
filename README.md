# Anti-Taylor Swift bot (UGA AV Club)
author: Daniel Redder

----
This tool is a python tool based on python's [GroupyAPI](https://pypi.org/project/GroupyAPI/) which will kick users from a group if they say too many in a small set of words. This could be redone to use some fancy NLP stuff, but it probably isn't neccesary for this task.

## How to

This tool function by executing the `main.py` file every 1-2 minutes. This tool will check the last `k` messages in `active_servers`'s groupchat for words from the defined `sus` list, and if the number of these words are greater or equal to `words` then it will remove the user and notify `admin`. 

 It is recommended that this is done on a linux based machine, but it will work on any. The only thing that needs to change is how you are automatically calling the `main.py` file.

 1. install [python](https://www.python.org/downloads/) 3.8 or 3.9
 2. open `cmd` and run this command `pip install GroupyAPI` to install the groupme API package
 3. Get a groupme API key using a admin account for the groupme server, [groupmeDev](https://dev.groupme.com/)
 4. Download this repository
 5. create a file in the same directory called `secrets.py` Which has the following contents
 ```py
 client = "<your API key>"
 admin_init = "<The Admin's groupme client_id>"
```
You can get the admin's client_id using by setting the `user_id_mode` variable to `True` then running `main.py` like this `python main.py` in cmd after setting the `client` variable and setting `admin_init="test"` then simply look for the name of the admin and associated id. 

6. Now you should be good to go, just automatically call this file every minute or two. In linux you can use `cron` for this, in terminal type `crontab -e` to open your cron list. Then enter at the top of the file:
```* * * * * python <path to main.py>``` 
This will have it execute every minute. 
