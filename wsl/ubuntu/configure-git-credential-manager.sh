#! env bash
# https://zenn.dev/ttani/articles/wsl2-git-credential-manager
# https://learn.microsoft.com/ja-jp/windows/wsl/tutorials/wsl-git
git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/libexec/git-core/git-credential-manager.exe"
# Azure の追加の構成
# git config --global credential.https://dev.azure.com.useHttpPath true

git config --global core.autocrlf input
