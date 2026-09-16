  :ls                       see both buffers
  :vs                       split the window
  Ctrl-W l                  move into the right split
  :b default                show default.json there

  In the JSON:  /ALREADY_SHIPPED Enter  yy p
                then ciw or ci" the copied key to ORDER_ALREADY_CANCELLED

  Ctrl-W h                  back to the left split
  /SHIPPED' Enter           the guard in cancel()
  V2j y                     yank the three-line if block
  }p  or  jjp               paste it below, keeping the blank line
  then change SHIPPED to CANCELLED in both places on the copy

  :wa                       write both
  :qa

  Mental model: buffers are the files, windows are the panes, and
  :b <a few letters of the name> is the fastest way between them.
