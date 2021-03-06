# -*- coding: utf-8 -*-
# Copyright (c) 2017, Caitlah Technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
from frappe.utils import cstr, flt, fmt_money, formatdate
from frappe import msgprint, _, scrub

class Gate1(Document):
	
	def validate(self):
		self.validate_truck()
		self.validate_warrant_no()
		self.validate_driver()
		self.validate_company()


	def on_submit(self):
			
		if self.mydoctype == "CARGO":
			self.update_status()
			self.update_export_status()
			self.update_not_export_status()
			self.update_cargo_movement()
		if self.mydoctype == "EMPTY CONTAINERS":
			self.update_empty_containers_movement()


		
	def update_status(self):
		self.status = "Passed Gate 1"
	
	def validate_warrant_no(self):
			if self.work_type != 'Loading':
				if self.warrant_no != self.custom_warrant:
					msgprint(_("Please Make sure that is the correct WARRANT NO"), raise_exception=1)

	def validate_company(self):
		if not self.company:
			msgprint(_("Company is Manadory"), raise_exception=1)
		
	def validate_driver(self):
		if not self.drivers_information:
			msgprint(_("Drivers Information is Manadory"), raise_exception=1)
	
	def validate_truck(self):
		if not self.truck_licenses_plate:
			msgprint(_("Truck Information is Manadory"), raise_exception=1)

	def update_not_export_status(self):
		if self.qty > 1:
			frappe.db.sql("""Update `tabCargo` set security_item_count=1, gate1_status="Closed", status='Gate1' where name=%s""", (self.cargo_ref))
		if self.qty == 1:
			frappe.db.sql("""Update `tabCargo` set gate1_status="Closed", status='Gate1' where name=%s""", (self.cargo_ref))
		if self.qty == 0:
			frappe.db.sql("""Update `tabCargo` set gate1_status="Closed", status='Gate1' where name=%s""", (self.cargo_ref))

	def update_export_status(self):
		if self.status == 'Export':
			frappe.db.sql("""Update `tabCargo` set export_status="Gate1", gate1_status="Open", gate2_status="Open", payment_status="Open", yard_status="Open", inspection_status="Open" where name=%s""", (self.cargo_ref))


	def update_cargo_movement(self):

		val = frappe.db.get_value("Cargo", {"name": self.cargo_ref}, ["pat_code","cargo_type","container_no","agents","container_type","container_size", "chasis_no", "mark", "qty", "consignee",
		"container_content","cargo_description", "custom_warrant", "eta_date", "etd_date", "booking_ref"], as_dict=True)

		doc = frappe.new_doc("Cargo Movement")
		doc.update({
					"docstatus" : 1,
					"pat_code" : val.pat_code,
					"cargo_type" : val.cargo_type,
					"container_no" : val.container_no,
					"work_type" : self.work_type,
					"agents" : val.agents,
					"container_type" : val.container_type,
					"container_size" : val.container_size,
					"consignee" : val.consignee,
					"container_content" : val.container_content,
					"cargo_description" : val.cargo_description,
					"gate_status" : "OUT",
					"movement_date" : self.modified,
					"gate1_time" : self.modified,
					"truck" : self.truck_licenses_plate,
					"truck_driver" : self.drivers_information,
					"refrence": self.cargo_ref,
					"chasis_no" : val.chasis_no,
					"mark" : val.mark,
					"qty" : val.qty,
					"warrant_number" : self.warrant_no,
					"eta_date" : val.eta_date,
					"etd_date" : val.etd_date,
					"booking_ref" : val.booking_ref
				})
		doc.insert()
		doc.submit()
	
	def update_empty_containers_movement(self):

		val = frappe.db.get_value("Empty Containers", {"name": self.cargo_ref}, ["pat_code","cargo_type","container_no","agents","container_type","container_size", "consignee",
		"container_content"], as_dict=True)

		doc = frappe.new_doc("Cargo Movement")
		doc.update({
					"docstatus" : 1,
					"pat_code" : val.pat_code,
					"cargo_type" : val.cargo_type,
					"container_no" : val.container_no,
					"work_type" : self.work_type,
					"agents" : val.agents,
					"container_type" : val.container_type,
					"container_size" : val.container_size,
					"consignee" : val.consignee,
					"container_content" : val.container_content,
					"cargo_description" : "Empty Container",
					"gate_status" : "OUT",
					"movement_date" : self.modified,
					"gate1_time" : self.modified,
					"truck" : self.truck_licenses_plate,
					"truck_driver" : self.drivers_information,
					"refrence": self.cargo_ref,
					"warrant_number" : "N/A"
				})
		doc.insert()
		doc.submit()

		frappe.db.sql("""Update `tabEmpty Containers` set gate1_date=%s, status='Gate 1' where name=%s""", (self.modified, self.cargo_ref))