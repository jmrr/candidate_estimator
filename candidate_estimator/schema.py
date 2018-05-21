import colander


class CandidateSchema(colander.MappingSchema):
    applicationId = colander.SchemaNode(colander.String())
    candidateId = colander.SchemaNode(colander.Integer())
    isRetake = colander.SchemaNode(colander.Bool())
    invitationDate = colander.SchemaNode(colander.DateTime())
    applicationTime = colander.SchemaNode(colander.DateTime())
    speechToText = colander.SchemaNode(colander.String())  # TODO: change
    videoLength = colander.SchemaNode(colander.Float())
    score = colander.SchemaNode(colander.Integer())
