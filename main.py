from groupy.client import Client as cli
from secrets import client, admin_init

client = cli.from_token(client)

#if you are trying to see user_ids for configuring admin user_id or you want to add to safe_senders set this as true to print out all user_ids
user_id_mode = False

#server name to look at
active_servers = ["UGA Aviation Club✈️"]

#number of messages per run to check
k=5

#number of words required for banning
words=2

#sus word list (to be expanded)
sus = ['taylor swift','selling','ticket','tickets',"-", 'sale']

#user_id to be contacted in the event of a kicking
admin = [admin_init]


"""
Function which handles kicking users / identifying if user is a safe-sender
"""
def handle(msg, members, safe_senders, count_list, group):
    
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
    except:
        #admin_chat.post(text="unable to remove, already kicked?")
        print("unable to kick, not sending notification message because it is likely a duplicate message, but be aware could be something sus")
        return None

    #notification message works
    group.post(text=f"{msg.data['name']} posted something SUS! \nWe thus kick them for saying sus words")

    #select admin dm
    admin_chat = None
    for chat in client.chats.list_all(): 
        admin_chat = chat if chat.data['other_user']['id'] in admin else admin_chat 
    
    #dm admin with post
    admin_chat.post(text = f"{msg.data['name']} was kicked \nFor saying the sus words {count_list} \n they said: \n {msg.data['text']}")
    

    #log the user
    print(bad_user)






"""
main function to be called which checks the last k messages in chat for sus words
"""
def checker():
    for group in client.groups.list():
        if group.name in active_servers:
            print(group.name)

            #collect the last k messages
            mesg_iter = group.messages.list_all()
            
            #identify self
            safe_senders = [client.user.me['user_id']]
            safe_senders= safe_senders + admin


            #collect messages
            try:
                messages = [next(mesg_iter) for x in range(k)]
            except:
                mesg_iter = group.messages.list_all()
                print('defaulting to all')
                messages=[]
                for x in mesg_iter:
                    messages.append(x)

            #collect list of all current members
            members = {f'{x.user_id}':x for x in group.members}

            

            #print(messages[0].data['text'])
            print(len(messages))
            for msg in messages:
                #collect text data
                msg_text = msg.data['text']

                #count number of sus word occurences
                count_list = [x for x in sus if x in msg_text.lower()]
                count = len(count_list)

                #print(count, msg.data['name'])

                #if sus then msg and ban!
                if count >= words:          
                    handle(msg,members,safe_senders,count_list,group)

                
if not user_id_mode:
    checker()


else:
    """
    quick utility for finding client_id's for selecting admin and safe senders
    """
    for group in client.groups.list():
        if group.name in active_servers:
            print(group.name)
            members = {f'{x.user_id}':x for x in group.members}
            for xp in members: print(xp, members[xp])


