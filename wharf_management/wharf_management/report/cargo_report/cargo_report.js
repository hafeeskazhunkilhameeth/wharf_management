// Copyright (c) 2016, Sione Taumoepeau and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Cargo Report"] = {
	"filters": [
//		{
//			"fieldname":"from_date",
//			"label": __("From Date"),
//			"fieldtype": "Date",
//			"default": frappe.datetime.get_today(),
//			"reqd": 1,
//			"width": "80"
//		},
//		{
//			"fieldname":"to_date",
//			"label": __("To Date"),
//			"fieldtype": "Date",
//			"reqd": 1,
//			"default": frappe.datetime.get_today()
//		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		},
//		{
//			"fieldname":"voyage_no",
//			"label": __("Voyage No"),
//			"fieldtype": "Data",
//			"options": "voyage_no"
//		},
		{
			"fieldname":"name",
			"label": __("Booking Ref"),
			"fieldtype": "Link",
			"options": "Booking Request"
		},

	]
}
