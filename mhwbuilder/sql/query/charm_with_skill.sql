SELECT Charm.id as c_id, Charm.name as c_name, sk_name1.name as sk1_name, sk_lvl1.level as sk1_level, sk_name2.name as sk2_name, sk_lvl2.level as sk2_level
FROM Charm
LEFT OUTER JOIN SkillLevel AS sk_lvl1 ON Charm.skill_level_1 = sk_lvl1.id
LEFT OUTER JOIN SkillLevel AS sk_lvl2 ON Charm.skill_level_2 = sk_lvl2.id
LEFT OUTER JOIN Skill AS sk_name1 ON sk_lvl1.base_skill = sk_name1.id
LEFT OUTER JOIN Skill AS sk_name2 ON sk_lvl2.base_skill = sk_name2.id
WHERE sk_name1.name = ?1 OR sk_name2.name = ?1;