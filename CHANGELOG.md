# Changelog

## Version 0.1.5

_Released 2020-10-14_

**Minor Changes**
- Fix package importing bug (v3 - one more subpackage)

## Version 0.1.4

_Released 2020-10-14_

**Minor Changes**
- Fix package importing bug (v2 - subpackages)

## Version 0.1.3

_Released 2020-10-14_

**Minor Changes**
- Fix package importing bug

## Version 0.1.2

_Released 2020-10-14_

**Major Changes**
- Update visability (now as `advancedbot`)

## Version 0.1.1

_Released 2020-10-13_

**Minor Changes**
- Fix build syntax bug

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

**Minor Changes:**
- Changed storage visability in utils wrapper class to public
- Made Role Auth method `login_as` password parameter - optional
- Add encoding parameter in File Manager util class

