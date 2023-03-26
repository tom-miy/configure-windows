# 使用法: winget export [-o] <output> [<オプション>]


# 次のオプションを使用できます。
# インストールされているパッケージの一覧をファイルに書き込みます。その後、パッケージを import コマンドを使用してインストールできます。

# 使用法: winget export [-o] <output> [<オプション>]

# 次の引数を使用できます。
#   -o,--output                 結果が書き込まれるファイル

# 次のオプションを使用できます。
#   -s,--source                 指定したソースからパッケージをエクスポートする
#   --include-versions          作成されたファイルにパッケージ バージョンを含める
#   --accept-source-agreements  ソース操作中にすべてのソース契約に同意する
#   -?,--help                   選択したコマンドに関するヘルプを表示
#   --wait                      終了する前に任意のキーを押すプロンプトをユーザーに表示します
#   --verbose,--verbose-logs    WinGet の詳細ログを有効にする
#   --disable-interactivity     対話型プロンプトを無効にします
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
winget export -o winget.original.json -s winget