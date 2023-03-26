#  使用法: winget import [-i] <import-file> [<オプション>]

# 次の引数を使用できます。
#   -i,--import-file             インストールするパッケージを記述したファイル

# 次のオプションを使用できます。
#   --ignore-unavailable         使用できないパッケージを無視する
#   --ignore-versions            インポート ファイルのパッケージ バージョンを無視する
#   --no-upgrade                 インストール済みバージョンが既に存在する場合はアップグレードをスキップします
#   --accept-package-agreements  パッケージのすべての使用許諾契約に同意する
#   --accept-source-agreements   ソース操作中にすべてのソース契約に同意する
#   -?,--help                    選択したコマンドに関するヘルプを表示
#   --wait                       終了する前に任意のキーを押すプロンプトをユーザーに表示します
#   --verbose,--verbose-logs     WinGet の詳細ログを有効にする
#   --disable-interactivity      対話型プロンプトを無効にします
# for PS v3
if( $PSVersionTable.PSVersion.Major -ge 3 ){
    Write-Output "Data from `$PSScriptRoot"
    $ScriptDir = $PSScriptRoot
}
# for PS v2
else{
    Write-Output "Data from `$MyInvocation.MyCommand.Path"
    $ScriptDir = Split-Path $MyInvocation.MyCommand.Path -Parent
}
winget import -i $ScriptDir\winget.json --ignore-unavailable  