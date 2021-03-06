# Copyright (c) 2013, Sione Taumoepeau and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns=get_columns()
	data=get_cargo_data(filters, columns)
	return columns, data

def get_columns():
	return []

def get_cargo_data(filters, columns):
	data = []

	cargo_data = get_cargo_details(filters)

	for cargo in cargo_data:
#		owner_posting_date = container["owner"]+cstr(container["posting_date"])
		row = [cargo.cargo_type, cargo.work_type, cargo.container_content, cargo.container_size, cargo.total, cargo.handling_fee]
		data.append(row)
	return data


def get_conditions(filters):
	conditions = "1=1"
#	if filters.get("from_date"): conditions += " and eta_date >= %(from_date)s"
#	if filters.get("to_date"): conditions += " and eta_date <= %(to_date)s"
	if filters.get("name"): conditions += " and booking_ref = %(name)s"
#	if filters.get("status"): conditions += " and status = %(status)s"
#	if filters.get("owner"): conditions += " and a.owner = %(owner)s"
#	if filters.get("pos_profile"): conditions += " and a.is_pos = %(pos_profile)s"
#	if filters.get("status"): conditions += " and a.status = %(status)s"
	return conditions

def get_cargo_details(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""
		select * from `tabCargo` 
			where  docstatus = 1
			and {conditions}
			and manifest_check = "Confirm"		
	""".format(conditions=conditions), filters, as_dict=1)