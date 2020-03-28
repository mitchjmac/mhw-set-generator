SELECT Skill.name as sk_name, SetBonus.name as sb_name, BonusRank.pieces as num_pieces
FROM Skill
JOIN SkillLevel ON Skill.id = SkillLevel.base_skill
JOIN BonusRank ON SkillLevel.id = BonusRank.skill_level
JOIN SetBonus ON SetBonus.id = BonusRank.set_bonus;