class Match:

    def __init__(self, values, matches, homeId, awayId, homePos, awayPos):

        self.matches = matches
        self.values = values
        self.homeId = homeId
        self.awayId = awayId
        self.homePos = homePos
        self.awayPos = awayPos

        date = self[self.matches.date]
        if len(date) > 9:
            self.month = int(date[3:5])
            self.day = int(date[0:2])
            year = int(date[6:9])
            self.year = 2000 + year if year < 20 else 1900 + year

    @property
    def date(self):
        return self[self.matches.date]

    @property
    def idM(self):
        return self[self.matches.idM]

    @property
    def league(self):
        return self[self.matches.league]

    def __getitem__(self, item):
        return self.values[self.matches.positions[item]]


class Matches:

    def __init__(self, path, idM=None, league=None, date=None, home=None, away=None, columns=None,
                 homePos=None, awayPos=None):

        self.idM = idM
        self.league = league
        self.date = date
        self.matches = []
        self.columns = []
        self.homePlayers = []
        self.awayPlayers = []

        if idM is not None:
            self.columns.append((idM, int))
        if league is not None:
            self.columns.append((league, int))
        if date is not None:
            self.columns.append((date, str))
        if home is not None:
            self.homePlayers = home
        if away is not None:
            self.awayPlayers = away
        if columns is not None:
            self.columns.extend(columns)

        self.positions = dict([(self.columns[i][0], i) for i in range(len(self.columns))])
        infile = open(path, 'r')
        headers = infile.readline().replace('\n', '').replace('\r', '').replace('"', '').split(',')

        hpos = open(homePos, 'r')
        apos = open(awayPos, 'r')
        hposheader = hpos.readline().replace('\n', '').replace('\r', '').replace('"', '').split(',')
        aposheader = apos.readline().replace('\n', '').replace('\r', '').replace('"', '').split(',')

        for line in infile:
            line = line.replace('\n', '').replace('\r', '').replace('"', '').split(',')
            values = []

            for column, _type in self.columns:
                values.append(_type(line[headers.index(column)]))

            homePlayers = []
            for homep in self.homePlayers:
                homePlayers.append(int(line[headers.index(homep)]))

            awayPlayers = []
            for awayp in self.awayPlayers:
                awayPlayers.append(int(line[headers.index(awayp)]))

            homePositions = []
            hposline = hpos.readline().replace('\n', '').replace('\r', '').replace('"', '').split(',')
            for homep in self.homePlayers:
                homePositions.append(hposline[hposheader.index(homep)])

            awayPositions = []
            aposline = apos.readline().replace('\n', '').replace('\r', '').replace('"', '').split(',')
            for awayp in self.awayPlayers:
                awayPositions.append(aposline[aposheader.index(awayp)])

            self.matches.append(Match(values, self, homePlayers, awayPlayers, homePositions, awayPositions))
        infile.close()

    def __len__(self):
        return len(self.matches)

    def __iter__(self):
        return iter(self.matches)
