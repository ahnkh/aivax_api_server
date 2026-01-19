

import os
import datetime
from typing import Any

from lib_include import *

# import sys
# import traceback

# import threading #tid 가져오기 위해 선언
# import time


'''
byte 기반 고속 buffer writer, 불필요한 연산 최소화
TODO: 거의 같고 연산만 다른 문제, 일단 넘어가자.
'''

class ByteBufferFastWriter:

    def __init__(self):
        
        self.__byteArray:bytearray = None #바이트 버퍼

        self.__nWriteCount:int = 0 #최대 버퍼 제한값

        self.__dictBulkOpt:dict = None #config option

        #임시경로, Bulk 경로
        self.__strTempFileFullPath:str = ""
        self.__strBulkFileFullPath:str = ""

        self.__nWriteLimit:int = 0 #저장 제한값

        #2025.09.10 부가정보의 수집 기능 추가 => 일단 제외해 보자.
        # self.__etcValue = {}
        
        self.__lastFlushTime:float = 0.0 #마지막 flush 시간, 직접 지정한다.

        pass
    
    def UpdateLastFlushTime(self, nLastFlushTime:float):
        
        self.__lastFlushTime = nLastFlushTime
        return ERR_OK
    
    def GetLastFlushTIme(self) -> float:
        
        return self.__lastFlushTime

    # #부가 정보, 필요한 여분의 정보를 저장하는 기능을 추가.
    # def UpdateEtcValue(self, strKey:str, value:Any):

    #     '''
    #     '''

    #     self.__etcValue[strKey] = value

    #     return ERR_OK
    
    # def GetEtcValue(self, strKey:str) -> Any:

    #     return self.__etcValue.get(strKey)

    #초기화 모듈, config와 분리를 위해, 밖에서 만들어서 던진다.
    def Initialize(self, dictOpt:dict):
        
        '''
        '''
        
        self.__byteArray:bytearray = bytearray()
        
        self.__nWriteCount = 0

        self.__dictBulkOpt = dictOpt.copy()

        #TODO: refactoring.
        strTempFilePath = self.__dictBulkOpt.get("temp_file_path")
        strBulkFilePath = self.__dictBulkOpt.get("bulk_file_path")

        self.__nWriteLimit = self.__dictBulkOpt.get("max_limit")
        
        self.__makeDirectory(strTempFilePath)
        self.__makeDirectory(strBulkFilePath)

        # if "/" != strBulkFilePath[len(strBulkFilePath) -1] :
        #     strBulkFilePath += "/"
        
        # if "/" != strTempFilePath[len(strTempFilePath) -1] :
        #     strTempFilePath += "/"
        
        # if (False == os.path.isdir(strTempFilePath)):
        #     os.makedirs(strTempFilePath)
            
            # LOG().info(f"create temp directory {strTempFilePath}")
            # self.__dictBulkOpt["temp_file_path"] = strTempFilePath #혹시모르니 update


        # if "/" != strBulkFilePath[len(strBulkFilePath) -1] :
        #     strBulkFilePath += "/"
            
        # if (False == os.path.isdir(strBulkFilePath)):
        #     os.makedirs(strBulkFilePath)

        #     LOG().info(f"create bulk directory {strBulkFilePath}")            
        #     self.__dictBulkOpt["bulk_file_path"] = strBulkFilePath

        self.__initializeFileWriteState()
        #self.__MakeFileName(self.__strTempFileFullPath, self.__strBulkFileFullPath, self.__dictBulkOpt)

        return ERR_OK


    def WriteLog(self, byteData:bytes):

        '''
        '''
        
        self.__byteArray.extend(byteData)
        
        self.__nWriteCount += 1

        #제한값 이상이면, 즉시 저장
        if self.__nWriteLimit <= self.__nWriteCount:
            self.FlushBuffer()
            pass

        return ERR_OK
    
    #데이터를 저장한다.
    def FlushBuffer(self):

        #버퍼가 비어있으면 종료
        if (0 == len(self.__byteArray)) or (0 == self.__nWriteCount):
            self.__initializeFileWriteState()
            return ERR_OK

        #파일에 저장 => TODO: byte 그대로 저장, 성능 개선.
        #TODO: 예외처리 보강
        # nErrWriteFile = FileIOHelper.WriteToUTF8File(self.__strBuffer, self.__strTempFileFullPath)
        
        # if ERR_FAIL == nErrWriteFile:
        #     LOG().error(f"fail write file {self.__strTempFileFullPath}")
        #     return ERR_FAIL
        
        #테스트용 로그 추가
        # LOG().debug(f"flush buffer to file, count = {self.__nWriteCount}, path = {self.__strTempFileFullPath} -> {self.__strBulkFileFullPath}")
        
        #TODO: 저장, binary 모드, 그대로 write
        #append, 파일이 존재하지 않으면 자동으로 생성된다. 
        # with open(self.__strTempFileFullPath, "ab") as f:  # binary mode
        #     f.write(self.__byteArray)
        
        with open(self.__strBulkFileFullPath, "ab") as f:  # binary mode
            f.write(self.__byteArray)
            

        #여기 로직 제거, 우선 동작 시험
        '''
        #한번더 체크
        bAccess = os.access(self.__strTempFileFullPath, os.W_OK)

        if False == bAccess:
            LOG().error(f"fail open file, access error path = {self.__strTempFileFullPath}, skip rename to {self.__strBulkFileFullPath}")
            return ERR_FAIL
        
        #이 로직은 향후 보강, fluentbit에 맞춰서 다시 고려하자. 우선 이상태로 개발 마무리.
        os.rename(self.__strTempFileFullPath, self.__strBulkFileFullPath)
        '''

        #저장이 마무리 되면, 다시 초기화 => 불함리한 부분이 있으나, 향후 리펙토링.
        self.__initializeFileWriteState()

        #2024.05.21 flush 이후 처리 스크립트 추가 => log rotation 용으로 사용
        flush_finish_script = self.__dictBulkOpt.get("flush_finish_script")

        #TODO: 만일 설정한다면, 반복 수행하기에, 별도의 예외처리는 수행하지 않는다.
        if None != flush_finish_script:
            os.system(flush_finish_script)

        return ERR_OK

    ########################################## private

    #파일 기록상태, 초기화 한다.
    def __initializeFileWriteState(self):

        # self.__strBuffer = ""
        self.__byteArray.clear()
        self.__nWriteCount = 0

        self.__strTempFileFullPath = ""
        self.__strBulkFileFullPath = ""

        self.__makeFileName(self.__dictBulkOpt)

        #LOG().debug("Initialize File Write State, tempfile={}, bulkfile={}".format(self.__strTempFileFullPath, self.__strBulkFileFullPath))

        return ERR_OK

    #파일명, 시작시점에 만들어서, 저장후 다시 생성 (저장시점에 만들면 날짜가 맞지 않을수 있다.)
    #member로 던지면, 값을 변경하면 같이 변경될듯.
    def __makeFileName(self, dictBulkOpt:dict):
        
        '''
        '''
        
        #현재 시간을 가져온다.

        strTempFileDir = dictBulkOpt.get("temp_file_path")
        strBulkFileDir = dictBulkOpt.get("bulk_file_path")
        
        # 사소한 예외처리, / 추가, 향후에.
        
        strCollectionName = dictBulkOpt.get("collection_prefix")

        now = datetime.datetime.now() #오늘날짜

        #TODO: 2025.10.14 사양 변경 테스트, 일자별로 한개의 파일을 생성하고
        # file을 append 모드로 관리한다.

        strDateYMD = now.strftime("%Y%m%d")
        # microsecond = now.microsecond

        pid = os.getpid()        
        #tid = threading.get_ident()
        #threading._get_ident()
        
        # 종속성 제거.
        # tid = threading.get_ident()

        #임시경로#컬렉션명#현재날짜(YMD)#고유값.json
        #추가적인 고유값 필요

        #TODO: 안들어가진다.. 멤버로 관리
        
        # self.__strTempFileFullPath = "{tempdir}{collection}#{date}#{msec}#{pid}#{tid}.json".format(
        #     tempdir = strTempFileDir,
        #     collection = strCollectionName,
        #     date = strDateYMD,
        #     msec = microsecond,
        #     pid = pid,
        #     tid = tid
        # )

        # self.__strBulkFileFullPath = "{bulkdir}{collection}#{date}#{msec}#{pid}#{tid}.json".format(
        #     bulkdir = strBulkFileDir,
        #     collection = strCollectionName,
        #     date = strDateYMD,
        #     msec = microsecond,
        #     pid = pid,
        #     tid = tid
        # )
        
        #TODO: rename 방식은, 로그가 남지 않는다. bulk 경로에 저장해야 한다. 
        #우선 설정 형상은 유지하고, bulk에만 기록하도록 수정한다.
        self.__strTempFileFullPath = f"{strTempFileDir}{strCollectionName}#{strDateYMD}{pid}.json"

        self.__strBulkFileFullPath = f"{strBulkFileDir}{strCollectionName}#{strDateYMD}#{pid}.json"

        #LOG().debug("tempfile = {}, destfile = {}".format(strTempFilePath, strBulkFilePath))

        return ERR_OK
    
    #디렉토리 생성
    def __makeDirectory(self, strDirectory:str):
        
        '''
        '''
        
        if "/" != strDirectory[len(strDirectory) -1] :
            strDirectory += "/"
            
        if (False == os.path.isdir(strDirectory)):
            os.makedirs(strDirectory)
        
        return ERR_OK
