# Push Test Vector Generator

## Installing

### System requirements

Please be sure that the following are installed:

* Python virtualenv
* libssl-dev
* python 2+

### Installing

1. virtualenv .
1. bin/pip -r requirements.txt

## Running

You will need the registration information for your service worker.

e.g.
```
    navigator.serviceWorker.getRegistration().then(
        rr => rr.pushManager.getSubscription().then(
            ss => console.debug(JSON.stringify(ss.toJSON()))))
```

save this information to a file named `subscription.json`

You should also create a `data` file that contains whatever data you
wish to send to the remote browser. This data should be unencrypted.

Once you've created these files, you can run:
```
$ bin/python pusher.py
```

which will output a curl script you can use to send the data.

***NOTE***: the registered service worker script on the client is responsible
for displaying or taking any other action on the message that it 
receives. It is well worth opening the Developer:Browser Console in 
order to see if the User Agent encountered any problems. 

This script is ***NOT*** for production use and ***ONLY*** should be 
used for debugging and programming purposes.
