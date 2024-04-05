if status is-interactive
    # Commands to run in interactive sessions can go here
    starship init fish | source
    fish_add_path ~/go/bin        

    #ALIAS
    alias ls="lsd"
    alias l="ls -la"
    alias lt="l --tree"
    alias cat="bat -p"


    #FUNCTIONS
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
        echo $ports | tr -d '\n' | fish_clipboard
        echo -e "[*] Ports copied to clipboard\n"  >> extractPorts.tmp
        cat extractPorts.tmp; rm extractPorts.tmp
    end
end
