--  ROOMS:  office = 0, bedroom = 1
--  USERS:  nobody = 0, silveira = 1, carlos = 2, cesar = 3, guest = 4
--  LIGHT:  off = 0, on = 1
--  TEMPERATURE:  off = 0, on = 1
--  CURTAIN: off = 0, on = 1

-- gera 2048 rows aleatorias válidas dentro do dominio do projeto
insert into houseStates(room, userName, hourOfDay, light, temperature, curtain)
  SELECT abs(random() % 2), abs(random() % 5), abs(random() % 2), abs(random() % 2), abs(random() % 30) - abs(random() % 10), abs(random() % 2)
   FROM (SELECT * FROM (
         (SELECT 0 UNION ALL SELECT 1) t2,
         (SELECT 0 UNION ALL SELECT 1) t4,
         (SELECT 0 UNION ALL SELECT 1) t8,
         (SELECT 0 UNION ALL SELECT 1) t16,
         (SELECT 0 UNION ALL SELECT 1) t32,
         (SELECT 0 UNION ALL SELECT 1) t64,
         (SELECT 0 UNION ALL SELECT 1) t128,
         (SELECT 0 UNION ALL SELECT 1) t256,
         (SELECT 0 UNION ALL SELECT 1) t512,
         (SELECT 0 UNION ALL SELECT 1) t1024,
         (SELECT 0 UNION ALL SELECT 1) t2048
         )
    ) LIMIT 246;







