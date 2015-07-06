class VoteManager:
    def __init__(self):
        self.currentVote = None

    def start(self, user, name):
        if self.currentVote:
            raise OngoingVoteException()
        self.currentVote = Vote(name)

    def vote(self, user, vote):
        if not self.currentVote:
            raise NoVoteException()
        self.currentVote.vote(user["id"], vote)

    def state(self):
        if not self.currentVote:
            raise NoVoteException()
        return VoteResult(self.currentVote, False)

    def close(self, user):
        if not self.currentVote:
            raise NoVoteException()
        vote = self.currentVote
        self.currentVote = None
        return VoteResult(vote, True)

class VoteResult:
    def __init__(self, vote, end):
        if not isinstance(vote, Vote):
            raise ValueError("Vote is not a vote")
        self.name = vote.name
        self.votesFor = vote.votesFor
        self.votesAgainst = vote.votesAgainst
        self.voteCount = len(vote.votes)
        self.rate = 0 if self.voteCount == 0 else self.votesFor / self.voteCount
        self.end = bool(end)

class Vote:
    def __init__(self, name):
        self.name = name
        self.votesFor = 0
        self.votesAgainst = 0
        self.votes = []

    def has_voted(self, user_id):
        return user_id in self.votes

    def vote(self, user_id, vote):
        if self.has_voted(user_id):
            raise AlreadyVoteException()
        self.votes.append(user_id)
        if vote:
            self.votesFor += 1
        else:
            self.votesAgainst += 1

class VoteException(Exception):
    pass

class OngoingVoteException(VoteException):
    pass

class NoVoteException(VoteException):
    pass

class AlreadyVoteException(VoteException):
    pass
