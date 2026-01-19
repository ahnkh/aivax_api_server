USE stock_base_info

SHOW TABLES
DESC stock_base_info

-----------------------------------------------------------------------------

-- DROP table stockcsvcodedb;

SELECT * FROM stock_base_info.stock_base_info ORDER BY NO desc
SELECT * FROM stock_base_info.stock_csv_code_db ORDER BY NO desc

SELECT * FROM stock_base_info.stock_base_info WHERE STOCK_NAME LIKE '%창해%'


-----------------------------------------------------------------------------

/**
* 종목 업데이트 이력
*/

-- DROP TABLE stock_base_info.STOCK_BASE_INFO_HISTORY

-- DELETE FROM stock_base_info.STOCK_BASE_INFO_HISTORY  WHERE 1=1

SELECT * FROM stock_base_info.STOCK_BASE_INFO_HISTORY WHERE stock_code = '000020' ORDER BY  REG_DATE DESC, STOCK_CODE

SELECT * FROM stock_base_info.STOCK_BASE_INFO_HISTORY WHERE REG_DATE >= 20220601 ORDER BY STOCK_CODE

-- LAST 쿼리 미지원
-- SELECT LAST(REG_DATE) FROM stock_base_info.STOCK_BASE_INFO_HISTORY

INSERT INTO stock_base_info.STOCK_BASE_INFO_HISTORY VALUES ('00000', 'test', 'test', 20170101, '', '')
COMMIT

ALTER TABLE stock_base_info.STOCK_BASE_INFO_HISTORY DROP PRIMARY KEY


DESC stock_base_info.STOCK_BASE_INFO_HISTORY

-- INSERT INTO STOCK_BASE_INFO_HISTORY (STOCK_CODE, CURRENT_STOCK_NAME, OLD_STOCK_NAME, REG_DATE) VALUES ('test', 'test', 'test', 1);

SELECT * FROM stock_base_info.STOCK_BASE_INFO_HISTORY ORDER BY REG_DATE DESC

-- DELETE FROM stock_base_info.STOCK_BASE_INFO_HISTORY WHERE 1=1
-- COMMIT

SELECT STOCK_CODE FROM stock_base_info.STOCK_BASE_INFO_HISTORY GROUP BY STOCK_CODE

SELECT COUNT(1) FROM stock_base_info.STOCK_BASE_INFO_HISTORY
