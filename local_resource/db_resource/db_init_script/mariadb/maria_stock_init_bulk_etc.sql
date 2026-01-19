
/*
create database stock_dbb_bulk;
create database stock_dbb_2;

별도의 dbb에 반영할수 있게, dbb명은 추가 X

mysql -u root -p -D stock_dbb < maria_stock_init_bulk_etc.sql
*/

/*
두번 실행할때의 처리, 만일 기존 테이블의 완전 삭제시 별도 drop 
mariadb는 대소문자를 가리지 않아, 대소문자 구문 무의미 
*/

USE STOCK_DBB_BULK;

SHOW TABLES;

/* DESC DAILY_BULK_DATA_2012 */

/**
* Naver 재무재표, 데이터가 많지 않아 년단위로 자르지 않고 저장 (월에 한번 정도라서)
* 이름 그대로 사용.
*/

CREATE TABLE IF NOT EXISTS STOCK_DBB_BULK.NAVER_FINANCE
(
	NO INT NOT NULL, /* No */
	DIVISION VARCHAR(16) NOT NULL, /* 구분(코스피/코스닥) */
	REG_DATE VARCHAR(16) NOT NULL DEFAULT '', /* 수집날짜, YYYY-MM-DD */
	STOCK_CODE VARCHAR(16) NOT NULL, /* 종목코드 (키) */
	STOCK_CODE_VALID VARCHAR(16) NOT NULL DEFAULT '', /* 종목코드 유효성 : 종목코드 000000으로 대체 가능 하기는 하나, 조작없는 순수 데이터가 필요.*/

	STOCK_NAME VARCHAR(128) NOT NULL DEFAULT '', /* 종목명*/
	FACE_VALUE INT NOT NULL DEFAULT 0, /* 액면가,*/
	PUBLIC_STOCKS INT NOT NULL DEFAULT 0, /* 상장주식수(천주)*/
	MARKET_CAPITAL INT NOT NULL DEFAULT 0, /* 시가총액(억)*/

	SALES INT NOT NULL DEFAULT 0, /* 매출액(억),*/
	TOTAL_ASSET INT NOT NULL DEFAULT 0, /* 자산총계(억),*/
	TOTAL_DEBT INT NOT NULL DEFAULT 0, /* 부채총계(억),*/
	FOREIGN_RATE DECIMAL(10,3) DEFAULT 0.0, /* 외국인비율,*/
	BUSINESS_PROFIT INT NOT NULL DEFAULT 0, /* 영업이익(억),*/

	CURRENT_NET_PROFIT INT NOT NULL DEFAULT 0, /* 당기순이익(억),*/
	INCOME_PER_SHARE INT NOT NULL DEFAULT 0, /* 주당순이익(억),*/
	COMMON_DIVIDEND INT NOT NULL DEFAULT 0, /* 보통주배당금(원),*/
	GROW_RATE_SALES DECIMAL(10,3) DEFAULT 0.0, /* 매출액증가율,*/
	BUSINESS_PROFIT_GROW_RATE DECIMAL(10,3) DEFAULT 0.0, /* 영업이익증가율,*/

	PER DECIMAL(10,3) DEFAULT 0.0,
	ROE DECIMAL(10,3) DEFAULT 0.0,
	ROA DECIMAL(10,3) DEFAULT 0.0,
	PBR DECIMAL(10,3) DEFAULT 0.0,
	INTERNAL_RESERVE_RATE DECIMAL(10,3) DEFAULT 0.0, /* 유보율*/

	PRIMARY KEY (NO, STOCK_CODE, REG_DATE)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX IF NOT EXISTS UIX_NAVER_FINANCE_CODE_DATE ON STOCK_DBB_BULK.NAVER_FINANCE(STOCK_CODE, REG_DATE);


/* ---------------------------------------------------------------- */

/**
* 종목 뉴스 데이터, db 저장
* TEXT 형태 고려.
*/

/**
- 일자 
- 지역 (한국, 미국, 유럽, 기타)
- 구분 (종목정보, 실적, 테마뉴스, )
- 종목명 (종목이 바뀔때 문제, 종목코드에 대한 링크, 여러개 구분자 개선 검토)
- 제목 (title), 기본 정도
- 뉴스링크 , 웹 링크
- 메모 (뉴스중 주요 정보)
- DESC (개인 메모)
- THEME (향후 업데이트)
- 키워드 (검색 키워드)
- 출처 (http:// htts:// 이후 / 까지 잘라서 저장 (정규 표현식?)
*/

/*DROP INDEX IX_STOCK_NEWS_BULK_DATA_REG_DATE ON STOCK_NEWS_BULK_DATA;*/
/*DROP INDEX IX_STOCK_NEWS_BULK_DATA_STOCK_NAME ON STOCK_NEWS_BULK_DATA;*/

/* DROP TABLE STOCK_NEWS_BULK_DATA */

CREATE TABLE IF NOT EXISTS STOCK_DBB_BULK.STOCK_NEWS_BULK_DATA   
(    
	NO BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	REG_DATE VARCHAR(32) NOT NULL, /* 등록일자 (VARCHAR)*/
	REGION VARCHAR(32) DEFAULT '', /* 지역 (KOREA, USA, EURO, ASIS, ETC)*/
	CATEGORY VARCHAR(32) DEFAULT '', /* 구분 (종목정보, 실적, 테마뉴스, 등등)*/
	STOCK_NAME VARCHAR(128) DEFAULT '', /* 종목명 (국내, 해외)*/
	NEWS_TITLE VARCHAR(256) DEFAULT '', /* 뉴스 제목*/
	WEB_LINK VARCHAR(256) DEFAULT '', /* 뉴스 링크 (많이 길수 있음)*/
	HIGHLIGHT TEXT, /* 뉴스중 주요 정보*/
	MYNOTE TEXT, /* 개인 메모*/
	THEME VARCHAR(256) DEFAULT '', /* 뉴스 테마*/
	NEWS_KEYWORD VARCHAR(256) DEFAULT '' /* 키워드*/
) 
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 


CREATE INDEX IF NOT EXISTS IX_STOCK_NEWS_BULK_DATA_REG_DATE ON STOCK_DBB_BULK.STOCK_NEWS_BULK_DATA(REG_DATE);
CREATE INDEX IF NOT EXISTS IX_STOCK_NEWS_BULK_DATA_STOCK_NAME ON STOCK_DBB_BULK.STOCK_NEWS_BULK_DATA(STOCK_NAME);

/**
INSERT INTO stock_dbb_bulk.STOCK_NEWS_BULK_DATA (REG_DATE, REGION, CATEGORY, STOCK_NAME, NEWS_TITLE, WEB_LINK, NEWS_PROVIDER) 
VALUES (20220507, 'KOREA', '종목정보', '강원랜드', '카지노 산업 정상국면 돌입…내국인 카지노 가파른 실적회복', 'https://n.news.naver.com/mnews/article/018/0005226558?sid=101', 'n.news.naver.com')
*/

/* 중간 종료*/
/*EXIT */
