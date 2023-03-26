import sys
import os
import datetime
import fnmatch
import pyauto
import helper
from keyhac import *


def configure(keymap):

    # --------------------------------------------------------------------
    # Text editer setting for editting config.py file

    # Setting with program file path (Simple usage)
    if 1:
        keymap.editor = helper.resolve_path(r"AppData\Local\Programs\Microsoft VS Code\Code.exe")

    # Setting with callable object (Advanced usage)
    if 0:
        def editor(path):
            shellExecute( None, helper.resolve_path(r"AppData\Local\Programs\Microsoft VS Code\Code.exe"), '"%s"'% path, "" )
        keymap.editor = editor

    # --------------------------------------------------------------------
    # Customizing the display

    # Font
    keymap.setFont( "MS Gothic", 12 )

    # Theme
    keymap.setTheme("black")




    ## IMEを切り替える
    #
    #  @param flag      切り替えフラグ（True:IME ON / False:IME OFF）
    #
    def switch_ime(flag):

        # バルーンヘルプを表示する時間(ミリ秒)
        BALLOON_TIMEOUT_MSEC = 500

        # if not flag:
        if flag:
            ime_status = 1
            message = u"[あ]"
            key ="(124)"
        else:
            ime_status = 0
            message = u"[_A]"
            key ="(125)"
        # IMEのON/OFFをセット
        # keymap.wnd.setImeStatus(ime_status)
        # IMEの状態をバルーンヘルプで表示
        keymap.popBalloon("ime_status", message, BALLOON_TIMEOUT_MSEC)
        keymap.InputKeyCommand( key )()
        return key
# --------------------------------------------------------------------
# 131 0x83	VK_F20	F20キー	[F20]
# 132 0x84	VK_F21	F21キー	[F21]
# 133 0x85	VK_F22	F22キー	[F22]
# 134 0x86	VK_F23	F23キー	[F23]
# 135 0x87	VK_F24	F24キー	[F24]
    # Simple key replacement
    # keymap.replaceKey( "LWin", 235 )
    # keymap.replaceKey( "RWin", 255 )
    if 1:   # [半角／全角]
        keymap.replaceKey( "PrintScreen", 125 )
        keymap_global = keymap.defineWindowKeymap()
        keymap_global["U-(125)"] = lambda: helper.double_key(switch_ime)  # 押す
        keymap_global["D-(125)"] = lambda: None                    # 離す

    # User modifier key definition
    keymap.defineModifier( 131, "User0" )

    # Global keymap which affects any windows
    if 1:
        keymap_global = keymap.defineWindowKeymap()
        def multi_mod(k1,k2):
            keymap_global[ "U0-"+k1 ] = k2
            keymap_global[ "U0-A-"+k1 ] = "A-" +k2
            keymap_global[ "U0-A-C-"+k1 ] = "A-C-" +k2
            keymap_global[ "U0-A-C-S-"+k1 ] = "A-C-S-" +k2
            keymap_global[ "U0-C-"+k1 ] = "C-" +k2
            keymap_global[ "U0-C-S-"+k1 ] = "C-S-" +k2
            keymap_global[ "U0-S-"+k1 ] = "S-" +k2

        multi_mod("1" , "F1")
        multi_mod("2" , "F2")
        multi_mod("3" , "F3")
        multi_mod("4" , "F4")
        multi_mod("5" , "F5")
        multi_mod("6" , "F6")
        multi_mod("7" , "F7")
        multi_mod("8" , "F8")
        multi_mod("9" , "F9")
        multi_mod("0" , "F10")
        multi_mod("Minus" , "F11")
        multi_mod("Plus" , "F12")

        multi_mod("K" , "Up")                  # Move cursor up
        multi_mod("J" , "Down")                # Move cursor down
        multi_mod("L" , "Right")               # Move cursor right
        multi_mod("H" , "Left")                # Move cursor left

        multi_mod("Comma" , "PageUp")                # Move to beginning of line
        multi_mod("Period" , "PageDown")                 # Move to end of line
        
        multi_mod("A" , "Home")                # Move to beginning of line
        multi_mod("E" , "End")                 # Move to end of line

    if 0:
        keymap_global = keymap.defineWindowKeymap()

        # USER0-Up/Down/Left/Right : Move active window by 10 pixel unit
        keymap_global[ "U0-Left"  ] = keymap.MoveWindowCommand( -10, 0 )
        keymap_global[ "U0-Right" ] = keymap.MoveWindowCommand( +10, 0 )
        keymap_global[ "U0-Up"    ] = keymap.MoveWindowCommand( 0, -10 )
        keymap_global[ "U0-Down"  ] = keymap.MoveWindowCommand( 0, +10 )

        # USER0-Shift-Up/Down/Left/Right : Move active window by 1 pixel unit
        keymap_global[ "U0-S-Left"  ] = keymap.MoveWindowCommand( -1, 0 )
        keymap_global[ "U0-S-Right" ] = keymap.MoveWindowCommand( +1, 0 )
        keymap_global[ "U0-S-Up"    ] = keymap.MoveWindowCommand( 0, -1 )
        keymap_global[ "U0-S-Down"  ] = keymap.MoveWindowCommand( 0, +1 )

        # USER0-Ctrl-Up/Down/Left/Right : Move active window to screen edges
        keymap_global[ "U0-C-Left"  ] = keymap.MoveWindowToMonitorEdgeCommand(0)
        keymap_global[ "U0-C-Right" ] = keymap.MoveWindowToMonitorEdgeCommand(2)
        keymap_global[ "U0-C-Up"    ] = keymap.MoveWindowToMonitorEdgeCommand(1)
        keymap_global[ "U0-C-Down"  ] = keymap.MoveWindowToMonitorEdgeCommand(3)

        # Clipboard history related
        keymap_global[ "C-S-Z"   ] = keymap.command_ClipboardList     # Open the clipboard history list
        keymap_global[ "C-S-X"   ] = keymap.command_ClipboardRotate   # Move the most recent history to tail
        keymap_global[ "C-S-A-X" ] = keymap.command_ClipboardRemove   # Remove the most recent history
        keymap.quote_mark = "> "                                      # Mark for quote pasting

        # Keyboard macro
        keymap_global[ "U0-0" ] = keymap.command_RecordToggle
        keymap_global[ "U0-1" ] = keymap.command_RecordStart
        keymap_global[ "U0-2" ] = keymap.command_RecordStop
        keymap_global[ "U0-3" ] = keymap.command_RecordPlay
        keymap_global[ "U0-4" ] = keymap.command_RecordClear
    if 1:

        # キーストロークの入力
        def send_keys(*keys):
            keymap.beginInput()
            for key in keys:
                keymap.setInput_FromString(str(key))
            keymap.endInput()
            keymap._fixFunnyModifierState()

        # 文字列の入力
        def send_string(s):
            keymap.beginInput()
            keymap.setInput_Modifier(0)
            for c in s:
                keymap.input_seq.append(pyauto.Char(c))
            keymap.endInput()

        # 上記2つを組み合わせる
        def send_input(sequence, sleep=0.01):
            for elem in sequence:
                delay(sleep)
                try:
                    send_keys(elem)
                except:
                    send_string(elem)

        # 有効なパスのファイルもしくは URL の実行
        def execute_path(s, arg=None):
            if s:
                if s.startswith("http") or helper.to_local_path(s):
                    keymap.ShellExecuteCommand(None, s, arg, None)()


        # クロージャ生成
        def pseudo_cuteExec(exe_name, class_name, exe_path):
            def _executer():
                found_wnd = helper.find_window(exe_name, class_name)
                if not found_wnd:
                    execute_path(exe_path)
                else:
                    if found_wnd != keymap.getWindow():
                        if helper.activate_window(found_wnd):
                            return None
                    send_keys("LCtrl-LAlt-Tab")
            return _executer
        for key, params in {
                "Win-A-C": (
                    "slack.exe",
                    "Chrome_WidgetWin_1",
                     helper.resolve_path(r"AppData\Local\slack\slack.exe")
                ),
                "Win-A-F": (
                    "vivaldi.exe",
                    "Chrome_WidgetWin_1",
                     helper.resolve_path(r"AppData\Local\Vivaldi\Application\vivaldi.exe")
                ),
                "Win-A-B": (
                    "Biscuit.exe",
                    "Chrome_WidgetWin_1",
                     helper.resolve_path(r"AppData\Local\Programs\biscuit\Biscuit.exe")
                ),
                "Win-A-A": (
                    "Code.exe",
                    "Chrome_WidgetWin_1",
                     helper.resolve_path(r"AppData\Local\Programs\Microsoft VS Code\Code.exe")
                ),
                "Win-A-G": (
                    "gitkraken.exe",
                    "Chrome_WidgetWin_1",
                     helper.resolve_path(r"AppData\Local\gitkraken\gitkraken.exe")
                ),
                "Win-A-D": (
                    "datagrip64.exe",
                    "SunAwtFrame",
                     helper.resolve_path(r"AppData\Local\JetBrains\Toolbox\apps\datagrip\ch-0\222.4345.5\bin\datagrip64.exe")
                ),
                "Win-A-E": (
                    "EXCEL.EXE",
                    "XLMAIN",
                    None
                ),
            }.items():
                keymap_global[key] = pseudo_cuteExec(*params)
    # USER0-F1 : Test of launching application
    if 0:
        keymap_global[ "U0-F1" ] = keymap.ShellExecuteCommand( None, helper.resolve_path(r"AppData\Local\Programs\Microsoft VS Code\Code.exe"), "", "" )


    # USER0-F2 : Test of sub thread execution using JobQueue/JobItem
    if 0:
        def command_JobTest():

            def jobTest(job_item):
                shellExecute( None, helper.resolve_path(r"AppData\Local\Programs\Microsoft VS Code\Code.exe"), "", "" )

            def jobTestFinished(job_item):
                print( "Done." )

            job_item = JobItem( jobTest, jobTestFinished )
            JobQueue.defaultQueue().enqueue(job_item)

        keymap_global[ "U0-F2" ] = command_JobTest


    # Test of Cron (periodic sub thread procedure)
    if 0:
        def cronPing(cron_item):
            os.system( "ping -n 3 www.google.com" )

        cron_item = CronItem( cronPing, 3.0 )
        CronTable.defaultCronTable().add(cron_item)


    # USER0-F : Activation of specific window
    if 0:
        keymap_global[ "U0-F" ] = keymap.ActivateWindowCommand( "cfiler.exe", "CfilerWindowClass" )


    # USER0-E : Activate specific window or launch application if the window doesn't exist
    if 0:
        def command_ActivateOrExecuteNotepad():
            wnd = Window.find( "Notepad", None )
            if wnd:
                if wnd.isMinimized():
                    wnd.restore()
                wnd = wnd.getLastActivePopup()
                wnd.setForeground()
            else:
                executeFunc = keymap.ShellExecuteCommand( None, r"C:\Users\TomotakaMiyagawa\AppData\Local\Programs\Microsoft VS Code\Code.exe", "", "" )
                executeFunc()

        keymap_global[ "U0-E" ] = command_ActivateOrExecuteNotepad


    # Ctrl-Tab : Switching between console related windows
    if 0:

        def isConsoleWindow(wnd):
            if wnd.getClassName() in ("PuTTY","MinTTY","CkwWindowClass"):
                return True
            return False

        keymap_console = keymap.defineWindowKeymap( check_func=isConsoleWindow )

        def command_SwitchConsole():

            root = pyauto.Window.getDesktop()
            last_console = None

            wnd = root.getFirstChild()
            while wnd:
                if isConsoleWindow(wnd):
                    last_console = wnd
                wnd = wnd.getNext()

            if last_console:
                last_console.setForeground()

        keymap_console[ "C-TAB" ] = command_SwitchConsole


    # USER0-Space : Application launcher using custom list window
    if 0:
        def command_PopApplicationList():

            # If the list window is already opened, just close it
            if keymap.isListWindowOpened():
                keymap.cancelListWindow()
                return

            def popApplicationList():

                applications = [
                    ( "Notepad", keymap.ShellExecuteCommand( None, r"C:\Users\TomotakaMiyagawa\AppData\Local\Programs\Microsoft VS Code\Code.exe", "", "" ) ),
                    ( "Paint", keymap.ShellExecuteCommand( None, "mspaint.exe", "", "" ) ),
                ]

                websites = [
                    ( "Google", keymap.ShellExecuteCommand( None, "https://www.google.co.jp/", "", "" ) ),
                    ( "Facebook", keymap.ShellExecuteCommand( None, "https://www.facebook.com/", "", "" ) ),
                    ( "Twitter", keymap.ShellExecuteCommand( None, "https://twitter.com/", "", "" ) ),
                ]

                listers = [
                    ( "App",     cblister_FixedPhrase(applications) ),
                    ( "WebSite", cblister_FixedPhrase(websites) ),
                ]

                item, mod = keymap.popListWindow(listers)

                if item:
                    item[1]()

            # Because the blocking procedure cannot be executed in the key-hook,
            # delayed-execute the procedure by delayedCall().
            keymap.delayedCall( popApplicationList, 0 )

        keymap_global[ "U0-Space" ] = command_PopApplicationList


    # USER0-Alt-Up/Down/Left/Right/Space/PageUp/PageDown : Virtul mouse operation by keyboard
    if 0:
        keymap_global[ "U0-A-Left"  ] = keymap.MouseMoveCommand(-10,0)
        keymap_global[ "U0-A-Right" ] = keymap.MouseMoveCommand(10,0)
        keymap_global[ "U0-A-Up"    ] = keymap.MouseMoveCommand(0,-10)
        keymap_global[ "U0-A-Down"  ] = keymap.MouseMoveCommand(0,10)
        keymap_global[ "D-U0-A-Space" ] = keymap.MouseButtonDownCommand('left')
        keymap_global[ "U-U0-A-Space" ] = keymap.MouseButtonUpCommand('left')
        keymap_global[ "U0-A-PageUp" ] = keymap.MouseWheelCommand(1.0)
        keymap_global[ "U0-A-PageDown" ] = keymap.MouseWheelCommand(-1.0)
        keymap_global[ "U0-A-Home" ] = keymap.MouseHorizontalWheelCommand(-1.0)
        keymap_global[ "U0-A-End" ] = keymap.MouseHorizontalWheelCommand(1.0)


    # Execute the System commands by sendMessage
    if 0:
        def close():
            wnd = keymap.getTopLevelWindow()
            wnd.sendMessage( WM_SYSCOMMAND, SC_CLOSE )

        def screenSaver():
            wnd = keymap.getTopLevelWindow()
            wnd.sendMessage( WM_SYSCOMMAND, SC_SCREENSAVE )

        keymap_global[ "U0-C" ] = close              # Close the window
        keymap_global[ "U0-S" ] = screenSaver        # Start the screen-saver


    # Test of text input
    if 0:
        keymap_global[ "U0-H" ] = keymap.InputTextCommand( "Hello / こんにちは" )


    # For Edit box, assigning Delete to C-D, etc
    if 0:
        keymap_edit = keymap.defineWindowKeymap( class_name="Edit" )

        keymap_edit[ "C-D" ] = "Delete"              # Delete
        keymap_edit[ "C-H" ] = "Back"                # Backspace
        keymap_edit[ "C-K" ] = "S-End","C-X"         # Removing following text


    # Customize Notepad as Emacs-ish
    # Because the keymap condition of keymap_edit overlaps with keymap_notepad,
    # both these two keymaps are applied in mixed manner.
    if 1:
        keymap_notepad = keymap.defineWindowKeymap( exe_name=r"C:\Users\TomotakaMiyagawa\AppData\Local\Programs\Microsoft VS Code\Code.exe", class_name="Edit" )

        # Define Ctrl-X as the first key of multi-stroke keys
        # keymap_notepad[ "C-X" ] = keymap.defineMultiStrokeKeymap("C-X")

        keymap_notepad[ "C-P" ] = "Up"                  # Move cursor up
        keymap_notepad[ "C-N" ] = "Down"                # Move cursor down
        keymap_notepad[ "C-F" ] = "Right"               # Move cursor right
        keymap_notepad[ "C-B" ] = "Left"                # Move cursor left
        keymap_notepad[ "C-A" ] = "Home"                # Move to beginning of line
        keymap_notepad[ "C-E" ] = "End"                 # Move to end of line
        keymap_notepad[ "A-F" ] = "C-Right"             # Word right
        keymap_notepad[ "A-B" ] = "C-Left"              # Word left
        keymap_notepad[ "C-V" ] = "PageDown"            # Page down
        keymap_notepad[ "A-V" ] = "PageUp"              # page up
        keymap_notepad[ "A-Comma" ] = "C-Home"          # Beginning of the document
        keymap_notepad[ "A-Period" ] = "C-End"          # End of the document
        # keymap_notepad[ "C-X" ][ "C-F" ] = "C-O"        # Open file
        # keymap_notepad[ "C-X" ][ "C-S" ] = "C-S"        # Save
        # keymap_notepad[ "C-X" ][ "C-W" ] = "A-F","A-A"  # Save as
        # keymap_notepad[ "C-X" ][ "U" ] = "C-Z"          # Undo
        # keymap_notepad[ "C-S" ] = "C-F"                 # Search
        # keymap_notepad[ "A-X" ] = "C-G"                 # Jump to specified line number
        # keymap_notepad[ "C-X" ][ "H" ] = "C-A"          # Select all
        # keymap_notepad[ "C-W" ] = "C-X"                 # Cut
        # keymap_notepad[ "A-W" ] = "C-C"                 # Copy
        # keymap_notepad[ "C-Y" ] = "C-V"                 # Paste
        # keymap_notepad[ "C-X" ][ "C-C" ] = "A-F4"       # Exit


    # Customizing clipboard history list
    if 0:
        # Enable clipboard monitoring hook (Default:Enabled)
        keymap.clipboard_history.enableHook(True)

        # Maximum number of clipboard history (Default:1000)
        keymap.clipboard_history.maxnum = 1000

        # Total maximum size of clipboard history (Default:10MB)
        keymap.clipboard_history.quota = 10*1024*1024

        # Fixed phrases
        fixed_items = [
            ( "name@server.net",     "name@server.net" ),
            ( "Address",             "San Francisco, CA 94128" ),
            ( "Phone number",        "03-4567-8901" ),
        ]

        # Return formatted date-time string
        def dateAndTime(fmt):
            def _dateAndTime():
                return datetime.datetime.now().strftime(fmt)
            return _dateAndTime

        # Date-time
        datetime_items = [
            ( "YYYY/MM/DD HH:MM:SS",   dateAndTime("%Y/%m/%d %H:%M:%S") ),
            ( "YYYY/MM/DD",            dateAndTime("%Y/%m/%d") ),
            ( "HH:MM:SS",              dateAndTime("%H:%M:%S") ),
            ( "YYYYMMDD_HHMMSS",       dateAndTime("%Y%m%d_%H%M%S") ),
            ( "YYYYMMDD",              dateAndTime("%Y%m%d") ),
            ( "HHMMSS",                dateAndTime("%H%M%S") ),
        ]

        # Add quote mark to current clipboard contents
        def quoteClipboardText():
            s = getClipboardText()
            lines = s.splitlines(True)
            s = ""
            for line in lines:
                s += keymap.quote_mark + line
            return s

        # Indent current clipboard contents
        def indentClipboardText():
            s = getClipboardText()
            lines = s.splitlines(True)
            s = ""
            for line in lines:
                if line.lstrip():
                    line = " " * 4 + line
                s += line
            return s

        # Unindent current clipboard contents
        def unindentClipboardText():
            s = getClipboardText()
            lines = s.splitlines(True)
            s = ""
            for line in lines:
                for i in range(4+1):
                    if i>=len(line) : break
                    if line[i]=='\t':
                        i+=1
                        break
                    if line[i]!=' ':
                        break
                s += line[i:]
            return s

        full_width_chars = "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！”＃＄％＆’（）＊＋，−．／：；＜＝＞？＠［￥］＾＿‘｛｜｝～０１２３４５６７８９　"
        half_width_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}～0123456789 "

        # Convert to half-with characters
        def toHalfWidthClipboardText():
            s = getClipboardText()
            s = s.translate(str.maketrans(full_width_chars,half_width_chars))
            return s

        # Convert to full-with characters
        def toFullWidthClipboardText():
            s = getClipboardText()
            s = s.translate(str.maketrans(half_width_chars,full_width_chars))
            return s

        # Save the clipboard contents as a file in Desktop directory
        def command_SaveClipboardToDesktop():

            text = getClipboardText()
            if not text: return

            # Convert to utf-8 / CR-LF
            utf8_bom = b"\xEF\xBB\xBF"
            text = text.replace("\r\n","\n")
            text = text.replace("\r","\n")
            text = text.replace("\n","\r\n")
            text = text.encode( encoding="utf-8" )

            # Save in Desktop directory
            fullpath = os.path.join( getDesktopPath(), datetime.datetime.now().strftime("clip_%Y%m%d_%H%M%S.txt") )
            fd = open( fullpath, "wb" )
            fd.write(utf8_bom)
            fd.write(text)
            fd.close()

            # Open by the text editor
            keymap.editTextFile(fullpath)

        # Menu item list
        other_items = [
            ( "Quote clipboard",            quoteClipboardText ),
            ( "Indent clipboard",           indentClipboardText ),
            ( "Unindent clipboard",         unindentClipboardText ),
            ( "",                           None ),
            ( "To Half-Width",              toHalfWidthClipboardText ),
            ( "To Full-Width",              toFullWidthClipboardText ),
            ( "",                           None ),
            ( "Save clipboard to Desktop",  command_SaveClipboardToDesktop ),
            ( "",                           None ),
            ( "Edit config.py",             keymap.command_EditConfig ),
            ( "Reload config.py",           keymap.command_ReloadConfig ),
        ]

        # Clipboard history list extensions
        keymap.cblisters += [
            ( "Fixed phrase", cblister_FixedPhrase(fixed_items) ),
            ( "Date-time", cblister_FixedPhrase(datetime_items) ),
            ( "Others", cblister_FixedPhrase(other_items) ),
        ]

