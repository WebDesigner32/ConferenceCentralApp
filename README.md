##**Conference Central API**##

##**Project Goals**##

This project aims to provide session functionality and user wishlists to the conference central application. Indexes and queries are emphasized and
implementation of endpoint methods and classes are heavily used.

## Products
- [App Engine][1]

## Language
- [Python][2]

## APIs
- [Google Cloud Endpoints][3]

## Setup Instructions
1. Update the value of `application` in `app.yaml` to the app ID you
   have registered in the App Engine admin console and would like to use to host
   your instance of this sample.
2. Update the values at the top of `settings.py` to
   reflect the respective client IDs you have registered in the
   [Developer Console][4].
3. Update the value of CLIENT_ID in `static/js/app.js` to the Web client ID
4. (Optional) Mark the configuration files as unchanged as follows:
   `$ git update-index --assume-unchanged app.yaml settings.py static/js/app.js`
5. Run the app with the devserver using `dev_appserver.py DIR`, and ensure it's running by visiting your local server's address (by default [localhost:8080][5].)
6. (Optional) Generate your client library(ies) with [the endpoints tool][6].
7. Deploy your application. To do this, type `$ appcfg.py update DIR`. If valid,
you can use the application by visiting: https://APPIDGOESHERE.appspot.com.

## Test Instructions

1. To test endpoint methods I provided, visit:
[https://conference-central-966.appspot.com/_ah/api/explorer][7].

2. To obtain a valid websafeConferenceKey for the API Explorer from the link
provided in the first step, visit Show Conferences and click Details to access a conference details page, and then copy the websafeConferenceKey from the URL. Similarly, to obtain a valid sessionConferenceKey, visit the response from the getConferenceSessions method and copy the websafeKey.

##**Task 1: Add Sessions to a Conference**##

The kind Session is defined in models.py like so:

class Session(ndb.Model):
    name = ndb.StringProperty(required = True)
    highlights = ndb.StringProperty(repeated = True)
    speakers = ndb.KeyProperty(kind = Speaker, repeated = True)
    duration = ndb.TimeProperty()
    typeOfSession = ndb.StringProperty()
    date = ndb.DateProperty()
    startTime = ndb.TimeProperty()
    location = ndb.StringProperty()

As you can see, there can be multiple highlights and speakers in a session,
and a session is created as a child of an existing conference. In addition, the key is incorporated in the key for the session.

The SessionForm class allows for the creation of a session object. When a request is made for a current session, the message field websafeKey holds a urlsafe string that can change back to the initial key which establishes the session as unique. Finally, the SessionsForms class yields multiple SessionForm objects.

The Speaker class just has the name property for the speaker. The name for the speaker is used to identity the speaker uniquely and it is used as an input for a form. As for the required getSessionsBySpeaker method, the class SpeakerForm is implemented to add a speaker for the method.

Finally, the project uses the following as endpoints and private methods for the Session and Speaker kinds: getConferenceSessions, getConferenceSessionsByType, getSessionsBySpeaker, createSession,  _copySessionToForm, _createSessionObject, _getConferenceSessions, and _getKeyForSpeaker.

##**Task 3: Work on indexes and queries**##

###**Come up with 2 additional queries**###

"""Panel or Expert Sessions"""

sessions = Session.query(ndb.OR(Session.typeOfSession == TypeOfSession.Panel,
                         Session.typeOfSession == TypeOfSession.Expert))

"""Obtain all sessions that have 0 seats available."""

confs = Conference.query(Conference.maxAttendees == 0)
allSessions = []
for conf in confs:
    allSessions += Session.query(ancestor = conf.key)

###**Solve the following query related problem**###

####**Problem Statement**####

Let’s say that you don't like workshops and you don't like sessions after 7 pm. How would you handle a query for all non-workshop sessions before 7 pm? What is the problem for implementing this query? What ways to solve it did you think
of?

####**Solution**####

We can filter the query by way of two inequality filters. For instance, for
all sessions != Workshop, and for all sessions <= 7 pm. The problem with implementing this query is that in Datastore we cannot use inequalities for multiple properties.

The way I got past this barrier was to implement two queries, each with an inequality filter. Finally, I merged the two results.

[1]: https://developers.google.com/appengine
[2]: http://python.org
[3]: https://developers.google.com/appengine/docs/python/endpoints/
[4]: https://console.developers.google.com/
[5]: https://localhost:8080/
[6]: https://developers.google.com/appengine/docs/python/endpoints/endpoints_tool
[7]: https://conference-central-966.appspot.com/_ah/api/explorer
