  :vimgrep /pattern/ **/*.ts     search the repo, fill the quickfix list
  :vimgrep /\<Foo\>/ **/*.ts     whole word only
  :copen  :cclose                open / close the results window
  :cn  :cp                       next / previous result
  :cfirst  :clast                jump to the first / last one
  :cdo s/old/new/g | update      run a substitution on EVERY result
                                 and save each file  - the big gun

  In the :copen window, Enter opens the result under the cursor.

  If you install ripgrep later:
      :set grepprg=rg\ --vimgrep
      :grep Foo          same quickfix list, much faster on big repos
