let s:pyscript = expand('<sfile>:p:h:h') . '/static/mkdpreview.py'

function! s:update_preview()
  call http#post('http://localhost:8081/', {
  \ "data" : join(getline(1, line('$')), "\n")
  \})
endfunction

function! s:mkdpreview(bang)
  if a:bang == '!'
    if has('win32') || has('win64')
      silent exe "!start pythonw ".shellescape(s:pyscript)
    else
      call system(printf("%s & 2>&1 /dev/null", s:pyscript))
    endif
    if v:shell_error != 0 && ((has('win32') || has('win64')) && v:shell_error != 52)
      echohl ErrorMsg | echomsg "fail to start 'mkdpreview.py'" | echohl None
      return
    endif
    augroup MkdPreview
      autocmd!
      autocmd BufWritePost <buffer> call <SID>update_preview()
    augroup END
  endif
  call s:update_preview()
endfunction

command! -bang MkdPreview call <SID>mkdpreview('<bang>')
