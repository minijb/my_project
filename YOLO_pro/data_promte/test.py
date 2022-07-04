from utils.config import config
from utils.random_data import get_random_data_mixup


con = config()
get_random_data_mixup(con.get_img(),(416,416),con,False)

# print(create_config())