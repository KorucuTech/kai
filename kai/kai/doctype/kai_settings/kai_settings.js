// Copyright (c) 2024, Kemal Korucu and contributors
// For license information, please see license.txt

frappe.ui.form.on("KAI Settings", {
	refresh(frm) {

	},
    clear_response(frm) {
        frm.set_value('system_response', '');
    },
    send_request(frm) {
        frappe.call({
            method: "kai.kai.doctype.kai_settings.kai_settings.ai_call",
            args: {
                enabled: frm.doc.enabled,
                llm: frm.doc.llm,

                system_prompt: frm.doc.system_prompt,
                agent_instruction_prompt: frm.doc.agent_instruction_prompt,
                user_request: frm.doc.user_request
            },
            freeze: true,
            callback: (r) => {
                frm.set_value('system_response', r.message);
                console.log(r);
            },
            error: (r) => {
                frm.set_value('system_response', "ERROR: " + JSON.stringify(r.message));
                console.log(r);
            }
        });
    }
});

