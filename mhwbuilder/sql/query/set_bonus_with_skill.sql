SELECT SetBonus.name as sb_name
FROM SetBonus
JOIN BonusRank ON SetBonus.id = BonusRank.set_bonus
JOIN SkillLevel ON BonusRank.skill_level = SkillLevel.id
JOIN Skill ON SkillLevel.base_skill = Skill.id
WHERE Skill.name = ?1;