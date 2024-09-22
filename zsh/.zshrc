HISTFILE=~/.config/zsh/.histfile
HISTSIZE=5000
SAVEHIST=100000
setopt autocd extendedglob
unsetopt beep
bindkey -v

alias ls="lsd"
alias la="ls -lA"
alias l="ls -l"
alias lr="ls -lRs"
alias cat="bat"
# Configure the prompt with embedded Solarized color codes
eval "$(starship init zsh)"
