from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QTextEdit
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from platforms.echo import EchoChatClient, Message
from platforms.gistcomments import GistCommentChatClient, Message

# # TODO:
# 1) clean up a bit actually looks pretty good
# 2) add a menu item for deleting your previous messages and another for deleting the room/gist

# shift to messaging menu should have
class ChatWidget(QWidget):

    def __init__(self, parent=None, platform=None, email=None, password=None, target=None, cipherType=None, cipherPass=None, credentials=None):

        super(ChatWidget, self).__init__(parent)
        self.platform = platform
        self.chatclient = None

        if platform == 'echo':
            print('setting echo chat client')
            # this is pretty clever pass in the gui callback to whichever library
            # callback we need to use for message receipt gj me
            self.chatclient = EchoChatClient(msgReceivedCallback=self.messageReceived,
                cipherType=cipherType, cipherPass=cipherPass)

        elif platform == 'gist':
            print('setting gist chat client')
            gist_id = credentials.get('gist_id', None)
            oauth_token = credentials.get('oauth_token', None)

            self.chatclient = GistCommentChatClient(msgReceivedCallback=self.messageReceived,
                cipherType=cipherType, cipherPass=cipherPass, oauth_token=oauth_token, gist_id=gist_id)

        self.setStatusTip(platform)
        self.initUI()


    def initUI(self):
        layout = QGridLayout()

        self.chatHistory = QTextEdit()
        self.chatInput = QLineEdit()
        self.chatHistory.setReadOnly(True)
        self.chatHistory.setLineWrapMode(QTextEdit.NoWrap)

        layout.addWidget(self.chatHistory, 1, 0)
        layout.addWidget(self.chatInput, 2, 0)

        self.setLayout(layout)

    # for sending messages
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.chatclient.sendMessage(self.chatInput.text())
            self.chatHistory.moveCursor(QtGui.QTextCursor.End)
            self.chatInput.clear()
            event.accept()
        else:
            event.ignore()

    def messageReceived(self, msg):
        self.chatHistory.insertPlainText("{}: {}\n".format(msg.sender, msg.text))
