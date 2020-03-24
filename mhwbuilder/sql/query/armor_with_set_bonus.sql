SELECT Armor.id as a_id, Armor.name as a_name, Armor.type as a_type, Armor.slot_1, Armor.slot_2, Armor.slot_3, sk_name1.name as sk1_name, sk_lvl1.level as sk1_level, sk_name2.name as sk2_name, sk_lvl2.level as sk2_level, SetBonus.name as sb_name
FROM Armor
LEFT OUTER JOIN SkillLevel AS sk_lvl1 ON Armor.skill_level_1 = sk_lvl1.id
LEFT OUTER JOIN SkillLevel AS sk_lvl2 ON Armor.skill_level_2 = sk_lvl2.id
LEFT OUTER JOIN Skill AS sk_name1 ON sk_lvl1.base_skill = sk_name1.id
LEFT OUTER JOIN Skill AS sk_name2 ON sk_lvl2.base_skill = sk_name2.id
LEFT OUTER JOIN SetBonus ON Armor.bonus = SetBonus.id
WHERE SetBonus.name = ?1;