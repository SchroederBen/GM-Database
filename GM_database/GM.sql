CREATE SCHEMA GM_DATABASE; 

-- Creating the Player table
CREATE TABLE Player (
    PlayerID INT PRIMARY KEY,
    Name VARCHAR(255),
    Age INT,
    Position VARCHAR(50)
);

-- Creating the Coach table
CREATE TABLE Coach (
    CoachID INT PRIMARY KEY,
    Name VARCHAR(255),
    Role VARCHAR(50),
    Age INT
);

-- Creating the Player_Salary table
CREATE TABLE Player_Salary (
    SalaryID INT PRIMARY KEY,
    PlayerID INT,
    Contract_length INT,
    Amount_of_Money DECIMAL(19, 4),
    FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID)
);

-- Creating the Coach_Salary table
CREATE TABLE Coach_Salary (
    SalaryID INT PRIMARY KEY,
    CoachID INT,
    Contract_length INT,
    Amount_of_Money DECIMAL(19, 4),
    FOREIGN KEY (CoachID) REFERENCES Coach(CoachID)
);

-- Creating the Stats table
CREATE TABLE Stats (
    PlayerID INT PRIMARY KEY,
    Assists INT,
    Goals INT,
    Points INT,
    FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID)
);

-- Creating the Injury table
CREATE TABLE Injury (
    InjuryID INT PRIMARY KEY,
    PlayerID INT,
    Severity VARCHAR(255),
    date_of_injury DATE,
    date_of_return DATE,
    days_out INT,
    FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID)
);

-- Creating the Injured_Body_Part table
CREATE TABLE Injured_Body_Part (
    InjuryID INT,
    Body_Part VARCHAR(255),
    FOREIGN KEY (InjuryID) REFERENCES Injury(InjuryID)
);

SHOW TABLES IN GM_DATABASE;
