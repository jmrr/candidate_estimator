""" REST API endpoints.
"""
import logging

from pyramid.security import Allow, Everyone
from cornice.resource import resource, view
from cornice.validators import colander_body_validator

from candidate_estimator import model
from candidate_estimator.schema import CandidateSchema

log = logging.getLogger(__name__)


@resource(collection_path='/candidates', path='/candidates/{candidate_id}')
class Candidate(object):

    def __init__(self, request, context=None):
        self.request = request

    def __acl__(self):
        return [(Allow, Everyone, 'everything')]

    # def collection_get(self):
    #     return self.request.db.query(model.Candidates).all()

    def get(self):
        candidate = self.request.db.query(model.Candidates).get(
            self.request.matchdict['candidate_id']
        )
        if not candidate:
            self.request.errors.add('url', 'candidate_id', 'Candidate not found')
            self.request.errors.status = 404
            return

        return {
            'id': candidate.id,
            'applicationId': candidate.applicationId,
            'candidateId': candidate.candidateId,
            'isRetake': candidate.isRetake,
            'invitationDate': candidate.invitationDate.isoformat(),
            'applicationTime': candidate.applicationTime.isoformat(),
            'speechToText': candidate.speechToText,
            'videoLength': candidate.videoLength,
            'score': candidate.score,
        }

    @view(
        content_type='application/json',
        schema=CandidateSchema(),
        validators=(colander_body_validator,)
    )
    def collection_post(self):
        db = self.request.db
        new_candidate = model.Candidates.from_dict(self.request.validated)
        db.add(new_candidate)
        db.flush()  # here we get id from DB
        return {
            'id': new_candidate.id,
            'applicationId': new_candidate.applicationId,
            'candidateId': new_candidate.candidateId,
            'isRetake': new_candidate.isRetake,
            'invitationDate': new_candidate.invitationDate.isoformat(),
            'applicationTime': new_candidate.applicationTime.isoformat(),
            'speechToText': new_candidate.speechToText,
            'videoLength': new_candidate.videoLength,
            'score': new_candidate.score,
        }
