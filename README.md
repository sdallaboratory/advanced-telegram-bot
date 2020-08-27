# Advanced Telegram Bot
Python library containing utils for telegram bots

### Available utils
- Locale-dependent data storage
- Logger
- Role system
- State system
- User meta data storage

### Dependencies
```
pymongo >= 3.0
```

### Usage
Just import the class and you're good to go
```
from telegramutilsservice import TelegramUtilsService
```

### Ways of storing your data
##### MongoDB
To use mongo as a storage you have to provide its data for authorization to the class like so:
```
TelegramUtilsService(
	roles = { roles dict here },
	states = [ states list here ],
	users_collection_name="users-collection-name-here",
	logs_collection_name="logs-collection-name-here",
	state_with_params=False/True,
	locales_folder="locales-folder-here",
	db_address="db-ip-address-here",
	db_port="db-port-here",
	db_username="db-username-here",
	db_password="db-password-here",
	db_name="db-name-here")
```
Also you should create collections in mongo by youserlf, according to col. names you provide in constructor

##### Local Storage (JSONs)
To use local storage based on jsons  you have to provide the folder path to the class like so:
```
TelegramUtilsService(
	roles = { roles dict here },
	states = [ states list here ],
	users_collection_name="users-collection-name-here",
	logs_collection_name="logs-collection-name-here",
	state_with_params=False/True,
	locales_folder="locales-folder-here",
	"storage_folder"="storage-folder-path-here")
```