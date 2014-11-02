insert into devices (name, mask, micro_id, kind, localization, status) values ("luz branca", "mascara_luz", 1, "lampada", "sala", "off");
insert into devices (name, mask, micro_id, kind, localization, status) values ("luz vermelha", "mascara_luz", 2, "lampada", "quarto", "off");
insert into devices (name, mask, micro_id, kind, localization, status) values ("sensor temperatura", "mascara_temp", 3, "sensor temp", "sala", "22");
insert into devices (name, mask, micro_id, kind, localization, status) values ("sensor luminosidade", "mascara_lumin", 4, "sensor lumin", "sala", "45");
insert into devices (name, mask, micro_id, kind, localization, status) values ("luz branca", "mascara_luz", 5, "lampada", "cozinha", "off");

insert into events (status, operator, mic_id, occurred_at) values ("on", "rafael", 2, "2014-10-10T15:10:55.299");
insert into events (status, operator, mic_id, occurred_at) values ("off", "rafael", 2, "2014-10-10T15:12:55.299");
insert into events (status, operator, mic_id, occurred_at) values ("on", "rafael", 1, "2014-10-10T15:16:55.299");
insert into events (status, operator, mic_id, occurred_at) values ("20", "rafael", 3, "2014-10-10T15:20:55.299");
insert into events (status, operator, mic_id, occurred_at) values ("23", "rafael", 3, "2014-10-10T15:25:55.299");
