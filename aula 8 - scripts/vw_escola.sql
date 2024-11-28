CREATE  VIEW `vw_escola` AS 
select `escola`.`CO_ENTIDADE` AS `CO_ENTIDADE`,`escola`.`NO_ENTIDADE` AS `NO_ENTIDADE`,`escola`.`NU_COMPUTADOR` AS `NU_COMPUTADOR`,`escola`.`NU_SALAS_EXISTENTES` AS `NU_SALAS_EXISTENTES`,(case `escola`.`TP_LOCALIZACAO` when 1 then 'Urbana' when 2 then 'Rural' end) AS `TP_LOCALIZACAO`,(case `escola`.`TP_DEPENDENCIA` when 1 then 'Federal' when 2 then 'Estadual' when 3 then 'Municipal' when 4 then 'Privada' end) AS `TP_DEPENDENCIA` 
from `escola` where (`escola`.`TP_SITUACAO_FUNCIONAMENTO` = 1) 
order by `escola`.`NO_ENTIDADE`;
