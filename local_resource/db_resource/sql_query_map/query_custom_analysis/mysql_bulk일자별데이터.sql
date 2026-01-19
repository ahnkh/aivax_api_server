

USE stock_dbb_bulk

SHOW TABLES

DESC DAILY_BULK_DATA_2022



SELECT * from view_daily_bulk_data;

SELECT COUNT(1), REG_DATE FROM stock_dbb_bulk.daily_bulk_data_2012 GROUP BY REG_DATE DESC
SELECT COUNT(1), REG_DATE FROM stock_dbb_bulk.daily_bulk_data_2021 GROUP BY REG_DATE DESC

SELECT * FROM daily_bulk_data_2022 WHERE STOCK_NAME = '한양증권우' ORDER BY REG_DATE DESC

SELECT * FROM daily_bulk_data_2021 WHERE STOCK_NAME = '현대에이치티' AND REG_DATE = 20210419 ORDER BY REG_DATE DESC

DESC stock_dbb_bulk.daily_bulk_data_2022

-- 일자별 수집된 종목 건수
SELECT replace(reg_date, ',', ''), COUNT(1) FROM stock_dbb_bulk.daily_bulk_data_2022 GROUP BY reg_date ORDER BY reg_date DESC
SELECT replace(reg_date, ',', ''), COUNT(1) FROM stock_dbb_bulk.daily_bulk_data_2018 GROUP BY reg_date ORDER BY reg_date DESC
SELECT replace(reg_date, ',', ''), COUNT(1) FROM stock_dbb_bulk.daily_bulk_data_2014 GROUP BY reg_date ORDER BY reg_date DESC

SELECT * FROM stock_dbb_bulk.daily_bulk_data_2013 WHERE STOCK_NAME LIKE '%신송홀딩스%'

-- 종목정보와 부가정보 join (query 확장)
SELECT 
	-- (SELECT DISTINCT (NO) FROM stock_base_info.stock_csv_code_db WHERE stock_code = bulk_data.stock_code LIMIT 1) AS NO, 
	stock_code_db.no,
	bulk_data.stock_code, 
	bulk_data.stock_name, 
	bulk_data.unit_price 
FROM 
(
	-- (SELECT * from stock_dbb_bulk.daily_bulk_data_2022 where reg_date = 20220617) AS bulk_data -- , 
	(SELECT * from stock_dbb_bulk.daily_bulk_data_2022) AS bulk_data -- , 
	
	inner JOIN (select NO, stock_code from stock_base_info.stock_csv_code_db) AS stock_code_db ON bulk_data.stock_code = stock_code_db.stock_code
) 

SELECT NO, bulkdata.stock_code, stockcode.stock_name, unit_price, replace(reg_date, ',', '')
FROM 

stock_dbb_bulk.daily_bulk_data_2022 AS bulkdata, 
stock_base_info.stock_csv_code_db AS stockcode

WHERE bulkdata.stock_code = stockcode.stock_code
ORDER BY stockcode.stock_code





/** Naver Finance **/

SELECT REG_DATE, COUNT(1) from naver_finance GROUP BY REG_DATE ORDER BY REG_DATE desc

SELECT COUNT(1) from naver_finance WHERE REG_DATE = '2022-06-30' AND DIVISION = 'KOSDAQ'

SELECT * FROM naver_finance WHERE REG_DATE = '2022-06-15' AND PER >= 1.0 AND PER <= 3.0 AND PBR <= 2.0 AND ROA >= 10.0 AND TOTAL_ASSET <= 3000;

SELECT COUNT(1) FROM naver_finance WHERE REG_DATE = '2022-06-15' AND*/ STOCK_NAME = '휴마시스'

SELECT * FROM naver_finance WHERE REG_DATE = '2022-06-15'

SELECT DIVISION, REG_DATE FROM naver_finance GROUP BY DIVISION, REG_DATE ORDER BY REG_DATE desc


/** 뉴스 정보 **/

-- 일별 뉴스 건수 

DESC stock_news_bulk_data

-- 일별 주식 뉴스 건수 통계

SELECT COUNT(1), REG_DATE FROM stock_dbb_bulk.stock_news_bulk_data GROUP BY REG_DATE ORDER BY REG_DATE DESC

SELECT * FROM stock_news_bulk_data ORDER BY NO DESC

-- DELETE FROM stock_news_bulk_data WHERE REG_DATE >= '2022-06-27'
-- DELETE FROM stock_news_bulk_data WHERE REG_DATE >= '2022-07-06'
COMMIT

-- 신규 상장

SELECT NEWS_KEYWORD FROM stock_news_bulk_data GROUP BY NEWS_KEYWORD

SELECT 
	NO, 
	STOCK_NAME AS 종목명, 
	replace(REG_DATE, '00:00:00', '') AS 등록일, 
	NEWS_TITLE AS 기사제목, 
	HIGHLIGHT, 
	MYNOTE 
FROM stock_news_bulk_data WHERE NEWS_KEYWORD LIKE '%신규상장%' AND REG_DATE >= '2022-06-27' 
GROUP BY STOCK_NAME 
ORDER BY REG_DATE DESC

-- 특정 일자 전체 검색

SELECT 
	NO, 
	replace(REG_DATE, ' 00:00:00','') AS 등록일,  
	REGION AS 지역, 
	STOCK_NAME AS 종목명, 
	NEWS_TITLE AS 기사제목, 		
	NEWS_KEYWORD AS 키워드,
	MYNOTE AS 메모, 
	WEB_LINK AS 링크, 
	HIGHLIGHT AS 요약	

FROM stock_news_bulk_data 
WHERE REG_DATE >= '2022-07-06' AND NEWS_KEYWORD != '' -- AND MYNOTE != ''
AND NEWS_TITLE != '' 
-- AND NEWS_KEYWORD NOT IN ('신규상장', '매각', '유상증자', '신규상장,IPO', '자사주취득', '비대면진료', '부동산', '금리', '환율', '금리,부채', 'ETF,펀드', '유가') AND REGION = '한국'
-- GROUP BY WEB_LINK, STOCK_NAME
-- GROUP BY STOCK_NAME
ORDER BY REG_DATE DESC, STOCK_NAME DESC


SELECT COUNT(1) AS CNT, STOCK_NAME FROM stock_news_bulk_data WHERE REG_DATE >= '2022-06-01' GROUP BY STOCK_NAME ORDER BY CNT DESC, REG_DATE DESC

SELECT NO, REG_DATE AS 등록일, REGION AS 지역, STOCK_NAME AS 종목명, NEWS_TITLE AS 기사제목, WEB_LINK AS 링크, HIGHLIGHT AS 요약, MYNOTE AS 메모, NEWS_KEYWORD AS 키워드
-- SELECT *
FROM stock_news_bulk_data WHERE REG_DATE >= '2022-06-01' AND STOCK_NAME != '-'  ORDER BY STOCK_NAME, REG_DATE DESC

SELECT 1


SELECT 
	NO, 
	replace(REG_DATE, ' 00:00:00','') AS 등록일,  
	STOCK_NAME AS 종목명, 
	NEWS_TITLE AS 기사제목, 		
	NEWS_KEYWORD AS 키워드,
	MYNOTE AS 메모, 
	WEB_LINK AS 링크, 
	HIGHLIGHT AS 요약	

FROM stock_news_bulk_data 
WHERE REG_DATE >= '2022-06-20' AND NEWS_KEYWORD != '' AND MYNOTE != ''
AND NEWS_KEYWORD NOT IN ('신규상장', '매각', '유상증자', '신규상장,IPO', '자사주취득', '비대면진료', '부동산', '금리', '환율', '금리,부채', 'ETF,펀드', '유가') AND REGION = '한국'
-- GROUP BY WEB_LINK, STOCK_NAME
-- GROUP BY STOCK_NAME
ORDER BY REG_DATE DESC, STOCK_NAME DESC	


SELECT 
	NO, 
	replace(REG_DATE, ' 00:00:00','') AS 등록일,  
	-- STOCK_NAME AS 종목명, 
	NEWS_TITLE AS 기사제목, 		
	NEWS_KEYWORD AS 키워드,
	MYNOTE AS 메모, 
	WEB_LINK AS 링크, 
	HIGHLIGHT AS 요약	

FROM stock_news_bulk_data 
WHERE REG_DATE >= '2022-06-13' AND NEWS_KEYWORD != '' AND NEWS_KEYWORD IN ('부동산', '환율', '물가', '경기', '금리', '경기,전망') 
-- GROUP BY WEB_LINK, STOCK_NAME
-- GROUP BY STOCK_NAME
ORDER BY REG_DATE DESC, STOCK_NAME DESC	


SELECT 
	NO, 
	replace(REG_DATE, ' 00:00:00','') AS 등록일,  
	-- STOCK_NAME AS 종목명, 
	NEWS_TITLE AS 기사제목, 		
	NEWS_KEYWORD AS 키워드,
	MYNOTE AS 메모, 
	WEB_LINK AS 링크, 
	HIGHLIGHT AS 요약	

FROM stock_news_bulk_data 
WHERE REG_DATE >= '2022-06-13' AND NEWS_KEYWORD != '' AND NEWS_KEYWORD NOT IN ('금리',  '환율', '유가', '물가', '유가,금리') AND REGION != '한국'
-- GROUP BY WEB_LINK, STOCK_NAME
-- GROUP BY STOCK_NAME
ORDER BY REG_DATE DESC, STOCK_NAME DESC


SELECT CATEGORY FROM stock_news_bulk_data GROUP BY CATEGORY

UPDATE stock_news_bulk_data SET STOCK_NAME = '-' WHERE NO = 819
COMMIT

SELECT * FROM stock_news_bulk_data WHERE NEWS_KEYWORD = '부동산'

