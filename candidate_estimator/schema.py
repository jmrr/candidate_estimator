import colander


class SpeechToText(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())
    time = colander.SchemaNode(colander.Float())
    duration = colander.SchemaNode(colander.Float())
    confidence = colander.SchemaNode(colander.Float())


class SpeechToTextSequence(colander.SequenceSchema):
    sequence = SpeechToText()


class CandidateSchema(colander.MappingSchema):
    applicationId = colander.SchemaNode(colander.String())
    candidateId = colander.SchemaNode(colander.Integer())
    isRetake = colander.SchemaNode(colander.Bool())
    invitationDate = colander.SchemaNode(colander.DateTime())
    applicationTime = colander.SchemaNode(colander.DateTime())
    speechToText = SpeechToTextSequence()
    videoLength = colander.SchemaNode(colander.Float())
    score = colander.SchemaNode(colander.Integer())
