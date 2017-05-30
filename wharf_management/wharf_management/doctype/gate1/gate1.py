# -*- coding: utf-8 -*-
# Copyright (c) 2017, Caitlah Technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
from frappe.utils import cstr, flt, fmt_money, formatdate
from frappe import msgprint, _, scrub

class Gate1(Document):
	
	def on_submit(self):
		self.update_gate1_status()
	
	def validate(self):
		self.validate_warrant_no()
		
	
	def validate_warrant_no(self):
		if self.warrant_no != self.custom_warrant:
			msgprint(_("Please Make sure that is the correct WARRANT NO"), raise_exception=1)
			
	
	def update_gate1_status(self):
		frappe.db.sql("""Update `tabCargo` set yard_slot=%s, gate1_status="Closed", status='Gate1' where name=%s""", (self.custom_code, self.cargo_ref))