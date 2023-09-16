from chat import get_response
import sys

text_message = sys.argv[1]
if text_message == None:
    print('error')

text_response = get_response(text_message)
print('<respon>' + text_response)