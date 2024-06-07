from tools.tools import get_api_key, remove_api_key, move_first_key_to_end      


api_key = get_api_key()
print(api_key)
move_first_key_to_end()
api_key = get_api_key()
print(api_key)