# configure-windows
Windows開発環境構築メモ

## Tools
- [keyhac](https://sites.google.com/site/craftware/keyhac-ja)
- [executor](https://executor.dk)
- [chgkey](https://forest.watch.impress.co.jp/library/software/changekey/)

## Wsl
### Wsl Env
[Windows および Linux ファイル システム間での作業](https://learn.microsoft.com/ja-jp/windows/wsl/filesystems)

```
$env:WSLENV="USERPROFILE/pu:DISPLAY"
```
### 1password
[SSH client compatibility](https://developer.1password.com/docs/ssh/agent/compatibility/)
[1Passwordのssh-agent機能をWSL2でも利用する](https://qiita.com/mfunaki/items/db6e1ffcf1e6f1eff252)
wingetで入れたnpiperelayは以下に置かれる

"$USERPROFILE/AppData/Local/Microsoft/WinGet/Packages/jstarks.npiperelay_Microsoft.Winget.Source_8wekyb3d8bbwe/npiperelay.exe"

./.bash_profileや~/.bashrc
```bash
export SSH_AUTH_SOCK=$HOME/.ssh/agent.sock
socat UNIX-LISTEN:$SSH_AUTH_SOCK,fork EXEC:"npiperelay.exe -ei -s //./pipe/openssh-ssh-agent",nofork &

# Configure ssh forwarding
export SSH_AUTH_SOCK=$HOME/.ssh/agent.sock
# need `ps -ww` to get non-truncated command for matching
# use square brackets to generate a regex match for the process we want but that doesn't match the grep command running it!
ALREADY_RUNNING=$(ps -auxww | grep -q "[n]piperelay.exe -ei -s //./pipe/openssh-ssh-agent"; echo $?)
if [[ $ALREADY_RUNNING != "0" ]]; then
    if [[ -S $SSH_AUTH_SOCK ]]; then
        # not expecting the socket to exist as the forwarding command isn't running (http://www.tldp.org/LDP/abs/html/fto.html)
        echo "removing previous socket..."
        rm $SSH_AUTH_SOCK
    fi
    echo "Starting SSH-Agent relay..."
    # setsid to force new session to keep running
    # set socat to listen on $SSH_AUTH_SOCK and forward to npiperelay which then forwards to openssh-ssh-agent on windows
    (setsid socat UNIX-LISTEN:$SSH_AUTH_SOCK,fork EXEC:"npiperelay.exe -ei -s //./pipe/openssh-ssh-agent",nofork &) >/dev/null 2>&1
fi
```
### dotfiles

```
bash -c "$(curl -fsSL https://raw.githubusercontent.com/{your account name}/dotfiles/main/install.sh)"
```