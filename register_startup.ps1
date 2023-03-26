# スタートアップ フォルダーにアプリケーションのショートカットを作成する
# https://nasunoblog.blogspot.com/2016/02/powershell-how-to-create-shortcut-in-startup-folder.html
# Current Userのスタートアップを指定したい場合は-Currentuser スイッチをつけます。
# New-StartupApp `
#     -CurrentUser `
#     -LinkName "SoftTilt" `
#     -ExeName "C:\My Program\SoftTilt\SoftTilt.exe" `
#     -IconName "C:\My Program\SoftTilt\SoftTilt.exe"

# 全ユーザーにしたい場合は-Currentuser スイッチを付けません。
# New-StartupApp `
#     -LinkName "SoftTilt" `
#     -ExeName "C:\My Program\SoftTilt\SoftTilt.exe" `
#     -IconName "C:\My Program\SoftTilt\SoftTilt.exe"
function New-StartupApp{
    param(
        [switch]$CurrentUser,

        [parameter(mandatory)]
        [string]$LinkName,

        [parameter(mandatory)]
        [string]$ExeName,

        [parameter(mandatory)]
        [string]$IconName
    )

    # スタートアップ フォルダーを指定
    $Reg = "{0}:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
    if($CurrentUser -eq $true){
        $startupPath = $(Get-ItemProperty ($Reg -f "HKCU")).startup
    }
    else{
        $StartupPath = $(Get-ItemProperty ($Reg -f "HKLM")).'common startup'
    }

    # ショートカット先をチェック
    $ShortCutPath = "{0}\$linkName.lnk" -f $StartupPath

    if((Test-Path -Path $ShortCutPath) -eq $true){
        Write-Host "$LinkName.lnk Existed." -ForegroundColor Yellow
        return
    }

    # ショートカットを作る
    $WsShell = New-Object -ComObject WScript.Shell
    $ShortCut = $WsShell.CreateShortcut($shortCutPath)
    $ShortCut.TargetPath = $exeName
    $ShortCut.IconLocation = $iconName
    $ShortCut.Save()

    Write-Host "$linkName.lnk Created." -ForegroundColor Cyan
}