#!/usr/bin/env python

"""
main.py -- Udacity conference server-side Python App Engine
    HTTP controller handlers for memcache & task queue access

$Id$

created by wesc on 2014 may 24

"""

__authors__ = 'wesc+api@google.com (Wesley Chun) and Landon Bennett'

import webapp2
from google.appengine.api import app_identity
from google.appengine.api import mail
from google.appengine.api import memcache
from google.appengine.ext import ndb

from conference import ConferenceApi
from models import Speaker
from models import Session


class SetAnnouncementHandler(webapp2.RequestHandler):
    def get(self):
        """Set Announcement in Memcache."""
        ConferenceApi._cacheAnnouncement()
        self.response.set_status(204)


class SendConfirmationEmailHandler(webapp2.RequestHandler):
    def post(self):
        """Send email confirming Conference creation."""
        mail.send_mail(
            'noreply@%s.appspotmail.com' % (
                app_identity.get_application_id()),     # from
            self.request.get('email'),                  # to
            'You created a new Conference!',            # subj
            'Hi, you have created a following '         # body
            'conference:\r\n\r\n%s' % self.request.get(
                'conferenceInfo')
        )


class ReviewSpeakersForSessions(webapp2.RequestHandler):
    def post(self):
        """Will review for additional sessions by speakers."""
        # turns urlsafe key string into conference key
        c_key = ndb.Key(urlsafe=self.request.get('c_key_str'))
        # all sessions are obtained from conference
        conference_Sessions = Session.query(ancestor=c_key)
        # all speakers are obtained
        speakers = Speaker.query()
        # speakers sorted by their names
        speakers = speakers.order(Speaker.name)
        # featured speakers as empty list
        ftrdSpkrKeys = []
        # review each speaker
        for spkr in speakers:
            count = 0
            # counts number of sessions speaker holds in conference
            for session in conference_Sessions:
                for cs_speaker_key in session.speakers:
                    if spkr.key == cs_speaker_key:
                        count += 1
                        # feature speaker if in greater than one session
                        if count == 2:
                            # the featured speakers list gets speaker key
                            # appended
                            ftrdSpkrKeys.append(cs_speaker_key)
        # The urlsafe key for conference is set as memcache key.
        MEMCACHE_CONFERENCE_KEY = "FEATURED:%s" % c_key.urlsafe()
        # Set in memcache and arrange the featured speakers announcement when
        # there are featured speakers at conference.
        if ftrdSpkrKeys:
            count = 0
            featured = "FEATURED SPEAKERS AND SESSIONS FOR THE CONFERENCE:  "
            for speaker_key in ftrdSpkrKeys:
                count += 1
                featured += " FEATURED %s: %s SESSIONS: " % (
                    count, speaker_key.get().name)
                sessionsFtrdSpkrs = conference_Sessions.filter(
                    Session.speakers == speaker_key)
                featured += ", ".join(sess.name for sess in sessionsFtrdSpkrs)
            memcache.set(MEMCACHE_CONFERENCE_KEY, featured)
        else:
            # If there are no featured speakers at conference,
            # delete the memcache announcements entry.
            featured = ""
            memcache.delete(MEMCACHE_CONFERENCE_KEY)

app = webapp2.WSGIApplication([
    ('/crons/set_announcement', SetAnnouncementHandler),
    ('/tasks/send_confirmation_email', SendConfirmationEmailHandler),
    ('/tasks/review_speakers_for_sessions', ReviewSpeakersForSessions)
], debug=True)
