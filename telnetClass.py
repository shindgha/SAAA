import telnetlib
import time

class TelnetCilent:

    def __init__(self):
        self.hostIP = ''
        self.userName = ''
        self.userPassword = ''
        self.devID = ''

        self.loginPrompt = ''
        self.passwordPrompt = ''
        self.cmdLines = ''
        self.resultDictText = {}

    def SetHostIPAdress(self, hostIP_, devID_):
        self.hostIP = hostIP_
        self.devID = devID_

    def SetLoginPrompt(self, loginPrompt_, passworddPrompt_):
        self.loginPrompt = loginPrompt_
        self.passwdPrompt = passworddPrompt_

    def SetUserNameAndPwd(self, userName_, userPSW_):
        self.userName = userName_
        self.userPassword = userPSW_

    def SetCommandLines(self, CmdLines_):
        self.cmdLines = CmdLines_

    def ConnTelnetToHost(self):
        print("{}에 접속을 시도 합니다. ".format(self.devID))
        try:
            self.connTelnet = telnetlib.Telnet(self.hostIP, 23, 3)
            self.connTelnet.set_debuglevel(1)
            return self.connTelnet
        except Exception as err:
            print("HostIP {}는 {} 발생으로 접속에 실패 했습니다.".format(self.hostIP, err))

    def LoginAndExecCommand(self, hostType_, cmdList_):
        hostType = hostType_
        cmdList = cmdList_
        try:
            if hostType == 'ANY-LAG' or hostType == 'ANY-LLS':
                self.connTelnet.read_until(b"login: ", 2)
                self.connTelnet.write(self.userName.encode('ascii') + b"\n")
                self.connTelnet.read_until(b"Password: ", 2)
                self.connTelnet.write(self.userPassword.encode('ascii') + b"\n")
                self.SendCommand(cmdList)
            elif hostType == 'ANY-LAG' or hostType == 'ANY-LLS':
                self.connTelnet.read_until(b"login: ", 2)
                self.connTelnet.write(self.userName.encode('ascii') + b"\n")
                self.connTelnet.read_until(b"Password: ",2)
                self.connTelnet.write(self.userPassword.encode('ascii') + b"\n")
                self.SendCommand(cmdList)
            else:
                self.connTelnet.read_until(b"login: ", 2)
                self.connTelnet.write(self.userName.encode('ascii') + b"\n")
                self.connTelnet.read_until(b"Password: ", 2)
                self.connTelnet.write(self.userPassword.encode('ascii') + b"\n")
                self.SendCommand(cmdList)
        except Exception as err:
            print("HostIP {}는 {} 발생으로 로그인에 실패 했습니다.".format(self.hostIP, err))


    def SendCommand(self, cmdLines_):
        cmdLines = cmdLines_
        try:
            for cmdline in cmdLines:
                time.sleep(1)
                self.connTelnet.write(cmdline.encode('ascii') + b"\n")

            lastpost_raw = self.connTelnet.read_all()
            self.connTelnet.close()
            lastpost_decode = lastpost_raw.decode("utf-8")
            strText = lastpost_decode.rstrip("\r\n")
            self.resultDictText = {self.devID : strText}
        except Exception as e:
            print("{}와 같은 에러가 발생 했습니다.".format(e))
            self.connTelnet.close()


