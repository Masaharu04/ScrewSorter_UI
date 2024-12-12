import struct

DUMMYCOMMAND = 0 #ダミー ver 1.1修正 ダミーコマンド追加
CONNECTCHECK = 1 # 接続確認
CONNECTCHECKRESPONSE = 2 # 接続確認応答
OPERATIONSTATUS = 3 # 操作状態
SENSORINFOREQUEST = 4 # センサー情報要求
SENSORINFO = 5 # センサー情報
INPUTSECTIONSETTINGCHANGE = 6 # 投入部設定変更
DISCRIMINATIONSETTINGCHANGE = 7 # 判別部設定変更
BOLTREQUEST = 8 # ボルト要求
DISCRIMINATIONRESULTSUMMARY = 9 # 判別部結果総数
DISCRIMINATIONRESULT = 10 # 判別結果
INPUTSTOCKERSTATUS = 11 # 投入部ストッカ状況
ERRORINFO = 12 # エラー情報
MODULEOPERATION = 13 # モジュール動作
STOCKERTYPECHANGE = 14 # ストッカ種別変更
MOTORRESET = 15 # モータリセット
MOTORMANUALOPERATION = 16 # モーター手動操作
MIDSTOCKERSTATUSREQUEST = 17 # 中間ストッカ状況要求
MIDSTOCKERSTATUS = 18 # 中間ストッカ状況
SOLENOIDINDIVIDUALOPERATION = 19 # ソレノイド個別操作
ONECYCLEOPERATION = 20 # ワンサイクル動作
DISCHARGEOPERATION = 21 # 排出動作
STOPCOMMAND = 22 # 停止命令
SHUTDOWNCOMMAND = 23 # シャットダウン命令
IMAGEPROCESSINGREQUEST = 24 # 画像処理要求
IMAGEPROCESSINGRESULT = 25 # 画像処理結果
RETURNSECTIONOPERATIONSTARTREQUEST = 26 # 返却部動作開始要求
PATROLLAMPSTATECHANGE = 27 # パトランプ状態変更


class Protocol:
    def __init__(self):
        self.stockerTypeChange = None
        self.errorInfo = None
        self.inputStockerStatus = None
        #pass


    def create_struct(self,data, struct_format):
        # 構造体のサイズを計算
        struct_size = struct.calcsize(struct_format)

        # データサイズが構造体サイズより小さい場合に警告
        if len(data) < struct_size:
            print("Warning: Received data size is smaller than expected structure size")
            return None
        # データを構造体に変換
        result = struct.unpack(struct_format, data[:struct_size])

        return result

    def set_protocol(self,receivedata, structsize):
        p = Protocol()
        print(receivedata)
        command = receivedata[1]

        if command == DUMMYCOMMAND:  # ダミーコマンド
            print("set_protocol function [this is dummy command]")
        elif command == CONNECTCHECK:  # 接続確認
            #p.connectionCheck = self.create_struct(receivedata, structsize[1])
            p.connectionCheck = ConnectionCheck(receivedata[0],receivedata[1])
        elif command == CONNECTCHECKRESPONSE:  # 接続確認応答
            #p.connectionCheckResponse = create_struct(receivedata, structsize[2])
            p.connectionCheckResponse = ConnectionCheckResponse(receivedata[0],receivedata[1],receivedata[2])
        elif command == OPERATIONSTATUS:  # 操作状態
            #p.operationStatus = create_struct(receivedata, structsize[3])
            p.operationStatus = OperationStatus(receivedata[0],receivedata[1],receivedata[2])
        elif command == SENSORINFOREQUEST:  # センサー情報要求
            #p.sensorInfoRequest = create_struct(receivedata, structsize[4])
            p.sensorInfoRequest = SensorInfoRequest(receivedata[0],receivedata[1],receivedata[2])
        elif command == SENSORINFO:  # センサー情報
            #p.sensorInfo = create_struct(receivedata, structsize[5])
            p.sensorInfo = SensorInfo(receivedata[0],receivedata[1],receivedata[2],receivedata[3])
        elif command == INPUTSECTIONSETTINGCHANGE:  # 投入部設定変更
            #p.inputSectionSettingsChange = create_struct(receivedata, structsize[6])
            p.inputSectionSettingsChange = InputSectionSettingsChange(receivedata[0],receivedata[1],receivedata[2],receivedata[3])
        elif command == DISCRIMINATIONSETTINGCHANGE:  # 判別部設定変更
            #p.discriminationSettingsChange = create_struct(receivedata, structsize[7])
            p.discriminationSettingsChange = DiscriminationSettingsChange(receivedata[0],receivedata[1],receivedata[2])
        elif command == BOLTREQUEST:  # ボルト要求
            #p.boltRequest = create_struct(receivedata, structsize[8])
            p.boltRequest = BoltRequest(receivedata[0],receivedata[1])
        elif command == DISCRIMINATIONRESULTSUMMARY:  # 判別部結果総数
            #p.discriminationResultSummary = create_struct(receivedata, structsize[9])
            p.discriminationResultSummary = DiscriminationResultSummary(receivedata[0],receivedata[1],receivedata[2],receivedata[3],receivedata[4],receivedata[5],receivedata[6],receivedata[7],receivedata[8],receivedata[9],receivedata[10],receivedata[11])
        elif command == DISCRIMINATIONRESULT:  # 判別結果
            #p.discriminationResult = create_struct(receivedata, structsize[10])
            p.discriminationResult = DiscriminationResult(receivedata[0],receivedata[1],receivedata[2])
        elif command == INPUTSTOCKERSTATUS:  # 投入部ストッカ状況
            #p.inputStockerStatus = create_struct(receivedata, structsize[11])
            p.inputStockerStatus = InputStockerStatus(receivedata[0],receivedata[1],receivedata[2])
        elif command == ERRORINFO:  # エラー情報
            #p.errorInfo = create_struct(receivedata, structsize[12])
            p.errorInfo = ErrorInfo(receivedata[0],receivedata[1],receivedata[2])
        elif command == MODULEOPERATION:  # モジュール動作
            #p.moduleOperation = create_struct(receivedata, structsize[13])
            p.moduleOperation = ModuleOperation(receivedata[0],receivedata[1],receivedata[2],receivedata[3])
        elif command == STOCKERTYPECHANGE:  # ストッカ種別変更
            #p.stockerTypeChange = create_struct(receivedata, structsize[14])
            p.stockerTypeChange = StockerTypeChange(receivedata[0],receivedata[1],receivedata[2],receivedata[3],receivedata[4])
        elif command == MOTORRESET:  # モータリセット
            #p.motorReset = create_struct(receivedata, structsize[15])
            p.motorReset = MotorReset(receivedata[0],receivedata[1])
        elif command == MOTORMANUALOPERATION:  # モーター手動操作
            #p.motorManualOperation = create_struct(receivedata, structsize[16])
            p.motorManualOperation = MotorManualOperation(receivedata[0],receivedata[1],receivedata[2])
        elif command == MIDSTOCKERSTATUSREQUEST:  # 中間ストッカ状況要求
            #p.midStockerStatusRequest = create_struct(receivedata, structsize[17])
            p.midStockerStatusRequest = MidStockerStatusRequest(receivedata[0],receivedata[1])
        elif command == MIDSTOCKERSTATUS:  # 中間ストッカ状況
            #p.midStockerStatus = create_struct(receivedata, structsize[18])
            p.midStockerStatus = MidStockerStatus(receivedata[0],receivedata[1],receivedata[2])
        elif command == SOLENOIDINDIVIDUALOPERATION:  # ソレノイド個別操作
            #p.solenoidIndividualOperation = create_struct(receivedata, structsize[19])
            p.solenoidIndividualOperation = SolenoidIndividualOperation(receivedata[0],receivedata[1],receivedata[2],receivedata[3],receivedata[4])
        elif command == ONECYCLEOPERATION:  # ワンサイクル動作
            #p.oneCycleOperation = create_struct(receivedata, structsize[20])
            p.oneCycleOperation = OneCycleOperation(receivedata[0],receivedata[1])
        elif command == DISCHARGEOPERATION:  # 排出動作
            #p.dischargeOperation = create_struct(receivedata, structsize[21])
            p.dischargeOperation = DischargeOperation(receivedata[0],receivedata[1])
        elif command == STOPCOMMAND:  # 停止命令
            #p.stopCommand = create_struct(receivedata, structsize[22])
            p.stopCommand = StopCommand(receivedata[0],receivedata[1])
        elif command == SHUTDOWNCOMMAND:  # シャットダウン命令
            #p.shutdownCommand = create_struct(receivedata, structsize[23])
            p.shutdownCommand = ShutdownCommand(receivedata[0],receivedata[1])
        elif command == IMAGEPROCESSINGREQUEST:  # 画像処理要求
            #p.imageProcessingRequest = create_struct(receivedata, structsize[24])
            p.imageProcessingRequest = ImageProcessingRequest(receivedata[0],receivedata[1])
        elif command == IMAGEPROCESSINGRESULT:  # 画像処理結果
            #p.imageProcessingResult = create_struct(receivedata, structsize[25])
            p.imageProcessingResult = ImageProcessingResult(receivedata[0],receivedata[1],receivedata[2])
        elif command == RETURNSECTIONOPERATIONSTARTREQUEST:  # 返却部動作開始要求
            #p.returnSectionOperationStartRequest = create_struct(receivedata, structsize[26])
            p.returnSectionOperationStartRequest = ReturnSectionOperationStartRequest(receivedata[0],receivedata[1])
        elif command == PATROLLAMPSTATECHANGE:  # パトランプ状態変更
            #p.patrolLampStateChange = create_struct(receivedata, structsize[27])
            p.patrolLampStateChange = PatrolLampStateChange(receivedata[0],receivedata[1],receivedata[2])
        else:
            print(f"Error: Unknown structure type received (command: {command})")

        return p



class ConnectionCheck:
    def __init__(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class ConnectionCheckResponse:
    def __init__(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class OperationStatus:
    def __init__(self, address: int, command: int, status: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.status = status  # 状況

class SensorInfoRequest:
    def __init__(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class SensorInfo:
    def __init__(self, address: int, command: int, data1: int, data2: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.data1 = data1      # データ1
        self.data2 = data2      # データ2

class InputSectionSettingsChange:
    def __init__(self, address: int, command: int, upspeed: int, downspeed: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.upspeed = upspeed  # アップスピード
        self.downspeed = downspeed  # ダウンスピード

class DiscriminationSettingsChange:
    def __init__(self, address: int, command: int, speed: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.speed = speed  # スピード

class BoltRequest:
    def __init__(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class DiscriminationResultSummary:
    def __init__(self, address: int, command: int, boltA1: int, boltA2: int, boltB1: int, boltB2: int,
                 boltC1: int, boltC2: int, boltEtc1: int, boltEtc2: int, boltRe1: int, boltRe2: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.boltA1 = boltA1  # ボルトA1
        self.boltA2 = boltA2  # ボルトA2
        self.boltB1 = boltB1  # ボルトB1
        self.boltB2 = boltB2  # ボルトB2
        self.boltC1 = boltC1  # ボルトC1
        self.boltC2 = boltC2  # ボルトC2
        self.boltEtc1 = boltEtc1  # ボルトEtc1
        self.boltEtc2 = boltEtc2  # ボルトEtc2
        self.boltRe1 = boltRe1  # ボルトRe1
        self.boltRe2 = boltRe2  # ボルトRe2

class DiscriminationResult:
    def __init__(self, address: int, command: int, decision: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.decision = decision  # 判定結果

class InputStockerStatus:
    def __init__(self, address: int, command: int, capacity: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.capacity = capacity  # 容量

class ErrorInfo:
    def __init__(self, address: int, command: int, errorCode: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.errorCode = errorCode  # エラーコード

class ModuleOperation:
    def __init__(self, address: int, command: int, modules: int, status: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.modules = modules  # モジュール数
        self.status = status  # ステータス

class StockerTypeChange:
    def __init__(self, address: int, command: int, A: int, B: int, C: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.A = A  # A
        self.B = B  # B
        self.C = C  # C

class MotorReset:
    def __init__(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class MotorManualOperation:
    def __init__(self, address: int, command: int, status: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.status = status  # ステータス

class MidStockerStatusRequest:
    def __init__(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class MidStockerStatus:
    def __init__(self, address: int, command: int, capacity: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.capacity = capacity  # 容量

class SolenoidIndividualOperation:
    def __init__(self, address: int, command: int, modules: int, solenoidId: int, sec: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.modules = modules  # モジュール数
        self.solenoidId = solenoidId  # ソレノイドID
        self.sec = sec  # 秒数

class OneCycleOperation:
    def __init__(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class DischargeOperation:
    def __init__(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class StopCommand:
    def __init__(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class ShutdownCommand:
    def __init__(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class ImageProcessingRequest:
    def __init__(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class ImageProcessingResult:
    def __init__(self, address: int, command: int, result: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.result = result  # 結果

class ReturnSectionOperationStartRequest:
    def __init__(self, address: int, command: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド

class PatrolLampStateChange:
    def __init__(self, address: int, command: int, lampState: int):
        self.address = address  # アドレス情報
        self.command = command  # コマンド
        self.lampState = lampState  # ランプ状態
