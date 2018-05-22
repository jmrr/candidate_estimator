""" REST API endpoints.
"""
import logging

from pyramid.security import Allow, Everyone
from cornice.resource import resource, view
from cornice.validators import colander_body_validator

from candidate_estimator import model
from candidate_estimator.schema import CandidateSchema

log = logging.getLogger(__name__)


@resource(
    collection_path='/candidates',
    path='/candidates/{candidate_id}',
)
class Candidate(object):

    def __init__(self, request, context=None):
        self.request = request

    def __acl__(self):
        return [(Allow, Everyone, 'everything')]

    def get(self):
        request = self.request
        candidate_id = request.matchdict['candidate_id']
        candidate = request.db.query(model.Candidates).get(candidate_id)
        if not candidate:
            request.errors.add('url', 'candidate_id', 'Candidate not found')
            request.errors.status = 404
            return

        return candidate.serialize()

    @view(
        content_type='application/json',
        schema=CandidateSchema(),
        validators=(colander_body_validator,)
    )
    def collection_post(self):
        db = self.request.db
        validated = self.request.validated
        new_candidate = model.Candidates.deserialize(validated)

        timedelta = (
                new_candidate.applicationTime
                - new_candidate.invitationDate
        ).seconds
        video_length = new_candidate.videoLength

        predicted_score = int(self.request.registry.model.predict([[
            timedelta,
            video_length,
        ]])[0])

        new_candidate.predictedScore = predicted_score
        db.add(new_candidate)
        db.flush()  # here we get id from DB
        return {
            'predictedScore': new_candidate.predictedScore,
            'isHired': bool(new_candidate.predictedScore > 3),
        }
