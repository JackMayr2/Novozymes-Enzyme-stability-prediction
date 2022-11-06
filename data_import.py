import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

lis1 = api.competitions_list(search= ('novozymes-enzyme-stability-prediction'))
api.competition_download_files('novozymes-enzyme-stability-prediction')
# open in finder, then unzip and folders will be in the correct place
# open in finder, then unzip and folders will be in the correct place