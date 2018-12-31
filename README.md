# appium-openstf-hockeyapp

This was a small project created to simplify the execution process of a pipeline using [Appium](http://appium.io), [OpenSTF](https://openstf.io), [Docker](https://www.docker.com), and [HockeyApp](https://www.hockeyapp.net)

If you would like to try and use this there are some things you will need to configure to use:

* Setup a .env file and match it with the variables in use  
* Follow the steps for OpenSTF [API](https://github.com/openstf/stf/blob/master/doc/API.md) use and copy your `adbkey` and `adbkey.pub` to the `appium-server` folder  
* Modify the `test-runner.sh` script to match your Android apps name (lines 104 & 109)  
* Place your Pytest suite into a `tests` folder
