let s:pyscript = expand('<sfile>:p:h:h') . '/static/mkdpreview.py'

function! s:update_preview()
  let ret = webapi#http#post('http://localhost:8081/', {
  \ "data" : join(getline(1, line('$')), "\n"),
  \ "type" : &filetype
  \})
  echo ret.content
endfunction

function! s:mkdpreview(bang)
  if a:bang == '!'
    if has('win32') || has('win64')
      if exists('g:mkdpreview_python_path')
        silent exe printf("!start %s %s",
        \ shellescape(g:mkdpreview_python_path),
        \ shellescape(s:pyscript))
      else
        silent exe "!start pythonw ".shellescape(s:pyscript)
      endif
    else
      if exists('g:mkdpreview_python_path')
        call system(printf("%s %s & 2>&1 /dev/null",
        \ shellescape(g:mkdpreview_python_path),
        \ shellescape(s:pyscript)))
      else
        call system(printf("%s & 2>&1 /dev/null", shellescape(s:pyscript)))
      endif
    endif
    sleep 1
    " FIXME: On MacOSX system() above return v:shell_error 7.
    "if v:shell_error != 0 && ((has('win32') || has('win64')) && v:shell_error != 52)
    "  echohl ErrorMsg | echomsg "fail to start 'mkdpreview.py'" | echohl None
    "  return
    "endif
    augroup MkdPreview
      autocmd!
      autocmd BufWritePost <buffer> call <SID>update_preview()
    augroup END
  endif
  call s:update_preview()
endfunction

command! -bang MkdPreview call <SID>mkdpreview('<bang>')
