These scripts’ purpose is to help you navigate your workspaces
regardless of `desktop environment` or `window manager`.

They require `xdotool` and `wmctrl` in order to work.
If you don't have these packages, you can install them using
your distro’s package manager.

## Installation:

### Debian
```
sudo apt-get install wmctrl xdotool
```
### Arch Linux
```
sudo pacman -S wmctrl xdotool
```

## Usage:
```
./desktop.sh -p # move to previous workspace
./desktop.sh -n # move to next workspace
./window.sh -l # tile window to left side of the screen
./window.sh -r # tile window to right side of the screen
./window.sh -M # maximize window
./window.sh -m # restore window
./window.sh -f # toggle fullscreen
./window.sh -s n # send active window to workspace number "n"
```
In order to use these scripts, you'll probably want to set
them to specific keybindings. Also, you should use the full
path to the files, or move/copy/symlink them to any folder in
your `PATH`.

---------

O propósito destes scripts é ajudar o usuário por diferentes
espaços de trabalho independente de `ambiente de desktop` ou de
`gerenciador de janelas`.

Para que funcionem, você precisa ter os pacotes `xdotool` e
`wmctrl`. Você pode instalar ambos usando o gerenciador de
pacotes da sua distro.
## Instalação:

### Debian
```
sudo apt-get install wmctrl xdotool
```
### Arch Linux
```
sudo pacman -S wmctrl xdotool
```

## Uso:
```
./desktop.sh -p # mover para o espaço de trabalho anterior
./desktop.sh -n # mover para o espaço de trabalho seguinte
./window.sh -l # alinhar a janela ao lado esquerdo da tela
./window.sh -r # alinhar a janela ao lado direito da tela
./window.sh -M # maximizar janela
./window.sh -m # restaurar janela
./window.sh -f # adicionar/remover janela cheia
./window.sh -s n # enviar janela ativa ao espaço de trabalho "n"
```
Para usar esses scripts, é recomendável executá-los através de
atalhos de teclado. Para executar os comandos, você deve usar o
caminho completo dos scripts, ou mover/copiar/linkar para
qualquer pasta listada no `PATH`.
