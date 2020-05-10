"plugin install
call plug#begin()

    Plug 'frazrepo/vim-rainbow' " rainbow bracket

    Plug 'preservim/nerdcommenter' " easier commenting

    Plug 'preservim/nerdtree' " better file manager

    Plug 'junegunn/fzf', { 'do': './install --bin' }

    Plug 'junegunn/fzf.vim' " fuzzy search

    Plug 'mileszs/ack.vim'

    Plug 'dense-analysis/ale' " Linting

    Plug 'sainnhe/sonokai' " theme colour

    Plug 'tpope/vim-surround' " surround functionaliy IE cs\"' to change \" to '

    Plug 'ervandew/supertab' " tab completion

    Plug 'vimwiki/vimwiki' " markdown in vim

call plug#end()

" fix opacity for vim in alacritty

hi! Normal ctermbg=NONE guibg=NONE
hi! NonText ctermbg=NONE guibg=NONE guifg=NONE ctermfg=NONE

" required for vimwiki
" others are already enabled below
" filetype plugin on, syntax on
set nocompatible
set background=dark
set t_Co=256

let wiki_1 = {}
let wiki_1.path = '~/vimwiki/'
let wiki_1.syntax = 'markdown'
let wiki_1.ext = '.md'

let g:vimwiki_list = [wiki_1]
let g:vimwiki_ext2syntax = {'.md': 'markdown', '.markdown': 'markdown', '.mdown': 'markdown'}

au BufRead,BufNewFile *.ms,*.me,*.mom,*.man set filetype=groff
au BufWrite *.ms,*.me,*.man :silent !groff -ms -T pdf % > %:r.pdf 
"au BufWrite *.mom :silent !pdfmom % > %:r.pdf 
filetype plugin on " allows nerdcommenter to work
let g:ale_sign_column_always = 1
let g:ale_linters={ 'python': ['pylint', 'flake8'], }
let g:ale_fixers={'*' : [], 'python' : ['autopep8'] }
let g:ackprg = 'ag --vimgrep' " use ag with ack

let g:SuperTabDefaultCompletionType = "<c-n>" " done for proper tab completion

syntax enable           " enable syntax processing
" the configuration options should be placed before `colorscheme sonokai`
let g:sonokai_style = 'andromeda'
let g:sonokai_enable_italic = 1
let g:sonokai_disable_italic_comment = 1
colorscheme sonokai

" remember code folds
autocmd BufWinLeave *.* mkview
autocmd BufWinEnter *.* silent loadview
" numbering on side
set number
set relativenumber
set wildmenu
" Always show the status line
set laststatus=2

" " Format the status line
set statusline=\ %F%m%r%h\ %w\ \ CWD:\ %r%{getcwd()}%h\ \ \Line:\ %l\ \ Column:\ %c

"commands for python formatting
set shiftwidth=4  " operation >> indents 4 columns; << unindents 4 columns
set tabstop=4     " a hard TAB displays as 4 columns
set expandtab     " insert spaces when hitting TABs
set softtabstop=4 " insert/delete 4 spaces when hitting a TAB/BACKSPACE
set shiftround    " round indent to multiple of 'shiftwidth'
set autoindent    " align the new line indent with the previous line
syntax on         " turns on syntax highlighting
set history=500   " How far you can undo

set autoread      " If file is changed from outside vim update
let mapleader = ","
" fast saving
nmap <leader>w :w<cr>

" :W sudo saves the file
command! W execute 'w !sudo tee % > /dev/null' <bar> edit!

" A buffer becomes hidden when it is abandoned
set hid

" Configure backspace so it acts as it should act
set backspace=eol,start,indent
set whichwrap+=<,>,h,l

" Ignore case when searching
set ignorecase

" When searching try to be smart about cases
set smartcase

" Highlight search results
set hlsearch

" Makes search act like search in modern browsers
set incsearch

" Don't redraw while executing macros (good performance config)
set lazyredraw

" For regular expressions turn magic on
set magic

" Show matching brackets when text indicator is over them
set showmatch
" How many tenths of a second to blink when matching brackets
set mat=2

" No annoying sound on errors
set noerrorbells
set novisualbell
set t_vb=
set tm=500

set encoding=utf8

" Turn backup off
set nobackup
set nowb
set noswapfile


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" REMAPPNGS                                                    "
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" easier navigation
map <C-j> <C-W>j
map <C-k> <C-W>k
map <C-h> <C-W>h
map <C-l> <C-W>l

" NerdTree Toggle
map <leader>F :NERDTreeToggle<CR>

"split resizing
nnoremap <silent> <Leader>+ :exe "resize " . (winheight(0) * 3/2)<CR>
nnoremap <silent> <Leader>- :exe "resize " . (winheight(0) * 2/3)<CR>
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Helper functions
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" Delete trailing white space on save, useful for some filetypes ;)
fun! CleanExtraSpaces()
    let save_cursor = getpos(".")
    let old_query = getreg('/')
    silent! %s/\s\+$//e
    call setpos('.', save_cursor)
    call setreg('/', old_query)
endfun


autocmd BufWritePre *.txt,*.js,*.py,*.wiki,*.sh,*.coffee :call CleanExtraSpaces()
