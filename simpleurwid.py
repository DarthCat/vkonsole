# coding=utf8			

import urwid
import random
import string

def random_str(len):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(len))


class MainWrapper(urwid.Frame):
	pass


class EditBox(urwid.Edit):
	pass

class Messages(urwid.ListBox):
	def __init__(self, messages):
		mes_widgets = []
		for mes in messages:
			#if mes['out']:
			if bool(random.getrandbits(1)):
				mes_widgets.append(urwid.Text(random_str(50), 'right'))
			else:
				mes_widgets.append(urwid.Text(random_str(50), 'left'))
		walker = urwid.SimpleListWalker(mes_widgets)
		super(Messages, self).__init__(walker)




class Border(urwid.WidgetWrap):
	def __init__(self, w, title=None,  title_attr=None,  border_attr=None):
		# Define the border characters
		self.tline = urwid.AttrWrap(urwid.Divider("─"),  border_attr)	# Top Line
		self.bline = urwid.AttrWrap(urwid.Divider("─"),  border_attr)	# Bottom Line
		self.lline = urwid.AttrWrap(urwid.SolidFill("│"),  border_attr)	# Left Line
		self.rline = urwid.AttrWrap(urwid.SolidFill("│"),  border_attr)	# Right Line
		self.tlcorner = urwid.AttrWrap(urwid.Text("┌"),  border_attr)	# and the four corners
		self.trcorner = urwid.AttrWrap(urwid.Text("┐"),  border_attr)
		self.blcorner = urwid.AttrWrap(urwid.Text("└"),  border_attr)
		self.brcorner = urwid.AttrWrap(urwid.Text("┘"),  border_attr)
		
		if title is None:
			self.title=""
		else:
			self.title = " %s " % (title)		# Add two spaces to the title

		self.titlelen = len(self.title)
		self.title = urwid.AttrWrap(urwid.Text(self.title),  title_attr)

		# Create the top line
		top = urwid.Columns([ ('fixed', 1, self.tlcorner), ('fixed',  self.titlelen, self.title), 
							('weight' , 1, self.tline), ('fixed', 1, self.trcorner) ])

		# This is what will be wrapped 
		middle = urwid.Columns( [('fixed', 1, self.lline),
							w, ('fixed', 1, self.rline)], box_columns = [0,2], focus_column = 1)
		
		# Create the bottom line
		bottom = urwid.Columns([ ('fixed', 1, self.blcorner),
							('weight',  1, self.bline), ('fixed', 1, self.brcorner) ])

		# and pile them all together
		pile = urwid.Pile([('flow',top),middle,('flow',bottom)],
							focus_item = 1)
			
		urwid.WidgetWrap.__init__(self, pile)

	def set_attr(self, attr):
		self.set_attr( attr)



#TORNADO.EVENTLOOP


if __name__ == '__main__':
	eb = Border(EditBox(""))
	x = [urwid.Text(str(x**3), 'right') for x in range(50)]
	messages = Border(Messages(range(30)))		
	p = urwid.Pile([messages, ('pack', eb)], focus_item=1)
	mainloop = urwid.MainLoop(p)
	mainloop.run()