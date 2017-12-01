# -*- coding: utf-8 -*-
# Copyright (c) 2017, Sione Taumoepeau and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint, throw
from frappe.model.document import Document

class DevaningRequest(Document):

	def validate_container_no(self):
    		container_number=None
		container_number = frappe.db.sql("""Select name from `tabCargo` where container_no=%s and work_type="Discharged" """, (self.container_no))

		if not container_number:
			val_empty = ""
			val_empty = self.container_type
			val_empty = self.container_size
    			frappe.throw(_("There is no Container No : {0} in the Cargo List").format(self.container_no))
		
		else:
#    			container_ref = frappe.db.get_value("Export", {"container_no": self.container_no}, "name")
    			val = frappe.db.get_value("Cargo", {"container_no": self.container_no}, ["container_type","container_size","pat_code","container_content"], as_dict=True)
#			self.yard_slot = val.yard_slot
#			self.main_gate_start = val.main_gate_start
#			self.main_gate_ends = val.main_gate_ends
#			self.gate1_start = val.gate1_start
#			self.gate1_ends = val.gate1_ends
#			self.driver_start = val.driver_start
#			self.driver_ends = val.driver_ends
			self.container_type = val.container_type
			self.container_size = val.container_size
#			self.pat_code = val.pat_code
#			self.container_content = val.container_content
#			self.seal_1 = val.seal_1
    			
			frappe.msgprint(_("Container No : {0} is in the Cargo list go ahead and submit your Devanning Request").format(self.container_no))