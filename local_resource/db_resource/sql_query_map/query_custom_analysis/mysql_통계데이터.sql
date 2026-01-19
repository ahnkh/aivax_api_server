
use stock_dbb_statics

/** 일별 변화 통계 **/

DESC price_daily_change_statics_2022

SELECT 
	STOCK_NAME AS 종목명,
	replace(REG_DATE, ',', '') AS 등록일, 
	CONCAT (PRICE_CHANGE* 100, '%') AS 단가변화, 
	CURRENT_PRICE AS 전일단가, 
	NEXT_PRICE AS 금일단가 
FROM price_daily_change_statics_2022 
WHERE /* REG_DATE = 20211231 AND*/ STOCK_NAME = 'LG에너지솔루션' ORDER BY REG_DATE DESC;

SELECT COUNT(1), REPLACE (REG_DATE, ',', '') FROM stock_dbb_statics.price_daily_change_statics_2012 GROUP BY REG_DATE;
SELECT COUNT(1), REPLACE (REG_DATE, ',', '') FROM stock_dbb_statics.price_daily_change_statics_2013 GROUP BY REG_DATE;
SELECT COUNT(1), REPLACE (REG_DATE, ',', '') FROM stock_dbb_statics.price_daily_change_statics_2014 GROUP BY REG_DATE;
SELECT COUNT(1), REPLACE (REG_DATE, ',', '') FROM stock_dbb_statics.price_daily_change_statics_2015 GROUP BY REG_DATE;
SELECT COUNT(1), REPLACE (REG_DATE, ',', '') FROM stock_dbb_statics.price_daily_change_statics_2016 GROUP BY REG_DATE;
SELECT COUNT(1), REPLACE (REG_DATE, ',', '') FROM stock_dbb_statics.price_daily_change_statics_2017 GROUP BY REG_DATE;
SELECT COUNT(1), REPLACE (REG_DATE, ',', '') FROM stock_dbb_statics.price_daily_change_statics_2018 GROUP BY REG_DATE;
SELECT COUNT(1), REPLACE (REG_DATE, ',', '') FROM stock_dbb_statics.price_daily_change_statics_2019 GROUP BY REG_DATE;
SELECT COUNT(1), REPLACE (REG_DATE, ',', '') FROM stock_dbb_statics.price_daily_change_statics_2020 GROUP BY REG_DATE;
SELECT COUNT(1), REPLACE (REG_DATE, ',', '') FROM stock_dbb_statics.price_daily_change_statics_2021 GROUP BY REG_DATE;
SELECT COUNT(1), REPLACE (REG_DATE, ',', '') FROM stock_dbb_statics.price_daily_change_statics_2022 GROUP BY REG_DATE ORDER BY REG_DATE DESC;

DELETE FROM price_daily_change_statics_2012

COMMIT;
