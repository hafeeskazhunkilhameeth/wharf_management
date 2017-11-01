# -*- coding: utf-8 -*-
# Copyright (c) 2017, Caitlah Technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.utils import cstr, flt, fmt_money, formatdate
from frappe import msgprint, _, scrub
from frappe.model.document import Document
from erpnext.controllers.accounts_controller import AccountsController
from erpnext.accounts.party import get_party_account


class CargoManifest(Document):

	#	def validate(self):
	#		self.cretate_manifest_list()

#		def on_submit(self):
#			self.update_cargo_table()


#		def update_cargo_table(self):
#			frappe.db.sql("""Update `tabCargo` set vessel = %s, voyage_no = %s where parent = %s""", (self.vessel, self.voyage_no, self.name))
#			frappe.db.sql("""Update `tabCargo` set status='Unknown' where parent = %s""", (self.name))


		def get_manifest(self):
			condition = ""
			manifest_list = frappe.db.sql("""select name as cargo_refrence, container_no, bol, cargo_type,
			work_type, container_size, container_content, status, voyage_no, booking_ref from `tabCargo` where booking_ref = %s and final_status in ("Discharged","Loading")""",(self.booking_ref), as_dict=1)

			entries = sorted(list(manifest_list))

			self.set('manifest_list', [])

			for d in entries:
				row = self.append('manifest_table', {
					'container_size':d.container_size,
					'container_no':d.container_no,
					'cargo_type':d.cargo_type,
					'work_type':d.work_type,
					'container_content':d.container_content,
					'status':d.status,
					'container_size':d.container_size,
					'voyage_no':d.voyage_no,
					'booking_ref':d.booking_ref,
					'cargo_refrence': d.cargo_refrence
				})


		def get_manifest_summary_list(self):
			condition = ""
			manifest_summary_table = frappe.db.sql("""select cargo_type, container_content, work_type, container_size, count(name) as container
				from `tabCargo` where cargo_type = "Container" and booking_ref = %s and final_status in ("Discharged","Loading") group by work_type, container_content, container_size""", (self.booking_ref), as_dict=1)

			entries = sorted(list(manifest_summary_table))

			self.set('manifest_summary_table', [])

			for d in entries:
				row = self.append('manifest_summary_table', {
					'cargo_type': d.cargo_type,
					'container_content': d.container_content,
					'work_type': d.work_type,
					'container_size': d.container_size,
					'Container' : d.container
				})
			
		def get_bbulks_summary_list(self):
    			condition = ""
			bbulks_summary_table = frappe.db.sql("""select cargo_type, work_type, sum(net_weight) as weight
				from `tabCargo` where cargo_type != "Container" and booking_ref = %s and final_status in ("Discharged","Loading") group by work_type""", (self.booking_ref), as_dict=1)

			bbulks_entries = sorted(list(bbulks_summary_table))

			self.set('bbulks_summary_table', [])

			for b in bbulks_entries:
				row = self.append('bbulks_summary_table', {
					'cargo_type': b.cargo_type,
					'work_type': b.work_type,
					'weight':b.weight
				})
