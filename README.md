# Deck Tracking

The idea of Deck Tracking is to be able to give users individual tracking codes which will allow you to monitor how often it's accessed, who it's being shared with, location of views, etc. We all know that Decks get passed around, this allows you to track that behavior. You wouldn't run your website without analytics, so why would you share your deck without Analytics?

This software uses free 3rd party services like Mixpanel (event tracking), Olark (live website chat), scribd (hosting of the deck). You'll need to create an account with each of these in order to run this software properly.

## Installation

### Google App Engine

This runs atop Google App Engine. You'll have to create an account, create an app, and modify the `app.yaml` file contained herein. You'll want to change the `application: <YOUR APP NAME>` section in that file.

### Defining Global Variables

In `main.py` you should see a section marked Global Variables. For these you'll want to put in the codes from 3rd party services as appropriate:

```python
baseUrl     = "http://deck.example.com"
adminEmail  = "admin@example.com" #person who needs to be notified if somethings not working
scribdEmbed = "bla bla bla" #this should be the embed code you get from scribd
mixpEmbed   = "bla bla bla" #this should be the embed code you get from olark
olarkEmbed  = "bla bla bla" #this should be the embed code you get from mixpanel
```

After you've included all of the above, go ahead and push your app live to Google App Engine

### Creating Unique Codes

If you go to `http://deck.yoursite.com/addUsers` you'll see a dialogue box prompting you for a name and an email address. Enter both of these and the click on the Create button. You'll be given a unique code to give this user. Data will be appropriately filled into the DB and sent to Olark / Mixpanel every time she logs in.
