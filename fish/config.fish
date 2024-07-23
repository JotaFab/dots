
if status is-interactive
    
    zoxide init fish | source
    atuin init fish --disable-up-arrow | source
    # Commands to run in interactive sessions can go here
    starship init fish | source
    fish_add_path ~/go/bin        
    #ALIAS

    alias fzf="fzf --height 40% --layout reverse --border --tmux 70%"
    alias ls="lsd -l"
    alias l="ls -ar"
    alias lt="ls --tree"
    alias cat="bat -p"
    alias icat="kitten icat"
    alias s="kitten ssh"
    alias z="cd"
    #FUNCTIONS
    set -Ux EDITOR neovim
    function mkt
        mkdir {nmap,content,exploits,scripts}
    end
        # extractPorts allPorts
    function extractPorts
        set ports (cat $argv | grep -oP '\d{1,5}/open' | awk '{print $1}' FS='/' | xargs | tr ' ' ',')
        set ip_address (cat $argv | grep -oP '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' | sort -u | head -n 1)
        echo -e "\n[*] Extracting information...\n" > extractPorts.tmp
        echo -e "\t[*] IP Address: $ip_address"  >> extractPorts.tmp
        echo -e "\t[*] Open ports: $ports\n"  >> extractPorts.tmp
        echo $ports | tr -d '\n' | wl-copy 
        echo -e "[*] Ports copied to clipboard\n"  >> extractPorts.tmp
        cat extractPorts.tmp; rm extractPorts.tmp
    end
end

# Created by `pipx` on 2024-05-23 02:42:41
set PATH $PATH /home/jotafab/.local/bin
