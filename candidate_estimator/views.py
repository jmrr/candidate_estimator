""" REST API endpoints.
"""
import logging

from pyramid.security import Allow, Everyone
from cornice.resource import resource, view
from cornice.validators import colander_body_validator

from candidate_estimator import model
from candidate_estimator.schema import ProfileSchema

log = logging.getLogger(__name__)


@resource(
    collection_path='/profiles',
    path='/profiles/{profile_id}',
)
class Profile(object):

    def __init__(self, request, context=None):
        self.request = request

    def __acl__(self):
        return [(Allow, Everyone, 'everything')]

    def get(self):
        request = self.request
        profile_id = request.matchdict['profile_id']
        profile = request.db.query(model.Profile).get(profile_id)
        if not profile:
            request.errors.add('url', 'profile_id', 'Profile not found')
            request.errors.status = 404
            return

        return profile.serialize()

    @view(
        content_type='application/json',
        schema=ProfileSchema(),
        validators=(colander_body_validator,)
    )
    def collection_post(self):
        db = self.request.db
        validated = self.request.validated
        new_profile = model.Profile.deserialize(validated)

        timedelta = (
                new_profile.applicationTime
                - new_profile.invitationDate
        ).seconds
        video_length = new_profile.videoLength

        predicted_score = int(self.request.registry.model.predict([[
            timedelta,
            video_length,
        ]])[0])

        new_profile.predictedScore = predicted_score
        db.add(new_profile)
        db.flush()  # here we get id from DB
        return {
            'predictedScore': new_profile.predictedScore,
            'isHired': bool(new_profile.predictedScore > 3),
        }
