# tg-account-type-detector
## Telegram Account Type Detector (channel / group / user / bot)


### Structure
* `type-detector.py` - Main module
* `example.py` - Code with an example of use
* `requirements.txt` - List of libraries to install via pip
* `.env.example` - Example of a `.env` file, take data from [`my.telegram.org/apps`](https://my.telegram.org/apps)

### Details
* The `.env` file should be located in the same folder with the main code and contain the variables specified in the example — `USBOT_API_ID` and `USBOT_API_HASH`


* The first time the `get_type_via_userbot` function is called, the console will require you to enter the phone number in international format, and then the login code == start of the session, which will be saved in the file `my_own_app.session`
