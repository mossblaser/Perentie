#!/usr/bin/env python

"""
Debugger GUI main executable.
"""

import sys
import gtk

from view.target_selection import TargetSelection

if __name__=="__main__":
	# Enable GTK multi-threading support
	gtk.gdk.threads_init()
	gtk.gdk.threads_enter()
	
	# Start the target selection UI. This parses the command line and shows the
	# MainWindow when connected.
	TargetSelection(sys.argv)
	
	# GTK Mainloop
	gtk.main()
