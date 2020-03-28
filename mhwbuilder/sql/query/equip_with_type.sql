SELECT Equipment.name
FROM Equipment
WHERE Equipment.type = ?1
ORDER BY Equipment.name;