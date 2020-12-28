    # make a punter (player) class, there will be a few of those
    class Punter:
        def __init__(self, name):
            self.name = name
            self.total = 1000  # how much money they have left # random.randint(0,1000) #
            self.pick = -1  # which horse they have picked, 0-6, -1=not made a pick
            self.stake = 0  # how much they have bet on the horse+row_spacing
            self.totalwinnings = 0  # running total of all winnings
            self.numberofturns = 0  # count of how many turns this punter has
