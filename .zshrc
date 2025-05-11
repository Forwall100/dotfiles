autoload -Uz compinit promptinit
compinit
promptinit
zstyle ':completion:*' menu select

# Включаем ctrl + left/right
bindkey "^[[1;5C" forward-word
bindkey "^[[1;5D" backward-word

# Эта настройка установит тему walters для приглашения командной строки
prompt redhat

alias wd='wg-quick down /etc/wireguard/pcun.conf'
alias wu='wg-quick up /etc/wireguard/pcun.conf'
alias sshs='ssh user@89.31.117.60 -p 2222'
alias oserve='nohup ollama serve > ollama.log 2>&1 &'
alias yays='yay --noconfirm'

export OLLAMA_HOST="192.168.31.62"
export OPENROUTER_API_KEY="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"
export OPENAI_API_KEY="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"

# Created by `pipx` on 2025-02-04 10:20:23
export PATH="$PATH:/home/user/.local/bin"
export TERM=xterm-256color
export LANG=en_US.UTF-8
