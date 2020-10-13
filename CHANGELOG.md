# Changelog

## Version 0.1.1

_Released 2020-10-13_

**Minor chages**
- Build syntax bug fixed

## Version 0.1.0

_Released 2020-10-13_

**Major Changes:**
- Restructure lib to be like package (with `__init__.py`'s)
- Add Locale Manager inline/reply keyboard support

**New Features:**
- Utils wrapper class change for `TelegramBot` instead of `TelegramUtilsService`
- Add routing class to handle income updates, `route` decorator
- Add sending class to send outcoming messages
- Add automatic logging on sending messages

**Minor changes:**
- Changed storage visability in utils wrapper class to public
- Made Role Auth method `login_as` password parameter - optional
- Add encoding parameter in File Manager util class

