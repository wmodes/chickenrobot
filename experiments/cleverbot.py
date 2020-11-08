import cleverbot

cb = cleverbot.Cleverbot('YOUR_API_KEY', cs='76nxdxIJ02AAA', timeout=60, tweak1=0, tweak2=100, tweak3=100)

convo = cb.conversation()

while(1):
    input = prompt('> ')
    try:
        reply = convo.say(input)
    except cleverbot.APIError as error:
        print(error.error, error.status)
    print(reply)
