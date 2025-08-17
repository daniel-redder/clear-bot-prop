from groupy.client import Client as cli
from typing import List, Any
import yaml
import random

with open("config.yaml", "r") as f:
    secrets = yaml.safe_load(f)


client = cli.from_token(secrets['client'])
admins = secrets['admin_ids']
ignored = secrets['ignored_ids']


def handle(members: List[Any], safe_senders:List[str], group:Any, admin_chats, count:int=None, msg:str=None):
    """
    Function which handles kicking users / identifying if user is a safe-sender
    
    Args:
        members (List of groupy member type... whatever): ...
        safe_senders (List[str]): list of safe user ids
        group (groupy server type): ...
        count (int): number of impermissible words said
        msg (str): string message which resulted in banning (or none)
    """

    #identify sus user
    try:
        bad_user = members[msg.data['sender_id']]
    except:
        print("caught missing user")
        return None
    
    #is it a user we don't care about
    if msg.data['sender_id'] in safe_senders:
        print(msg.data['name'], " is a safe sender")
        return None

    #get em outta here
    try:
        bad_user.remove()
        return msg.data['name']
    except:
        print("unable to kick, not sending notification message because it is likely a duplicate message, but be aware could be something sus")
        return None
    


def checker():
    """
    main function to be called which checks the last k messages in chat for sus words
    """
    for group in client.groups.list():
        if group.name in secrets['servers']:
            #collect list of all current members
            members = {f'{x.user_id}':x for x in group.members}
            
            #identify self
            safe_senders = [client.user.me['user_id']]
            safe_senders= safe_senders + admins + ignored

            #collect the last k messages
            mesg_iter = group.messages.list_all()

            #collect messages
            try:
                messages = [next(mesg_iter) for x in range(secrets['blocking']['words_to_check'])]
            except:
                mesg_iter = group.messages.list_all()
                print('defaulting to all')
                messages=[]
                for x in mesg_iter:
                    messages.append(x)
            
            kicked_users = []

            #block for messages
            for msg in messages:
                msg_text = msg.data['text']
                #count number of sus word occurences
                count_list = [x for x in secrets['blocking']['sus'] if x in msg_text.lower()]
                count = len(count_list)

                #if sus then msg and ban!
                if count >= secrets['blocking']['impermissible_words']:          
                    kicked_users.append(handle(
                        members=members,
                        group=group,
                        safe_senders=safe_senders,
                        admin_chats=None, #TODO implement admin dms...
                        count=count,
                        msg=msg
                    ))
            
            all_members = {k:m for k,m in members.items() if m.name not in kicked_users and k not in safe_senders}

            if secrets['blocking']['capital_names']:
                bad_names = {k:m for k,m in all_members.items() if m.name.isupper()}
                for user, userobj in bad_names:
                    userobj.remove()
                    all_members.pop(user)
                bad_names = [m.name for m in list(bad_names.values())]
            else:
                bad_names = []

            kick_message = random.choice(secrets['kick_messages'])
            kicked_users = kicked_users + bad_names
            kicked_users = [k for k in kicked_users if k is not None]

            if len(kicked_users) > 0:
                group.post(
                    text=kick_message + " kicked: " + ', '.join(kicked_users)
                )




                
if not secrets['user_id_mode']:
    checker()
else:
    """
    quick utility for finding client_id's for selecting admin and safe senders
    """
    for group in client.groups.list():
        if group.name in secrets['servers']:
            print(group.name)
            members = {f'{x.user_id}':x for x in group.members}
            for xp in members: print(xp, members[xp])


