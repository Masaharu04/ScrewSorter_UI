import struct

DUMMYCOMMAND = 0x00                        #ダミー (0)
CONNECTCHECK = 0x01                        # 接続確認 (1)
CONNECTCHECKRESPONSE = 0x02                # 接続確認応答 (2)
OPERATIONSTATUS = 0x03                     # 動作状況 (3)
SENSORINFOREQUEST = 0x04                   # センサー情報要求 (4)
SENSORINFO = 0x05                          # センサー情報 (5)
CONFIGURATIONCHANGE = 0x06                 # 設定変更命令 (6)
BOLTREQUEST = 0x07                         # ボルト要求 シャッター開閉要求 (7)
DISCRIMINATIONRESULT = 0x08                # 判別結果 (8)
ERRORINFO = 0x09                           # エラー情報 (9)
MODULEOPERATION = 0x0A                     # モジュール動作 (10)
STOCKERTYPECHANGE = 0x0B                   # ストッカ種別変更 (11)
MOTORRESET = 0x0C                          # モータリセット (12)
MOTORMANUALOPERATION = 0x0D                # モーター手動操作 (13)
SOLENOIDINDIVIDUALOPERATION = 0x0E         # ソレノイド個別操作 (14)
DISCHARGEOPERATION = 0x0F                  # 排出動作 (15)
STOPCOMMAND = 0x10                         # 停止命令 (16)
SHUTDOWNCOMMAND = 0x11                     # シャットダウン命令 (17)
RETURNSECTIONOPERATIONSTARTREQUEST = 0x12  # 返却部動作開始要求 (18)
PATROLLAMPSTATECHANGE = 0x13               # パトランプ状態変更 (19)


INPUTUNITADDRESS = 0x01 #投入
DISCRIMINATIONUNITADDRESS = 0x02  #判別
ALIGNMENTUNITADDRESS = 0x03  #整列
RETURNUNITADDRESS = 0x04  #返却
DISPLAYUNITADDRESS = 0x05 #表示部
COMMUNICATIONUNITADDRESS = 0x06  #通信
EXTERIORUNITADDRESSADDRESS = 0x08   #外部
IMAGEPROCESSINGUNITADDRESS = 0x09

structsize = [
    0, 2, 2, 3, 2, 4, 4, 2, 3, 3, 3, 5, 2, 3, 3, 2, 2, 2, 2, 3
]


class Structure:
    def __init__(self):
        self.ConnectionCheck = ConnectionCheck()
        self.ConnectionCheckResponse = ConnectionCheckResponse()
        self.OperationStatus = OperationStatus()
        self.SensorInfoRequest = SensorInfoRequest()
        self.SensorInfo = SensorInfo()
        self.ConfigurationChange = ConfigurationChange()
        self.BoltRequest = BoltRequest()
        self.DiscriminationResult = DiscriminationResult()
        self.ErrorInfo = ErrorInfo()
        self.ModuleOperation = ModuleOperation()
        self.StockerTypeChange = StockerTypeChange()
        self.MotorReset = MotorReset()
        self.MotorManualOperation = MotorManualOperation()
        self.SolenoidIndividualOperation = SolenoidIndividualOperation()
        self.DischargeOperation = DischargeOperation()
        self.StopCommand = StopCommand()
        self.ShutdownCommand = ShutdownCommand()
        self.ReturnSectionOperationStartRequest = ReturnSectionOperationStartRequest()
        self.PatrolLampStateChange = PatrolLampStateChange()

class Protocol:
    def __init__(self):
        
        self.stockerTypeChange = None
        self.errorInfo = None
        print("init_call")
        self.s = Structure()
        print(self.s.ConnectionCheck)

    def set_protocol(self,receivedata, structsize):
        command = receivedata[1]

        if command == DUMMYCOMMAND:  # ダミーコマンド
            print("set_protocol function [this is dummy command]")
        elif command == CONNECTCHECK:  # 接続確認
            self.s.ConnectionCheck.input(receivedata[0],receivedata[1])
        elif command == CONNECTCHECKRESPONSE:  # 接続確認応答
            self.s.ConnectionCheckResponse.input(receivedata[0],receivedata[1])
        elif command == OPERATIONSTATUS:  # 操作状態
            self.s.OperationStatus.input(receivedata[0],receivedata[1],receivedata[2])
        elif command == SENSORINFOREQUEST:  # センサー情報要求
            self.s.SensorInfoRequest.input(receivedata[0],receivedata[1])
        elif command == SENSORINFO:  # センサー情報
            self.s.SensorInfo.input(receivedata[0],receivedata[1],receivedata[2],receivedata[3])
        elif command ==  CONFIGURATIONCHANGE:  # ボルト要求
            self.s.ConfigurationChange.input(receivedata[0],receivedata[1],receivedata[2],receivedata[3])
        elif command == BOLTREQUEST:  # ボルト要求
            self.s.BoltRequest.input(receivedata[0],receivedata[1])
        elif command == DISCRIMINATIONRESULT:  # 判別結果
            self.s.DiscriminationResult.input(receivedata[0],receivedata[1],receivedata[2])
        elif command == ERRORINFO:  # エラー情報
            self.s.ErrorInfo.input(receivedata[0],receivedata[1],receivedata[2])
        elif command == MODULEOPERATION:  # モジュール動作
            self.s.ModuleOperation.input(receivedata[0],receivedata[1],receivedata[2])
        elif command == STOCKERTYPECHANGE:  # ストッカ種別変更
            self.s.StockerTypeChange.input(receivedata[0],receivedata[1],receivedata[2],receivedata[3],receivedata[4])
        elif command == MOTORRESET:  # モータリセット
            self.s.MotorReset.input(receivedata[0],receivedata[1])
        elif command == MOTORMANUALOPERATION:  # モーター手動操作
            self.s.MotorManualOperation.input(receivedata[0],receivedata[1],receivedata[2])
        elif command == SOLENOIDINDIVIDUALOPERATION:  # ソレノイド個別操作
            self.s.SolenoidIndividualOperation.input(receivedata[0],receivedata[1],receivedata[2])
        elif command == DISCHARGEOPERATION:  # 排出動作
            self.s.DischargeOperation.input(receivedata[0],receivedata[1])
        elif command == STOPCOMMAND:  # 停止命令
            self.s.StopCommand.input(receivedata[0],receivedata[1])
        elif command == SHUTDOWNCOMMAND:  # シャットダウン命令
            self.s.ShutdownCommand.input(receivedata[0],receivedata[1])
        elif command == RETURNSECTIONOPERATIONSTARTREQUEST:  # 返却部動作開始要求
            self.s.ReturnSectionOperationStartRequest.input(receivedata[0],receivedata[1])
        elif command == PATROLLAMPSTATECHANGE:  # パトランプ状態変更
            self.s.PatrolLampStateChange.input(receivedata[0],receivedata[1],receivedata[2])
        else:
            print(f"Error: Unknown structure type received (command: {command})")


class ConnectionCheck:
    def __init__(self):
        self.address = None  # アドレス情報
        self.command = None  # コマンド

    def input(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class ConnectionCheckResponse:
    def __init__(self):
        self.address = None  # アドレス情報
        self.command = None  # コマンド

    def input(self,address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class OperationStatus:
    def __init__(self):
        self.address = None
        self.command = None
        self.status = None

    def input(self, address: int, command: int, status: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.status = status  # 状況

class SensorInfoRequest:
    def __init__(self):
        self.address = None
        self.command = None      

    def input(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class SensorInfo:
    def __init__(self):
        self.address = None
        self.command = None
        self.data1 = None
        self.data2 = None        

    def input(self, address: int, command: int, data1: int, data2: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.data1 = data1      # データ1
        self.data2 = data2      # データ2


class ConfigurationChange:
    def __init__(self):
        self.address = None
        self.command = None
        self.data1 = None  
        self.data2 = None  

    def input(self, address: int, command: int, data1: int, data2: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.data1 = data1  
        self.data2 = data2  




class BoltRequest:
    def __init__(self):
        self.address = None
        self.command = None   

    def input(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド



class DiscriminationResult:
    def __init__(self):
        self.address = None   # アドレス情報
        self.command = None  # コマンド
        self.decision = None  # 判定結果

    def input(self, address: int, command: int, decision: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.decision = decision  # 判定結果

class ErrorInfo:
    def __init__(self,):
        self.address = None
        self.command = None
        self.errorCode = None

    def input(self, address: int, command: int, errorCode: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.errorCode = errorCode  # エラーコード

class ModuleOperation:
    def __init__(self):
        self.address = None
        self.command = None
        self.status = None
    
    def input(self, address: int, command: int, status: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.status = status  # ステータス

class StockerTypeChange:
    def __init__(self):
        self.address = None
        self.command = None
        self.A = None
        self.B = None
        self.C = None

    def input(self, address: int, command: int, A: int, B: int, C: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.A = A  # A
        self.B = B  # B
        self.C = C  # C

class MotorReset:
    def __init__(self):
        self.address = None  # アドレス情報
        self.command = None  # コマンド

    def input(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class MotorManualOperation:
    def __init__(self):
        self.address = None
        self.command = None
        self.status = None

    def input(self, address: int, command: int, status: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.status = status  # ステータス

class SolenoidIndividualOperation:
    def __init__(self):
        self.address = None
        self.command = None
        self.solenoidId = None

    def input(self, address: int, command: int, solenoidId: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.solenoidId = solenoidId  # ソレノイドID

class DischargeOperation:
    def __init__(self):
        self.address = None
        self.command = None

    def input(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class StopCommand:
    def __init__(self):
        self.address = None
        self.command = None

    def input(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class ShutdownCommand:
    def __init__(self):
        self.address = None
        self.command = None
    
    def input(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class ReturnSectionOperationStartRequest:
    def __init__(self):
        self.address = None
        self.command = None

    def input(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class PatrolLampStateChange:
    def __init__(self):
        self.address = None
        self.command = None
        self.lampState = None

    def input(self, address: int, command: int, lampState: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.lampState = lampState  # ランプ状態
