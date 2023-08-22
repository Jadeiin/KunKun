CREATE TABLE IF NOT EXISTS User (
	UserID INTEGER PRIMARY KEY AUTOINCREMENT,
	UserIP TEXT NOT NULL,
	UserName TEXT,
	UserPasswordSha1 BLOB NOT NULL
);

CREATE TABLE IF NOT EXISTS Room (
	RoomID INTEGER PRIMARY KEY AUTOINCREMENT,
	RoomName TEXT NOT NULL
	-- RoomOwner INTEGER REFERENCES User(UserID) ON DELETE CASCADE ON UPDATE CASCADE,
	-- RoomDescription TEXT
);

CREATE TABLE IF NOT EXISTS Msg (
	MsgID INTEGER PRIMARY KEY AUTOINCREMENT,
	MsgSender INTEGER REFERENCES User(UserID) ON DELETE CASCADE ON UPDATE CASCADE,
	RoomID INTEGER REFERENCES Room(RoomID) ON DELETE CASCADE ON UPDATE CASCADE,
	MsgContent TEXT NOT NULL,
	MsgSendtime NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS RoomMember (
	RoomID INTEGER REFERENCES Room(RoomID) ON DELETE CASCADE ON UPDATE CASCADE,
	UserID INTEGER REFERENCES User(UserID) ON DELETE CASCADE ON UPDATE CASCADE
	-- LastRead INTEGER REFERENCES Msg(MsgID)
);

CREATE TABLE IF NOT EXISTS RoomAdmin (
	RoomID INTEGER REFERENCES Room(RoomID) ON DELETE CASCADE ON UPDATE CASCADE,
	UserID INTEGER REFERENCES User(UserID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- CREATE TABLE IF NOT EXISTS UserBlock (
-- 	RoomID INTEGER REFERENCES Room(RoomID) ON DELETE CASCADE ON UPDATE CASCADE,
-- 	UserID INTEGER REFERENCES User(UserID) ON DELETE CASCADE ON UPDATE CASCADE
-- );