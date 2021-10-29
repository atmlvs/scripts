FROM docker.io/library/archlinux:latest

RUN sed -i '1i Server = http://mirrors.aliyun.com/archlinux/$repo/os/$arch' /etc/pacman.d/mirrorlist \
    && sed -i '$i SigLevel = TrustAll' /etc/pacman.conf \
    && sed -i -r 's/^NoExtract\s*=\s*.*/# \0/g' /etc/pacman.conf \
    && pacman -Syyu --noconfirm \
    && pacman -Su --noconfirm\
    && pacman -Syy --noconfirm git vim neovim zsh oh-my-zsh-git \
    maven yay zsh python3 tmux python2 zsh-autosuggestions zsh-syntax-highlighting \
    zsh-theme-powerlevel10k ranger python-pip python-neovim wl-clipboard fzf ripgrep man-db \
    gcc clang base-devel wqy-zenhei noto-fonts-cjk wget unzip thefuck \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && pacman -Scc --noconfirm \
    && rm -rf /var/lib/pacman/sync/* /var/cache/pacman/pkg/* \
    && echo "" > /var/log/pacman.log