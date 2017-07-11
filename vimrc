"
" Cheatsheet of VIM commands/shortcuts
" http://www.worldtimzone.com/res/vi.html
"
" Notes -
" - to re-indent all code in vim enter gg=G in normal mode
"

" Basics "
syntax on
set number "line numbers
set ts=4 "tabs = 4 spaces
set expandtab "expand tabs into spaces
set showmatch "highlight matching brackets
set cursorline "underline cursor line
set mouse=a "allow mause actions
set smarttab
set shiftwidth=4
let python_highlight_all=1
set backspace=indent,eol,start

" Vundle stuff "
set nocompatible              " be iMproved, required
filetype off                  " required

set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

call vundle#end()            " required
filetype plugin indent on    " required


" Plugins "

Plugin 'joshdick/onedark.vim'
Plugin 'sheerun/vim-polyglot'
Plugin 'scrooloose/nerdtree'
Plugin 'kien/ctrlp.vim'
Plugin 'ervandew/supertab'

" Colors "

if (empty($TMUX))
    if (has("nvim"))
        let $NVIM_TUI_ENABLE_TRUE_COLOR=1
    endif
    if (has("termguicolors"))
        set termguicolors
    endif
endif

colorscheme onedark

" Strip trailing whitespaces from lines when :q is called "
autocmd BufWritePre * %s/\s\+$//e

" Remove background color and cursorline highlighting"
hi Normal guibg=NONE ctermbg=NONE
hi CursorLine cterm=NONE ctermbg=NONE ctermfg=NONE

