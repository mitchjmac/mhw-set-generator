CREATE TABLE IF NOT EXISTS Armor (
    id            integer PRIMARY KEY,
    name          text    NOT NULL,
    type          text    NOT NULL,
    skill_level_1 integer,
    skill_level_2 integer,
    bonus         integer,
    slot_1        integer,
    slot_2        integer,
    slot_3        integer,
    FOREIGN KEY (skill_level_1) REFERENCES SkillLevel (id),
    FOREIGN KEY (skill_level_2) REFERENCES SkillLevel (id)
);

CREATE TABLE IF NOT EXISTS Charm (
    id            integer PRIMARY KEY,
    name          text    NOT NULL,
    skill_level_1 integer NOT NULL,
    skill_level_2 integer,
    FOREIGN KEY (skill_level_1) REFERENCES SkillLevel (id),
    FOREIGN KEY (skill_level_2) REFERENCES SkillLevel (id)
);

CREATE TABLE IF NOT EXISTS Decoration (
    id            integer PRIMARY KEY,
    name          text    NOT NULL,
    slot          integer NOT NULL,
    skill_level_1 integer NOT NULL,
    skill_level_2 integer,
    FOREIGN KEY (skill_level_1) REFERENCES SkillLevel (id),
    FOREIGN KEY (skill_level_2) REFERENCES SkillLevel (id)
);

CREATE TABLE IF NOT EXISTS Skill (
    id   integer PRIMARY KEY,
    name text    NOT NULL
);

CREATE TABLE IF NOT EXISTS SkillLevel (
    id          integer PRIMARY KEY,
    level       integer NOT NULL,
    base_skill  integer NOT NUll,
    FOREIGN KEY (base_skill) REFERENCES Skill (id)
);

CREATE TABLE IF NOT EXISTS SetBonus (
    id   integer PRIMARY KEY,
    name text    NOT NULL
);

CREATE TABLE IF NOT EXISTS BonusRank (
    set_bonus   integer NOT NULL,
    skill_level integer NOT NULL,
    pieces      integer NOT NUll,
    FOREIGN KEY (set_bonus)   REFERENCES SetBonus (id),
    FOREIGN KEY (skill_level) REFERENCES SkillLevel (id),
    PRIMARY KEY (set_bonus, skill_level)
);