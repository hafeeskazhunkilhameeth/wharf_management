// Copyright (c) 2017, Caitlah Technology and contributors
// For license information, please see license.txt

frappe.ui.form.on('Wharf Payment Fee', {
	refresh: function(frm) {

	},

	onload: function(frm) {

		frappe.call({
			"method": "frappe.client.get",
			args: {
				doctype: "Cargo",
				name: frm.doc.cargo_ref,
				filters: {
						'docstatus' : 1
						},
			},
			callback: function (data) {
				cur_frm.set_value("cargo_ref", data.message["name"]);
				cur_frm.set_value("container_no", data.message["container_no"]);
				cur_frm.set_value("voyage_no", data.message["voyage_no"]);
				cur_frm.set_value("vessel", data.message["vessel"]);
				cur_frm.set_value("eta_date", data.message["eta_date"]);
				cur_frm.set_value("cargo_type", data.message["cargo_type"]);
				cur_frm.set_value("yard_slot", data.message["yard_slot"]);
				cur_frm.set_value("consignee", data.message["consignee"]);
				cur_frm.set_value("container_type", data.message["container_type"]);
				if (frm.doc.cargo_type == "Container"){
					frm.set_value("free_storage_days", 10);
				} else if (frm.doc.cargo_type != "Container"){
					frm.set_value("free_storage_days", 5);
				}
				cur_frm.set_value("container_size", data.message["container_size"]);
				cur_frm.set_value("container_content", data.message["container_content"]);

				cur_frm.set_df_property("voyage_no", "read_only", 1);
				cur_frm.set_df_property("vessel", "read_only", 1);
				cur_frm.set_df_property("eta_date", "read_only", 1);
				cur_frm.set_df_property("cargo_type", "read_only", 1);
				cur_frm.set_df_property("container_no", "read_only", 1);
							
				cur_frm.set_df_property("yard_slot", "read_only", 1);
				cur_frm.set_df_property("consignee", "read_only", 1);
				cur_frm.set_df_property("container_type", "read_only", 1);
				cur_frm.set_df_property("container_size", "read_only", 1);
				cur_frm.set_df_property("container_content", "read_only", 1);
				cur_frm.set_df_property("free_storage_days", "read_only", 1);
			}
		})

	},
	posting_date: function(frm){
		
		var storagedays = frappe.datetime.get_day_diff( frm.doc.posting_date, frm.doc.eta_date );
//		var storagedays = (frm.doc.posting_date, frm.doc.eta_date);
		frm.set_value("storage_days", storagedays);
//		calculate_storage_fee(frm);
			
	
	},
	
	custom_code: function(frm) {
		if (frm.doc.custom_code == "DDL"){
			frm.set_value("delivery_code", "DIRECT DELIVERY")
		} else if (frm.doc.custom_code == "DDLW"){
			frm.set_value("delivery_code", "DIRECT DELIVERY WAREHOUSE")
		} else if (frm.doc.custom_code == "IDL"){
			frm.set_value("delivery_code", "INSPECTION DELIVERY")
		} else if (frm.doc.custom_code == "IDLW"){
			frm.set_value("delivery_code", "INSPECTION DELIVERY WAREHOUSE")
		}
	}
});

var calculate_storage_fee = function(frm){

	

//	frm.set_value("total_amount_paid", total_amount);
		
}