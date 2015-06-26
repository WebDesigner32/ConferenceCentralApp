##**Conference Central API**##

##**Project Goals**##

This project aims to provide session and speaker functionality with user
wishlists for the conference central application. Indexes and queries are
emphasized and implementation of endpoint methods and classes are heavily used.

## Products
- [App Engine][1]

## Language
- [Python][2]

## APIs
- [Google Cloud Endpoints][3]

## Installation Instructions

1. Install Google App Engine SDK for Python at:
[https://cloud.google.com/appengine/downloads][4].

## Setup Instructions

1. Set the `Project ID` from the [Developer Console][5] as the value for
   `application` in `app.yaml`.
2. Set the `Client IDs` you registered in the [Developer Console][5] as the
   values for WEB_CLIENT_ID, ANDROID_CLIENT_ID, and IOS_CLIENT_ID in
   `settings.py`.
3. Set the Web client ID as the value for CLIENT_ID in `static/js/app.js`.
5. In GoogleAppEngineLauncher, right click and then click `New`. Leave the
   `Application ID` blank and then specify the `Application Directory`. Next, you
   can set `Port`. Once completed, continue by clicking `Create`.
6. In GoogleAppEngineLauncher, click `Run`.
6. Check if the app is running by visiting [localhost:8080][6]. If you are
   using a port other than the default 8080, say 9080 for example, then you
   visit localhost:9080.
7. Using GoogleAppEngineLauncher, click Deploy.
8. Check if the deployed application is running by visiting:
   https://PROJECTIDGOESHERE.appspot.com.

## Test Instructions

1. Like in the final step for `Setup Instructions`, you can access my version
   of the deployed application by visiting:
   [https://conference-central-966.appspot.com][7]
2. To test endpoint methods I provided, visit:
   [https://conference-central-966.appspot.com/_ah/api/explorer][8], and then
   click `conference API`. From there you will see the endpoint methods you can
   test. Before you can test the endpoint methods, make sure that
   `Authorize requests using OAuth 2.0:` in the top-right is toggled to `ON`.
   Then select `https://www.googleapis.com/auth/userinfo.email` in the window
   that pops up, and then click `Authorize`.

   *If you run into any issues testing the application, then consider either
   using or not using Incognito mode for the Chrome Browser. Another problem
   you may encounter involves the toggle resetting its value to OFF for
   `Authorize requests using OAuth 2.0:` in the top-right of the Google APIs
   Explorer. Merely toggle back to ON and resume testing.

3. To obtain the `websafeConferenceKey` asked for in the Google APIs Explorer,
   go to [https://conference-central-966.appspot.com][7] and then click
   `Show Conferences` and then click `Details` to access the details for a
   conference. Once that is completed, copy the `websafeConferenceKey` from the
   end of the URL and then paste it in the asked for field in the Google APIs
   Explorer to continue.

   Similarly, to obtain the `websafeSessionKey`, visit the response from the
   `getConferenceSessions` method in the Google APIs Explorer and then copy the
   `websafeKey` from the session you are interested in. Once it is copied, you
   can continue by pasting it in the `websafeSessionKey` field asked for in the
   Google APIs Explorer.

   *When testing in the Google APIs Explorer, leave the `fields` fields blank.

##**Task 1: Add Sessions to a Conference**##

The kind Session is defined in models.py like so:

**class Session(ndb.Model):**
    **name = ndb.StringProperty(required=True)**
    **highlights = ndb.StringProperty(repeated=True)**
    **speakers = ndb.KeyProperty(kind=Speaker, repeated=True)**
    **duration = ndb.TimeProperty()**
    **typeOfSession = ndb.StringProperty()**
    **date = ndb.DateProperty()**
    **startTime = ndb.TimeProperty()**
    **location = ndb.StringProperty()**

As you can see, there can be multiple highlights and speakers in a session.
The session is created as a child of an existing conference.

The SessionForm class allows for the creation of a session object. When a
request is made for a current session, the message field `websafeKey` holds a
urlsafe string that can change back to the initial key which establishes the
session as unique. Finally, the SessionsForms class yields multiple SessionForm
objects.

The Speaker class has a single property, the name property, for the speaker.
The name for the speaker is used to identify the speaker uniquely and it is
used as an input for a form. As for the required `getSessionsBySpeaker` method,
the class SpeakerForm is implemented to add a speaker for the method.

Finally, the project uses the following as endpoints and private methods for
the Session and Speaker kinds: `getConferenceSessions`,
`getConferenceSessionsByType`, `getSessionsBySpeaker`, `createSession`,
`_copySessionToForm`, `_createSessionObject`, `_getConferenceSessions`,
and `_getKeyForSpeaker`.

*When testing the available methods via the Google APIs Explorer, provide
information for all fields except for the `fields` fields and then click
`Execute` for each method.

##**Task 2: Add Sessions to User Wishlist**##

Start with the `addSessionToWishlist` method. Here, you must provide the
`websafeKey` in the `websafeSessionKey` field for the session you are
interested in adding. To do that, see the last half of Step 3 from
`Test Instructions`. Once provided, click `Execute`.

Moving forward, you will want to retrieve sessions in your wishlist, and so you
must go to the required method `getSessionsInWishlist` and then click
`Execute`.

##**Task 3: Work on indexes and queries**##

###**Come up with 2 additional queries**###

Sometimes, users for many reasons want to have knowledge of the conferences
that have minimum and maximum attendees. Therefore, I have implemented in
`conference.py` two methods that query all conferences having min attendees <=5
(`getMinAttndsConfs`) and max attendees >= 100 (`getMaxAttndsConfs`). Examples
of conferences with minimum attendees are private board meetings for CEOs and
examples of conferences with maximum attendees are popular sporting events.

*Simply click `Execute` to obtain desired results for both methods.

###**Solve the following query related problem**###

**Let’s say that you don't like workshops and you don't like sessions after
7 pm. How would you handle a query for all non-workshop sessions before 7 pm?
What is the problem for implementing this query? What ways to solve it did you
think of?**

####**Reason for Problem with Query and Its Solution**####

We can filter the query with two inequality filters. For instance, for
all sessions != Workshop, and for all sessions <= 7 pm. The problem with
implementing this query is that in Datastore we cannot use inequalities for
multiple properties.

The way I could surpass this barrier is by implementing two queries, each with
an inequality filter. From there, I can combine the two results.

Task 4: Add a Task

Once a session is made, the default taskqueue gets a new task added to it. All
sessions of a conference are reviewed for any speaker that has greater than one
session in that conference once `ReviewSpeakersForSessions` in `main.py` is
executed. In the event a speaker does have greater than one session, then the
speaker gets featured and a new Memcache entry is made or overwrites the
previous entry, giving a list of all featured speakers and their sessions for
the conference. Note that `getFeaturedSpeaker` has a `websafeConferenceKey`
field. Once the `websafeConferenceKey` is provided (see first half of Step 3 in
`Test Instructions` if unsure) and you have clicked `Execute`, then the method
will return the featured speakers and their sessions as the Memcache entry.

[1]: https://developers.google.com/appengine
[2]: http://python.org
[3]: https://developers.google.com/appengine/docs/python/endpoints/
[4]: https://cloud.google.com/appengine/downloads
[5]: https://console.developers.google.com/
[6]: https://localhost:8080/
[7]: [https://conference-central-966.appspot.com]
[8]: https://conference-central-966.appspot.com/_ah/api/explorer
